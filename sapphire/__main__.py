from sys import *

if version_info[:2] != (3, 6):
    exit('error: required python: 3.6.x')

from __parser__ import *
from subprocess import run, PIPE
from os.path import *

from argparse import ArgumentParser

def readfile(filename):
    f = None
    if filename == '-':
        f = stdin
    else:
        try: f = open(filename, 'r')
        except Exception as e: exit('error: %s' % e)

    try: data = f.read()
    except Exception as e: exit('error: %s' % e)

    f.close()
    return data

if __name__ == '__main__':

    argparser = ArgumentParser(description='Py-like to Brainfuck compiler.')
    argparser.add_argument('srcfile', metavar='file.sph', type=str, help=
            'Source file')
    argparser.add_argument('-o', metavar='output.b', type=str, help=
            'Output file')
    argparser.add_argument('-S', action='store_true', help='Output assembly')

    args = argparser.parse_args()

    path = dirname(__file__) + '/'
    code = readfile(args.srcfile)

    parser = Parser(path)
    parser.parse(code, args.srcfile)

    asm = parser.asm.code

    # print(asm)

    if args.o == None:
        args.o = 'output.b'

    output = asm

    if args.S:
        pass

    else:
        bf = run([path+'bfasm'], stdout=PIPE, input=asm, encoding='ascii')
        output = bf.stdout

    if args.o == '-':
        print(output, end='')

    else:
        f = open(args.o, 'w')
        f.write(output)
        f.close()

