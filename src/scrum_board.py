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

    def create_story(self, id, sprint, assigned_to, user_type, story_desc, priority=-1, estimate=-1):
        story = {
            "id": id,
            "priority": priority,
            "estimate": estimate,
            "sprint": sprint,
            "status": "",
            "assigned_to": assigned_to,
            "user_type": user_type,
            "story": story_desc
        }

        self.pb['product_backlog'].append(story)
        print(self.pb['product_backlog'])
        with open(SCRUM_BOARD, 'w') as f:
            json.dump(self.pb, f, indent=4)

    def read(self, id, log):  # [id: int, log: str = None]
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
        tuples = self.reader.search(
            lookup=lookup_text, logs=logs, fields=fields)
        if tuples is None:
            return "Internal error: Fields or swimlanes did not match JSON."
        if len(tuples) == 0:
            return "Didn't find anything for "+lookup_text+", try again?"
        # Extract entries only (not logs)
        result = []
        for t in tuples:
            result.append(t[0])
        return result

    def delete_story(self, story_id):
        story_id = int(story_id)
        story_obj, source_log = self.reader.read(
            id=story_id)
        if story_obj is None or source_log is None:
            return "Story with \"ID " + str(story_id) + "\" does not exist."

        if source_log == "archived":
            return "Story with \"ID " + str(story_id) + "\" has already been deleted."

        moved_story, new_log = self.reader.move(
            story_id, 'archived', source_log)

        if moved_story == None or new_log == None:
            return "Could not delete \"ID " + str(story_id) + "\" story."
        else:
            return "Successfully deleted " + "\"ID " + str(story_id) + ": " + moved_story["story"] + "\"" + " from " + source_log

    def list_all_stories(self):
        return self.reader.read_log()
