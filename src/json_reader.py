import json
from os import read

class json_interface():
    def __init__(self, file_path):
        pass # Opens file_name in data directory
    def create(self, entry: object, log: str):
        pass # Adds the entry to specified log
    def read(self, id: int, log: str = None): # Return Tuple[object, str]
        pass # Returns entry obj and log str. If input log if None (default), must scan all logs.
             # If id# is not in log or file, returns None.
    def delete(self, id: int, log: str = None): # Return Tuple[obj, str]
        pass # Removes id# from log (!!HARD DELETE!!). Use for update operations.
    def search_string(self, lookup: str, log: str = None) -> object:
        pass # lookup by string
    def list_logs(self) -> list:
        pass # Returns a list of logs in file_name: ["product_backlog","sprint_backlog",...]
    def close(self):
        pass # Closes the file reader

"""
TODO: implement search by status, priority, etc
may be coupled with id search
repeated code in read, delete - can be abstracted if you have time
"""

class json_reader(json_interface):
    def __init__(self, file_path: str):
        self._f = open(file=file_path, mode="r+") # access mode: read and write. TODO: slashes
        self._j = json.load(self._f)
    
    def create(self, entry: object, log: str):
        self._j[log].append(entry)                   # Add to python obj
        self._f.seek(0)
        self._f.write(json.dumps(self._j, indent=4)) # Write python obj to file
        self._f.truncate()
    
    def read(self, id: int, log: str = None): # Return Tuple[object, str]
        # Helper function for reading specific log
        def _read_log(self, r_log: str) -> object:
            entries = self._j[r_log]
            for e in entries:
                if e["id"] == id:
                    return e
            return None
        # Read specified log
        if log is not None:
            return self._read_log(id, log), log
        # Scan over logs
        for l in self.list_logs():
            result = self._read_log(id, l)
            if (result != None):
                return result, l
        return None, None

    def update(self, id, field, value):
        # loop through each log
        print(id, field, value)
        for k, v in self._j.items():
            # loop through each story in a log
            for i in v:
                # if id matches
                if i['id'] == int(id):
                    # update field with value
                    i[field] = value
                    # and write updated json to file
                    self._f.seek(0)
                    self._f.write(json.dumps(self._j, indent=4))
                    self._f.truncate()
                    return i # success
        return None # failure

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

    def search_string(self, lookup: str, log: str = None) -> object:
        pass # TODO: lookup by string

    def list_logs(self) -> list:
        return list(self._j.keys())

    def close(self):
        self._f.close()


"""# Tests:
my_json_reader = json_reader(file_path="../data/scrum_board_copy.json")

obj, log = my_json_reader.delete(id=4)
print(str(obj))

my_json_reader.close()"""