import json
from os import read

class json_interface():
    def __init__(self, file_path: str = "../data/scrum_board.json"):
        pass # Opens file_name in data directory. default file_name is scrum_board.json
    def create(self, entry: object, log: str = "product_backlog"):
        pass # Adds the entry to specified log in file_name
    def read(self, id: int, log: str = None): # Return Tuple[object, str]
        pass # Returns entry id# and log-str. If input log if None (default), must scan all logs.
             # If id# is not in log or file, returns None.
    def update(self, id: int, entry: object, log: str = None): # Return Tuple[object, str]
        pass # Replaces id# with new entry
    def delete(self, id: int, log: str = None): # Return str
        pass # Removes id# from log (!!HARD DELETE!!)
    def search_string(self, lookup: str, log: str = None) -> object:
        pass # lookup by string
    def list_logs(self) -> list:
        pass # Returns a list of logs in file_name
    def close(self):
        pass # closes the file reader

"""  TODO return which log the object is located in
hopefully the json reader will not be used to manage any non scrum board files
may need to implement search by status, priority, etc
"""

class json_reader(json_interface):
    def __init__(self, file_path: str = "../data/scrum_board.json"):
        self._f = open(file=file_path, mode="r+") # access mode read and write. TODO: slashes
        self._j = json.load(self._f)
        
    # Helper function for reading specific log
    def _read_log(self, id: int, r_log: str) -> object:
        entries = self._j[r_log]
        for e in entries:
            if e["id"] == id:
                return e
        return None
    
    def create(self, entry: object, log: str):
        pass # Adds the entry to specified log in file_name
    
    def read(self, id: int, log: str = None): # Return Tuple[object, str]
        if log != None:
            return self._read_log(id, log), log
        else: # scan over logs
            for l in self.list_logs():
                result = self._read_log(id, l)
                if (result != None):
                    return result, l
            return None, None

    def update(self, id: int, entry: object, log: str = None): # Return Tuple[object, str]
        # TODO: does not check if id# already exists somewhere
        pass # idk if this should actually be an operation
        """if log is None:
            for l in self.list_logs():
                result = self._read_log(id, l)
                if (result != None):
                    log = l
        self._j[log].append(story)
        print(self.sb['product_backlog'])
        with open(SCRUM_BOARD, 'w') as f
            json.dump(self.sb, f, indent=4)"""


    def delete(self, id: int, log: str = None):
        # Helper function for deleting from specific log
        def delete_from_log(l: str):
            entries = self._j[l] # Array of objs
            for idx in range(0, len(entries)):
                if entries[idx]["id"] == id:
                    self._j[l].pop(idx) # Remove from python obj
                    self._f.seek(0)
                    self._f.write(json.dumps(self._j, indent=4)) # Write python obj to file
                    self._f.truncate()
                    return l
            return None

        if log is not None:
            return delete_from_log(log)

        log_list = self.list_logs()
        num_logs = len(log_list)
        idx = 0
        result = None
        while idx < num_logs and result is None:
            result = delete_from_log(log_list[idx])
            idx = idx + 1
        return result
        

    def search_string(self, lookup: str, log: str = None) -> object:
        pass # lookup by string
    def list_logs(self) -> list:
        return list(self._j.keys())
    def close(self):
        self._f.close()


# Tests:
"""my_json_reader = json_reader(file_path="../data/scrum_board_copy.json")

result = my_json_reader.delete(id=4)
print(str(result))

my_json_reader.close()"""