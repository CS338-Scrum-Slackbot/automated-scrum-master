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
import json
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
        self.sid = 6

        # log of story being updated:
        self.update_log = ''
        # story object being updated:
        self.story_update = {}
        # Interface with JSON data
        self.scrum_board = ScrumBoard()
        # Modal editor
        self.editor = ModalEditor()

    def process_user_msg(self, text: str):
        """
        Need to make some assumptions about how users will communicate with the bot (at least pre-NLP)
        Command: "create a story" will make a button that opens a create story modal
        """
        # words = text.lower().split(' ')

        # command = ""
        # for word in words:
        #     if word in self.commands.keys():
        #         command = word

        # action = self.commands[command]
        # if command == "create":
        #     action(self.sid, 2, "customer", "create story test")
        #     self.text = "Successfully added story."
        # if command == "update":
        #     id, field, value = words[1], words[2], ' '.join(words[3:])
        #     # rudimentary input checks
        #     if field not in self.fields:
        #         self.text = f"Invalid field \'{field}\'. Must be one of [{', '.join(self.fields)}]"
        #         return
        #     if field == 'priority': value = self.priorities[value]
        #     elif field in ['estimate','sprint']:
        #         try: value = int(value)
        #         except:
        #             self.text = f"Invalid input type for {field}. Given {type(value)}; expected int."
        #             return
        #     success = action(id, field, value)
        #     self.text = "Successfully updated story." if success else f"Could not find story with id {id}."
        # else:
        #     self.text = "Sorry, I don't recognize that command."

        self.text = text

        if "create a story" in text:
            self._create_modal_btn(text="Create a Story",
                                   action_id="create-story")
        elif "delete story" in text:
            self._create_modal_btn(text="Delete a Story",
                                   action_id="delete-story")
        # End example
        elif "update story" in text:
            try:
                id = int(text.split(' ')[-1])
            except:
                self.text = "Story ID must be an int."
                return
            self.story_update, self.update_log = jr.json_reader(
                "data/scrum_board.json").read(id)
            self._create_modal_btn(
                text=f"Update Story {id}", action_id="update-story")
        elif "read" in text:
            # Sample message: @Miyagi read 1 from product_backlog
            # @Miyagi read 1
            read_text = " ".join(text.split()[1:])
            id_text = int(text.split()[1])
            log = None
            from_idx = read_text.find("from")
            if from_idx != -1:
                log_idx = from_idx + 5
                log = read_text[log_idx:]
            self.text = self.scrum_board.read(id=id_text, log=log)
        elif "search story" in text:
            self._create_modal_btn(text="Search story",
                                   action_id="search-story")
        # Example
        elif "example modal" in text:
            self._create_modal_btn(text="Example Modal", action_id="example")
        else:
            self.text = "Command not found, please use a keyword ('create', 'read', 'update', 'delete')."

    def _create_modal_btn(self, text="", action_id=""):
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
                        "value": "click_me_123",
                        "action_id": action_id
                    },
                ]
            }
        ] if text != "" else None
        self.text = ""

    # @staticmethod
    def create_modal(self, action_id):
        # Add an if-clause to parse what happens if we receive your action_id to create a modal
        if action_id == "create-story":
            return CREATE_STORY_MODAL
        elif action_id == "delete-story":
            return DELETE_STORY_MODAL
        elif action_id == "update-story":
            return self.fill_update_modal(UPDATE_STORY_MODAL, self.story_update['id'])
        elif action_id == "search-story":
            return self.editor.edit_search_story_modal()
        elif action_id == "example":
            return EXAMPLE_MODAL
        else:
            return ""

    def fill_update_modal(self, modal, id):
        self.story_update, self.update_log = jr.json_reader(
            "data/scrum_board.json").read(id)
        modal['title']['text'] = f'Update Story {self.story_update["id"]}'
        for b in modal['blocks']:
            if b['label']['text'] == 'Estimate':
                b['element']['initial_value'] = str(
                    self.story_update['estimate']) if self.story_update['estimate'] != -1 else "0"
            elif b['label']['text'] == 'Priority':
                if self.story_update['priority'] != -1:
                    p = list(self.priorities.keys())[
                        list(self.priorities.values()).index(self.story_update['priority'])]
                    b['element']['initial_option']['text']['text'] = p
                    b['element']['initial_option']['value'] = p.lower()
                else:
                    b['element']['initial_option']['text']['text'] = 'Low'
                    b['element']['initial_option']['value'] = 'low'
            elif b['label']['text'] == 'Status':
                b['element']['initial_option']['text']['text'] = self.story_update['status'].capitalize(
                ) if self.story_update['status'] else 'None'
                b['element']['initial_option']['value'] = self.story_update['status'] if self.story_update['status'] else 'none'
            elif b['label']['text'] == 'User Type':
                b['element']['initial_value'] = self.story_update['user_type'].capitalize()
            elif b['label']['text'] == 'User Story':
                b['element']['initial_value'] = self.story_update['story'].capitalize()
            elif b['label']['text'] == 'Assigned To':
                b['element']['initial_user'] = self.story_update['assigned_to']
        return modal

    def process_modal_submission(self, payload, callback_id):
        payload_values = list(payload['view']['state']['values'].values())

        # Add an if-clause here with your callback_id used in the modal
        if callback_id == "create-story-modal":
            self._process_story_submission(payload_values)
        elif callback_id == "delete-story-modal":
            self._process_delete_story(payload_values)
        elif callback_id == "update-story-modal":
            self._process_update_submission(payload_values)
        elif callback_id == "search-story-modal":
            self._process_search_story(payload_values)
        elif callback_id == "example-modal":
            # Here's where you call the function to process your modal's submission
            # e.g. self._process_example_submission(payload_values)
            pass
        else:
            pass

    def _process_update_submission(self, payload_values):
        try:
            estimate = int(self._get_plaintext_input_item(payload_values, 0))
        except:
            self.text = "Estimate must be an integer."
            self.blocks = None
            return
        priority = self.priorities[self._get_radio_group_item(
            payload_values, 1).capitalize()]
        status = self._get_radio_group_item(payload_values, 2)
        assigned_to = self._get_userselect_item(payload_values, 5)
        user_type = self._get_plaintext_input_item(payload_values, 3)
        story_desc = self._get_plaintext_input_item(payload_values, 4)
        update = self.scrum_board.update_story({
            "id": self.story_update['id'],
            "priority": priority,
            "estimate": estimate,
            "sprint": self.story_update['sprint'],
            "status": status,
            "assigned_to": assigned_to,
            "user_type": user_type,
            "story": story_desc
        }, self.update_log)
        self.text = f"Story {self.story_update['id']} updated successfully!" if update else "Failed to update story."
        self.blocks = None

    # Parses the payload of the create-story modal submission
    # To parse different modals, you need to create a new function that handles your modal
    def _process_story_submission(self, payload_values):
        board = self._get_dropdown_select_item(payload_values, 0)
        priority = int(self._get_dropdown_select_item(payload_values, 1))
        estimate = int(self._get_dropdown_select_item(payload_values, 2))
        sprint = self._get_plaintext_input_item(payload_values, 3)
        assigned_to = self._get_userselect_item(payload_values, 4)
        user_type = self._get_plaintext_input_item(payload_values, 5)
        story_desc = self._get_plaintext_input_item(payload_values, 6)

        create_story = self.scrum_board.create_story({
            "id": self.story_update["id"],
            "priority": priority,
            "estimate": estimate,
            "sprint": sprint,
            "status": status,
            "assigned_to": assigned_to,
            "user_type": user_type,
            "story": story_desc
        }, board)

        self.text = f"Story {self.story_update['id']} created successfully!" if update else "Failed to create story."
        self.blocks = None

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
        self.text = self.scrum_board.search(
            lookup_text=lookup_text, logs=swimlanes, fields=fields)
        self.blocks = None

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
