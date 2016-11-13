import ply.lex as lex

tokens = ['SLASH',
          'EQUALS',
          'VAR',
          'REGEX',
          'LPAREN',
          'RPAREN',
          'GT',
          'COMMA']

#todo: make t_error
#create precedence
t_ignore = ' \t'
t_SLASH = r'\/'
t_EQUALS = r'='
t_GT = r'>'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_VAR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_REGEX = r'\"[a-zA-Z_][a-zA-Z0-9_\*]*\"'

lex.lex()

def lexer(st):
    lex.input(st)

    toks = []
    while True:
        tok = lex.token()
        if not tok:
            break

        toks += [tok]

    return [(token.type, token.value) for token in toks]


def test():


    lex.input("_=mydir//_/(bar1, bar2)")
    while True:
        tok = lex.token()
        if not tok: break
        print(tok)
