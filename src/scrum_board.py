""" 
Scrum board API for simple interfacing with data 
    pb: product backlog
    sb: sprint backlog
    s: sprint
    td: to-do
"""
import json
import json_reader as jr

SCRUM_BOARD = './data/scrum_board.json'

class ScrumBoard:
    def __init__(self):
        # Can do this with other backlogs as well
        """with open(SCRUM_BOARD, 'r') as pb:
            self.pb = json.load(pb)"""

    def create_story(self):
        pass

    def read_story(self, params: list): # id: int, log: str = None)
        reader = jr.json_reader(file_path="data/scrum_board.json")  # Open reader
        id = int(params[0])                                         # Get id, log from params
        log = None
        if len(params) > 1:
            log = params[1]
        obj, log_str = reader.read(id=id, log=log)             # Read from json
        reader.close()                                         # Close json reader
        if obj is None or log_str is None:
            return "Story not found."
        return "Reading story from "+log_str+": "+json.dumps(obj)

    
    def update_story(self):
        pass

    def delete_story(self):
        pass

    