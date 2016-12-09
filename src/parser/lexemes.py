import re
from parsec import *

whitespace = regex(r'\s*', re.MULTILINE)

lexeme = lambda p: p << whitespace
keyword = lambda p: p < none_of(r'\s+')

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

# todo: should be keywords: shouldn't parse something like 'matchhi'
match_tok    = lexeme(string('match'))
dest_tok     = lexeme(string('dest'))
file_tok     = lexeme(string('file'))
dir_tok      = lexeme(string('dir'))
matchpat_tok = lexeme(string('matchpat'))

globExpr    = r'[A-Za-z0-9_\*\?\[\]\-\.\!]+'
identExpr   = r'[A-Za-z_][A-Za-z_0-9]*'       # same as Python's identifiers
dirnameExpr = r'[A-Za-z0-9_\.]+'       # todo: expand to allow more dirnames

ident   = lexeme(regex(identExpr))
glob    = lexeme(regex('({0}|<{1}={0}>|<\\\\{1}>)+'.format(globExpr, identExpr)))
dirname = lexeme(regex(('({0}|<\\\\{1}>)+'.format(dirnameExpr, identExpr))))

