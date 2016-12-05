from lexemes import *
from ir import *
from parsec import *


''' My current grammar for source trees (matches)

<assignment> : IDENT EQUALS <tree-pattern-without-var>

<tree-pattern> : IDENT EQUALS <tree-pattern-without-var>
               | <tree-pattern-without-var>

<tree-pattern-without-var> : <dir-name>                         # DirGlob
                           | <dir-name> SLASH <tree-pattern>    # Child
                           | DOUBLE_STAR SLASH <tree-pattern>   # Descendant
                           | LPAREN <tree-pattern-list> RPAREN  # List
                           | LBRACE IDENT RBRACE                # Variable

<tree-pattern-list> : | <tree-pattern>
                      | <tree-pattern> COMMA <tree-pattern-list>

<dir-name> : GLOB
'''


@generate
def dirGlob():
    '''Parse a directory name'''
    globname = yield glob
    return DirGlob(globname)

@generate
def dirFile():
    ''' Parse a dirItem marked as a file '''
    file = yield file_tok >> colon >> dirGlob
    file.attr = 'file'
    return file

@generate
def dirDir():
    ''' Parse a dirItem marked as a directory '''
    directory = yield dir_tok >> colon >> dirGlob
    directory.attr = 'dir'
    return directory

@generate
def dirItem():
    '''Parse a directory name'''
    dItem = yield dirFile ^ dirDir ^ dirGlob
    return dItem

@generate
def treePatternList():
    ''' parse a tree pattern'''
    pats = yield lparen >> sepBy(treePattern, comma) << rparen
    return TreePatternList(pats)

@generate
def treePatternDir():
    ''' parse a trivial treePattern'''
    dItem = yield dirItem
    return TreePatternDir(dItem)

@generate
def treePatternChild():
    ''' parse a tree pattern with children '''
    parent = yield dirItem
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
    tPat = yield tPatWithVar ^ tPatWithoutVar
    return tPat

@generate
def assignment():
    ''' parse an arbitrary tree pattern '''
    tpat = yield tPatWithVar
    return tpat


