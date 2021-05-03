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

    def create_story(self, story,log):
        print(f'Creating story: {story} in log {log}')
        return self.reader.create(story, log)

    def read(self, id, log): # [id: int, log: str = None]
        obj, log_str = self.reader.read(id=id, log=log)  # Read from json
        if obj is None or log_str is None:
            return "Story not found."
        return "Reading story from "+log_str+": "+json.dumps(obj)

    def read_all(self, log):
        obj, log_str = self.reader.read_all(log=log)
        if obj is None or log_str is None:
            return f"Could not find any stories in log {log}"
        return obj

    def update_story(self, story, log):
        print(f'UPDATING STORY: {story}')
        return jr.json_reader(SCRUM_BOARD).update(story['id'], story, log)

    def search(self, lookup_text: str, logs: list, fields: list):
        tuples = self.reader.search(lookup=lookup_text, logs=logs, fields=fields)
        if tuples is None:
            return "Internal error: Fields or swimlanes did not match JSON."
        if len(tuples) == 0:
            return "Didn't find anything for "+lookup_text+", try again?"
        result = "Found these for "+lookup_text+"\n"
        for t in tuples:
            result = result + str(t[0]) + "\n"
        return result
    
    def delete_story(self):
        pass

    