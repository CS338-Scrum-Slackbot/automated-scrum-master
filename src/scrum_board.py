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

    def create_story(self, story, log):
        if log in ['previous_sprint', 'archived']:
            return 0
        sid = self.reader.read_metadata_field("sid")
        story["id"] = sid
        print(f'Creating story: {story} in log {log}')
        success = self.reader.create(story, log)
        if not success:
            return 0
        else:
            self.reader.write_metadata_field("sid", sid+1)
            return sid


    def read_story(self, id, log):  # [id: int, log: str = None]
        obj, log_str = self.reader.read(id=id, log=log)  # Read from json
        if obj is None and log is None:
            return "Story not found in your board."
        elif obj is None and log is not None:
            return f"Story not found in {log}, try a different swimlane?\nYou can also read the whole board using `read story {id}`"
        return [obj, log_str]

    def get_logs(self):
        return self.reader._list_logs

    def read_log(self, log):
        story_list = self.reader.read_log(log=log)
        if story_list is None and log is None:
            return "No stories in your board."
        elif story_list is None and log is not None:
            return f"Could not find any stories in {log}."
        return story_list

    def update_story(self, story, log, new_log):
        print(f'UPDATING STORY: {story}')
        if log in ['previous_sprint', 'archived']:
            return 0
        return self.reader.update(story['id'], story, log, new_log)

    def search_story(self, lookup_text: str, logs: list, fields: list):
        # from slack_interface import get_all_members
        # members = get_all_members()
        # possible_members = []
        # for m in members:
        #     possible_members.append(m['profile']['real_name'])
        #     possible_members.append(m['profile']['display_name'])
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

    def create_swimlane(self, log_name: str):
        if self.reader.create_swimlane(log_name):
            return f"Successfully created new swimlane {log_name}."
        else: return f"Swimlane {log_name} already exists: try creating a different name, or update this one using `update swimlane`."

    def update_swimlane(self, old_name:str, new_name:str):
        result =  self.reader.update_swimlane(old_name, new_name)
        if result == 1: return f"Successfully updated {old_name} to {new_name}."
        elif result == -1: return f"Swimlane {old_name} does not exist." # This should not happen bc of the modal
        elif result == -2: return f"Swimlane {new_name} already exists: try updating {old_name} with a different name."
        else: return "Internal error."

    def list_user_swimlanes(self):
        return self.reader.list_user_gen_logs()