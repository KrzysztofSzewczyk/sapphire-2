from __lexer__ import *
from sys import *

def readfile(filename):
    try: f = open(filename, 'r')
    except Exception as e: exit('error: %s' % e)
    
    try: data = f.read()
    except Exception as e: exit('error: %s' % e)
    
    f.close()
    return data

if __name__ == '__main__':
    if len(argv) < 3:
        exit('usage: python sapphire <file.sph> <file.b>')

    code = readfile(argv[1])

    for i, line in enumerate(code.splitlines()):
        tokens = lex(line)

        for token in tokens:
            print(str(i + 1) + ':', token)

        print()
