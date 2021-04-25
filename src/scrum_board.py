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

    def read_story(self, params: list):  # [id: int, log: str = None]
        id = int(params[0])  # Get id
        log = None
        if len(params) > 1:
            log = params[1]  # Get user-specified log is possible
        obj, log_str = self.reader.read(id=id, log=log)  # Read from json
        if obj is None or log_str is None:
            return "Story not found."
        return "Reading story from "+log_str+": "+json.dumps(obj)

    def update_story(self):
        pass

    def delete_story(self):
        scrum_reader = jr.json_reader(
            file_path="./data/scrum_board.json")
        logs = scrum_reader.list_logs()
        print(*logs)
        scrum_reader.close()
        pass
