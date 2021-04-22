""" 
Scrum board API for simple interfacing with data 
    pb: product backlog
    sb: sprint backlog
    s: sprint
    td: to-do
"""
import json
import json_reader as jr

SCRUM_BOARD = 'data/scrum_board.json'

class ScrumBoard:
    def __init__(self):
        # Can do this with other backlogs as well
        with open(SCRUM_BOARD, 'r') as pb:
            self.pb = json.load(pb)
        self.reader = jr.json_reader(file_path=SCRUM_BOARD)  # Open reader

    def create_story(self):
        pass

    def read_story(self, params: list): # [id: int, log: str = None]
        id = int(params[0])  # Get id
        log = None
        if len(params) > 1:
            log = params[1]  # Get user-specified log is possible
        obj, log_str = self.reader.read(id=id, log=log)  # Read from json
        if obj is None or log_str is None:
            return "Story not found."
        return "Reading story from "+log_str+": "+json.dumps(obj)

    
    def update_story(self, id, field, value):
        reader = jr.json_reader(SCRUM_BOARD)
        story, log = reader.read(id)
        if story: 
            story[field] = value
            return reader.update(id, story, log)
        else: return None


    def delete_story(self):
        pass

    