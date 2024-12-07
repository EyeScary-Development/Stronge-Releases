import json
from output.producesyntaxed import producesyntaxed
from output.colours import *

keywords = ['print', 'input', 'if', 'else', 'def', 'try:', 'except:', 'return', 'import', 'from', 'for', 'in', 'match', 'case', 'and', 'or']

with open("settings", "r") as f:
	global autoReplacements
	settings = f.readlines()
	for line in settings:
		if line.startswith('py-auto:'):
			autoReplacements = json.loads(line.split("py-auto: ")[1])

def canfloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def colourKeywords(part):
    producesyntaxed(part, BLUE)

#Colour print or input
def colourPI(part, words):
    if len(words) > 1 and len(part) == 5:
        producesyntaxed(part, BLUE)
    else:
        producesyntaxed(part, YELLOW)

#Colour normal BLUE/RED stuff
def colour(part, words, correctLength, correctLineLength=1):
    if len(words) >= correctLineLength and len(part) == correctLength:
        producesyntaxed(part, BLUE)
    else:
        producesyntaxed(part, RED)

def PYsyntax(lnnum, line: str):
    line = line.removesuffix("\n")
    print(f"\n{lnnum} :", end=" ")
    words = line.split(" ")
    for part in words:
        match part:
            case _ if canfloat(part) == True:
                producesyntaxed(part, ORANGE)
            case _ if part in keywords:
                colourKeywords(part)
            case "exit":
                producesyntaxed(part, BLUE2)
            case _:
                producesyntaxed(part, GREEN)

#Autocomplete (language server)
def PYautocomplete(sentence):
    words = sentence.split() #Split the words in the input
    if words[0] in autoReplacements: #If the first word can be replaced, replace it
        words[0] = autoReplacements[words[0]]
        words = ' '.join(words)
        return words
    else:
        return sentence
