from sly import Lexer

class Lexer(Lexer):
    tokens = { ID, STRING, NUMBER, AS,
               IF, DEF, ELSE, WHILE,
               EQ, NE, LE, GE, LT, GT,
               COMMENT }
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
    LE = r'<='
    GE = r'>='
    LT = r'<'
    GT = r'>'
    COMMENT = r'\#.*'

    @_(r'0x[0-9a-fA-F]+', r'\d+')
    def NUMBER(self, t):
        if t.value.startswith('0x'):
            t.value = int(t.value[2:], 16)
        else:
            t.value = int(t.value)
        return t

def lex(line, ln_no):
    try:
        tokens = []
        lexer = Lexer()
        for token in lexer.tokenize(line):
            token.value = str(token.value)
            if not token.value.startswith('#'):
                tokens += [token.value]
        return tokens
    except Exception as e:
        exit('error: %s (line %d)' % (e, ln_no))
