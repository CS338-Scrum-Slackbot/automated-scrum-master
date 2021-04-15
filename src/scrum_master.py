"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard

class ScrumMaster:
    
    def __init__(self):
        self.text = ""

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
            "create": scrum_board.create_story,
            "read": scrum_board.read_story,
            "update": scrum_board.update_story,
            "delete": scrum_board.delete_story
        }

    def process_text(self, text):
        """ 
        Need to make some assumptions about how users will communicate with the bot (at least pre-NLP)
        """
        words = text.lower().split(' ')

        command = ""
        for word in words:
            if word in self.commands.keys():
                command = word
        
        action = self.commands[command]
        if command == "create":
            action(self.sid, 2, "customer", "create story test")
            self.text = "Successfully added story."

    def get_response(self):
        return self.text