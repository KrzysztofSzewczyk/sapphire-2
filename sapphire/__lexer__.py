from sly import Lexer

class Lexer(Lexer):
    tokens = { ID, STRING, NUMBER, AS,
               IF, DEF, ELSE, WHILE,
               EQ, NE, LE, GE, LT, GT,
               COMMENT, GLOBAL, IMPORT,
               RAISE }
    ignore = ' \t'
    literals = '+-*/%=,()[]'

    STRING = r'"(?:[^"\\]|\\.)*"'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # keywords
    ID['if'] = IF
    ID['as'] = AS
    ID['def'] = DEF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['global'] = GLOBAL
    ID['import'] = IMPORT
    ID['raise'] = RAISE

    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='
    LT = r'<'
    GT = r'>'
    COMMENT = r'\#.*'

    NUMBER = r'(0x[0-9a-fA-F]+)|(\d+)'

def lex(line, ln_no):
    try:
        tokens = []
        lexer = Lexer()
        lt = None

        for i, token in enumerate(lexer.tokenize(line)):
            token.value = str(token.value)
            
            if i == 0:
                if token.value == 'global': lt = 'global'
                if token.value == 'import': lt = 'import'

            else:
                if lt == 'global':
                    if i % 2 == 1 and token.type != 'ID':
                        exit('error: expected identifier at token' + 
                                ' %d (line %d)' % (i + 1, ln_no))
                    if i % 2 == 0 and token.value != ',':
                        exit('error: expected `,` at token' + 
                                ' %d (line %d)' % (i + 1, ln_no))
                
                elif lt == 'import':
                    if i % 2 == 1 and token.type != 'ID':
                        exit('error: expected identifier at token' + 
                                ' %d (line %d)' % (i + 1, ln_no))
                    if i % 2 == 0 and token.value != '.':
                        exit('error: expected `.` at token' + 
                                ' %d (line %d)' % (i + 1, ln_no))

            if not token.value.startswith('#'):
                tokens += [token.value]
        return tokens
    except Exception as e:
        exit('error: %s (line %d)' % (e, ln_no))

