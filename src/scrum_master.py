"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard
from modal_editor import ModalEditor
from block_ui.create_story_ui import CREATE_STORY_MODAL
from block_ui.delete_story_ui import DELETE_STORY_MODAL
from block_ui.confirm_delete_ui import CONFIRM_DELETE_MODAL
from block_ui.update_story_ui import UPDATE_STORY_MODAL
from block_ui.example_modal_ui import EXAMPLE_MODAL
from block_ui.read_story_ui import READ_STORY_BLOCK
from block_ui.set_sprint_ui import SET_SPRINT_MODAL
from block_ui.sprint_end_msg_ui import SPRINT_END_MSG
# INIT_HOME_PAGE, SWIMLANE_HEADER, SWIMLANE_FOOTER, SORT_DROPDOWN, STORY_BLOCK, RADIO_INIT_OPTION, SWIMLANE_OPTION
from block_ui.home_page_ui import *
import json
import copy
import re
from datetime import datetime
import itertools
import string
from spellchecker import SpellChecker

SYNONYMS = 'data/synonyms.json'
help_msg = "Here are the commands you can use with *@Miyagi*. Text in _italic_ represents data fields and [text] are optional fields: \n *:heavy_plus_sign: create story* \n *:pencil2: update story _id_* \n *:heavy_multiplication_x: delete story* \n *:book: read [_id_] [from _swimlane name_]* \n *:mag: search* \n *:alarm_clock: set sprint* \n *:heavy_plus_sign: create swimlane* \n *:pencil2: update swimlane* \n *:heavy_multiplication_x: delete swimlane* \n *:newspaper: read _swimlane name_*"
fail_msg = "Command not found. " + help_msg

emojis = {
    "priority": {
        -1: "None ",
        1: ":large_green_square:",
        2: ":large_yellow_square:",
        3: ":large_red_square:"
    },
    "status": {
        "to-do": ":inbox_tray:",
        "in-progress": ":clock2:",
        "completed": ":white_check_mark:"
    }
}


