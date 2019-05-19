from __lexer__ import *
from sys import *

class CodeGen:
    
    def __init__(self):
        self.code = ''
        self.lbli = 1

    def __call__(self, *a):
        self.code += '  ' + a[0] + ' ' + (', '.
        join([str(e) for e in a[1:]])) + '\n'
    
    def label(self, i = None):
        if i == True:
            pass
        elif i == None:
            self.code += 'lbl %d\n' % self.lbli
        else:
            self.code += 'lbl %d\n' % i
            return
        self.lbli += 1
        return self.lbli - 1

class Parser:

    def __init__(self, path):

        # create codegen
        self.asm = CodeGen()
        self.asm('stk 32')
        self.asm('org 0')

        # init memory
        self.meminit()

        # set compiler path
        self.path = path

    def compile(self, expr):
        try:
           co = compile(expr, self.lnerr, 'eval')
        except SyntaxError as e:
           print(e.text)
           print((e.offset - 1) * ' ' + '^')
           exit('error: %s (%s)' % (e.msg.replace(
                'EOF', 'EOL'), self.lnerr))
        except Exception as e:
           exit('error: %s (%s)' % (e, self.lnerr))

        return co

    def get_cocode(self, co):
        return list(zip(*[iter(list(co.co_code))] * 2))

    def function(self, expr):
        co = self.compile(expr)
        cocode = self.get_cocode(co)
        
        try:
            if (cocode[-1] != (83, 0) or
                cocode[0][0] != 101 or
                cocode[-2][0] != 131):
                exit('error: invalid function (line %d)' % self.ln_no)
        except:
            exit('error: invalid function (line %d)' % self.ln_no)
        
        cocode = cocode[1:-2]
        argi = 0

        for c1, c2 in cocode:

            if c1 != 101:
                exit('error: invalid function (line %d)' % self.ln_no)

            name = co.co_names[c2]
            addr = self.addr(name)
            argi += 1

            self.asm.code += '\n'
            self.asm('; <= ' + name + ' =>')
            self.asm('mov', 'r4', addr)
            self.asm('sto', 'r4', 'r' + str(argi))

    def expr(self, expr, var_address=None):
        co = self.compile(expr)
        cocode = self.get_cocode(co)

        def op(instr):
            self.asm('pop', 'r2')
            self.asm('pop', 'r1')
            self.asm(instr, 'r1', 'r2')
            self.asm('psh', 'r1')
        
        def build_array(c2):
            self.memi += c2
            self.asm('mov', 'r4', c2)
            self.asm('mov', 'r1', self.memi)
            lbl = self.asm.label()
            
            self.asm('dec', 'r1')
            self.asm('pop', 'r2')
            self.asm('sto', 'r1', 'r2')
            self.asm('dec', 'r4')
            
            self.asm('jnz', 'r4', lbl)
            self.asm('psh', self.memi - c2)
        
        for i, c in enumerate(cocode):
            c1, c2 = c
            
            # subscr
            if c1 == 25:
                name = co.co_names[cocode[i - 2][1]]
                addr = self.addr(name)
                self.asm('pop', 'r1')
                self.asm('pop', 'r2')
                self.asm('add', 'r2', 'r1')
                self.asm('rcl', 'r1', 'r2')
                self.asm('psh', 'r1')

            # call function
            elif c1 == 131:
                
                # args
                for i in range(c2):
                    self.asm('pop', 'r' + str(c2 - i))
                
                # call
                back = self.asm.label(i = True)
                # function address
                self.asm('pop', 'r4')
                # push back address
                self.asm('psh', back)
                # jump to function
                self.asm('jmp', 'r4')
                # back label
                self.asm('lbl', back)
                # push returned value
                self.asm('psh', 'r1')

            # build array
            elif c1 == 103:
                build_array(c2)

            # load const
            elif c1 == 100:
                c = co.co_consts[c2]
                
                if isinstance(c, float):
                    c = int(c)
            
                if c == None:
                    self.asm('psh', 0)
                elif isinstance(c, int):
                    self.asm('psh', c)
                elif isinstance(c, tuple):
                    for x in c:
                        self.asm('psh', x)
                    build_array(len(c))
                elif isinstance(c, str):
                    self.asm('org', self.memi)
                    self.asm.code += 'txt "'
                    string = True
                    for x in c:
                        x = ord(x)
                        if x >= 32 and chr(x) != '"':
                            if string == False:
                                string = True
                                self.asm.code += 'txt "'
                            self.asm.code += chr(x)
                        else:
                            string = False
                            self.asm.code += '"\ndb_ %d\n' % x
                    if string:
                        self.asm.code += '"\n'
                    self.asm('db_', 0)
                    self.asm('psh', self.memi)
                    self.memi += c2 + 1
                else:
                    exit('error: invalid const %s at `%s` (line %d)' % (
                        str(bytes(str(c).encode()))
                        [1:], expr, self.ln_no))

            # load variable
            elif c1 == 101:
                self.asm('rcl', 'r1', self.addr(co.co_names[c2]))
                self.asm('psh', 'r1')
            
            # assign
            elif c1 == 83:
                if var_address != None:
                    self.asm('pop', 'r1')
                    self.asm('mov', 'r2', var_address)
                    self.asm('sto', 'r2', 'r1')

            elif c1 == 0x17 or c1 == 0x37: op('add')
            elif c1 == 0x18 or c1 == 0x38: op('sub')
            elif c1 == 0x14 or c1 == 0x39: op('mul')
            elif c1 == 0x15 or c1 == 0x1b or c1 == 0x3a: op('div')

            # compare op
            elif c1 == 107:

                cops = {
                    '<':  0,
                    '<=': 1,
                    '==': 2,
                    '!=': 3,
                    '>':  4,
                    '>=': 5,
                }

                if c2 == cops['==']:   op('eq_')
                elif c2 == cops['!=']: op('ne_')
                elif c2 == cops['<=']: op('le_')
                elif c2 == cops['>=']: op('ge_')
                elif c2 == cops['<']:  op('lt_')
                elif c2 == cops['>']:  op('gt_')
                else:
                    exit('error: unknown operator %d at `%s` (line %d)' % (
                        c2, expr, self.ln_no))
            
            # invalid expression
            else:
                exit('error: invalid expression `%s` (line %d)' % (
                    expr, self.ln_no))

    def meminit(self):
        # key: varname, value: address
        self.mem = {}
        # to determine address
        self.memi = 0
        # to determine the existence of var
        self.variables = []

    def addr(self, name, glbl = False):
        
        # local variable
        if not glbl:
            
            # function name + variable name
            f = self.func
            f = '' if f == None else f
            f = f + '.' + name
        
        # global variable
        else:
            f = '.' + name
        
        # create if variable doesn't exist
        if f not in self.variables:
            self.variables += [f]
            self.mem[f] = self.memi
            self.memi += 1

        # return address of variable
        return self.mem[f]

    def get_indent(self, line):
        # remove spaces from right ' a ' -> ' a'
        rline = line.rstrip()
        # return rline with removed stripped line
        return rline.replace(line.strip(), '')

    def close(self, tc):
        # print(self.lnerr, tc)
                    
        self.asm.code += '\n'
        self.asm('; end')

        if tc[0] == 'else': self.asm('lbl', tc[2])
        if tc[0] == 'if': self.asm('lbl', tc[2])

        if tc[0] == 'while':
            self.asm('jmp', tc[3])
            self.asm('lbl', tc[2])

        # def, indent, skip, addr, flbl
        if tc[0] == 'def':
            self.func = None
            self.asm('ret')
            self.asm('lbl', tc[2])
            self.asm('mov', 'r1', tc[3])
            self.asm('sto', 'r1', tc[4])
       
    def parse(self, code):
        
        # global
        self.func = None

        # (stmt, indent, ...)
        self.to_close = []

        # count lines of code
        line_count = code.count('\n')

        for i, line in enumerate((code + '\n\n').splitlines()):
            
            self.ln_no = i + 1
            tokens = lex(line, self.ln_no)
            lnerr = 'line %d' % self.ln_no
            self.lnerr = lnerr
            self.line = line
            
            kw = [
                'def',
                'if',
                'while',
                'global',
                'as',
            ]

            if len(tokens) == 1 and tokens[0] in kw:
                print(line)
                print((len(line) - 1) * ' ' + '^')
                exit('error: invalid syntax')

            if len(tokens) > 1 and tokens[0] == 'else':
                print(line)
                print((len(line) - 1) * ' ' + '^')
                exit('error: invalid syntax')
                
                
            if (len(tokens) != 0 and
                line.strip() != '' and
                tokens[0] == 'else'):

                for i, tc in enumerate(reversed(self.to_close)):
                
                    if tc[0] == 'if':
                        break
                
                    if tc[1] == self.get_indent(line):
                        for j in range(i + 1):
                            self.close(self.to_close.pop())

                self.asm.code += '\n'
                self.asm('; else')
                
                sklb = self.asm.label(i = True)
                
                self.asm('jmp', sklb)
                self.asm('lbl', tc[2])

                self.to_close += [('else', self.get_indent(line), sklb)]
                continue

            if line.strip() != '' or line_count == i:
                for i, tc in enumerate(reversed(self.to_close)):
                
                    if tc[1] == self.get_indent(line):
                        for j in range(i + 1):
                            self.close(self.to_close.pop())

            if line.strip() == '' or len(tokens) == 0:
                continue

            self.asm.code += '\n'
            self.asm('; ' + line.strip())

            # inline asm
            if tokens[0] == 'as':
                
                if tokens[1][0] != '"' or tokens[1][-1] != '"':
                    exit('error: expected string after `as` (%s)' % lnerr)

                self.asm(eval(tokens[1]))
            
            # global
            elif tokens[0] == 'global':
                
                if self.func == None:
                    exit('error: invalid use of global out of function (%s)'
                            % lnerr)

                for v in ''.join(tokens[1:]).split(','):
                    a = self.addr(v, glbl = True)
                    n = self.func + '.' + v
                    self.mem[n] = a
                    self.variables += [n]
                    
            # import
            elif tokens[0] == 'import':
                fn = ''.join(tokens[1]).replace('.', '/') + '.sph'
                try:
                    f = open(fn, 'r')
                except:
                    try:
                        f = open(self.path + '../libsapphire2/' + fn, 'r')
                    except:
                        exit('error: module `%s` not found (%s)' % (
                            fn, lnerr))

                module_code = f.read()
                f.close()

                self.parse(module_code)

            # function
            elif tokens[0] == 'def':

                skip = self.asm.label(i = True)
                flbl = self.asm.label(i = True)
                addr = self.addr(tokens[1])
               
                self.asm('jmp', skip)
                self.asm('lbl', flbl)

                self.func = tokens[1]
                self.function(' '.join(tokens[1:]))

                self.to_close += [('def', self.get_indent(line),
                    skip, addr, flbl)]
            
            # if statement
            elif tokens[0] == 'if':
                
                cond = ' '.join(tokens[1:])
                self.expr(cond)
                sklb = self.asm.label(i = True)
                
                self.asm('pop', 'r1')
                self.asm('jz_', 'r1', sklb)
                
                self.to_close += [('if', self.get_indent(line), sklb)]
            
            # while statement
            elif tokens[0] == 'while':
                
                sklb = self.asm.label(i = True)
                back = self.asm.label(i = True)
                
                cond = ' '.join(tokens[1:])
                self.asm('lbl', back)
                self.expr(cond)
                
                self.asm('pop', 'r1')
                self.asm('jz_', 'r1', sklb)
                
                self.to_close += [('while', self.get_indent(line),
                    sklb, back)]

            # var assign
            elif len(tokens) > 1 and tokens[1] == '=':
                
                name = tokens[0]
                addr = self.addr(name)
                expr = ' '.join(tokens[2:])
                self.expr(expr, var_address=addr)

            # expr
            else:

                self.expr(' '.join(tokens))
                self.asm('pop', 'r1')

