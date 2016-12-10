from lexemes import *
from ir import *
from parsec import *


'''
Parser for match trees.  Here is my current grammar for match trees:

<tree-pattern> : IDENT EQUALS <tree-pattern-without-var>
               | <tree-pattern-without-var>

<tree-pattern-without-var> : <dir-glob>                         # DirGlob
                           | <dir-glob> SLASH <tree-pattern>    # Child
                           | DOUBLE_STAR SLASH <tree-pattern>   # Descendant
                           | LPAREN <tree-pattern-list> RPAREN  # List
                           | LBRACE IDENT RBRACE                # Variable

<tree-pattern-list> : | <tree-pattern>
                      | <tree-pattern> COMMA <tree-pattern-list>

<dir-glob> : <attr> COLON GLOB

<attr> : FILE_TOK
       | DIR_TOK
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
    '''Parse a directory item, which is either a file or a directory'''
    dItem = yield dirFile ^ dirDir ^ dirGlob
    return dItem

@generate
def treePatternList():
    ''' parse a tree pattern'''
    pats = yield lparen >> sepBy(matchTreePattern, comma) << rparen
    return TreePatternList(pats)

@generate
def treePatternDir():
    ''' parse a trivial treePattern'''
    dName = yield dirItem
    return TreePatternDir(dName)

@generate
def treePatternChild():
    ''' parse a tree pattern with children '''
    parent = yield dirItem
    children = yield slash >> matchTreePattern
    return TreePatternChild(parent, children)

@generate
def treePatternDesc():
    ''' parse a tree pattern of the form **/ '''
    child = yield stars >> slash >> matchTreePattern
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
def matchTreePattern():
    ''' parse an arbitrary tree pattern '''
    tpat = yield tPatWithVar ^ tPatWithoutVar
    return tpat