class ScrumMaster:
    # Interface with JSON data

    # Command keyword list (CRUD)
    # e.g. action = commands[keyword]
    #      action(story)
    # commands = {
    #     "create": scrum_board.create_story,
    #     "read": scrum_board.read_story,
    #     "update": scrum_board.update_story, # of form: @Bot update [field] [value]
    #     "delete": scrum_board.delete_story
    # }

    priorities = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    fields = {
        "priority",
        "estimate",
        "sprint",
        "status",
        "assigned_to",
        "user_type",
        "story"
    }

    def __init__(self):
        self.text = "\0"
        self.blocks = None

        # Interface with JSON data
        self.scrum_board = ScrumBoard()

        # Modal editor
        self.editor = ModalEditor()

        with open(SYNONYMS, 'r') as f:
            self.synonyms = json.load(f)

        self.spell = SpellChecker()
        self.spell.word_frequency.load_dictionary('data/freq_synonyms.json')
        with open("data/nonwords.json", "r") as f:
            nonwords = json.load(f)
            for word in nonwords:
                self.spell.word_frequency.pop(word)

    def reset_sprint_info(self):
        self.scrum_board.write_metadata_field('current_sprint_starts', 0)
        self.scrum_board.write_metadata_field('current_sprint_ends', 0)
        self.scrum_board.write_metadata_field('sprint_duration', 0)
        sm = self.scrum_board.read_metadata_field('scheduled_messages')
        sm['end_sprint'] = 0
        self.scrum_board.write_metadata_field('scheduled_messages', sm)

    def update_home(self, payload, metadata=""):
        print(f'UPDATE HOME METADATA: {metadata}')
        sprint_header = []
        swimlane_select = []
        story_blocks = []
        swimlane_header = []
        swimlane_footer = []
        sort_by_block = []

        init_option, sort_by = None, None
        if metadata and metadata != 'None':
            md = json.loads(metadata)
            init_option = md['swimlane'] if md['swimlane'] != 'UNSELECTED' else None
            if init_option:
                sort_by_block = SORT_DROPDOWN
            if 'sort_by' in md:
                sort_by = md['sort_by'] if md['sort_by'] != "UNSORTED" else None
            else: 
                sort_by = None

        if not init_option:
            if 'swimlane_select' in payload['view']['state']['values']:
                init_option = payload['view']['state']['values']['swimlane_select']['swimlane_select']['selected_option']['value']
                logs = self.scrum_board.get_logs()
                if init_option not in logs:
                    init_option = None
                sort_by_block = SORT_DROPDOWN
            else:
                init_option = None

        if not sort_by:
            if 'sort_by' in payload['view']['state']['values']:
                if payload['view']['state']['values']['sort_by']['sort_by']['selected_option']:
                    sort_by = payload['view']['state']['values']['sort_by']['sort_by']['selected_option']['value']
                else:
                    sort_by = None
            else:
                sort_by = None

        if init_option not in self.scrum_board.get_logs():
            init_option = "Product Backlog"

        metadata2 = {"swimlane": init_option if init_option else "Product Backlog",
                     "sort_by": sort_by if sort_by else "UNSORTED"}

        if init_option:
            swimlane_header = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": init_option,
                        "emoji": True
                    }
                }
            ]
            swimlane_footer = [
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": "/ "+init_option,
                            "emoji": True
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "divider"
                }
            ]
            stories = self.scrum_board.read_log(init_option)
            if not isinstance(stories, str):
                flatten = lambda *n: (e for a in n
                                      for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))
                if sort_by:
                    stories = sorted(stories, key=lambda x: x[sort_by])
                story_blocks = flatten(
                    [self._story_to_msg(story, md=json.dumps(metadata2)) for story in stories])
            else:
                story_blocks = [{
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "There are no stories in this swimlane.",
                        "emoji": True
                    }
                }]
        swimlane_select = self.populate_swimlanes(
            INIT_HOME_PAGE, init_option=init_option)
        for x in range(len(swimlane_select[3]['elements'])):
            swimlane_select[3]['elements'][x]['value'] = json.dumps(metadata2)

        sprint_start = self.scrum_board.read_metadata_field(
            'current_sprint_starts')
        sprint_end = self.scrum_board.read_metadata_field(
            'current_sprint_ends')
        curr_sprint = self.scrum_board.read_metadata_field('current_sprint')
        sprint_header = SPRINT_HEADER
        if sprint_start:
            sprint_header[0]['text']['text'] = f'Sprint {curr_sprint}'
            sprint_header[1]['elements'][0][
                'text'] = f"*Started:* {datetime.fromtimestamp(sprint_start).strftime('%Y-%m-%d at %H:%M')}"
            sprint_header[1]['elements'][1][
                'text'] = f"*Ends:* {datetime.fromtimestamp(sprint_end).strftime('%Y-%m-%d at %H:%M')}"
        else:
            sprint_header[0]['text']['text'] = "No sprint in progress."
            sprint_header[1]['elements'][0]['text'] = "To start a sprint, tell Miyagi \"set sprint\"."
            sprint_header[1]['elements'][1]['text'] = " "

        ui = list(itertools.chain(sprint_header, swimlane_select,
                                  swimlane_header, sort_by_block, story_blocks, swimlane_footer))

        view = {
            "type": 'home',
            "title": {
                "type": "plain_text",
                "text": "Test home tab!"
            },
            "blocks": ui,
            "private_metadata":  json.dumps(metadata2)
        }
        return view

    def populate_swimlanes(self, blocks, init_option=None):
        swimlanes = self.scrum_board.get_logs()
        blocks[0]['accessory']['options'] = [
            {
                "text": {
                    "type": "plain_text",
                    "text": s,
                    "emoji": True
                },
                "value": s
            }
            for s in swimlanes
        ]
        if init_option:
            blocks[0]['accessory']['initial_option'] = {
                "value": init_option,
                "text": {
                    "type": "plain_text",
                    "text": init_option
                }
            }
        return blocks

    def create_story(self):
        msg, blocks = self._create_modal_btn(text="Create Story",
                                             action_id="create-story")
        self.text, self.blocks = msg, blocks

    def delete_story(self):
        msg, blocks = self._create_modal_btn(text="Delete Story",
                                             action_id="delete-story")
        self.text, self.blocks = msg, blocks

    def update_story(self):
        ids = re.findall('\d+', self.text)
        if len(ids) == 0:
            self.text = "You must include the ID of the story you want to update."
            return
        id = int(ids[0])
        result = self.scrum_board.read_story(id)
        if isinstance(result, str):
            self.text = result
            return
        story = result[0]
        log = result[1]
        if log == "Previous Sprint" or log == "Archived":
            self.text = f"Cannot update stories in {log}."
            return
        metadata = {"story": story, "log": log}
        msg, blocks = self._create_modal_btn(text=f"Update Story {id}",
                                             action_id="update-story",
                                             metadata=json.dumps(metadata))
        self.text, self.blocks = msg, blocks

    def read_story(self):
        text = self.text.lower()
        logs = self.scrum_board.get_logs()
        log = None
        for l in logs:
            if self.normalize(l) in text:
                log = l
                break

        ids = re.findall('\d+', self.text)
        if len(ids) > 0:
            # If ID is specified, read specific story.
            id = int(ids[0])
            result = self.scrum_board.read_story(id=id, log=log)
            if isinstance(result, str):
                self.text = result  # Handles error case of string from scrum_board
                return
            # Otherwise, stories is one obj that is pretty-printed.
            story = result[0]
            log = result[1]
            self.blocks = self._story_to_msg(story)
            self.text = f"Story {id} from {log}:"
        elif log:
            # If there is no ID but there is a log, return the swimlane/log/entire board.
            stories = self.scrum_board.read_log(log=log)
            self.blocks = []
            if isinstance(stories, str):
                self.text = stories  # Handles error case of string from scrum_board
                return
            for story in stories:
                self.blocks += self._story_to_msg(story)
            
            # Make sure stories are under 50 blocks
            self.blocks = self.blocks[:50]
            for i in range(len(self.blocks)-1, 0, -1):
                if self.blocks[i]['type'] == 'actions':
                    self.blocks = self.blocks[:i+2]
                    break
            self.text = "Story:"
        else:
            self.text = "Could not understand read command."

    def search_story(self):
        msg, blocks = self._create_modal_btn(text="Search story",
                                             action_id="search-story")
        self.text, self.blocks = msg, blocks

    def set_sprint(self):
        msg, blocks = self._create_modal_btn(text="Set Sprint",
                                             action_id="set-sprint")
        self.text, self.blocks = msg, blocks

    def create_swimlane(self):
        msg, blocks = self._create_modal_btn(text="Create swimlane",
                                             action_id="create-swimlane")
        self.text, self.blocks = msg, blocks

    def _get_my_stories(self, user_id):
        name = self._get_member_name(user_id)
        first_name = name.split(' ')[0]

        story_logs = list(set(self.scrum_board.get_logs()) - set(["Previous Sprint", "Archived"]))
        stories = self.scrum_board.search_story(name, story_logs, [], include_archived=False)

        if isinstance(stories, list):
            self.blocks = [{
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"Hello {first_name}, here are your stories!",
                }
            }]
            for story in stories:
                self.blocks += self._story_to_msg(story)
            self.text = "Hello! Here are your stories."
        else:
            self.text = f"Hi {first_name}, you have no stories!"

    # Where action="update" or "delete"
    def update_or_delete_swimlane(self, action: str):
        if len(self.scrum_board.list_user_swimlanes()) == 0:
            # if there are no user-generated swimlanes ..
            self.text = f"You have no swimlanes to {action}. You cannot {action} default swimlanes, but you may create new ones using `create swimlane`."
            return
        else:
            msg, blocks = self._create_modal_btn(text=f"{action.title()} swimlane",
                                                 action_id=f"{action}-swimlane")
            self.text, self.blocks = msg, blocks

    def normalize(self, s):
        for p in string.punctuation:                    # Remove punctuation
            s = s.replace(p, '')
        s = re.sub(pattern='\s+', string=s, repl=' ')   # Replace whitespace
        return s.lower().strip()                        # Lowercase, strip whitespace

    def find_synonyms(self, text: str):
        text = text.split()
        synonyms = []
        for word in text:
            if word in self.synonyms:
                synonyms.extend(self.synonyms[word].split())
        return synonyms

    def is_in(self, words, text_str):
        text_lst = text_str.split(' ')
        for word in words:
            if word in text_lst:
                return True
        return False

    def spellcheck(self, text: str):
        correct = []
        for word in text.split(" "):
            correct.append(self.spell.correction(word))
        return " ".join(correct)

    def determine_command(self, text: str, user_id: str):
        self.text = text
        synonyms = self.find_synonyms(text)

        if user_id and (self.is_in(("hello", "hi"), text) or self.is_in(("me", "my"), text)):
            self._get_my_stories(user_id)
        elif "read" in synonyms:
            self.read_story()
        elif "search" in synonyms:
            self.search_story()
        elif "sprint" in synonyms:
            self.set_sprint()
        elif "swimlane" in synonyms:
            if "create" in synonyms:
                self.create_swimlane()
            elif "update" in synonyms:
                self.update_or_delete_swimlane("update")
            elif "delete" in synonyms:
                self.update_or_delete_swimlane("delete")
            else:
                self.text = fail_msg
        elif "update" in synonyms and re.findall('\d+', text):
            self.update_story()
        elif "update" in synonyms:
            self.text = "Please specify whether you want to update a story (use the word \"story\" or specify an story ID) or a swimlane."
        elif "create" in synonyms:
            self.text = "Please specify whether you want to create a story or a swimlane."
        elif "delete" in synonyms:
            self.text = "Please specify whether you want to delete a story or a swimlane."
        elif "help" in synonyms:
            self.text = help_msg
        elif "end demo" in text:
            self.text = "*Click :thumbsup: and Subscribe if you enjoyed the demo! Does anyone have any questions?*"
        elif "story" in synonyms:
            if "create" in synonyms:
                self.create_story()
            elif "delete" in synonyms:
                self.delete_story()
            elif "update" in synonyms:
                self.update_story()
            elif "search" in synonyms:
                self.search_story()
            else:
                self.text = fail_msg
        else:
            self.text = fail_msg

    def process_user_msg(self, text: str, user_id: str = None):
        text = self.normalize(text)
        text = self.spellcheck(text)
        self.determine_command(text, user_id)

    def _create_modal_btn(self, text="", action_id="", metadata="None"):
        """Creates an interactive button so that we can obtain a trigger_id for modal interaction

        IMPORTANT!!! Remember what action_id you used because you will need to use it in create_modal
        """

        blocks = [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": text,
                        },
                        "value": metadata,
                        "action_id": action_id
                    },
                ],
            }
        ] if text != "" else None

        msg = ""
        return msg, blocks

    def create_modal(self, action_id, metadata):
        # Add an if-clause to parse what happens if we receive your action_id to create a modal
        if action_id == "create-story":
            return self._fill_create_modal(CREATE_STORY_MODAL, metadata)
        elif action_id == "delete-story":
            return self._fill_delete_modal(DELETE_STORY_MODAL, metadata)
        elif action_id == "update-story":
            return self._fill_update_modal(UPDATE_STORY_MODAL, metadata)
        elif action_id == "search-story":
            return self.editor.edit_search_story_modal()
        elif action_id == 'set-sprint':
            return self.init_sprint_modal(SET_SPRINT_MODAL)
        elif action_id == "create-swimlane":
            modal = self.editor.edit_create_swimlane_modal()
            modal['private_metadata'] = metadata
            return modal
        elif action_id == "update-swimlane":
            modal = self.editor.edit_update_or_delete_swimlane_modal("update")
            modal['private_metadata'] = metadata
            return modal
        elif action_id == "delete-swimlane":
            modal = self.editor.edit_update_or_delete_swimlane_modal("delete")
            modal['private_metadata'] = json.dumps({"swimlane": "UNSELECTED"})
            return modal
        elif action_id == "example":
            return EXAMPLE_MODAL
        else:
            return ""

    def _fill_create_modal(self, modal, metadata):
        logs = self._get_valid_logs(create=1)
        swimlane_options = [
            {
                "text": {
                    "type": "plain_text",
                    "text": x,
                    "emoji": True
                },
                "value": x
            }
            for x in logs
        ]
        modal['blocks'][1]['element']['options'] = swimlane_options
        curr_sprint = str(
            self.scrum_board.read_metadata_field("current_sprint"))
        modal['blocks'][4]['element']['placeholder']['text'] = "Current sprint number: "+curr_sprint
        modal['private_metadata'] = metadata
        return modal

    def _fill_delete_modal(self, modal, metadata=None):
        try:
            init_value = json.loads(metadata)['story']
        except:
            init_value = ""
        modal['blocks'][1]['element']['initial_value'] = init_value  # md['story']
        modal['private_metadata'] = metadata
        return modal

    def _fill_confirm_delete_modal(self, modal, metadata, callback_id):
        modal['view']['private_metadata'] = metadata
        modal['view']['callback_id'] = callback_id
        return modal

    def init_sprint_modal(self, modal):
        today = datetime.now().strftime("%Y-%m-%d %H:%M").split()
        modal['blocks'][1]['elements'][0]['initial_date'] = today[0]
        modal['blocks'][1]['elements'][1]['initial_time'] = today[1]

        exists = self.check_if_sprint_exists()
        # if there is a sprint that already exists, tell user this
        # to ensure they actually want to reset sprint
        if exists:
            curr_sprint_start = self.scrum_board.read_metadata_field(
                "current_sprint_starts")
            curr_sprint_end = self.scrum_board.read_metadata_field(
                "current_sprint_ends")
            prepend = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*WARNING:* _You already have a sprint set that" +
                        f" started on {datetime.fromtimestamp(curr_sprint_start).strftime('%Y-%m-%d at %H:%M')}" +
                            f" and ends on {datetime.fromtimestamp(curr_sprint_end).strftime('%Y-%m-%d at %H:%M')}." +
                    " You may set a new sprint, but this will *end the current sprint* and start a new one!_"
                }
            }
            modal_with_warning = copy.deepcopy(modal)
            modal_with_warning['blocks'].insert(0, prepend)
            return modal_with_warning

        return modal

    def _get_valid_logs(self, create=0):
        # can create a story in any swimlane EXCEPT previous_sprint and archived
        if create:
            return [x for x in self.scrum_board.get_logs() if x not in ['Previous Sprint', 'Archived']]
        # can move a story to any swimlane EXCEPT previous_sprint
        else:
            return [x for x in self.scrum_board.get_logs() if x != 'Previous Sprint']

    def _fill_update_modal(self, modal, metadata):
        logs = self._get_valid_logs(create=0 if metadata else 1)
        swimlane_options = [
            {
                "text": {
                    "type": "plain_text",
                    "text": x,
                    "emoji": True
                },
                "value": x
            }
            for x in logs
        ]
        data = json.loads(metadata)
        story_update = data['story']
        modal['title']['text'] = f'Update Story {story_update["id"]}'
        if 'swimlane' in data:
            private_metadata = {
                "story": story_update, "log": data["log"], "swimlane": data["swimlane"], "sort_by": data["sort_by"]}
        else:
            private_metadata = {"story": story_update, "log": data["log"]}
        # f'{story_update["id"]},{data["log"]}'
        modal['private_metadata'] = json.dumps(private_metadata)
        for b in modal['blocks']:
            if b['label']['text'] == 'Swimlane':
                b['element']['options'] = swimlane_options
                b['element']['initial_option']['text']['text'] = data['log']
                b['element']['initial_option']['value'] = data['log']
            elif b['label']['text'] == 'Estimate':
                b['element']['initial_option']['text']['text'] = str(
                    story_update['estimate']) if story_update['estimate'] != -1 else "1"
                b['element']['initial_option']['value'] = str(
                    story_update['estimate']) if story_update['estimate'] != -1 else "1"
            elif b['label']['text'] == 'Sprint':
                curr_sprint = str(
                    self.scrum_board.read_metadata_field("current_sprint"))
                # if story_update['sprint'] else curr_sprint
                b['element']['initial_value'] = str(story_update['sprint'])
                b['element']['placeholder']['text'] = "Current sprint number: "+curr_sprint
            elif b['label']['text'] == 'Priority':
                if story_update['priority'] != -1:
                    p = list(self.priorities.keys())[
                        list(self.priorities.values()).index(story_update['priority'])]
                    b['element']['initial_option']['text']['text'] = p
                    b['element']['initial_option']['value'] = p.lower()
                else:
                    b['element']['initial_option']['text']['text'] = 'Low'
                    b['element']['initial_option']['value'] = 'low'
            elif b['label']['text'] == 'Status':
                b['element']['initial_option']['text']['text'] = story_update['status'].capitalize(
                ) if story_update['status'] else 'None'
                b['element']['initial_option']['value'] = story_update['status'].lower(
                ) if story_update['status'] else 'none'
            elif b['label']['text'] == 'User Type':
                b['element']['initial_value'] = story_update['user_type'].capitalize()
            elif b['label']['text'] == 'Story Title':
                b['element']['initial_value'] = story_update['story'].capitalize()
            elif b['label']['text'] == 'Assigned To':
                b['element']['initial_user'] = story_update['assigned_to'] if story_update['assigned_to'] else "None"
            elif b['label']['text'] == 'Description':
                b['element']['initial_value'] = story_update['description']
        return modal

    def process_modal_submission(self, payload, callback_id):
        payload_values = list(payload['view']['state']['values'].values())

        # Add an if-clause here with your callback_id used in the modal
        if callback_id == "create-story-modal":
            self._process_create_update_submission(payload_values)
        elif callback_id == "delete-story-modal":
            return self._process_delete_story(payload_values)
        elif callback_id == "confirm-delete-story-modal":
            md = json.loads(payload['view']['private_metadata'])
            self._process_story_confirm_delete(md)
        elif callback_id == "confirm-story-modal":
            self._process_confirm_story(payload_values)
        elif callback_id == "search-story-modal":
            self._process_search_story(payload_values)
        elif callback_id == "create-swimlane-modal":
            self._process_create_swimlane(payload_values)
        elif callback_id == "update-swimlane-modal":
            names = self._process_update_swimlane(payload_values)
            return names
        elif callback_id == "confirm-delete-swimlane-modal":
            md = json.loads(payload['view']['private_metadata'])
            self._process_swimlane_confirm_delete(md)
        elif callback_id == "example-modal":
            # Here's where you call the function to process your modal's submission
            # e.g. self._process_example_submission(payload_values)
            pass
        elif callback_id == "update-story-modal":
            md = json.loads(payload['view']['private_metadata'])
            self._process_create_update_submission(
                payload_values, [md["story"]["id"], md["log"]])  # payload['view']['private_metadata'].split(','))
        elif callback_id == "start-sprint-modal":
            pass
            # ignore because this is handled in slack_interface.py
            # since we need the client to schedule a message
        else:
            pass

    def process_delete_sequence(self, payload):
        callback_id = payload['view']['callback_id']
        payload_values = list(payload['view']['state']['values'].values())
        print(
            f"PROCESS DELETE METADATA: {payload['view']['private_metadata']}")
        if payload['view']['private_metadata'] != "None":
            metadata = json.loads(payload['view']['private_metadata'])
        else:
            metadata = {"swimlane": "Product Backlog", "sort_by": "UNSORTED"}

        if callback_id == "delete-story-modal":
            story_id_list = self._process_delete_story(payload_values)
            metadata['story'] = story_id_list
            injected_view = self._fill_confirm_delete_modal(
                modal=CONFIRM_DELETE_MODAL, metadata=json.dumps(metadata), callback_id="confirm-delete-story-modal")
        else:
            swimlane = self._process_delete_swimlane(payload_values)
            # metadata = {"swimlane": swimlane}
            metadata['swimlane-to-delete'] = swimlane
            injected_view = self._fill_confirm_delete_modal(
                modal=CONFIRM_DELETE_MODAL, metadata=json.dumps(metadata), callback_id="confirm-delete-swimlane-modal")

        return injected_view

    def _process_start_sprint_submission(self, payload_values):
        start_date = payload_values[0]['sprint-date']['selected_date']
        start_time = payload_values[0]['sprint-time']['selected_time']
        duration = int(payload_values[1]['duration']
                       ['selected_option']['text']['text'])
        unit = payload_values[1]['unit']['selected_option']['text']['text']
        seconds_table = {
            'days': 86400,
            'weeks': 604800,
            'months': 2419200,
        }
        duration_in_seconds = duration * seconds_table[unit]
        unix_start = int(datetime.strptime(
            f'{start_date} {start_time}', '%Y-%m-%d %H:%M').timestamp())
        unix_end = unix_start + duration_in_seconds
        self.scrum_board.write_metadata_field(
            'current_sprint_starts', unix_start)
        self.scrum_board.write_metadata_field('current_sprint_ends', unix_end)

        # TODO:
        # schedule a message for when the sprint ends (unix_end)

        self.text = f"Sprint has been set!\nIt begins on {start_date} at {start_time} " + \
                    f"and ends on {datetime.fromtimestamp(unix_end).strftime('%Y-%m-%d at %H:%M')}."
        self.blocks = None

    def move_sb_to_sprint(self):
        curr_sprint = self.scrum_board.read_metadata_field("current_sprint")
        self.scrum_board.write_metadata_field(
            field="current_sprint", value=curr_sprint+1)
        sb = self.scrum_board.read_log('Sprint Backlog')
        if not isinstance(sb, str):  # Indicates that sprint backlog is empty
            for s in sb:
                if s['status'] == "":
                    s['status'] = 'to-do'
                s['sprint'] = curr_sprint+1
                self.scrum_board.update_story(
                    s, "Sprint Backlog", "Current Sprint")

    def start_new_sprint(self):
        sprint_start = self.scrum_board.read_metadata_field(
            'current_sprint_starts')
        sprint_end = self.scrum_board.read_metadata_field(
            'current_sprint_ends')
        sprint_duration = self.scrum_board.read_metadata_field(
            'sprint_duration')

        self.scrum_board.write_metadata_field(
            'current_sprint_starts', sprint_start + sprint_duration)
        self.scrum_board.write_metadata_field(
            'current_sprint_ends', sprint_end + sprint_duration)

        # self.move_sb_to_sprint()

    def extend_sprint(self, new_end, success):
        # NOTE: extends sprint by ONE day
        if success:
            curr_sprint = self.scrum_board.read_metadata_field(
                "current_sprint")
            self.scrum_board.write_metadata_field(
                'current_sprint_ends', new_end)
            self.text = f"Sprint {curr_sprint} successfully extended." + \
                f" It now ends on {datetime.fromtimestamp(new_end).strftime('%Y-%m-%d at %H:%M')}"
        else:
            self.text = 'Extending sprint failed. Please try again.'

    def end_sprint(self, button=False, success=True):
        if success:
            # NOTE: ALSO STARTS NEW SPRINT
            curr_sprint = self.scrum_board.read_metadata_field(
                "current_sprint")
            self.text = f"Sprint {curr_sprint} has ended!\n"

            curr_sprint_log = self.scrum_board.read_log('Current Sprint')
            for s in curr_sprint_log:
                if s['status'] == 'completed':
                    # move to previous sprints
                    self.scrum_board.update_story(
                        s, "Current Sprint", "Previous Sprint")
                else:
                    s['sprint'] += 1
                    self.scrum_board.update_story(
                        s, "Current Sprint", "Current Sprint")

            self.start_new_sprint()
            if button:
                self.move_sb_to_sprint()
                sprint_end = self.scrum_board.read_metadata_field(
                    'current_sprint_ends')
                self.text += f"Sprint {curr_sprint+1} has started and ends {datetime.fromtimestamp(sprint_end).strftime('%Y-%m-%d at %H:%M')}"
        else:
            self.text = "Failed to end sprint. Please try again or manually set a new sprint."

    def handle_sprint_submission(self, start, end, success=None):
        self.text = ""
        if success:
            curr_sprint_start = self.scrum_board.read_metadata_field(
                "current_sprint_starts")
            # if a sprint already exists, user was warned and still set a new one.
            # so end the current sprint
            if curr_sprint_start != 0:
                self.end_sprint()

            self.scrum_board.write_metadata_field(
                'current_sprint_starts', start)
            self.scrum_board.write_metadata_field('current_sprint_ends', end)
            self.scrum_board.write_metadata_field('sprint_duration', end-start)

            # move stories in Sprint Backlog to Current Sprint swimlane:
            self.move_sb_to_sprint()

            # save scheduled message in metadata
            self.save_sched_message(
                'end_sprint', success["scheduled_message_id"])
            # sched_msgs = self.scrum_board.read_metadata_field("scheduled_messages")
            # msg_id = success["scheduled_message_id"]
            # sched_msgs['end_sprint'] = msg_id
            # self.scrum_board.write_metadata_field('scheduled_messages', sched_msgs)

            curr_sprint = self.scrum_board.read_metadata_field(
                "current_sprint")
            self.text += f"Sprint {curr_sprint} has been set!\nIt begins on {datetime.fromtimestamp(start).strftime('%Y-%m-%d at %H:%M')} " + \
                f"and ends on {datetime.fromtimestamp(end).strftime('%Y-%m-%d at %H:%M')}."
            self.blocks = None
        else:
            self.text = "Failed to set sprint. Please try again."
            self.blocks = None

    def save_sched_message(self, field, msg_id):
        sched_msgs = self.scrum_board.read_metadata_field("scheduled_messages")
        sched_msgs[field] = msg_id
        self.scrum_board.write_metadata_field('scheduled_messages', sched_msgs)

    def get_end_sprint_msg_id(self):
        sched_msgs = self.scrum_board.read_metadata_field("scheduled_messages")
        return sched_msgs['end_sprint']

    def check_if_sprint_exists(self):
        sched_msgs = self.scrum_board.read_metadata_field("scheduled_messages")
        return sched_msgs['end_sprint']  # will be 0 if not set

    def get_sprint_end_msg(self, start, end):
        msg = SPRINT_END_MSG
        new_sprint = self.scrum_board.read_metadata_field("current_sprint") + 1
        msg['blocks'][0]['text']['text'] = f"Sprint {new_sprint} has ended!"
        msg['blocks'][1]['elements'][0][
            'text'] = f"*Started:* {datetime.fromtimestamp(start).strftime('%Y-%m-%d at %H:%M')}"
        msg['blocks'][1]['elements'][1][
            'text'] = f"*Ended:* {datetime.fromtimestamp(end).strftime('%Y-%m-%d at %H:%M')}"
        return msg

    def _process_create_update_submission(self, payload_values, metadata=[]):
        desc = self._get_plaintext_input_item(payload_values, 8)
        estimate = int(self._get_dropdown_select_item(payload_values, 7))
        priority = self.priorities[self._get_radio_group_item(
            payload_values, 6).capitalize()]
        status = self._get_radio_group_item(payload_values, 5)
        assigned_to = self._get_userselect_item(payload_values, 4)
        try:
            sprint = int(self._get_plaintext_input_item(payload_values, 3))
        except:
            self.text = "Sprint must be an integer."
            self.blocks = None
            return
        user_type = self._get_plaintext_input_item(payload_values, 2)
        story_title = self._get_plaintext_input_item(payload_values, 1)
        swimlane = self._get_dropdown_select_item(payload_values, 0)

        story = {
            "id": int(metadata[0]) if metadata else None,
            "priority": priority,
            "estimate": estimate,
            "sprint": sprint,
            "status": status,
            "assigned_to": assigned_to,
            "user_type": user_type,
            "story": story_title,
            "description": desc
        }

        if metadata:
            update = self.scrum_board.update_story(
                story, metadata[1], swimlane)
            self.text = f"Story {int(metadata[0])} updated successfully!" if update else f"Failed to update story {int(metadata[0])}."
            self.blocks = None
        else:
            created_sid = self.scrum_board.create_story(story, swimlane)
            self.text = f"Story {created_sid} created successfully!" if created_sid else "Failed to create story."
            self.blocks = None

    def _story_to_msg(self, story, md=""):
        story_data, log = self.scrum_board.read_story(story['id'], log=None)
        block = copy.deepcopy(READ_STORY_BLOCK)

        story_content, actions = block[3]['fields'], block[5]['elements']

        # Set the context field to the story's log
        block[1]['elements'][0]['text'] = f"{' '.join([tag[0].upper() + tag[1:] for tag in log.split('_')])}"

        for k, v in story_data.items():
            if v:
                if k == "id":
                    block[0]['text']['text'] = f"Story ID: {v}"
                else:
                    story_content.append({
                        "type": "mrkdwn",
                        "text": self._get_msg_text(k, v)
                    })

        if log != "Previous Sprint" and log != "Archived":
            for action in actions:
                if action['text']['text'] == 'Update':
                    story, log = self.scrum_board.read_story(story['id'])
                    metadata = {"story": story, "log": log}
                    if md:
                        mdata = json.loads(md)
                        metadata["swimlane"] = mdata["swimlane"]
                        metadata["sort_by"] = mdata["sort_by"]
                    action['action_id'] = "update-story"
                    action['value'] = json.dumps(metadata)
                else:
                    action['action_id'] = "delete-story"
                    metadata = {"story": f"story {str(story['id'])}"}
                    if md:
                        mdata = json.loads(md)
                        metadata["swimlane"] = mdata["swimlane"]
                        metadata["sort_by"] = mdata["sort_by"]
                    action['value'] = json.dumps(metadata)
        else:
            block = block[:-2]
        return block

    def _get_msg_text(self, key, val):
        label = ' '.join([tag[0].upper() + tag[1:] for tag in key.split('_')])
        text = f"*{label}:* "

        if label == "Priority" or label == "Status":
            try:
                emoji = emojis[key][val]
            except KeyError:
                emoji = ""

            if label == "Priority":
                for k, v in self.priorities.items():
                    if v == val:
                        val = k
                        break
            return text + f"{val}\t" + emoji
        elif label == "Assigned To":
            return text + self._get_member_name(val)
        elif label == "Estimate" or label == "Sprint" or label == "User Type" or label == "Story" or label == "Description":
            return text + f"{val}"
        else:
            return ""

    def _process_delete_story(self, payload_values):
        story_id_string = self._get_plaintext_input_item(
            payload_values, 0)
        story_id_list = re.findall(r'[0-9]+', story_id_string)
        return ",".join(story_id_list)

    def _process_story_confirm_delete(self, payload_values):
        story_ids = payload_values
        story_id_list = story_ids['story'].split(",")

        for story_id in story_id_list:
            response = self.scrum_board.delete_story(int(story_id))
            self.text = self.text + "\n" + response
        self.blocks = None

    def _process_swimlane_confirm_delete(self, payload_values):
        swimlane_name = payload_values["swimlane-to-delete"]
        self.text = self.scrum_board.delete_swimlane(swimlane_name)
        self.blocks = None

    def _process_search_story(self, payload_values):
        lookup_text = self._get_plaintext_input_item(payload_values, 0)
        fields = self._get_static_multi_select_item(payload_values, 1)
        swimlanes = self._get_static_multi_select_item(payload_values, 2)
        include_archived = self._get_checkboxes_action(payload_values, 3)
        include_archived = False if include_archived == [] else True
        stories = self.scrum_board.search_story(
            lookup_text=lookup_text, logs=swimlanes, fields=fields, include_archived=include_archived)
        self.blocks = []
        if isinstance(stories, str):
            self.text = stories  # Handles error case of string from scrum_board
            return
        # Otherwise, stories is a list of objs that are pretty-printed.
        for story in stories:
            self.blocks += self._story_to_msg(story)
        self.text = "Story:"

    def _process_create_swimlane(self, payload_values):
        log_name = self._get_plaintext_input_item(payload_values, 0)
        self.text = self.scrum_board.create_swimlane(log_name=log_name)
        self.blocks = []

    def _process_update_swimlane(self, payload_values):
        old_name = self._get_dropdown_select_item(payload_values, 0)
        new_name = self._get_plaintext_input_item(payload_values, 1)
        self.text = self.scrum_board.update_swimlane(old_name, new_name)
        self.blocks = []
        return [old_name, new_name]

    def _process_delete_swimlane(self, payload_values):
        selected_option = self._get_dropdown_select_item(payload_values, 0)
        idx = selected_option.find("(")
        name = selected_option[:idx-1]  # need to remove " (X)" notation
        return name

    @staticmethod
    def _get_member_name(id):
        with open('data/scrum_board.json') as f:
            id_to_name = json.load(f)['metadata']['id_to_name']
        try:
            return id_to_name[id]
        except KeyError:
            return id

    # Methods to help parse modal submission payload fields
    @staticmethod
    def _get_userselect_item(payload_values, index):
        return payload_values[index]['users_select-action']['selected_user']

    @ staticmethod
    def _get_dropdown_select_item(payload_values, index):
        return payload_values[index]['static_select-action']['selected_option']['text']['text']

    @ staticmethod
    def _get_plaintext_input_item(payload_values, index):
        return payload_values[index]['plain_text_input-action']['value']

    @staticmethod
    def _get_radio_group_item(payload_values, index):
        return payload_values[index]['radio_buttons-action']['selected_option']['value']

    @staticmethod
    def _get_static_multi_select_item(payload_values, index):
        selected_text = []
        selected_options = payload_values[index]['multi_static_select-action']['selected_options']
        for x in selected_options:
            selected_text.append(x['text']['text'])
        return selected_text

    @staticmethod
    def _get_checkboxes_action(payload_values, index):
        return payload_values[index]["actionId-0"]['selected_options']

    def get_response(self):
        # self.text is the textual message to be displayed by bot
        # self.blocks is the interactive message (e.g. modal) to be displayed in JSON
        return (self.text, self.blocks)

    def reset(self):
        self.text, self.blocks = "\0", None
