import re
import json
import copy
import json_reader as jr
from block_ui.search_story_ui import SEARCH_STORY_MODAL
from block_ui.create_swimlane_ui import CREATE_SWIMLANE_MODAL
from block_ui.update_swimlane_ui import UPDATE_SWIMLANE_MODAL, UPDATE_NO_SWIMLANES_MODAL
from block_ui.delete_swimlane_ui import DELETE_SWIMLANE_MODAL, DELETE_NO_SWIMLANES_MODAL

SCRUM_BOARD = 'data/scrum_board.json'


class ModalEditor:
    def __init__(self) -> None:
        pass

    def _generate_select_options(self, text_list: list, value: str) -> list:
        # value is arbitrary, but it should be something like 'field' or 'log' depending on what you are listing
        empty_option = {'text': {'type': 'plain_text', 'text': '', 'emoji': True},  # text is displayed to user
                        'value': ''}
        result_list = []

        # compile field options
        for idx in range(len(text_list)):
            option = copy.deepcopy(empty_option)
            option["text"]["text"] = text_list[idx]
            option["value"] = f"{value}-{idx}"
            result_list.append(option)

        return result_list

    def edit_search_story_modal(self, modal=SEARCH_STORY_MODAL):
        self.reader = jr.json_reader(file_path=SCRUM_BOARD)  # Open reader
        # Get lists from reader
        fields = self.reader.list_fields()
        logs = self.reader.list_logs()[:]
        logs.remove("Archived")
        for idx in range(len(fields)):
            f = fields[idx]
            f = f.title()
            f = re.sub(pattern='_', string=f, repl=' ')   # Replace underscore
            fields[idx] = f

        # Get option list for field & log lists
        field_block = self._generate_select_options(fields, "field")
        log_block = self._generate_select_options(logs, "log")

        # Overwrite modal options with the compiled options
        modal['blocks'][2]["accessory"]["options"] = field_block
        modal['blocks'][3]["accessory"]["options"] = log_block
        return modal

    def edit_create_swimlane_modal(self, modal=CREATE_SWIMLANE_MODAL):
        self.reader = jr.json_reader(file_path=SCRUM_BOARD)  # Open reader
        # Get lists from reader
        logs = self.reader.list_logs()

        # compile log/swimlane options
        message = "Existing swimlanes:\n"
        for f in logs:
            message += f"{f}, "
        message = message[:-2]  # Crop trailing ", "

        # Overwrite modal options with the compiled options
        modal['blocks'][0]["text"]["text"] = message
        return modal

    # same action as in scrum_master.create_modal()
    def edit_update_or_delete_swimlane_modal(self, action: str):
        modal = UPDATE_SWIMLANE_MODAL if action == "update" else DELETE_SWIMLANE_MODAL
        self.reader = jr.json_reader(file_path=SCRUM_BOARD)     # Open reader
        logs = self.reader.list_user_gen_logs()                 # Get lists from reader
        if len(logs) == 0:
            if action == "update":
                return UPDATE_NO_SWIMLANES_MODAL
            else:
                return DELETE_NO_SWIMLANES_MODAL
        if action == "delete":
            for idx in range(len(logs)):
                num_stories = len(self.reader.read_log(logs[idx]))
                logs[idx] += f" ({num_stories})"
        log_block = self._generate_select_options(
            logs, "log")  # Get option list for log list
        # Overwrite modal options with the compiled options
        modal['blocks'][1]["element"]["options"] = log_block
        return modal
