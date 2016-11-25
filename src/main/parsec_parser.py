import re
from diregex_ir import *
from parsec import *

''' My current grammar (subject to change)
<program> : <tree-pattern>

<tree-pattern> : <dir-name>
               | <dir-name> SLASH <tree-pattern>
               | DOUBLE_STAR SLASH <tree-pattern>
               | LPAREN <tree-pattern-list> RPAREN

<tree-pattern-list> : | <tree-pattern>
                      | <tree-pattern> COMMA <tree-pattern-list>

<dir-name> : GLOB
           | IDENT
           | GLOB EQUALS IDENT
           | LBRACE IDENT RBRACE
'''

whitespace = regex(r'\s*', re.MULTILINE)

lexeme = lambda p: p << whitespace

lbrace = lexeme(string('{'))
rbrace = lexeme(string('}'))
lparen = lexeme(string('('))
rparen = lexeme(string(')'))
equals = lexeme(string('='))
slash = lexeme(string('/'))
gt = lexeme(string('>'))
lt = lexeme(string('<'))
comma = lexeme(string(','))
ident = lexeme(regex(r'[A-Za-z_][A-Za-z_0-9]*'))
glob = lexeme(regex(r'[A-Za-z0-9_\*\?\[\]\-]+'))
stars = lexeme(string('**'))
identchars = r'A-Za-z_0-9'

@generate
def dirGlob():
    '''Parse a directory name'''
    globname = yield glob
    return DirName(globname)

@generate
def dirGlobWithVar():
    '''Parse a named directory'''
    globname = yield glob
    varname = yield equals >> ident
    return DirName(globname, varname)

@generate
def dirName():
    '''Parse any directory'''
    dName = yield dirGlobWithVar ^ dirGlob
    return dName

@generate
def treePatternList():
    ''' parse a tree pattern'''
    pats = yield lparen >> sepBy(treePattern, comma) << rparen
    return TreePatternList(pats)

@generate
def treePatternDir():
    ''' parse a trivial treePattern'''
    dName = yield dirName
    return TreePatternDir(dName)

@generate
def treePatternChild():
    ''' parse a tree pattern with children '''
    parent = yield dirName
    children = yield slash >> treePattern
    return TreePatternChild(parent, children)

@generate
def treePatternDescendant():
    ''' parse a tree pattern of the form ** '''
    child = yield stars >> slash >> treePattern
    return TreePatternDescendant(child)

@generate
def treePattern():
    ''' parse an arbitrary tree pattern '''
    tpat = yield treePatternDescendant \
                ^ treePatternChild \
                ^ treePatternList \
                ^ treePatternDir
    return tpat

parser = whitespace >> treePattern
'''
result = parser.parse('a=hello/(y*abc=goodbye, list)')
print(type(parser))
print(result)
'''
def parse(st):
    return parser.parse(st)


print(parse('(sib1, sib2)'))
