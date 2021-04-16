import json

class json_interface():
    def __init__(self, file_name: str = "scrum_board.json"):
        pass # Opens file_name in data directory. default file_name is scrum_board.json
    def create(self, entry: object, log: str):
        pass # Adds the entry to specified log in file_name
    def read(self, id: int, log: str = None) -> object:
        pass # Returns entry id# from log. If log if None (default), must scan all logs.
             # Preferably check if the id# is valid before calling the json interface.
             # If id# is not in log or file, returns None.
    def update(self, id: int, entry: object, log: str = None):
        pass # Replaces id# with new entry
    def delete(self, id: int, log: str = None):
        pass # Removes id# from log (!!HARD DELETE!!)
    def search_string(self, lookup: str, log: str = None) -> object:
        pass # lookup by string
    def list_logs(self) -> list:
        pass # Returns a list of logs in file_name
    def close(self):
        pass # closes the file reader

class json_reader(json_interface):
    def __init__(self, file_name: str = "scrum_board.json"):
        self._f = open("..\data\\"+file_name, "r")
        self._j = json.load(self._f)
        print(str(self._j))

    def create(self, entry: object, log: str):
        pass # Adds the entry to specified log in file_name
    def read(self, id: int, log: str = None) -> object:
        pass # Returns entry id# from log. If log if None (default), must scan all logs.
             # Preferably check if the id# is valid before calling the json interface.
             # If id# is not in log or file, returns None.
    def update(self, id: int, entry: object, log: str = None):
        pass # Replaces id# with new entry
    def delete(self, id: int, log: str = None):
        pass # Removes id# from log (!!HARD DELETE!!)
    def search_string(self, lookup: str, log: str = None) -> object:
        pass # lookup by string
    def list_logs(self) -> list:
        pass # Returns a list of logs in file_name
    def close(self):
        self._f.close()


#my_json_reader = json_reader()
#my_json_reader.close()
