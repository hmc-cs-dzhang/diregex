import ply.lex as lex

tokens = ['SLASH',
          'EQUALS',
          'COMMA',
          'LPAREN',
          'RPAREN',
          'DOUBLE_STAR',
          'IDENT',
          'GLOB']

#todo: make t_error

t_ignore = ' \t'
t_SLASH = r'\/'
t_EQUALS = r'='
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOUBLE_STAR = r'\*\*'
t_IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*(?=(/|,|\s|$|\)))'
t_GLOB = r'([\w?\<\>\[\]\-\\.!]|\*(?!\*))+'

# Error handling rule from PLY manual
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

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


    lex.input("*=mydir/**/file/_a?[1-5]*=hi/yo=hi2")
    while True:
        tok = lex.token()
        if not tok: break
        print(tok)

def testtoken():
    import re
    m = re.search(t_IDENT, "yo=hi2")
    print(m)

