class json_in():
    def __init__(self, file_name: str):
        pass # Opens file_name
    def create(self, entry: object, log: str):
        pass # Adds the entry to specified log in file_name
    def read(self, id: int, log: str) -> object:
        pass # Finds entry by id#
    def update(self, id: int, entry: object, log: str):
        pass # Replaces id# in log with the new entry
    def delete(self, id: int, log: str):
        pass # Removes id# from log (!!HARD DELETE!!)
    def search(self, lookup: str, log: str) -> object:
        pass # Searches log by string
    def list_logs(self) -> list:
        pass # Returns a list of logs in file_name
    def close(self):
        pass # closes the file reader

class json_interface(json_in):
    pass