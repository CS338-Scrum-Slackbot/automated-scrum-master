from spellchecker import SpellChecker
import json
import string
import re

# Adds our dictionary stored in freq_synonyms to the spellchecker's default dictionary
spell = SpellChecker() 
#spell = SpellChecker(language=None, case_sensitive=False) # turn off loading a built language dictionary, case sensitive off
spell.word_frequency.load_dictionary('data/freq_synonyms.json') # Adds our dictionary

def normalize(s):
    for p in string.punctuation:                    # Remove punctuation
        s = s.replace(p, '')
    s = re.sub(pattern='\s+', string=s, repl=' ')   # Replace whitespace
    return s.lower().strip()                        # Lowercase, strip whitespace

def run_tests():
    with open("src/spellchecker/test.json", "r") as f:
        tests = json.load(f)
        for t in tests:
            t = normalize(t)
            out = ""
            for word in t.split(" "):
                out += spell.correction(word) + " "
            print(out.strip(" "))

def freq(word):
    print(f"The current frequency of \'{word}\' is {spell.word_frequency.dictionary[word]}")