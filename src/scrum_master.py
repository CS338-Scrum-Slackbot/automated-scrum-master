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
        self.text = ""

        # Maintain current sprint
        self.current_sprint = 0

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
        if command == "update":
            id, field, value = words[1], words[2], ' '.join(words[3:])
            # rudimentary input checks
            if field not in self.fields: 
                self.text = f"Invalid field \'{field}\'. Must be one of [{', '.join(self.fields)}]"
                return
            if field == 'priority': value = self.priorities[value]
            elif field in ['estimate','sprint']: 
                try: value = int(value) 
                except: 
                    self.text = f"Invalid input type for {field}. Given {type(value)}; expected int."
                    return
            success = action(id, field, value)
            print(success)
            self.text = "Successfully updated story." if success else f"Could not find story with id {id}."
        else:
            self.text = "Sorry, I don't recognize that command."

    def get_response(self):
        return self.text