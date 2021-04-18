"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard

class ScrumMaster:
    
    # Interface with JSON data
    scrum_board = ScrumBoard()

    # Command keyword list (CRUD)
    # e.g. action = commands[keyword]
    #      action(story)
    commands = { 
        "create": scrum_board.create_story,
        "read": scrum_board.read_story,
        "update": scrum_board.update_story,
        "delete": scrum_board.delete_story
    }

    def __init__(self):
        self.text = ""

        # Maintain current sprint
        self.current_sprint = 0

    def process_text(self, text):
        """ 
        Need to make some assumptions about how users will communicate with the bot (at least pre-NLP)
        """
        self.text = text
        l = text.split()                        # input string -> list of words
        cmd = l[0]                              # Element 0 = command (eg read, update, etc)
        if cmd not in list(ScrumMaster.commands.keys()):
            self.text = "scrum_master: process_text expected first word to be command (create, read, update, or delete"
            return
        action = ScrumMaster.commands[l[0]]
        self.text = action(l[1:len(l)])         # Element 1:len = parameters (eg ID, log, etc)
        """ Using self.text for the return string - Caspar """
        pass

    def get_response(self):
        return self.text