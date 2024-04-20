import sys

#This doesn't really need to be part of the ESDExt so it's here now
def producesyntaxed(text, color, useSpace=True):
    try:
        if useSpace:
            sys.stdout.write(color + text + '\033[0m' + ' ')
        else:
            sys.stdout.write(color + text + '\033[0m')
    except:
        print(text)