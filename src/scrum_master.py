"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard
from block_ui.create_story_ui import CREATE_STORY_MODAL
from block_ui.delete_story_ui import DELETE_STORY_MODAL
from block_ui.example_modal_ui import EXAMPLE_MODAL


class ScrumMaster:

    def __init__(self):
        self.text = "\0"
        self.blocks = None

        # Maintain current sprint
        self.current_sprint = 0

        # Next story id
        self.sid = 6

        # Interface with JSON data
        self.scrum_board = ScrumBoard()

    def process_user_msg(self, text: str):
        """
        Need to make some assumptions about how users will communicate with the bot (at least pre-NLP)
        Command: "create a story" will make a button that opens a create story modal
        """

        self.text = text

        if "create a story" in text:
            self._create_modal_btn(text="Create a Story",
                                   action_id="create-story")
        elif "delete story" in text:
            self._create_modal_btn(text="Delete a Story",
                                   action_id="delete-story")
            # processed_text = text[14:]
            # response = self.scrum_board.delete_story()
            # print("deleted")
            # self.text = response
        # Example
        elif "example modal" in text:
            self._create_modal_btn(text="Example Modal", action_id="example")
        # End example
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

    @staticmethod
    def create_modal(action_id):
        # Add an if-clause to parse what happens if we receive your action_id to create a modal
        if action_id == "create-story":
            return CREATE_STORY_MODAL
        # TODO: Figure out flow for delete story
        elif action_id == "delete-story":
            return DELETE_STORY_MODAL
        elif action_id == "example":
            return EXAMPLE_MODAL
        else:
            return ""

    def process_modal_submission(self, payload, callback_id):
        payload_values = list(payload['view']['state']['values'].values())

        # Add an if-clause here with your callback_id used in the modal
        if callback_id == "create-story-modal":
            self._process_story_submission(payload_values)
        elif callback_id == "delete-story-modal":
            self._return_swimlane_stories(payload_values)
        elif callback_id == "example-modal":
            # Here's where you call the function to process your modal's submission
            # e.g. self._process_example_submission(payload_values)
            pass
        else:
            pass

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

        self.text = str([board, priority, estimate, sprint,
                         assigned_to, user_type, story_desc])

    def _return_swimlane_stories(self, payload_values):
        swimlane = self._get_dropdown_select_item(payload_values, 0)
        print(swimlane)
        self.text = "updated_modal"
        self.blocks = {
            "view": {
                "type": "modal",
                "title": {
                    "type": "plain_text",
                    "text": "Updated view"
                },
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": "I've changed and I'll never be the same. You must believe me."
                        }
                    }
                ]
            }
        }

    # Methods to help parse modal submission payload fields
    @ staticmethod
    def _get_userselect_item(payload_values, index):
        return payload_values[index]['users_select-action']['selected_user']

    @ staticmethod
    def _get_dropdown_select_item(payload_values, index):
        return payload_values[index]['static_select-action']['selected_option']['text']['text']

    @ staticmethod
    def _get_plaintext_input_item(payload_values, index):
        return payload_values[index]['plain_text_input-action']['value']

    def get_response(self):
        # self.text is the textual message to be displayed by bot
        # self.blocks is the interactive message (e.g. modal) to be displayed in JSON
        return (self.text, self.blocks)
