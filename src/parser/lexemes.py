import re
from parsec import *

""" This file contains the many lexemes that are shared across the different parsers """

# Examples from the parsec python library sample
whitespace = regex(r'\s*', re.MULTILINE)
lexeme = lambda p: p << whitespace

# Characaters
lbrace     = lexeme(string('{'))
rbrace     = lexeme(string('}'))
lparen     = lexeme(string('('))
rparen     = lexeme(string(')'))
lbrack     = lexeme(string('['))
rbrack     = lexeme(string(']'))
equals     = lexeme(string('='))
slash      = lexeme(string('/'))
gt         = lexeme(string('>'))
lt         = lexeme(string('<'))
comma      = lexeme(string(','))
backslash  = lexeme(string('\\'))
stars      = lexeme(string('**'))
colon      = lexeme(string(':'))
bang       = lexeme(string('!'))
eol        = lexeme(string('\n'))
eof        = whitespace >> lexeme(regex(r'$'))

# Keywords
match_tok     = lexeme(string('match'))
dest_tok      = lexeme(string('dest'))
file_tok      = lexeme(string('file'))
dir_tok       = lexeme(string('dir'))
matchname_tok = lexeme(string('matchname'))

# Expressions for globs and identifiers
globExpr    = r'[A-Za-z0-9_\*\?\[\]\-\.\!]+'
identExpr   = r'[A-Za-z_][A-Za-z_0-9]*'
dirnameExpr = r'[A-Za-z0-9_\.]+'        # todo: currently a limited set of characters
                                        # add more options for dirnames, possibly
                                        # with excape characters

ident   = lexeme(regex(identExpr))
glob    = lexeme(regex('({0}|<{1}={0}>|<\\\\{1}>)+'.format(globExpr, identExpr)))
dirname = lexeme(regex(('({0}|<\\\\{1}>)+'.format(dirnameExpr, identExpr))))

