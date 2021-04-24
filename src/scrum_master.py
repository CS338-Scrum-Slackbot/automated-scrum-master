"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard
from block_ui.create_story_ui import CREATE_STORY_MODAL
from block_ui.example_modal_ui import EXAMPLE_MODAL

class ScrumMaster:
    # Interface with JSON data

    # Command keyword list (CRUD)
    # e.g. action = commands[keyword]
    #      action(story)
    commands = { 
        "create": scrum_board.create_story,
        "read": scrum_board.read_story,
        "update": scrum_board.update_story, # of form: @Bot update [field] [value]
        "delete": scrum_board.delete_story
    }

    priorities = {
        "high": 3,
        "medium": 2,
        "low": 1 
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

         # Interface with JSON data
        scrum_board = ScrumBoard()
        

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

        if "create a story" in text:
            self._create_modal_btn(text="Create a Story", action_id="create-story")
        # Example
        elif "example modal" in text:
            self._create_modal_btn(text="Example Modal", action_id="example")
        # End example
        else:
            self.text = "Command not found, please use a keyword ('create', 'read', 'update', 'delete')."


    def _create_modal_btn(self, text="", action_id=""):
        """Creates an interactive button so that we can obtain a trigger_id for modal interaction
        
        IMPOTANT!!! Remember what action_id you used because you will need to use it in create_modal
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
        elif action_id == "example":
            return EXAMPLE_MODAL
        else:
            return ""
        
    def process_modal_submission(self, payload, callback_id):
        payload_values = list(payload['view']['state']['values'].values())

        # Add an if-clause here with your callback_id used in the modal
        if callback_id == "create-story-modal":
            self._process_story_submission(payload_values)
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

        self.text = str([board, priority, estimate, sprint, assigned_to, user_type, story_desc])
    
    # Methods to help parse modal submission payload fields
    @staticmethod
    def _get_userselect_item(payload_values, index):
        return payload_values[index]['users_select-action']['selected_user']

    @staticmethod
    def _get_dropdown_select_item(payload_values, index):
        return payload_values[index]['static_select-action']['selected_option']['text']['text']

    @staticmethod
    def _get_plaintext_input_item(payload_values, index):
        return payload_values[index]['plain_text_input-action']['value']

    def get_response(self):
        # self.text is the textual message to be displayed by bot
        # self.blocks is the interactive message (e.g. modal) to be displayed in JSON
        return (self.text, self.blocks)


