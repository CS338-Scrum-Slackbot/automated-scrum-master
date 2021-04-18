""" 
Scrum board API for simple interfacing with data 
    pb: product backlog
    sb: sprint backlog
    s: sprint
    td: to-do
"""
import json

SCRUM_BOARD = './data/scrum_board.json'

class ScrumBoard:
    def __init__(self):
        # Can do this with other backlogs as well
        self.sb = {}
        with open(SCRUM_BOARD, 'r') as f:
            self.sb = json.load(f)

    def create_story(self, id, sprint, assigned_to, user_type, story_desc):
        story = {
            "id": id,
            "priority": priority,
            "estimate":estimate,
            "sprint": sprint,
            "status": "",
            "assigned_to": assigned_to,
            "user_type": user_type,
            "story": story_desc
        }

        self.sb['product_backlog'].append(story)
        print(self.sb['product_backlog'])
        with open(SCRUM_BOARD, 'w') as f:
            json.dump(self.sb, f, indent=4)

    def read_story(self):
        pass
    
    def update_story(self):
        pass

    def delete_story(self):
        pass

    