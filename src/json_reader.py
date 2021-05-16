import json

"""
#### README
The sample code below shows usage of json_reader.
- You should use an import-as statement.
- The file_path starts with 'data/' NOT '../data/' or './data/'
- The reader may be stored as a class variable.
- The reader implements hard-deletion.

#### CODE:
import json_reader as jr

def my_func:
    reader = jr.json_reader(file_path="data/scrum_board.json")
"""

class json_reader():
    def __init__(self, file_path: str):
        self._file_path = file_path
        with open(file=self._file_path, mode="r") as f:
            self._j = json.load(f) # Load file into memory
        self._list_logs = list(self._j.keys())

        # quick fix for removing metadata key from swimlanes
        self._list_logs.remove('metadata')

        # Hard coded fields because it's hard to read them in (in case file is empty)
        # TODO: add description field when this feature is implemented
        self._list_fields = ["id","priority","estimate","sprint","status","assigned_to","user_type","story"]

    def write_to_file(self):
        try:
            with open(file=self._file_path, mode="r+") as f:
                f.seek(0)
                f.write(json.dumps(self._j, indent=4)) # Write python obj to file
                f.truncate()
                return 1
        except: return 0

    # ================
    # Entry-based ops
    # ================
    def create(self, entry: object, log: str):
        try:
            if log not in self._list_logs:
                return 0
            self._j[log]["stories"].append(entry)             # Add to python obj
            return self.write_to_file()
        except: return 0

    def refactor_helper(self, log, func):
        if log is not None and log in self._list_logs:
            return func(log), log
        # Scan over logs
        for l in self.list_logs():
            result = func(l)
            if (result != None):
                return result, l
        return None, None

    def read(self, id: int, log: str = None): # Return Tuple[object, str]
        # Helper function for reading specific log
        def helper(r_log: str) -> object:
            entries = self._j[r_log]["stories"]
            for e in entries:
                if e["id"] == id:
                    return e
            return None
        return self.refactor_helper(log, helper)

    def delete(self, id: int, log: str = None):  # Returns Tuple[object, str]
        # Helper function for deleting from specific log
        def helper(l: str):
            entries = self._j[l]["stories"] # Array of objs
            for idx in range(0, len(entries)):
                if entries[idx]["id"] == id:
                    e = self._j[l]["stories"].pop(idx) # Remove from python obj
                    if not self.write_to_file(): return 0 # Write to file failed
                    else: return e # Success: return old object
            return None
        return self.refactor_helper(log, helper)

    # Return Tuple[object, str]
    def update(self, id: int, new_entry: object, old_log: str = None, new_log: str = None):
        o, this_log = self.delete(id, old_log)
        if o is None or this_log is None:
            return None  # Deletion failed
        self.create(new_entry, new_log if new_log else old_log)
        return new_entry, new_log

    # Return Tuple[object, str]
    def move(self, id: int, dest_log: str, src_log: str = None):
        entry, src_log = self.delete(id, src_log)
        if entry is None or src_log is None:
            return None  # Deletion failed
        self.create(entry, dest_log)
        return entry, src_log

    def search(self, lookup: any, logs: list, fields: list): #- Return listof Tuple[object, str]
        lookup = str(lookup).lower()    # Cast to string and convert to lowercase
        found = []                      # Will hold the found entries
        # Helper function for reading specific log
        get_name = __import__('scrum_master').ScrumMaster._get_member_name
        def read_log(r_log: str):
            entries = self._j[r_log]["stories"]
            for e in entries:
                def compare_field(field_):
                    # from scrum_master import ScrumMaster
                    if field_ == 'assigned_to':
                        s = get_name(e[field_]).lower()
                    else: 
                        s = str(e[field_]).lower() # Cast field's value to string and convert to lowercase
                    if lookup in s: 
                        found.append([e, r_log])
                        return True
                    return False
                for f in fields:
                    if compare_field(f): break # If any field matches, stop comparing fields
        if logs == []:
            logs = self.list_logs()
        if fields == []:
            fields = self.list_fields()
        for l in logs:
            read_log(l)
        return found

    # ======================
    # Log/swimlane-based ops
    # ======================

    def list_logs(self) -> list:
        return self._list_logs

    def list_user_gen_logs(self) -> list:
        result = []
        for l in self.list_logs():
            if self._j[l]["user_generated"]:
                result.append(l)
        return result

    def list_fields(self) -> list:
        return self._list_fields

    def read_log(self, log: str = None): # Returns if log=None: object else: list
        if log is not None and log not in self.list_logs():
            return None # error
        if log is None:
            all_entries = []
            for l in self.list_logs():
                all_entries += self._j[l]["stories"]
            return all_entries
        else:
            return self._j[log]["stories"]

    def create_swimlane(self, log_name: str):
        if log_name in self.list_logs() or log_name == "metadata":
            return 0 # Log already exists
        try:
            self._list_logs.append(log_name)
            self._j[log_name] = {"user_generated": True,
                                        "stories": [] }
            return self.write_to_file()
        except: return 0

    def update_swimlane(self, old_name:str, new_name:str):
        if not old_name in self.list_logs():
            return -1 # old_name does not exist
        elif new_name in self.list_logs() or new_name == "metadata":
            return -2  # new_name already exists
        try:
            self._list_logs = [log if log != old_name else new_name for log in self._list_logs]
            self._j[new_name] = self._j.pop(old_name) # Transfers entries to new key while deleting the old
            return self.write_to_file()
        except: return 0

    # ===========
    #   METADATA
    # ===========
    def read_metadata_field(self, field:str):
        # fields are: "sid", "story_count", "current_sprint", "current_sprint_starts", current_sprint_ends", "id_to_name"
        return self._j["metadata"][field]

    def write_metadata_field(self, field:str, value:any):
        self._j["metadata"][field] = value
        return self.write_to_file()