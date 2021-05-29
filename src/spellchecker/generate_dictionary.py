import json

# Generates another JSON file where the original values (canonical keywords)
# have been replaced by '1', the same frquency for all words.
new_obj = None
with open("data/synonyms.json", "r") as f:
    obj = json.load(f)
    new_obj = {}
    for key in list(obj.keys()):
        if " " not in key:
            new_obj[key] = 1000000
with open("data/freq_synonyms.json", "r+") as f:
    f.seek(0)
    f.write(json.dumps(new_obj, indent=4)) # Write python obj to file
    f.truncate()

