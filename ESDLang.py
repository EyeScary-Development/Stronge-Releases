#Imports
import random
from typing import (List, Any)
import time

#Create lists to store information about the variables and functions
vars={}
functions={}

#Random number
def radno(input_list: List[Any]):
    return random.randint(int(input_list[1]),int(input_list[2]))

#maths operations
def mathsops(input_list: List[Any]):
    val1=float(vars[input_list[0]]) if input_list[0] in vars else float(input_list[0])
    cond=input_list[1]
    val2=float(vars[input_list[2]] if input_list[2] in vars else input_list[2])
    match cond:
        case "+":
            return val1+val2
        case "-":
            return val1-val2
        case "/":
            return val1/val2
        case "*":
            return val1*val2
        case _:
            return ValueError

#Input handler
def ins(string: str):
    if string.endswith(" "):
        return input(string[6:])
    else:
        return input(string[6:]+" ")

#If a string converts to float
def canfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

#Handles variables
def variablehandling(input_list: List[Any]):
    global vars
    input_list.pop(0)
    varname=input_list[0]
    input_list.pop(0)
    varval=input_list[0]
    varvalstring=' '.join(input_list)
    if varname in vars:
        if varval.startswith("-"):
            tosub=float(vars[varname])
            vars[varname]=tosub+float(varval)
        elif varval.startswith("+"):
            toadd=float(vars[varname])
            vars[varname]=toadd+float(varval)
        else:
            if varvalstring.startswith("input"):
                vars[varname]=ins(varvalstring)
            elif varvalstring.startswith("radnom"):
                vars[varname]=float(radno(varvalstring.split()))
            elif len(varvalstring)>1:
                vars[varname]=varvalstring
            else:
                if canfloat(varval):
                    vars[varname]=float(varval)
                else:
                    vars[varname]=varval
    else:
        if len(varvalstring.split())==1:
            if canfloat(varval):
                vars[varname]=float(varval)
            else:
                vars[varname]=varval
        else:
            if input_list[1] in ["*","/","+","-"] and len(input_list)==3:
                vars[varname]=float(mathsops(input_list))

            elif len(varvalstring.split())>1:
                if varvalstring.startswith("input"):
                    vars[varname]=ins(varvalstring)
                elif varvalstring.startswith("radnom"):
                    vars[varname]=float(radno(varvalstring.split()))
                else:
                    vars[varname]=varvalstring



#Print function
def printah(input_list: List[Any]):
    input_list.remove("write")
    for part in input_list:
        if part in vars:
            print(vars[part], end=" ")
        else:
            print(part, end=" ")
    print()

#Checks if conditions return true or false
def condcheck(input_list: List[Any]):
  if len(input_list) != 3:
      print("a conditioned statement requires 3 arguments, ", len(input_list), "are given")
  else:
    val1=float(input_list[0]) if canfloat(input_list[0]) else input_list[0]
    val2=float(input_list[2].strip("\n")) if canfloat(input_list[2]) else input_list[2].strip("\n")
    cond=input_list[1]
    if val1 in vars:
        val1=vars[val1]
    if val2 in vars:
        val2=vars[val2.strip("\n")]
    match cond:
      case">=":
        if val1 >= val2:
            return True
        else:
            return False
      case"<=":
        if val1 <= val2:
            return True
        else:
            return False
      case"=":
        if val1 == val2:
            return True
        else:
            return False
      case"x":
        if val1 != val2:
            return True
        else:
            return False
      case">":
        if val1 > val2:
            return True
        else:
            return False
      case"<":
        if val1 < val2:
            return True
        else:
            return False
      case _:
        print("error: condition to judge if statement on is not properly defined")

#interprets a line from a file and dispatches the appropriate data from that line to the appropriate functions
def interpret(file, cond=...):
            userInput = file.readline()
            if userInput.startswith("var"):
                variablehandling(userInput.strip("\n").split())
            elif userInput.startswith("function"):
                if userInput not in functions:
                    functionlogger(file, userInput.strip("\n").split(), userInput)
                else:
                    print("Error, 2 functions with same name")
            elif userInput == "quit\n":
                return True
            elif userInput.startswith("write"):
                printah(userInput.strip("/n").split())
            elif userInput.startswith("if"):
                ifchecker(userInput.strip("/n").split(), file)
            elif userInput.startswith("else"):
                ln=...
                while ln != "endstat\n":
                    ln=file.readline()
            elif userInput == "endwhile\n":
                file.seek(0)
                ln=...
                while ln != cond:
                    ln=file.readline()
            elif userInput.startswith("while"):
                whilechecker(userInput.strip("\n").split(), file)
            elif len(userInput.strip("\n").split()) == 3 and userInput.strip("\n").split()[1] in ["*","/","+","-"]:
                print(mathsops(userInput.split()))
            elif userInput.split()[0] in functions:
                functioncalled(file, userInput, userInput.strip("\n").split())
            elif userInput.startswith("endfunction"):
                return True

#Handles if statements
def ifchecker(input_list: List[Any], file):
    input_list.remove("if")
    cond=condcheck(input_list)
    if cond != True:
        ln=...
        while ln != "else\n":
            ln=file.readline()

#handles while statements
def whilechecker(input_list: List[Any], file):
    input_list.remove("while")
    condition="while "+' '.join(input_list)+'\n'
    while condcheck(input_list):
        if interpret(file, condition):
            break
    ln = ...
    while ln != "endwhile\n":
        ln=file.readline()

#stores functions and their starting line
def functionlogger(file, input_list: List[Any], line):
    input_list.remove("function")
    functions[input_list[0]]=line
    ln=...
    while ln != "endfunction "+input_list[0]+"\n":
        ln=file.readline()

#when a function is called, this function finds the function in the code, executes it and then returns to the line after it was called
def functioncalled(file, line, input_list: List[Any]):
    file.seek(0)
    currentline=...
    while currentline != functions[input_list[0]]:
        currentline=file.readline()
    end="endfunction "+input_list[0]
    while True:
        if interpret(file):
            break
    file.seek(0)
    ln=...
    while ln != line:
        ln=file.readline()

#Main function
def main(fileName="trun.esdla"):
    print("ESDLang 7 ...")
    time.sleep(0.5)
    with open(fileName, 'r') as file:
        while True:
            if interpret(file):
                break
if __name__ == "__main__": #Make sure to use this so it doesn't run main() when imported
    main()
