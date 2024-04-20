#Stronge v0.9.0
#See README.md for License and other info

#Import
import os
import sys
import json
import time
import multiprocessing
from producesyntaxed import producesyntaxed
from ESDLang import main as ESDmain
from ESDExt import ESDsyntax, ESDautocomplete
from pytube import YouTube
from playsound import playsound

if __name__ == "__main__":
    producesyntaxed("Main Process:\n", "\033[96m", False)
print("Defining variables...")

#Def vars
linenum = 1
filename = ""
fileExtension = ""
runOptionsMenu = 0
runEdit = 0
runPrimarySettings = 0
version = "v0.9.0"

#!Music section, please ignore
def download_audio(yt_link):
    print("Downloading Background Song...")
    try:
        yt = YouTube(yt_link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download()
        return audio_file
    except Exception as e:
        print("Error downloading audio:", str(e))
        return None

def play_song(name):
    while True: playsound(name)

print("Checking for song presence...")
if not os.path.exists(os.path.join(os.getcwd(), "Bad Pigges Phonk.mp4")):
    download_audio("https://www.youtube.com/watch?v=m6edyjDaebM")
#!End


print("Opening and setting settings...")
#Open the settings file (contains autocomplete settings)
with open("settings", "r") as f:
    global fileExtensionDefault
    settings = f.readlines()
    mainSettings = json.loads(settings[1]) #Yes, main settings are line 2
    fileExtensionDefault = mainSettings['fileExtensionDefault']


print("Defining functions...")
#Clear the terminal
def clearConsole():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

#Clear the file
def clearFile():
    with open(filename, 'w') as f:
        f.write("")

#Increment line number by one
def incln(forwards=True):
    global linenum
    if forwards:
        linenum+=1
    else:
        linenum-=1

#Append with a "\n" beforehand
def appendn(data):
    if os.path.exists(filename): #The whole point of this and the below code that reads check is to make sure that the file doesn't end up with a blank line one... yeah...
        check = True
    else:
        check = False

    with open(filename, 'a+') as f:
        if check:
            f.write("\n" + data)
        else:
            f.write(data)


#Print with line numbers and syntax highlighting for .esdla files
def pront(linenum, line):
    global fileExtension
    if fileExtension == "esdla":
        ESDsyntax(linenum, line)
    else:
        print(linenum, ":", line.strip("\n"))


#Reload file, as if you just loaded stronge and selected a file. This is needed when inserting lines before others or editing lines.
def reloadFile():
    global linenum
    linenum = 1
    clearConsole()
    loadFile()
    print()


#Rewrite a specific line by line number
def rewriteLine(line_number, new_content):
    with open(filename, 'r') as f: #Read lines in filename
        lines = f.readlines()
    if 0 < line_number <= len(lines): #If the line exists..
        lines[line_number - 1] = new_content + '\n' #Line number -1 cuz computers count from zero, add the new content and then newline
    else:
        print("Line number out of range.")
        return
    try:
        with open(filename, 'w') as f: #Write to the file with the line rewritten
            f.writelines(lines)
        reloadFile() #Refresh the file (as if stronge is starting up again)
    except Exception as e:
        print("Error while rewriting: " + e)

# Prompt the user to enter the new content for rewriting a specific line
def promptForRewrite(line_number):
    new_content = input(f"Enter new content for line {line_number}: ")
    rewriteLine(line_number, new_content)

# Insert a line before a specific line number
def insertBeforeLine(line_number, new_content):
    with open(filename, 'r') as f: #Read lines in filename
        lines = f.readlines()
    if 0 < line_number <= len(lines): #If the line exists...
        lines.insert(line_number - 1, new_content + '\n')
        incln() #Increment the line number that is being edited by one (so you can continue editing)
    else:
        print("Line number out of range.")
        return
    try:
        with open(filename, 'w') as f: #Write the file with the line removed
            f.writelines(lines)
        reloadFile() #Reload the file (as if stronge is starting up again)
    except Exception as e:
        print("Error while inserting: " + e)

# Prompt the user to enter the content for inserting before a specific line
def promptForInsert(line_number):
    new_content = input("Enter the content to insert: ")
    insertBeforeLine(line_number, new_content)

# Delete a specific line number
def deleteLine(line_number):
    with open(filename, 'r') as f: #Read lines in filename
        lines = f.readlines()
    if 0 < line_number <= len(lines): #If the line exists...
        if linenum-1 == line_number:
            print("Deleteing or editing the line above the current one inserts a blank line after you make more changes and idk why, enter to continue.")
            input()
        del lines[line_number - 1]
    else: #If it doesn't...
        print("Line number out of range.")
        return #Return to stop code execution in the function
    try:
        with open(filename, 'w') as f: #Write the file with the line removed
            f.writelines(lines)
        reloadFile() #Reload the file (as if stronge is starting up again)
    except Exception as e: #If problem...
        print("Error while deleting: " + str(e))

# Prompt the user to enter the line number to delete
def promptForDelete(line_number):
    confirm = input(f"Are you sure you want to delete line {line_number}? (Y/N): ")
    if confirm.lower() == "y":
        deleteLine(line_number)
    else:
        print("Deletion aborted.")

#Handle any commands with arguments (as in, in 'rewrite 3', 3 is the argument)
def argCommand(inp):
    if inp.startswith("rewrite"): #Rewrite command
        parts = inp.split(" ")
        if len(parts) == 2 and parts[1].isdigit(): #If the second thing after rewrite is a number (as in 'rewrite 3'), then prompt for rewrite with that line number
            line_number = int(parts[1])
            promptForRewrite(line_number) 
        else:
            print("Invalid syntax for rewrite command.") #Else, you did it wrong so it will tell you
    elif inp.startswith("insert"): #Insert command
        parts = inp.split(" ")
        if len(parts) == 2 and parts[1].isdigit(): #If the second thing after insert is a number (as in 'insert 3'), then prompt for insert at that line number
            line_number = int(parts[1])
            promptForInsert(line_number)
        else:
            print("Invalid syntax for insert command.") #Else, you did it wrong so it will tell you
    elif inp.startswith("delete"):  #If the second thing after delete is a number (as in 'delete 3'), then prompt for delete at that line number
        parts = inp.split(" ")
        if len(parts) == 2 and parts[1].isdigit():
            line_number = int(parts[1])
            promptForDelete(line_number)
        else:
            print("Invalid syntax for delete command.") #Else, you did it wrong so it will tell you
    else:
        appendn(inp) #Else, save the file with the inputted line appended
        reloadFile() #Reload the file (so syntax highlighting works)


# Handle the input of the user (check for commands and things)
def handleInput(inp):
    global linenum
    global runEdit
    if fileExtension == "esdla":
        inp = ESDautocomplete(inp)
    match inp: #Match the input to _
        case "exit" | "x": #Exit command
            runEdit = 0
        case "run": #Run command (uses ESDlang)
            if fileExtension == "esdla":
                clearConsole()
                ESDmain(filename)
                input("Program finished. enter to go back to home screen.")
                runEdit = 0
            else:
                print("not ESDLang")
        case "reset": #Reset file command (wipes the file)
            choic = input("Are you sure? Y/N: ")
            if choic.lower() == "y":
                clearFile()
                clearConsole()
                linenum = 0
        case _: #Case (any other not mentioned)
            argCommand(inp) #Commands with arguments (as in, in 'rewrite 3', 3 is the argument)



# Make a new line to write on, then parse the input to the check function
def newLine():
    global linenum
    inputtedLine = input(f"{linenum} : ")
    handleInput(inputtedLine)

# Load file
def loadFile():
    with open(filename, "r") as f:
        for line in f:
            pront(linenum, line)
            incln()

def editFile():
    global filename
    global fileExtension
    global fileExtensionDefault
    global linenum
    linenum = 1
    filename = input("Choose a filename: ")
    fileExtension = input("Choose file type: ")
    if fileExtension == "":
        filename = filename + "." + fileExtensionDefault
        fileExtension = fileExtensionDefault #This has to be done because otherwise anything that checks the file extension just breaks
    else:
        if fileExtension.startswith("."): #If the file extension starts with a '.', make it so it doesn't
            fileExtension = fileExtension.removeprefix(".")
        filename = filename.strip() + "." + fileExtension.strip()
    clearConsole()

    try: #Try to load the inputted file from save. If there is no file, just skip and create a new one.
        loadFile()
        print()
    except FileNotFoundError:
        pass

    global runEdit
    while runEdit: #Create a new line for you to write on in an infinite loop
        newLine()

#For editing primary settings, called by optionsMenu()
def editPrimarySettings(settings):
    allSettings = settings[0]
    primarySettings = settings[1]
    settingToModify = input("Which setting would you like to modify? (x to exit): ")
    if settingToModify == "x":
        pass
    elif settingToModify in primarySettings:
        whatToSetItTo = input("What would you like the setting set to?: ")
        primarySettings[settingToModify] = whatToSetItTo
        allSettings[1] = json.dumps(primarySettings)
        with open("settings", "w") as f:
            f.writelines(allSettings)
        clearConsole()
        displaySettings(1)
    else:
        print("That setting doesn't exist.")
        clearConsole()
        displaySettings(1)
    clearConsole()


def displaySettings(line):
    with open("settings", "r+") as f:
        allSettings = f.readlines()
        primarySettings = json.loads(allSettings[line])
    for setting in primarySettings:
        producesyntaxed(setting, '\033[38;5;226m')
        producesyntaxed("is set to ", '\033[96m', False)
        producesyntaxed(f"{primarySettings[setting]}\n", '\033[38;5;208m', False)
    editPrimarySettings([allSettings, primarySettings])


def optionsMenu():
    print("Welcome to the options menu. Options: ")
    print("edit primary (s)ettings\nview (r)eadme\ne(x)it options menu")
    command = input("Please enter a command: ").lower()
    clearConsole()
    match command:
        case "s":
            displaySettings(1)
        case "r":
            with open("README.md", "r") as f:
                producesyntaxed(f.read()+"\n", '\033[96m', False)
        case "x":
            global runOptionsMenu
            runOptionsMenu = 0
    

def home():
    print("Welcome to Stronge editor " + version)
    print("Available commands:\n(e)dit or create a file\n(o)ptions menu\ne(x)it Stronge")
    command = input("Please enter a command: ").lower()
    clearConsole()
    match command:
        case "o":
            global runOptionsMenu
            runOptionsMenu = 1 #Variable so the options menu runs
            while runOptionsMenu == 1:
                optionsMenu()
        case "e":
            global runEdit
            runEdit = 1 #Variable so the edit process runs
            editFile() #Triggers the edit process
        case "x":
            print("Exiting Stronge...")
            extremelyAmazingPhonkProcess.terminate()
            sys.exit()
        case _:
            print("Command not found. Returning home in 3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)
    clearConsole()


if __name__ == "__main__":
    producesyntaxed("Song Process:\n", "\033[96m", False)
    extremelyAmazingPhonkProcess = multiprocessing.Process(target=play_song, args=("Bad Pigges Phonk.mp4",))
    extremelyAmazingPhonkProcess.start()
    time.sleep(0.25)
    clearConsole()
    while True: home() 
else:
    print("Loaded Stronge!")