"""
Class to wrap the logic of the scrum master bot
"""

from scrum_board import ScrumBoard
import json_reader as jr
from block_ui.create_story_ui import CREATE_STORY_MODAL
from block_ui.update_story_ui import UPDATE_STORY_MODAL
from block_ui.example_modal_ui import EXAMPLE_MODAL
import json

class ScrumMaster:
    # Interface with JSON data

    # Command keyword list (CRUD)
    # e.g. action = commands[keyword]
    #      action(story)
    # commands = { 
    #     "create": scrum_board.create_story,
    #     "read": scrum_board.read_story,
    #     "update": scrum_board.update_story, # of form: @Bot update [field] [value]
    #     "delete": scrum_board.delete_story
    # }

    priorities = {
        "High": 3,
        "Medium": 2,
        "Low": 1 
    }

    fields = {
        "priority",
        "estimate",
        "sprint",
        "status",
        "assigned_to",
        "user_type",
        "story"
    }

    def __init__(self):
        self.text = "\0"
        self.blocks = None

        # Maintain current sprint
        self.current_sprint = 0

        # Next story id
        self.sid = 6

        # Interface with JSON data
        self.scrum_board = ScrumBoard()

    
    def create_story(self, text):
        self._create_modal_btn(text="Create a Story", action_id="create-story")

    def update_story(self, text):
        try: 
            id = int(text.split(' ')[-1])
        except: 
            self.text = "Story ID must be an int."
            return
        self.story_update, self.update_log = jr.json_reader("data/scrum_board.json").read(id)
        self._create_modal_btn(text=f"Update Story {id}", action_id="update-story")

    def read(self, text):
        pass

    def search(self, text):
        pass

    def start_sprint(self, text):
        self.current_sprint += 1
        jsr = jr.json_reader("data/scrum_board.json")
        sb = jsr.read_log('sprint_backlog')
        for s in sb: 
            if s['status'] != "": s['status'] = 'to-do'
            s['sprint'] += self.current_sprint
            jsr.update(id=s['id'], new_entry=s, log='sprint_backlog')
            jsr.move(id=s['id'], dest_log='current_sprint', src_log='sprint_backlog')
        
    def process_user_msg(self, text: str):
        """ 
        Need to make some assumptions about how users will communicate with the bot (at least pre-NLP)
        Command: "create a story" will make a button that opens a create story modal
        """

        if "create story" in text:
            self.create_story(text)
        # Example
        elif "example modal" in text:
            self._create_modal_btn(text="Example Modal", action_id="example")
        # End example
        elif "update story" in text:
            self.update_story(text)
        elif "read" in text:
            # Sample message: @Miyagi read 1 from product_backlog
            # @Miyagi read 1
            read_text = " ".join(text.split()[1:])
            id_text  = int(text.split()[1])
            log = None
            from_idx = read_text.find("from")
            if from_idx != -1:
                log_idx = from_idx + 5
                log = read_text[log_idx:]
            self.text = self.scrum_board.read(id=id_text, log=log)
        elif "search" in text:
            # Sample message: @Miyagi search x field in log: want to update
            colon_idx = text.find(":")
            lookup_text = text[colon_idx+2:] # everything after ": "
            
            parameter_text = text[:colon_idx] # everything before the colon
            parameter_text = " ".join(parameter_text.split()[1:]) # everything between "search " and the colon
            
            field_idx = parameter_text.find("field")
            field = None
            if field_idx != -1:
                field = parameter_text[:field_idx-1] # field is param_text before " field"

            in_idx = parameter_text.find("in")
            log = None
            if in_idx != -1:
                log = parameter_text[in_idx+3:colon_idx] # log is param_text between "in " and the colon (end)

            self.text = "field="+str(field)+"    log="+str(log)
            #self.scrum_board.search(lookup_text=lookup_text, log=log, field=field)
            # TODO: replace self.text with the call to search once json search is merged to main
        elif "start sprint" in text.lower():
            self.start_sprint(text)
        else:
            self.text = "Command not found, please use a keyword ('create', 'read', 'update', 'delete')."


    def _create_modal_btn(self, text="", action_id=""):
        """Creates an interactive button so that we can obtain a trigger_id for modal interaction
        
        IMPOTANT!!! Remember what action_id you used because you will need to use it in create_modal
        """
        self.blocks = [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": text,
                        },
                        "value": "click_me_123",
                        "action_id": action_id
                    },
                ]
            }
        ] if text != "" else None
        self.text = ""

    # @staticmethod
    def create_modal(self, action_id):
        # Add an if-clause to parse what happens if we receive your action_id to create a modal
        if action_id == "create-story":
            return CREATE_STORY_MODAL
        elif action_id == "example":
            return EXAMPLE_MODAL
        elif action_id == "update-story":
            return self.fill_update_modal(UPDATE_STORY_MODAL, self.story_update['id'])
        else:
            return ""

    def fill_update_modal(self, modal, id):
        story_update, update_log = jr.json_reader("data/scrum_board.json").read(id)
        modal['title']['text'] = f'Update Story {story_update["id"]}'
        modal['private_metadata'] = f'{story_update["id"]},{update_log}'
        for b in modal['blocks']:
            if b['label']['text'] == 'Estimate':
                b['element']['initial_option']['text']['text'] = str(story_update['estimate']) if story_update['estimate'] != -1 else "1"
                b['element']['initial_option']['value'] = str(story_update['estimate']) if story_update['estimate'] != -1 else "1"
            elif b['label']['text'] == 'Sprint':
                b['element']['initial_value'] = story_update['sprint'] if story_update['sprint'] else self.current_sprint 
            elif b['label']['text'] == 'Priority':
                if self.story_update['priority'] != -1: 
                    p = list(self.priorities.keys())[list(self.priorities.values()).index(story_update['priority'])]
                    b['element']['initial_option']['text']['text'] = p
                    b['element']['initial_option']['value'] = p.lower()
                else:
                    b['element']['initial_option']['text']['text'] = 'Low'
                    b['element']['initial_option']['value'] = 'low'
            elif b['label']['text'] == 'Status':
                b['element']['initial_option']['text']['text'] = story_update['status'].capitalize() if story_update['status'] else 'None'
                b['element']['initial_option']['value'] = story_update['status'] if story_update['status'] else 'none'
            elif b['label']['text'] == 'User Type':
                b['element']['initial_value'] = story_update['user_type'].capitalize()
            elif b['label']['text'] == 'Story Title':
                b['element']['initial_value'] = story_update['story'].capitalize()
            elif b['label']['text'] == 'Assigned To':
                b['element']['initial_user'] = story_update['assigned_to']
        return modal
        
    def process_modal_submission(self, payload, callback_id):
        payload_values = list(payload['view']['state']['values'].values())

        # Add an if-clause here with your callback_id used in the modal
        if callback_id == "create-story-modal":
            self._process_modal_submission(payload_values)
        elif callback_id == "example-modal":
            # Here's where you call the function to process your modal's submission
            # e.g. self._process_example_submission(payload_values)
            pass
        elif callback_id == "update-story-modal":
            self._process_modal_submission(
                payload_values, payload['view']['private_metadata'].split(','))
        else:
            pass

    def _process_modal_submission(self, payload_values, metadata=[]):
        i = 0 if metadata else 1
        estimate = int(self._get_dropdown_select_item(payload_values, i+6))
        priority = self.priorities[self._get_radio_group_item(payload_values, i+5).capitalize()]
        status = self._get_radio_group_item(payload_values, i+4)
        assigned_to = self._get_userselect_item(payload_values, i+3)
        try: sprint = int(self._get_plaintext_input_item(payload_values, i+2))
        except:
            self.text = "Sprint must be an integer."
            self.blocks = None
            return
        user_type = self._get_plaintext_input_item(payload_values, i+1)
        story_title = self._get_plaintext_input_item(payload_values, i)
        swimlane = metadata[1] if metadata else self._get_dropdown_select_item(payload_values, 0)

        story = {
                "id": int(metadata[0]) if metadata else self.sid,
                "priority": priority,
                "estimate": estimate,
                "sprint": sprint,
                "status": status,
                "assigned_to": assigned_to,
                "user_type": user_type,
                "story": story_title
                }

        if metadata:
            update = self.scrum_board.update_story(story, swimlane)
            self.text = f"Story {int(metadata[0])} updated successfully!" if update else f"Failed to update story {int(metadata[0])}."
            self.blocks = None
        else: 
            create_story = self.scrum_board.create_story(story, swimlane)
            self.text = f"Story {self.story_update['id']} created successfully!" if create_story else "Failed to create story."
            self.blocks = None
            self.sid += 1

    # def _process_update_submission(self, payload_values, metadata=[]):
    #     estimate = int(self._get_dropdown_select_item(payload_values, 6))
    #     priority = self.priorities[self._get_radio_group_item(payload_values, 5).capitalize()]
    #     status = self._get_radio_group_item(payload_values, 4)
    #     assigned_to = self._get_userselect_item(payload_values, 3)
    #     try: sprint = int(self._get_plaintext_input_item(payload_values, 2))
    #     except:
    #         self.text = "Sprint must be an integer."
    #         self.blocks = None
    #         return
    #     user_type = self._get_plaintext_input_item(payload_values, 1)
    #     story_title = self._get_plaintext_input_item(payload_values, 0)
    #     update = self.scrum_board.update_story({
    #             "id": int(metadata[0]),
    #             "priority": priority,
    #             "estimate": estimate,
    #             "sprint": sprint,
    #             "status": status,
    #             "assigned_to": assigned_to,
    #             "user_type": user_type,
    #             "story": story_title
    #         }, metadata[1])
    #     self.text = f"Story {int(metadata[0])} updated successfully!" if update else f"Failed to update story {int(metadata[0])}."
    #     self.blocks = None

    # # Parses the payload of the create-story modal submission
    # # To parse different modals, you need to create a new function that handles your modal
    # def _process_story_submission(self, payload_values):        
    #     board = self._get_dropdown_select_item(payload_values, 0)
    #     priority = int(self._get_dropdown_select_item(payload_values, 1))
    #     estimate = int(self._get_dropdown_select_item(payload_values, 2))
    #     sprint = self._get_plaintext_input_item(payload_values, 3)
    #     assigned_to = self._get_userselect_item(payload_values, 4)
    #     user_type = self._get_plaintext_input_item(payload_values, 5)
    #     story_desc = self._get_plaintext_input_item(payload_values, 6)

    #     create_story = self.scrum_board.create_story({
    #         "id": self.story_update["id"],
    #         "priority": priority,
    #         "estimate": estimate,
    #         "sprint": sprint,
    #         "status": status,
    #         "assigned_to": assigned_to,
    #         "user_type": user_type,
    #         "story": story_desc
    #     }, board)

    #     self.text = f"Story {self.story_update['id']} created successfully!" if update else "Failed to create story."
    #     self.blocks = None
    
    # Methods to help parse modal submission payload fields
    @staticmethod
    def _get_userselect_item(payload_values, index): 
        return payload_values[index]['users_select-action']['selected_user']

    @staticmethod
    def _get_dropdown_select_item(payload_values, index):
        return payload_values[index]['static_select-action']['selected_option']['text']['text']

    @staticmethod
    def _get_plaintext_input_item(payload_values, index):
        return payload_values[index]['plain_text_input-action']['value']

    @staticmethod
    def _get_radio_group_item(payload_values, index):
        return payload_values[index]['radio_buttons-action']['selected_option']['value']

    def get_response(self):
        # self.text is the textual message to be displayed by bot
        # self.blocks is the interactive message (e.g. modal) to be displayed in JSON
        return (self.text, self.blocks)


