import sys

def producesyntaxed(text: str, color, useSpace=True):
    try:
        if useSpace:
            sys.stdout.write(color + text + ' ' + '\033[0m')
        else:
            sys.stdout.write(color + text + '\033[0m')
    except:
        print(text)