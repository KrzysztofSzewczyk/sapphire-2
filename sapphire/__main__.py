from __parser__ import *
from sys import *
from subprocess import run, PIPE
from os.path import *

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

    path = dirname(__file__) + '/'
    code = readfile(argv[1])

    parser = Parser()
    parser.parse(code)

    asm = parser.asm.code

    # print(asm)
    bf = run([path+'bfasm'], stdout=PIPE, input=asm, encoding='ascii')

    f = open(argv[2], 'w')
    f.write(bf.stdout)
    f.close()

