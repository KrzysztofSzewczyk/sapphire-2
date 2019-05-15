from sly import Lexer

class Lexer(Lexer):
    tokens = { STRING, ID, NUMBER,
               IF, DEF, ELSE, WHILE }
    ignore = ' \t'
    literals = '+-*/%=,()[]'

    STRING = r'".*?"'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # keywords
    ID['if'] = IF
    ID['def'] = DEF
    ID['else'] = ELSE
    ID['while'] = WHILE

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
        tokens += [token.value]
    return tokens
