import json
import copy
import json_reader as jr
from block_ui.search_story_ui import SEARCH_STORY_MODAL
from block_ui.create_swimlane_ui import CREATE_SWIMLANE_MODAL
from block_ui.update_swimlane_ui import UPDATE_SWIMLANE_MODAL

SCRUM_BOARD = 'data/scrum_board.json'

class ModalEditor:
    def __init__(self) -> None:
        pass

    def _generate_select_options(self, text_list: list, value: str) -> list:
        # value is arbitrary, but it should be something like 'field' or 'log' depending on what you are listing
        empty_option = {'text': {'type': 'plain_text', 'text': '', 'emoji': True}, # text is displayed to user
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
        logs = self.reader.list_logs()

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
        for l in logs:
            message += f"{l}, "
        message = message[:-2] # Crop trailing ", "

        # Overwrite modal options with the compiled options
        modal['blocks'][0]["text"]["text"] = message
        return modal

    def edit_update_swimlane_modal(self, modal=UPDATE_SWIMLANE_MODAL):
        self.reader = jr.json_reader(file_path=SCRUM_BOARD)  # Open reader
        # Get lists from reader
        logs = self.reader.list_logs()
        # TODO: get list of user-generated logs only !!

        # Get option list for log list
        log_block = self._generate_select_options(logs, "log")

        # Overwrite modal options with the compiled options
        modal['blocks'][1]["element"]["options"] = log_block
        return UPDATE_SWIMLANE_MODAL