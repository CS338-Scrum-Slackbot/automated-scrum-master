import json
import copy
import json_reader as jr
from block_ui.search_story_ui import SEARCH_STORY_MODAL
from block_ui.create_swimlane_ui import CREATE_SWIMLANE_MODAL

SCRUM_BOARD = 'data/scrum_board.json'

class ModalEditor:
    def __init__(self) -> None:
        pass

    def edit_search_story_modal(self, modal=SEARCH_STORY_MODAL):
        self.reader = jr.json_reader(file_path=SCRUM_BOARD)  # Open reader
        # Get lists from reader
        fields = self.reader.list_fields()
        logs = self.reader.list_logs()

        # Iterate over field & log lists and create options
        field_block = []
        log_block = []
        empty_option = {'text': {'type': 'plain_text', 'text': '', 'emoji': True}, # text is displayed to user
                        'value': ''} # value is the key of this option

        # compile field options
        for idx in range(len(fields)):
            option = copy.deepcopy(empty_option)
            option["text"]["text"] = fields[idx]
            option["value"] = "field-"+str(idx)
            field_block.append(option)

        # compile log/swimlane options
        for idx in range(len(logs)):
            option = copy.deepcopy(empty_option)
            option["text"]["text"] = logs[idx]
            option["value"] = "log-"+str(idx)
            log_block.append(option)

        # Overwrite modal options with the compiled options
        modal['blocks'][2]["accessory"]["options"] = field_block
        modal['blocks'][3]["accessory"]["options"] = log_block
        return modal

    def edit_create_swimlane_modal(self, modal=CREATE_SWIMLANE_MODAL):
        self.reader = jr.json_reader(file_path=SCRUM_BOARD)  # Open reader
        # Get lists from reader
        logs = self.reader.list_logs()

        # Iterate over field & log lists and create options
        message = "Existing swimlanes:\n"

        # compile log/swimlane options
        for l in logs:
            message += f"{l}, "
        message = message[:-2] # Crop trailing ", "

        # Overwrite modal options with the compiled options
        modal['blocks'][0]["text"]["text"] = message
        return modal