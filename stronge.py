#Stronge v0.11.0
#See README.md for License and other info

#Import
import os
import sys
import json
import time
import multiprocessing
import requests
from output.producesyntaxed import producesyntaxed
from ESDLang import main as ESDmain
from extensions.ESDExt import ESDsyntax, ESDautocomplete
from extensions.PyExt import PYsyntax, PYautocomplete
from output.colours import BLUE2
from ezlog import log
from pytube import YouTube
from playsound import playsound

beginLoadTime = time.time()

if __name__ == "__main__":
    producesyntaxed("Main Process:\n", "\033[96m", False)
log("Defining variables...")

#Def vars
linenum = 1
filename = ""
fileExtension = ""
runOptionsMenu = 0
runEdit = 0
runPrimarySettings = 0
version = "v0.11.0"

log("Opening and setting settings...")
#Open the settings file (contains autocomplete settings)
with open("settings", "r") as f:
    global fileExtensionDefault
    settings = f.readlines()
    mainSettings = json.loads(settings[1]) #Yes, main settings are line 2
    fileExtensionDefault = mainSettings['fileExtensionDefault']
    musicYTlink = mainSettings['musicYTlink']

#Audio downloader (from youtube)
def download_audio(yt_link):
    log(f"Downloading new background song with link {yt_link}...")
    try:
        yt = YouTube(yt_link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(os.path.join(os.getcwd(), "resources"), "song.mp4")
        log("Success")
        return audio_file
    except Exception as e:
        log("Error downloading audio:" + str(e))
        return None

def play_song():
    try:
        while True: playsound(os.path.join(os.getcwd(), "resources", "song.mp4"))
    except Exception as e:
        log("playsound error "+ str(e))

log("Checking for song presence...")
if not os.path.exists(os.path.join(os.getcwd(), "resources", "song.mp4")):
    download_audio(musicYTlink) #Gotta love using YouTube as a CDN

log("Comparing old settings...")
#Checker to update anything that may need to be redownloaded based on setting changes
with open(os.path.join(os.getcwd(), "resources", "oldchecks"), "r") as f:
    oldchecks = f.readlines()
    if "youtu" not in musicYTlink:
        log("Invalid YT URL. Not playing music.")
    elif oldchecks[0] != musicYTlink:
        oldchecks[0] = musicYTlink
        download_audio(musicYTlink)
        with open(os.path.join(os.getcwd(), "resources", "oldchecks"), "w") as fw:
            fw.writelines(oldchecks)


log("Defining functions...")
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

#Append with a "\n" after
def appendn(data):
    with open(filename, 'a+') as f:
        f.write(data + "\n")


#Print with line numbers and syntax highlighting for .esdla files
def pront(linenum, line: str):
    global fileExtension
    if fileExtension == "esdla":
        ESDsyntax(linenum, line)
    elif fileExtension == "py":
        PYsyntax(linenum, line)
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
def rewriteLine(line_number):
    new_content = input(f"Enter new content for line {line_number}: ")
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
        log("Error while rewriting: " + e)

# Insert a line before a specific line number
def insertBeforeLine(line_number):
    new_content = input("Enter the content to insert: ")
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
        log("Error while inserting: " + e)

# Delete a specific line number
def deleteLine(line_number):
    with open(filename, 'r') as f: #Read lines in filename
        lines = f.readlines()
    if 0 < line_number <= len(lines): #If the line exists...
        del lines[line_number - 1]
    else: #If it doesn't...
        print("Line number out of range.")
        return #Return to stop code execution in the function
    try:
        with open(filename, 'w') as f: #Write the file with the line removed
            f.writelines(lines)
        reloadFile() #Reload the file (as if stronge is starting up again)
    except Exception as e: #If problem...
        log("Error while deleting: " + str(e))

# Prompt the user to enter the line number to delete
def promptForDelete(line_number):
    confirm = input(f"Are you sure you want to delete line {line_number}? (Y/N): ")
    if confirm.lower() == "y":
        deleteLine(line_number)
    else:
        print("Deletion aborted.")

#Handle any commands with arguments (as in, in 'rewrite 3', 3 is the argument)
def argCommand(inp: str):
    if inp.startswith("rewrite"): #Rewrite command
        parts = inp.split(" ")
        if len(parts) == 2 and parts[1].isdigit(): #If the second thing after rewrite is a number (as in 'rewrite 3'), then prompt for rewrite with that line number
            line_number = int(parts[1])
            rewriteLine(line_number) 
        else:
            print("Invalid syntax for rewrite command.") #Else, you did it wrong so it will tell you
    elif inp.startswith("insert"): #Insert command
        parts = inp.split(" ")
        if len(parts) == 2 and parts[1].isdigit(): #If the second thing after insert is a number (as in 'insert 3'), then prompt for insert at that line number
            line_number = int(parts[1])
            insertBeforeLine(line_number)
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
    elif fileExtension == "py":
        inp = PYautocomplete(inp)
    match inp: #Match the input to _
        case "exit" | "x": #Exit command
            runEdit = 0
        case "run" | "rn": #Run command (uses ESDLang)
            if fileExtension == "esdla":
                clearConsole()
                ESDmain(filename)
                input("Program finished. enter to go back to home screen.")
                runEdit = 0
            elif fileExtension == "py":
                clearConsole()
                os.system(f"python3 {filename}")
                input("Program finished. enter to go back to home screen.")
                runEdit = 0
            else:
                print("not ESDLang")
        case "reset" | "rs": #Reset file command (wipes the file)
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

def editFile(ogfn=""):
    global filename
    global fileExtension
    global fileExtensionDefault
    global linenum
    global runEdit
    linenum = 1
    if not ogfn == "":
        runEdit = True
        filename = ogfn
        filename, fileExtension = filename.split(".")
        if fileExtension.startswith("."): #If the file extension starts with a '.', make it so it doesn't
            fileExtension = fileExtension.removeprefix(".")
        filename = filename.strip() + "." + fileExtension.strip()
    else:
        filename = input("Choose a filename: ")
        fileExtension = input("Choose file type: ")
    if fileExtension == "":
        filename = filename + "." + fileExtensionDefault
        fileExtension = fileExtensionDefault #This has to be done because otherwise anything that checks the file extension just breaks
    elif ogfn == "":
        if fileExtension.startswith("."): #If the file extension starts with a '.', make it so it doesn't
            fileExtension = fileExtension.removeprefix(".")
        filename = filename.strip() + "." + fileExtension.strip()
    if "/" or "\\" not in filename:
        if ogfn == "":
            filename = os.path.join(os.getcwd(), "files", filename)
        else:
            filename = os.path.join(os.getcwd(), filename)
    clearConsole()

    try: #Try to load the inputted file from save. If there is no file, just skip and create a new one.
        loadFile()
        print()
    except FileNotFoundError:
        pass

    while runEdit: #Create a new line for you to write on in an infinite loop
        newLine()

    clearConsole()
    if not ogfn == "" and not None:
        while True: home()

#For editing primary settings, called by optionsMenu()
def editPrimarySettings(settings):
    allSettings = settings[0]
    primarySettings = settings[1]
    print("Settings may take a relaunch to update.")
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
        producesyntaxed("is set to ", BLUE2, False)
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
                producesyntaxed(f.read()+"\n", BLUE2, False)
        case "x":
            global runOptionsMenu
            runOptionsMenu = 0

def helpMenu():
    clearConsole()
    with open("HELP.md", "r") as f:
        producesyntaxed(f.read()+"\n", BLUE2, False)
    input("Enter to proceed back to main menu.")
    
def sysArgs():
    if len(sys.argv) >= 1:
        try: 
            sys.argv[2]
        except IndexError:
            try:
                return sys.argv[1]
            except IndexError:
                return ""

def home():
    print("Welcome to Stronge editor " + version)
    print("Available commands:\n(e)dit or create a file\n(o)ptions menu\n(h)elp\ne(x)it Stronge")
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
        case "h":
            helpMenu()
        case "x":
            log("Exiting Stronge...")
            try: extremelyAmazingPhonkProcess.terminate()
            except: pass
            sys.exit()
    clearConsole()


if __name__ == "__main__":
    log(f"Loaded main process in {time.time()-beginLoadTime} seconds")
    if "youtu" in musicYTlink:
        producesyntaxed("Song Process:\n", "\033[96m", False)
        extremelyAmazingPhonkProcess = multiprocessing.Process(target=play_song)
        extremelyAmazingPhonkProcess.start()
    elif "song" in musicYTlink:
        if not os.path.exists(os.path.join(os.getcwd(), "resources", "song.mp4")):
            audio_file = requests.get("https://dl.wilburwilliams.uk/api/raw/?path=/assets/stronge/song.mp4")
            with open(os.path.join(os.getcwd(), "resources", "song.mp4"), "wb") as f:
                f.write(audio_file.content)
        producesyntaxed("Song Process:\n", "\033[96m", False)
        extremelyAmazingPhonkProcess = multiprocessing.Process(target=play_song)
        extremelyAmazingPhonkProcess.start()

    time.sleep(1)
    clearConsole()
    ogfn = sysArgs()
    if ogfn != "":
        editFile(ogfn)
    else:
        while True: home() 
else:
    log(f"Loaded song process in {time.time()-beginLoadTime} seconds")
    producesyntaxed("Loaded Stronge!", '\033[38;5;120m', False)
