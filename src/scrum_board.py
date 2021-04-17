"""
Scrum board API for simple interfacing with data
    pb: product backlog
    sb: sprint backlog
    s: sprint
    td: to-do
"""
import json
import json_reader

SCRUM_BOARD = './data/scrum_board.json'


class ScrumBoard:
    def __init__(self):
        # Can do this with other backlogs as well
        self.scrum_reader = json_reader.json_interface(
            file_path="../data/scrum_board.json")
        with open(SCRUM_BOARD, 'r') as pb:
            self.pb = json.load(pb)

    def create_story(self):
        pass

    def read_story(self):
        pass

    def update_story(self):
        pass

    def delete_story(self):
        logs = self.scrum_reader.list_logs()
        print(*logs)
        pass
