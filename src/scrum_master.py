"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard
import json_reader as jr
from modal_editor import ModalEditor
from block_ui.create_story_ui import CREATE_STORY_MODAL
from block_ui.delete_story_ui import DELETE_STORY_MODAL
from block_ui.update_story_ui import UPDATE_STORY_MODAL
from block_ui.example_modal_ui import EXAMPLE_MODAL
from block_ui.read_story_ui import READ_STORY_BLOCK
import json
import copy
import re


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

        # Maintain current sprint
        self.current_sprint = 0

        # Next story id
        self.sid = 8

        # Interface with JSON data
        self.scrum_board = ScrumBoard()

        # Modal editor
        self.editor = ModalEditor()

    
    def create_story(self):
        self._create_modal_btn(text="Create a Story",
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
        story, log = jr.json_reader("data/scrum_board.json").read(id)
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
            jsr.update(id=s['id'], new_entry=s, log='sprint_backlog')
            jsr.move(id=s['id'], dest_log='current_sprint', src_log='sprint_backlog')

    def process_user_msg(self, text: str):
        """
        Need to make some assumptions about how users will communicate with the bot (at least pre-NLP)
        Command: "create a story" will make a button that opens a create story modal
        """
        self.text = text

        if "create story" in text.lower():
            self.create_story()
        elif "create a story" in text.lower():
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
            return CREATE_STORY_MODAL
        elif action_id == "delete-story":
            return DELETE_STORY_MODAL
        elif action_id == "update-story":
            return self.fill_update_modal(UPDATE_STORY_MODAL, metadata)
        elif action_id == "search-story":
            return self.editor.edit_search_story_modal()
        elif action_id == "example":
            return EXAMPLE_MODAL
        else:
            return ""

    def fill_update_modal(self, modal, metadata):
        data = json.loads(metadata)
        story_update = data['story']
        # story_update, update_log = jr.json_reader("data/scrum_board.json").read(id)
        modal['title']['text'] = f'Update Story {story_update["id"]}'
        modal['private_metadata'] = f'{story_update["id"]},{data["log"]}'
        for b in modal['blocks']:
            if b['label']['text'] == 'Estimate':
                b['element']['initial_option']['text']['text'] = str(story_update['estimate']) if story_update['estimate'] != -1 else "1"
                b['element']['initial_option']['value'] = str(story_update['estimate']) if story_update['estimate'] != -1 else "1"
            elif b['label']['text'] == 'Sprint':
                b['element']['initial_value'] = str(story_update['sprint']) if story_update['sprint'] else str(self.current_sprint)
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
                b['element']['initial_user'] = story_update['assigned_to']
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
        elif callback_id == "example-modal":
            # Here's where you call the function to process your modal's submission
            # e.g. self._process_example_submission(payload_values)
            pass
        elif callback_id == "update-story-modal":
            self._process_create_update_submission(
                payload_values, payload['view']['private_metadata'].split(','))
        else:
            pass

    def _process_create_update_submission(self, payload_values, metadata=[]):
        i = 0 if metadata else 1
        estimate = int(self._get_dropdown_select_item(payload_values, i+6))
        priority = self.priorities[self._get_radio_group_item(payload_values, i+5).capitalize()]
        status = self._get_radio_group_item(payload_values, i+4)
        assigned_to = self._get_userselect_item(payload_values, i+3)
        try: sprint = int(self._get_plaintext_input_item(payload_values, i+2))
        except:
            self.text = "Sprint must be an integer."
            self.blocks = None
            return
        user_type = self._get_plaintext_input_item(payload_values, i+1)
        story_title = self._get_plaintext_input_item(payload_values, i)
        swimlane = metadata[1] if metadata else self._get_dropdown_select_item(payload_values, 0).lower().replace(" ", "_")

        story = {
                "id": int(metadata[0]) if metadata else self.sid,
                "priority": priority,
                "estimate": estimate,
                "sprint": sprint,
                "status": status,
                "assigned_to": assigned_to,
                "user_type": user_type,
                "story": story_title
                }

        if metadata:
            update = self.scrum_board.update_story(story, swimlane)
            self.text = f"Story {int(metadata[0])} updated successfully!" if update else f"Failed to update story {int(metadata[0])}."
            self.blocks = None
        else: 
            create_story = self.scrum_board.create_story(story, swimlane)
            self.text = f"Story {self.sid} created successfully!" if create_story else "Failed to create story."
            self.blocks = None
            self.sid += 1


    def _story_to_msg(self, story):
        block = copy.deepcopy(READ_STORY_BLOCK)
        story_content = block[0]['fields']
        actions = block[1]['elements']

        for k, v in story.items():
            if v:
                story_content.append({
                    "type": "mrkdwn",
                    "text": f"*{k[0].upper() + k[1:]}:* {ScrumMaster._get_member_name(v) if k=='assigned_to' else v}",
                })

        for action in actions:
            if action['value'] == 'update-story':
                action['action_id'] = f"update-story-{story['id']}"
            elif action['value'] == 'move-story':
                action['action_id'] = f"move-story-{story['id']}"
            else:
                action['action_id'] = f"delete-story-{story['id']}"
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
        if isinstance(stories, str):
            self.text = stories # Handles error case of string from scrum_board
            return
        # Otherwise, stories is a list of objs that are pretty-printed.
        self.blocks = []
        for story in stories:
            self.blocks += self._story_to_msg(story)
        self.text = "Story:"
    
    @staticmethod
    def _get_member_name(id):
        from slack_interface import get_member
        ret = get_member(id)
        if ret:
            return ret['real_name'] if ret['real_name'] else ret['display_name']
        else:
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

    def get_response(self):
        # self.text is the textual message to be displayed by bot
        # self.blocks is the interactive message (e.g. modal) to be displayed in JSON
        return (self.text, self.blocks)

    def reset(self):
        self.text, self.blocks = "\0", None
