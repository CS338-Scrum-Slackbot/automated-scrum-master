"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard

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

        # Command keyword list (CRUD)
        # e.g. action = commands[keyword]
        #      action(story)
        self.commands = { 
            "create": "",
            "read": scrum_board.read_story,
            "update": scrum_board.update_story,
            "delete": scrum_board.delete_story
        }

    def process_modal(self, payload):
        print(payload)


    def process_text(self, text):
        """ 
        Need to make some assumptions about how users will communicate with the bot (at least pre-NLP)
        """
        command = text.lower().split(' ')[1]
        if command == "create":
            self._create_story()
        else:
            self.text = "Command not found, please use a keyword ('create', 'read', 'update', 'delete')."


    def _create_story(self):
        self.blocks = [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Create Modal",
                            "emoji": True
                        },
                        "value": "click_me_123",
                        "action_id": "create-modal"
                    },
                ]
            }
        ]
        self.text = ""
        

    def get_response(self):
        return (self.text, self.blocks)