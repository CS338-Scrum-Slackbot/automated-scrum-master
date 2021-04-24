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
    my_log = ... optional (same as above)
    my_obj, my_log = reader.delete(id=my_id, log=my_log)

    ...
    
    my_id = ...
    my_log = ... optional (same as above)
    new_obj = ... # update() returns the old object
    old_obj, my_log = reader.update(id=my_id, new_entry=new_obj, log=my_log)

    ...
    
    my_id = ...
    my_log = ... optional (same as above)
    move_to_log = ...
    my_obj, my_log = reader.move(id=my_id, dest_log=move_to_log, src_log=my_log)

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
    def search_story(self, lookup:str, log:str = None) -> object:
        pass # Lookup string in the story field. log (optional)

    # Log-based ops
    def list_logs(self) -> list:
        pass # Returns a list of logs in file_name: ["product_backlog","sprint_backlog",...]
    def list_fields(self) -> list:
        pass # Returns the list of fields for each story: ["id","priority","estimate",...]
    def read_log(self, log: str = None) -> list:
        pass # Returns all entries in the log, or all entries in the file if log=None
    
    def close(self):
        pass # Closes the file reader




class json_reader(json_interface):
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._list_logs = None
        with open(file=self._file_path, mode="r") as f:
            j = json.load(f)
            self._list_logs = list(j.keys())
            # Hard coded fields because it's hard to read them in (in case file is empty)
            self._list_fields = ["id","priority","estimate","sprint","status","assigned_to","user_type","story"]
            # TODO: implement indexing by users or team members here
    
    # Entry-based ops

    def create(self, entry: object, log: str):
        with open(file=self._file_path, mode="r+") as f:
            j = json.load(f)
            j[log].append(entry)                   # Add to python obj
            f.seek(0)
            f.write(json.dumps(j, indent=4)) # Write python obj to file
            f.truncate()
    
    def read(self, id: int, log: str = None): # Return Tuple[object, str]
        with open(file=self._file_path, mode="r") as f:
            j = json.load(f)
            # Helper function for reading specific log
            def read_log(r_log: str) -> object:
                entries = j[r_log]
                for e in entries:
                    if e["id"] == id:
                        return e
                return None
            # Read specified log
            if log is not None:
                return read_log(log), log
            # Scan over logs
            for l in self.list_logs():
                result = read_log(l)
                if (result != None):
                    return result, l
            return None, None

    def delete(self, id: int, log: str = None): # Returns Tuple[object, str]
        with open(file=self._file_path, mode="r+") as f:
            j = json.load(f)
            # Helper function for deleting from specific log
            def delete_from_log(l: str):
                entries = j[l] # Array of objs
                for idx in range(0, len(entries)):
                    if entries[idx]["id"] == id:
                        e = j[l].pop(idx) # Remove from python obj
                        f.seek(0)
                        f.write(json.dumps(j, indent=4)) # Write python obj to file
                        f.truncate()
                        return e, l
                return None, None
            # Remove from specified log
            if log is not None:
                return delete_from_log(log)
            # Iterate over all logs if not specified
            log_list = self.list_logs()
            num_logs = len(log_list)
            idx = 0
            result = None
            while idx < num_logs and result is None:
                result, _ = delete_from_log(log_list[idx])
                idx = idx + 1
            return result, log_list[idx-1]

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
            return [] # Invalid field or log

        # TODO: take this out of the WITH block. reason: don't need to open file
        with open(file=self._file_path, mode="r") as f:
            j = json.load(f)
            lookup = str(lookup)    # Cast to string
            found = []              # Will hold the found entries
            # Helper function for reading specific log
            def read_log(r_log: str):
                entries = j[r_log]
                for e in entries:
                    def compare_field(field_):
                        if lookup in str(e[field_]): # Cast the value to a string as well
                            found.append([e, r_log])
                    if field is not None:
                        compare_field(field)
                    else: # scan over all fields
                        for f in self._list_fields:
                            compare_field(f)

            if log is not None: # Read specified log
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

    def read_log(self, log: str = None) -> list:
        if log is not None and log not in self.list_logs():
            return None # error
        with open(file=self._file_path, mode="r+") as f:
            j = json.load(f)
            if log is None:
                return j
            else:
                return j[log]