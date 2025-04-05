#!/bin/env python
import sys
import os
import datetime
from functools import cmp_to_key

def lexicalSort(entries):
    alphabet = "āâãabcdēêẽefgxīîĩijklmnōôõopñrstūûũuvþðw'z "

    def compare(first, second):
        index = 0
        while index < min(len(first[0]), len(second[0])) and first[0][index] == second[0][index]:
            index += 1
        if index < len(first[0]) and index < len(second[0]):
            try:
                return -1 if alphabet.index(first[0][index]) < alphabet.index(second[0][index]) else 1
            except:
                return -1
        elif index < len(first[0]):
            return -1
        else:
            return 1

    entries.sort(key=cmp_to_key(compare))
    return entries

def main():
    base = os.path.join(os.path.dirname(sys.argv[0]), "..")
    dictionary_path = os.path.join(base, "dictionary.md")
    backup_path = os.path.join(base, "temp", f"dictionary_copy_{datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')}.md")
    dictionary_file = open(dictionary_path, "r+")
    backup_file = open(backup_path, "w")
    dictionary = dictionary_file.read()
    backup_file.write(dictionary)
    backup_file.close()

    heading_index = dictionary.find("## Word List")
    if heading_index == -1:
        print("No word list heading found. Maybe try updating the script? (the heading was probably modified)", file=sys.stderr)
        os._exit(-2)
    
    table = dictionary[heading_index:]
    occurences = [i for i, char in enumerate(table) if char == '\n']
    if len(occurences) < 5:
        print("Check table format and run this script again.")
        os._exit(-3)

    prepended = dictionary[:heading_index] + table[:occurences[3]+1]
    table = table[occurences[3]+1:]
    entries = "\n".join([element.strip() for element in table.split("\n")])
    entries = [element.split('|')[1:] for element in entries.split("|\n")]
    entries[-1].pop()
    entries = lexicalSort(entries)
    for i in range(0, len(entries)):
        entries[i] = '|' + '|'.join(entries[i])
    entries = '|\n'.join(entries)
    final_dictionary = prepended + entries + '|'
    print(final_dictionary)
    dictionary_file.seek(0)
    dictionary_file.truncate()
    dictionary_file.write(final_dictionary)
    dictionary_file.close()

if __name__ == "__main__":
    main()