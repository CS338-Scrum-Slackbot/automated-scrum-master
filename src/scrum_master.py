"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard
from modal_editor import ModalEditor
from block_ui.create_story_ui import CREATE_STORY_MODAL
from block_ui.delete_story_ui import DELETE_STORY_MODAL
from block_ui.update_story_ui import UPDATE_STORY_MODAL
from block_ui.example_modal_ui import EXAMPLE_MODAL
from block_ui.read_story_ui import READ_STORY_BLOCK
from block_ui.set_sprint_ui import SET_SPRINT_MODAL
from block_ui.home_page_ui import * #INIT_HOME_PAGE, SWIMLANE_HEADER, SWIMLANE_FOOTER, SORT_DROPDOWN, STORY_BLOCK, RADIO_INIT_OPTION, SWIMLANE_OPTION
import json
import copy
import re
from datetime import datetime
import itertools


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

    def update_home(self, payload, metadata=""):
        # print(json.dumps(payload, indent=4))
        # print(f'\n\nUPDATE HOME METADATA: {metadata}\n\n')
        swimlane_select = []
        story_blocks = []
        swimlane_header = []
        swimlane_footer = []
        sort_by_block = []

        init_option, sort_by = None, None
        if metadata and metadata != 'None':
            print(f'UPDATE HOME METADATA: {metadata}, {type(metadata)}')
            md = json.loads(metadata)
            print('\n\nSTORY IN METADATA\n\n')
            init_option = md['swimlane'] if md['swimlane'] != 'UNSELECTED' else None
            if init_option: sort_by_block = SORT_DROPDOWN
            sort_by = md['sort_by'] if md['sort_by'] != "UNSORTED" else None
            print(init_option, sort_by)
        
        if not init_option:
            if 'swimlane_select' in payload['view']['state']['values']:
                init_option = payload['view']['state']['values']['swimlane_select']['swimlane_select']['selected_option']['value']
                sort_by_block = SORT_DROPDOWN
            else: init_option = None

        if not sort_by:
            if 'sort_by' in payload['view']['state']['values']:
                if payload['view']['state']['values']['sort_by']['sort_by']['selected_option']:
                    sort_by = payload['view']['state']['values']['sort_by']['sort_by']['selected_option']['value']
                else: sort_by = None
            else: sort_by = None

        metadata2 = {"swimlane": init_option if init_option else "UNSELECTED", "sort_by": sort_by if sort_by else "UNSORTED"}

        if init_option: 
            # print(f'INIT OPTION!!!!!! {init_option}')
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
                if sort_by: stories = sorted(stories, key = lambda x: x[sort_by])
                story_blocks = flatten([self._story_to_msg(story, add_divider=True, md=json.dumps(metadata2)) for story in stories])
            else:
                story_blocks = [{
                                    "type": "section",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "There are no stories in this swimlane.",
                                        "emoji": True
                                    }
                                }]

        swimlane_select = self.populate_swimlanes(INIT_HOME_PAGE, init_option=init_option)
        for x in range(len(swimlane_select[3]['elements'])):
            swimlane_select[3]['elements'][x]['value'] = json.dumps(metadata2)
        

        ui = list(itertools.chain(swimlane_select, swimlane_header, sort_by_block, story_blocks, swimlane_footer))
        # print(f'\n\nUI: {json.dumps(ui, indent = 4)}\n\n')
        print(json.dumps(ui, indent=4))

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
        self._create_modal_btn(text="Create Story",
                                   action_id="create-story")

    def delete_story(self):
        self._create_modal_btn(text="Delete Story",
                                   action_id="delete-story")

    def update_story(self):
        try: 
            id = int(self.text.split(' ')[-1])
        except: 
            self.text = "Story ID must be an int."
            return
        result = self.scrum_board.read_story(id)
        if isinstance(result, str):
            self.text = result
            return
        story = result[0]
        log = result[1]
        metadata = {"story":story, "log":log}
        self._create_modal_btn(text=f"Update Story {id}", action_id="update-story", metadata=json.dumps(metadata))

    def read_story(self):
        try:
            read_text = " ".join(self.text.split()[2:])
        except ValueError:
            self.text = "Could not understand read story command."
            return

        try:
            id_text  = int(self.text.split()[2])
        except (ValueError, IndexError):
            id_text = None
            
        read_text = " ".join(self.text.split()[2:])
        log = None
        from_idx = read_text.find("from")
        if from_idx != -1:
            log_idx = from_idx + 5
            log = read_text[log_idx:]
        self.blocks = []
        if id_text:
            # If ID is specified, read specific story.
            result = self.scrum_board.read_story(id=id_text, log=log)
            if isinstance(result, str):
                self.text = result # Handles error case of string from scrum_board
                return
            # Otherwise, stories is one obj that is pretty-printed.
            story = result[0]
            log = result[1]
            self.blocks += self._story_to_msg(story)
            self.text = f"Story {id_text} from {log}:"
        else:
            # If there is no ID, return the swimlane/log/entire board.
            stories = self.scrum_board.read_log(log=log)
            self.blocks = []
            if isinstance(stories, str):
                self.text = stories # Handles error case of string from scrum_board
                return
            for story in stories:
                self.blocks += self._story_to_msg(story)
            self.text = "Story:"

    def search_story(self):
        self._create_modal_btn(text="Search story",
                                   action_id="search-story")

    def start_sprint(self):
        self.current_sprint += 1
        jsr = jr.json_reader("data/scrum_board.json")
        sb = jsr.read_log('sprint_backlog')
        for s in sb: 
            if s['status'] == "": s['status'] = 'to-do'
            s['sprint'] += self.current_sprint
            jsr.update(id=s['id'], new_entry=s, old_log='sprint_backlog')
            jsr.move(id=s['id'], dest_log='current_sprint', src_log='sprint_backlog')
        self._create_modal_btn(text="Set Sprint",
                                    action_id="set-sprint")

    def create_swimlane(self):
        self._create_modal_btn(text="Create swimlane",
                                   action_id="create-swimlane")

    def update_or_delete_swimlane(self, action: str): # Where action="update" or "delete"
        if len(self.scrum_board.list_user_swimlanes()) == 0:
            # if there are no user-generated swimlanes ..
            self.text = f"You have no swimlanes to {action}. You cannot {action} default swimlanes, but you may create new ones using `create swimlane`."
            return
        else: self._create_modal_btn(text=f"{action.title()} swimlane",
                                   action_id=f"{action}-swimlane")

    def process_user_msg(self, text: str):
        """
        Need to make some assumptions about how users will communicate with the bot (at least pre-NLP)
        Command: "create a story" will make a button that opens a create story modal
        """
        self.text = text

        if "create story" in text.lower():
            self.create_story()
        elif "delete story" in text.lower():
            self.delete_story()
        elif "update story" in text.lower():
            self.update_story()
        elif "read story" in text.lower():
            self.read_story()
        elif "search story" in text.lower():
            self.search_story()
        elif "start sprint" in text.lower():
            self.start_sprint()
        elif "create swimlane" in text.lower():
            self.create_swimlane()
        elif "update swimlane" in text.lower():
            self.update_or_delete_swimlane("update")
        elif "delete swimlane" in text.lower():
            self.update_or_delete_swimlane("delete")
        else:
            self.text = "Command not found, please use a keyword ('create', 'read', 'update', 'delete')."

    def _create_modal_btn(self, text="", action_id="", metadata="None"):
        """Creates an interactive button so that we can obtain a trigger_id for modal interaction

        IMPORTANT!!! Remember what action_id you used because you will need to use it in create_modal
        """
        self.blocks = [
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
        self.text = ""

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
            modal =  self.editor.edit_create_swimlane_modal()
            modal['private_metadata'] = metadata
            return modal
        elif action_id == "update-swimlane":
            modal =  self.editor.edit_update_or_delete_swimlane_modal("update")
            modal['private_metadata'] = metadata
            return modal
        elif action_id == "delete-swimlane":
            modal = self.editor.edit_update_or_delete_swimlane_modal("delete")
            modal['private_metadata'] = metadata
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
        curr_sprint = str(self.scrum_board.read_metadata_field("current_sprint"))
        modal['blocks'][4]['element']['placeholder']['text'] = "Current sprint number: "+curr_sprint
        modal['private_metadata'] = metadata
        return modal

    def _fill_delete_modal(self, modal, metadata=None):
        print(f'FILL DELETE MODAL METADATA: {metadata}')
        try:
            init_value = json.loads(metadata)['story']
        except:
            init_value = ""
        modal['blocks'][1]['element']['initial_value'] = init_value #md['story']
        modal['private_metadata'] = metadata
        return modal


    def init_sprint_modal(self, modal):
        today = datetime.now().strftime("%Y-%m-%d %H:%M").split()
        modal['blocks'][1]['elements'][0]['initial_date'] = today[0]
        modal['blocks'][1]['elements'][1]['initial_time'] = today[1]
        return modal

    def _get_valid_logs(self, create=0):
        # can create a story in any swimlane EXCEPT previous_sprint and archived
        if create: return [x for x in self.scrum_board.get_logs() if x not in ['Previous Sprint','Archived']]
        # can move a story to any swimlane EXCEPT previous_sprint
        else: return [x for x in self.scrum_board.get_logs() if x != 'Previous Sprint']

    def _fill_update_modal(self, modal, metadata):
        print(f'\n\nFILL UPDATE MODEL METADATA: {metadata}\n\n')
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
            private_metadata = {"story":story_update, "log": data["log"], "swimlane": data["swimlane"], "sort_by": data["sort_by"]}
        else:
            private_metadata = {"story":story_update, "log": data["log"]}
        modal['private_metadata'] = json.dumps(private_metadata) #f'{story_update["id"]},{data["log"]}'
        for b in modal['blocks']:
            if b['label']['text'] == 'Swimlane':
                b['element']['options'] = swimlane_options
                b['element']['initial_option']['text']['text'] = data['log']
                b['element']['initial_option']['value'] = data['log']
            elif b['label']['text'] == 'Estimate':
                b['element']['initial_option']['text']['text'] = str(story_update['estimate']) if story_update['estimate'] != -1 else "1"
                b['element']['initial_option']['value'] = str(story_update['estimate']) if story_update['estimate'] != -1 else "1"
            elif b['label']['text'] == 'Sprint':
                curr_sprint = str(self.scrum_board.read_metadata_field("current_sprint"))
                b['element']['initial_value'] = str(story_update['sprint']) #if story_update['sprint'] else curr_sprint
                b['element']['placeholder']['text'] = "Current sprint number: "+curr_sprint
            elif b['label']['text'] == 'Priority':
                if story_update['priority'] != -1: 
                    p = list(self.priorities.keys())[list(self.priorities.values()).index(story_update['priority'])]
                    b['element']['initial_option']['text']['text'] = p
                    b['element']['initial_option']['value'] = p.lower()
                else:
                    b['element']['initial_option']['text']['text'] = 'Low'
                    b['element']['initial_option']['value'] = 'low'
            elif b['label']['text'] == 'Status':
                b['element']['initial_option']['text']['text'] = story_update['status'].capitalize() if story_update['status'] else 'None'
                b['element']['initial_option']['value'] = story_update['status'].lower() if story_update['status'] else 'none'
            elif b['label']['text'] == 'User Type':
                b['element']['initial_value'] = story_update['user_type'].capitalize()
            elif b['label']['text'] == 'Story Title':
                b['element']['initial_value'] = story_update['story'].capitalize()
            elif b['label']['text'] == 'Assigned To':
                b['element']['initial_user'] = story_update['assigned_to'] if story_update['assigned_to'] else "None"
        return modal

    def process_modal_submission(self, payload, callback_id):
        payload_values = list(payload['view']['state']['values'].values())

        # Add an if-clause here with your callback_id used in the modal
        if callback_id == "create-story-modal":
            self._process_create_update_submission(payload_values)
        elif callback_id == "delete-story-modal":
            self._process_delete_story(payload_values)
        elif callback_id == "search-story-modal":
            self._process_search_story(payload_values)
        elif callback_id == "create-swimlane-modal":
            self._process_create_swimlane(payload_values)
        elif callback_id == "update-swimlane-modal":
            names = self._process_update_swimlane(payload_values)
            return names
        elif callback_id == "delete-swimlane-modal":
            self._process_delete_swimlane(payload_values)
        elif callback_id == "example-modal":
            # Here's where you call the function to process your modal's submission
            # e.g. self._process_example_submission(payload_values)
            pass
        elif callback_id == "update-story-modal":
            md = json.loads(payload['view']['private_metadata'])
            print(f'\n\nPROCESS MODAL SUBMISSION MD: {md}\n\n')
            # metadata = f'{md["story"]["id"]},{md["log"]}'
            self._process_create_update_submission(
                payload_values, [md["story"]["id"],md["log"]])#payload['view']['private_metadata'].split(','))
        elif callback_id == "start-sprint-modal":
            self._process_start_sprint_submission(payload_values)
        else:
            pass

    def  _process_start_sprint_submission(self, payload_values):
        print(json.dumps(payload_values, indent=4))
        start_date = payload_values[0]['sprint-date']['selected_date']
        start_time = payload_values[0]['sprint-time']['selected_time']
        duration = int(payload_values[1]['duration']['selected_option']['text']['text'])
        unit = payload_values[1]['unit']['selected_option']['text']['text']
        seconds_table = {
            'days': 86400,
            'weeks': 604800,
            'months': 2419200,
        }
        duration_in_seconds = duration * seconds_table[unit]
        unix_start = int(datetime.strptime(f'{start_date} {start_time}', '%Y-%m-%d %H:%M').timestamp())
        unix_end = unix_start + duration_in_seconds
        self.scrum_board.write_metadata_field('current_sprint_starts', unix_start)
        self.scrum_board.write_metadata_field('current_sprint_ends', unix_end)

        # TODO:
        # schedule a message for when the sprint ends (unix_end)
        
        self.text = f"Sprint has been set!\nIt begins on {start_date} at {start_time} " + \
                    f"and ends on {datetime.fromtimestamp(unix_end).strftime('%Y-%m-%d at %H:%M')}."
        self.blocks = None

    def _process_create_update_submission(self, payload_values, metadata=[]):
        # i = 0 if metadata else 1
        print(f'\n\nPROCESS UPDATE SUBMISSION MD: {metadata}\n\n')
        estimate = int(self._get_dropdown_select_item(payload_values, 7))
        priority = self.priorities[self._get_radio_group_item(payload_values, 6).capitalize()]
        status = self._get_radio_group_item(payload_values, 5)
        assigned_to = self._get_userselect_item(payload_values, 4)
        try: sprint = int(self._get_plaintext_input_item(payload_values, 3))
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
                "story": story_title
                }

        if metadata:
            update = self.scrum_board.update_story(story, metadata[1], swimlane)
            self.text = f"Story {int(metadata[0])} updated successfully!" if update else f"Failed to update story {int(metadata[0])}."
            self.blocks = None
        else: 
            created_sid = self.scrum_board.create_story(story, swimlane)
            self.text = f"Story {created_sid} created successfully!" if created_sid else "Failed to create story."
            self.blocks = None


    def _story_to_msg(self, story, add_divider = False, md=""):
        block = copy.deepcopy(READ_STORY_BLOCK)
        story_content = block[0]['fields']
        actions = block[1]['elements']

        for k, v in story.items():
            # if v:
            label = [tag[0].upper() + tag[1:] for tag in k.split('_')]
            story_content.append({
                "type": "mrkdwn",
                "text": f"*{' '.join(label)}:* {ScrumMaster._get_member_name(v) if k=='assigned_to' else v}",
            })

        # print(f'\n\nmd: {json.loads(md)}\n\n')
        for action in actions:
            if action['text']['text'] == 'Update':
                story, log = self.scrum_board.read_story(story['id'])
                metadata = {"story":story, "log":log}
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
                    metadata["swimlane"] =  mdata["swimlane"]
                    metadata["sort_by"] = mdata["sort_by"]
                action['value'] = json.dumps(metadata)

        if add_divider: block.append({"type": "divider"})
        return block


    def _process_delete_story(self, payload_values):
        story_id_string = self._get_plaintext_input_item(payload_values, 0)
        story_id_list = re.findall(r'[0-9]+', story_id_string)

        for story_id in story_id_list:
            response = self.scrum_board.delete_story(story_id)
            self.text = self.text + "\n" + response

        self.blocks = None

    def _process_search_story(self, payload_values):
        lookup_text = self._get_plaintext_input_item(payload_values, 0)
        fields = self._get_static_multi_select_item(payload_values, 1)
        swimlanes = self._get_static_multi_select_item(payload_values, 2)
        stories = self.scrum_board.search_story(lookup_text=lookup_text, logs=swimlanes, fields=fields )
        self.blocks = []
        if isinstance(stories, str):
            self.text = stories # Handles error case of string from scrum_board
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
        name = selected_option[:idx-1] # need to remove " (X)" notation
        self.text = self.scrum_board.delete_swimlane(name)
        self.blocks = []
        
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
        print(payload_values[index])
        return payload_values[index]['radio_buttons-action']['selected_option']['value']

    @staticmethod
    def _get_static_multi_select_item(payload_values, index):
        selected_text = []
        selected_options = payload_values[index]['multi_static_select-action']['selected_options']
        for x in selected_options:
            selected_text.append(x['text']['text'])
        return selected_text

    def get_response(self):
        # self.text is the textual message to be displayed by bot
        # self.blocks is the interactive message (e.g. modal) to be displayed in JSON
        return (self.text, self.blocks)

    def reset(self):
        self.text, self.blocks = "\0", None
