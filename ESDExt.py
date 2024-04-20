#ESDExt v0.3.0.

import json
from producesyntaxed import producesyntaxed

RED = '\033[38;5;203m'
ORANGE = '\033[38;5;208m'
GREEN = '\033[38;5;120m'
YELLOW = '\033[38;5;226m'
BLUE = '\033[38;5;117m' #dark-aqua sort of colour
BLUE2 = '\033[96m' #darker blue

with open("settings", "r") as f:
    global autoReplacements
    settings = f.readlines()
    autoReplacements = json.loads(settings[0])

def canfloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def colourElse(part, words):
    if len(words) == 1 and len(part) == 4:
        producesyntaxed(part, BLUE)
    else:
        producesyntaxed(part, RED)

def colourIf(part, words):
    if len(words) == 4:
        producesyntaxed(part, BLUE)
    else:
        producesyntaxed(part, RED)

#Colour write or input
def colourWI(part, words):
    if len(words) > 1 and len(part) == 5:
        producesyntaxed(part, BLUE)
    else:
        producesyntaxed(part, YELLOW)

#Colour quit
def colourQ(part, words):
    if len(words) == 1 and len(part) == 4:
        producesyntaxed(part, BLUE2)
    else:
        producesyntaxed(part, RED)

#Colour normal BLUE/RED stuff
def colour(part, words, correctLength, correctLineLength=1):
    if len(words) >= correctLineLength and len(part) == correctLength:
        producesyntaxed(part, BLUE)
    else:
        producesyntaxed(part, RED)

def ESDsyntax(lnnum, line: str):
    print(f"\n{lnnum} :", end=" ")
    words = line.split()
    for part in words:
        match part:
            case _ if canfloat(part) == True:
                        producesyntaxed(part, ORANGE)
            case "write" | "input":
                        colourWI(part, words)
            case _ if part.startswith("if"):
                        colourIf(part, words)
            case _ if part.startswith("else"):
                        colourElse(part, words)
            case "endstat":
                        colour(part, words, 7, 1)
            case "var":
                        colour(part, words, 3, 3)
            case "quit":
                    colourQ(part, words)
            case _:
                        producesyntaxed(part, GREEN)

#Autocomplete (language server)
def ESDautocomplete(sentence):
    words = sentence.split() #Split the words in the input
    if words[0] in autoReplacements: #If the first word can be replaced, replace it
        words[0] = autoReplacements[words[0]]
        words = ' '.join(words)
        return words
    else:
        return sentence

if __name__ == "__main__": print("you're not meant to run this directly, stop it!")