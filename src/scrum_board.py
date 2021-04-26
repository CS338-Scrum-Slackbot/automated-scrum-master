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

    def read(self, id, log): # [id: int, log: str = None]
        obj, log_str = self.reader.read(id=id, log=log)  # Read from json
        if obj is None or log_str is None:
            return "Story not found."
        return "Reading story from "+log_str+": "+json.dumps(obj)

    def update_story(self, story, log):
        print(f'UPDATING STORY: {story}')
        return jr.json_reader(SCRUM_BOARD).update(story['id'], story, log)

    def search(self, lookup_text, log, field):
        tuples = self.reader.search(lookup=lookup_text, log=log, field=field)
        if len(tuples) == 0:
            return "Didn't find anything for that search."
        result = "Found these: "
        for tuple in tuples:
            id = tuple[0]["id"]
            log = tuple[1]
            result.append("ID "+str(id)+" in "+str(log)+". ")
        return result
    
    def delete_story(self):
        pass

    