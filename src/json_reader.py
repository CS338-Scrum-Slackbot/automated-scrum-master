import json
from os import read

"""
#### README
The sample code below shows usage of json_reader.
- You should use an import-as statement.
- The file_path starts with 'data/' NOT '../data/' or './data/'
- You should probably call reader.close to close the opened file after your operation. I can't guarantee what happens if you don't.
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
    my_obj, my_log = reader.delete(self, id=my_id, log=my_log)

    ...

    my_logs = reader.list_logs()
    print(str(my_logs)) --> ["product_backlog",""sprint_backlog","current_sprint","archived"]

    ...

    reader.close()
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
    def update(self, id: int, new_entry: object, log: str = None) -> bool:
        pass # Updates id# with new_entry. Log is optional.
    def move(self, id: int, dest_log: str, src_log: str = None) -> bool:
        pass # Moves id# to the destination log. Source log of entry is optional.
    def search(self, lookup:str, log:str = None) -> object:
        pass # Lookup string in log (optional)

    # Log-based ops
    def list_logs(self) -> list:
        pass # Returns a list of logs in file_name: ["product_backlog","sprint_backlog",...]
    def read_log(self, log: str = None) -> list:
        pass # Returns all entries in the log, or all entries in the file if log=None
    
    def close(self):
        pass # Closes the file reader




class json_reader(json_interface):
    def __init__(self, file_path: str):
        self._f = open(file=file_path, mode="r+")     # RW mode
        self._j = json.load(self._f)
    
    # Entry-based ops

    def create(self, entry: object, log: str):
        self._j[log].append(entry)                   # Add to python obj
        self._f.seek(0)
        self._f.write(json.dumps(self._j, indent=4)) # Write python obj to file
        self._f.truncate()
    
    def read(self, id: int, log: str = None): # Return Tuple[object, str]
        # Helper function for reading specific log
        def read_log(r_log: str) -> object:
            entries = self._j[r_log]
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
        # Helper function for deleting from specific log
        def delete_from_log(l: str):
            entries = self._j[l] # Array of objs
            for idx in range(0, len(entries)):
                if entries[idx]["id"] == id:
                    e = self._j[l].pop(idx) # Remove from python obj
                    self._f.seek(0)
                    self._f.write(json.dumps(self._j, indent=4)) # Write python obj to file
                    self._f.truncate()
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

    def update(self, id: int, new_entry: object, log: str = None) -> bool:
        pass # Updates id# with new_entry. Log is optional.
    def move(self, id: int, dest_log: str, src_log: str = None) -> bool:
        pass # Moves id# to the destination log. Source log of entry is optional.
    def search(self, lookup:str, log:str = None) -> object:
        pass # Lookup string in log (optional)

    # Log-based ops

    def list_logs(self) -> list:
        return list(self._j.keys())

    def read_log(self, log: str = None) -> list:
        if log is None:
            return self._j
        elif log not in self.list_logs():
            return None # error
        else:
            return self._j[log]

    def close(self):
        self._f.close()




# Tests:
my_json_reader = json_reader(file_path="data/scrum_board_copy.json")

obj, log = my_json_reader.read(id=4, log="current_sprint")
print(str(obj))

my_json_reader.close()