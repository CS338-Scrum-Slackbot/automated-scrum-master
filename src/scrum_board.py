"""
Scrum board API for simple interfacing with data
    pb: product backlog
    sb: sprint backlog
    s: sprint
    td: to-do
"""
import json
import json_reader as jr

SCRUM_BOARD = 'data/demo.json'


class ScrumBoard:
    def __init__(self):
        # Can do this with other backlogs as well
        with open(SCRUM_BOARD, 'r') as pb:
            self.pb = json.load(pb)
        self.reader = jr.json_reader(file_path=SCRUM_BOARD)  # Open reader

    def create_story(self, story, log):
        print(f'Creating story: {story} in log {log}')
        return jr.json_reader(file_path=SCRUM_BOARD).create(story, log)

    def read_story(self, id, log):  # [id: int, log: str = None]
        obj, log_str = jr.json_reader(file_path=SCRUM_BOARD).read(id=id, log=log)  # Read from json
        if obj is None and log is None:
            return "Story not found in your board."
        elif obj is None and log is not None:
            return f"Story not found in {log}, try a different swimlane?\nYou can also read the whole board using `read story {id}`"
        return [obj, log_str]

    def read_log(self, log):
        story_list = jr.json_reader(file_path=SCRUM_BOARD).read_log(log=log)
        if story_list is None and log is None:
            return "No stories in your board."
        elif story_list is None and log is not None:
            return f"Could not find any stories in {log}"
        return story_list

    def update_story(self, story, log):
        print(f'UPDATING STORY: {story}')
        return jr.json_reader(SCRUM_BOARD).update(story['id'], story, log)

    def search_story(self, lookup_text: str, logs: list, fields: list):
        # from slack_interface import get_all_members
        # members = get_all_members()
        # possible_members = []
        # for m in members:
        #     possible_members.append(m['profile']['real_name'])
        #     possible_members.append(m['profile']['display_name'])
        tuples = jr.json_reader(file_path=SCRUM_BOARD).search(
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
        story_obj, source_log = jr.json_reader(file_path=SCRUM_BOARD).read(
            id=story_id)
        if story_obj is None or source_log is None:
            return "Story with \"ID " + str(story_id) + "\" does not exist."

        if source_log == "archived":
            return "Story with \"ID " + str(story_id) + "\" has already been deleted."

        moved_story, new_log = jr.json_reader(file_path=SCRUM_BOARD).move(
            story_id, 'archived', source_log)

        if moved_story == None or new_log == None:
            return "Could not delete \"ID " + str(story_id) + "\" story."
        else:
            return "Successfully deleted " + "\"ID " + str(story_id) + ": " + moved_story["story"] + "\"" + " from " + source_log

    def list_all_stories(self):
        return jr.json_reader(file_path=SCRUM_BOARD).read_log()
