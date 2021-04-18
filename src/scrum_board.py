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
        with open(SCRUM_BOARD, 'r') as pb:
            self.pb = json.load(pb)

    def create_story(self):
        pass

    def read_story(self):
        pass
    
    def update_story(self, id, field, value):
        return json_reader(SCRUM_BOARD).update(id, field, value)

    def delete_story(self):
        pass

    