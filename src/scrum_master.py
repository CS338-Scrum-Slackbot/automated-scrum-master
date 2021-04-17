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

        processed_text = text.split(" ")
        print(processed_text)

        if processed_text[0] == "delete":
            self.scrum_board.delete_story()
            print("deleted")

        pass

    def get_response(self):
        return self.text
