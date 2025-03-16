import random
import sys
import os

# Probabilities:
# * : 50%
# - : 1%
combinations = ["C*C*VV-L*", "N"]
threshold = 0.95
patterns = {
    "C": "pbtdkg'mnñfvþðszcxwrlj",
    "V": "aeiou",
    "L": "wlrjmns",
    "N": "mn",
}
consonants_by_place = [
    "pbmfvw",       # Labial
    "þð",           # Dental
    "tdnszrl",      # Alveolar
    "ñcj",          # Palatal
    "kgx",          # Velar
    "'",            # Glottal
]
consonants_by_manner = [
    "pbtdkg'",      # Plosives
    "mnñ",          # Nasal
    "fvþðszcx",     # Fricative
    "wrlj",         # Liquid
]
long_map = {
    "a":"ā",
    "e":"ē",
    "i":"ī",
    "o":"ō",
    "u":"ū",
}

disallowed_diphthongs = ["ae", "ea", "uo", "ou"]

def get_articulation(consonant):
    place = -1
    manner = -1
    for i in range(0, len(consonants_by_place)):
        if consonant in consonants_by_place[i]:
            place = i
            break
    for i in range(0, len(consonants_by_manner)):
        if consonant in consonants_by_manner[i]:
            manner = i
            break
    return (place, manner)

def generate_syllable():
    index = 0 if random.random() < threshold else 1
    combination = combinations[index]
    syllable = ""

    for i in range(0, len(combination)):
        # Skip the optional specifier
        if not combination[i].isalnum():
            continue
        # Continue if there is an optional specifier 50% of the time
        if i + 1 < len(combination) and combination[i + 1] == '*' and random.random() < 0.5:
            continue
        if i + 1 < len(combination) and combination[i + 1] == '-' and random.random() < 0.01:
            continue
        valid_chars = patterns[combination[i]]
        syllable += valid_chars[random.randrange(0, len(valid_chars))]
    if len(syllable) > 1:
        first_articulation = get_articulation(syllable[0]) 
        second_articulation = get_articulation(syllable[1])
        if(first_articulation[1] == 3 and syllable[1] in patterns["C"]) or (first_articulation == second_articulation and first_articulation != (-1, -1)):
            syllable = syllable[:1] + syllable[2:]

    return syllable

def generate_word():
    word = ""
    syllable_count = random.randrange(2, 4)
    for i in range(0, syllable_count):
        word += generate_syllable()
    
    return word

def normalize_word(word):
    word += ' '
    result = ""
    elongate = False
    articulation = (-1, -1)
    for i in range(1, len(word)):
        if word[i] == "'" and not word[i - 1] in patterns["V"] and not word[i - 1] in patterns["L"]:
            continue
        elif word[i - 1] == "'" and word[i] in patterns["C"]:
            continue
        elif word[i - 1] in patterns["V"] and word[i] in patterns["V"]:
            if word[i - 1] == word[i]:
                elongate = True
                continue
            elif (word[i-1] + word[i]) in disallowed_diphthongs:
                continue
        elif word[i - 1] == word[i]:
            continue
        if elongate:
            result += long_map[word[i - 1]]
        else:
            result += word[i - 1]
        elongate = False
    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: ")
        print(sys.argv[0], "[word_count]")
        os._exit(-1)
    for i in range(0, int(sys.argv[1])):
        word = generate_word()
        word = normalize_word(word) 
        print(word)

if __name__ == "__main__":
    main()
