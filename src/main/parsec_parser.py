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

lbrace  = lexeme(string('{'))
rbrace  = lexeme(string('}'))
lparen  = lexeme(string('('))
rparen  = lexeme(string(')'))
equals  = lexeme(string('='))
slash   = lexeme(string('/'))
gt      = lexeme(string('>'))
lt      = lexeme(string('<'))
comma   = lexeme(string(','))
stars   = lexeme(string('**'))
eof     = lexeme(regex(r'$'))

globexpr  = r'[A-Za-z0-9_\*\?\[\]\-\.]+'
identexpr = r'[A-Za-z_][A-Za-z_0-9]+'

ident  = lexeme(regex(identexpr))
glob   = lexeme(regex("({0}|<{1}={0}>|<\\\\{1}>)+".format(globexpr, identexpr)))

@generate
def dirGlob():
    '''Parse a directory name'''
    globname = yield glob
    return DirGlob(globname)

@generate
def dirGlobWithVar():
    '''Parse a named directory'''
    globname = yield ident
    varname  = yield equals >> glob
    return DirGlobWithVar(globname, varname)

@generate
def dirName():
    '''Parse any directory'''
    dName = yield dirGlobWithVar ^ dirGlob
    return dName

@generate
def treePatternList():
    ''' parse a tree pattern'''
    #var = yield ident << equals
    pats = yield lparen >> sepBy(treePattern, comma) << rparen
    return TreePatternList(pats)

@generate
def treePatternDir():
    ''' parse a trivial treePattern'''
    #var = yield ident << equals
    dName = yield dirName
    return TreePatternDir(dName)

@generate
def treePatternChild():
    ''' parse a tree pattern with children '''
    parent = yield dirName
    children = yield slash >> treePattern
    return TreePatternChild(parent, children)

@generate
def treePatternDesc():
    ''' parse a tree pattern of the form **/ '''
    child = yield stars >> slash >> treePattern
    return TreePatternDesc(child)

@generate
def treePatternVar():
    ''' parse a variable of the form {var} '''
    var = yield lbrace >> ident << rbrace
    return TreePatternVar(var)

@generate
def tPatWithoutVar():
    tPat = yield treePatternDesc \
           ^ treePatternChild \
           ^ treePatternList \
           ^ treePatternDir \
           ^ treePatternVar
    return tPat

@generate
def tPatWithVar():
    var  = yield ident << equals
    tPat = yield tPatWithoutVar

    tPat.var = var
    return tPat

@generate
def treePattern():
    ''' parse an arbitrary tree pattern '''
    tpat = yield tPatWithVar ^ tPatWithoutVar
    return tpat

program = whitespace >> treePattern << eof

def parse(st):
    return program.parse(st)
