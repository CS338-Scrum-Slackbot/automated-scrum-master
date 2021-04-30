import json
from os import read

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
    ...
    my_obj = ...
    my_log = ... 
    reader.create(entry=my_obj, log=my_log)
    ...
    my_id = ...
    my_log = ... optional if the user does not provide one. read() will return the log where it found the entry
    my_obj, my_log = reader.read(id=my_id, log=my_log)
    ...
    my_id = ...
    my_log = ... optional
    my_obj, my_log = reader.delete(id=my_id, log=my_log)
    ...    
    my_id = ...
    my_log = ... optional
    new_obj = ... # update() returns the old object
    old_obj, my_log = reader.update(id=my_id, new_entry=new_obj, log=my_log)
    ...    
    my_id = ...
    my_log = ... optional
    move_to_log = ...
    my_obj, my_log = reader.move(id=my_id, dest_log=move_to_log, src_log=my_log)
    ...
    my_lookup_term = ...
    my_log = ... optional
    my_field = ... optional
    found_tuples = reader.search(lookup=my_lookup_term, log=my_log, field=my_field):
    num_entries_found = len(found_tuples)
    ith_obj_found = found_tuples[i][0]
    log_of_ith_obj = found_tuples[i][1]
    ...
    my_logs = reader.list_logs()
    print(str(my_logs)) --> ["product_backlog",""sprint_backlog","current_sprint","archived"]
    ...
    my_log = ... optional
    result = read_log(log=my_log) -> list:
    # Returns all entries in the log, or all entries in the file if my_log=None
    

"""


class json_interface():
    def __init__(self, file_path):
        pass

    # Entry-based ops
    def create(self, entry: object, log: str):
        pass # Adds the entry to specified log
    def read(self, id: int, log: str = None): # Return Tuple[object, str]
        pass # If id# is found in the log or file (log=None), returns entry, log.
             # Otherwise, returns None, None
    def delete(self, id: int, log: str = None): # Return Tuple[obj, str]
        pass # Removes id# from log or file (log=None). (!!HARD DELETE!!)
    def update(self, id: int, new_entry: object, log: str = None): # Return Tuple[object, str]
        pass # Updates id# with new_entry. Log is optional. Returns the old object, log if update was successful.
    def move(self, id: int, dest_log: str, src_log: str = None): # Return Tuple[object, str]
        pass # Moves id# to the destination log. Source log of entry is optional. Returns the object, src_log if move was successful.
    def search(self, lookup: any, log:str = None, field:str = None): #- Return listof Tuple[object, str]
        pass # Lookup any contents: the field and log are optional.

    # Log-based ops
    def list_logs(self) -> list:
        pass # Returns a list of logs in file_name: ["product_backlog","sprint_backlog",...]
    def list_fields(self) -> list:
        pass # Returns the list of fields for each story: ["id","priority","estimate",...]
    def read_log(self, log: str = None) -> list:
        pass # Returns all entries in the log, or all entries in the file if log=None


class json_reader(json_interface):
    def __init__(self, file_path: str):
        self._file_path = file_path
        # Hard coded logs, field because it's hard to read them in (in case file is empty)
        self._list_logs = ["product_backlog","sprint_backlog","current_sprint","previous_sprints","archived"]
        self._list_fields = ["id","priority","estimate","sprint","status","assigned_to","user_type","story"]
        self._j = None # Load file into memory   
        with open(file=self._file_path, mode="r+") as f:
            self._j = json.load(f)

    # Entry-based ops

    def create(self, entry: object, log: str):
        with open(file=self._file_path, mode="r+") as f:
            self._j[log].append(entry)             # Add to python obj
            f.seek(0)
            f.write(json.dumps(self._j, indent=4)) # Write python obj to file
            f.truncate()
    
    def read(self, id: int, log: str = None): # Return Tuple[object, str]
        # Helper function for reading specific log
        def read_log(r_log: str) -> object:
            entries = self._j[r_log]
            for e in entries:
                if e["id"] == id:
                    return e
            return None
        # Read specified log
        if log is not None and log in self._list_logs:
            return read_log(log), log
        # Scan over logs
        for l in self.list_logs():
            result = read_log(l)
            if (result != None):
                return result, l
        return None, None

    def read_all(self, log: str = None):
        return ([e for e in self._j[log]], log) if log in self._j.keys() else (None, log)
            
    def delete(self, id: int, log: str = None): # Returns Tuple[object, str]
        with open(file=self._file_path, mode="r+") as f:
            # Helper function for deleting from specific log
            def delete_from_log(l: str):
                entries = self._j[l] # Array of objs
                for idx in range(0, len(entries)):
                    if entries[idx]["id"] == id:
                        e = self._j[l].pop(idx) # Remove from python obj
                        f.seek(0)
                        f.write(json.dumps(self._j, indent=4)) # Write python obj to file
                        f.truncate()
                        return e
                return None
            # Remove from specified log
            if log is not None and log in self._list_logs:
                return delete_from_log(log), log
            # Iterate over all logs if not specified
            for l in self.list_logs():
                result = delete_from_log(l)
                if (result != None):
                    return result, l
            return None, None

    def update(self, id: int, new_entry: object, log: str = None): # Return Tuple[object, str]
        o, this_log = self.delete(id, log)
        if o is None or this_log is None:
            return None # Deletion failed
        self.create(new_entry, this_log)
        return new_entry, this_log

    def move(self, id: int, dest_log: str, src_log: str = None): # Return Tuple[object, str]
        entry, src_log = self.delete(id, src_log)
        if entry is None or src_log is None:
            return None # Deletion failed
        self.create(entry, dest_log)
        return entry, src_log
        
    def search(self, lookup: any, log:str = None, field:str = None): #- Return listof Tuple[object, str]
        if field is not None and field not in self._list_fields or log is not None and log not in self.list_logs():
            return None # Invalid field or log
        lookup = str(lookup)    # Cast to string
        found = []              # Will hold the found entries
        # Helper function for reading specific log
        def read_log(r_log: str):
            entries = self._j[r_log]
            for e in entries:
                def compare_field(field_):
                    if lookup in str(e[field_]): # Cast the value to a string as well
                        found.append([e, r_log])
                        return True
                    return False
                if field is not None:
                    compare_field(field)
                else: # scan over all fields
                    for f in self._list_fields:
                        if compare_field(f): break # If any field matches, stop comparing fields
        if log is not None and log in self._list_logs: # Read specified log
            read_log(log)
        else:  # Scan over logs
            for l in self.list_logs():
                read_log(l)
        return found

    # Log-based ops

    def list_logs(self) -> list:
        return self._list_logs

    def list_fields(self) -> list:
        return self._list_fields

    def read_log(self, log: str = None): # Returns if log=None: object else: list
        if log is not None and log not in self.list_logs():
            return None # error
        if log is None:
            return self._j
        else:
            return self._j[log]