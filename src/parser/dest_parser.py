from lexemes import *
from ir import *
from parsec import *


''' My current grammar for source trees (matches)

<tree-pattern> : <tree-pattern-without-var>

<tree-pattern-without-var> : <dir-name>                         # DirName
                           | <dir-name> SLASH <tree-pattern>    # Child
                           | LPAREN <tree-pattern-list> RPAREN  # List
                           | LBRACE IDENT RBRACE                # Variable

<tree-pattern-list> : | <tree-pattern>
                      | <tree-pattern> COMMA <tree-pattern-list>

<dir-name> : DIRNAME
'''


@generate
def dirName():
    '''Parse a directory name'''
    globname = yield dirname
    return DirName(globname)

@generate
def treePatternList():
    ''' parse a tree pattern'''
    pats = yield lparen >> sepBy(destTreePattern, comma) << rparen
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
    children = yield slash >> destTreePattern
    return TreePatternChild(parent, children)

@generate
def treePatternVar():
    ''' parse a variable of the form {var} '''
    var = yield lbrace >> ident << rbrace
    return TreePatternVar(var)

@generate
def destTreePattern():
    tPat = yield treePatternChild \
           ^ treePatternList \
           ^ treePatternDir \
           ^ treePatternVar
    print("parsing dest tree")
    return tPat



