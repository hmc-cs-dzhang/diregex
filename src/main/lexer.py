import ply.lex as lex

tokens = ['SLASH',
          'DOUBLE_SLASH',
          'TILDE',
          'EQUALS',
          'AND',
          'OR',
          'VAR',
          'REGEX',
          'DOLLAR_SIGN',
          'LPAREN',
          'RPAREN']

#todo: make t_error
#create precedence
t_ignore = ' \t'
t_DOUBLE_SLASH = r'\/\/'
t_SLASH = r'\/'
t_TILDE = r'\~'
t_EQUALS = r'='
t_AND = r'\&+'
t_OR = r'\|+'
t_DOLLAR_SIGN = r'\$'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_VAR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_REGEX = r'\"[a-zA-Z_][a-zA-Z0-9_\*]*\"'

lex.lex()

def test():


    lex.input("_=mydir(//\"bar*\" & ~\"_\"=sib//\"springy\")")
    while True:
        tok = lex.token()
        if not tok: break
        print(tok)
