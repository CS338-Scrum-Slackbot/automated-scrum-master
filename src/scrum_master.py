"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard
import block_ui.create_story_ui as block_ui

class ScrumMaster:
    
    def __init__(self):
        self.text = "\0"
        self.blocks = None

        # Maintain current sprint
        self.current_sprint = 0

        # Next story id
        self.sid = 6

         # Interface with JSON data
        scrum_board = ScrumBoard()
        

    def process_text(self, text: str):
        """ 
        Need to make some assumptions about how users will communicate with the bot (at least pre-NLP)
        """
        if "create a story" in text:
            self._create_story_btn()
        else:
            self.text = "Command not found, please use a keyword ('create', 'read', 'update', 'delete')."


    def _create_story_btn(self):
        self.blocks = [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Create a Story",
                        },
                        "value": "click_me_123",
                        "action_id": "create-story"
                    },
                ]
            }
        ]
        self.text = ""

    @staticmethod
    def create_story_modal():
        return block_ui.CREATE_STORY_MODAL

    def process_story_submission(self, payload: dict):
        payload_values = list(payload['view']['state']['values'].values())
        
        priority = int(payload_values[0]['static_select-action']['selected_option']['text']['text'])
        estimate = int(payload_values[1]['static_select-action']['selected_option']['text']['text'])
        sprint = int(payload_values[2]['plain_text_input-action']['value'])
        assigned_to = payload_values[3]['users_select-action']['selected_user']
        user_type = payload_values[4]['plain_text_input-action']['value']
        story_desc = payload_values[5]['plain_text_input-action']['value']

        print(priority, estimate, sprint, assigned_to, user_type, story_desc)
        

    def get_response(self):
        # self.text is the textual message to be displayed by bot
        # self.blocks is the interactive message (e.g. modal) to be displayed in JSON
        return (self.text, self.blocks)