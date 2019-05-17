from sly import Lexer

class Lexer(Lexer):
    tokens = { ID, STRING, NUMBER, AS,
               IF, DEF, ELSE, WHILE,
               EQ, NE, LT, LE, GT, GE }
    ignore = ' \t'
    literals = '+-*/%=,()[]'

    STRING = r'".*?"'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # keywords
    ID['if'] = IF
    ID['as'] = AS
    ID['def'] = DEF
    ID['else'] = ELSE
    ID['while'] = WHILE

    EQ = r'=='
    NE = r'!='
    LT = r'<'
    LE = r'<='
    GT = r'>'
    GE = r'>='
    ignore_comment = r'\#.*'

    @_(r'0x[0-9a-fA-F]+', r'\d+')
    def NUMBER(self, t):
        if t.value.startswith('0x'):
            t.value = int(t.value[2:], 16)
        else:
            t.value = int(t.value)
        return t

def lex(line):
    tokens = []
    lexer = Lexer()
    for token in lexer.tokenize(line):
        tokens += [str(token.value)]
    return tokens
