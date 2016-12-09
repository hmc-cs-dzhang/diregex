from sys import path
path.append(__file__ + '../ir')

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
    name = yield dirname
    return DirName(name)

@generate
def dirFile():
    ''' Parse a dirItem marked as a file '''
    file = yield file_tok >> colon >> dirName
    file.attr = 'file'
    return file

@generate
def dirDir():
    ''' Parse a dirItem marked as a directory '''
    directory = yield dir_tok >> colon >> dirName
    directory.attr = 'dir'
    return directory

@generate
def dirItem():
    '''Parse a directory name'''
    dItem = yield dirFile ^ dirDir ^ dirName
    return dItem

@generate
def treePatternList():
    ''' parse a tree pattern'''
    pats = yield lparen >> sepBy(destTreePattern, comma) << rparen
    return TreePatternList(pats)

@generate
def treePatternDirWithoutSlash():
    dName = yield dirItem
    dName.attr = 'file'
    return dName

@generate
def treePatternDirWithSlash():
    dName = yield treePatternDirWithoutSlash << slash
    #if dName.attr != 'file':
    dName.attr = 'dir'
    return dName


@generate
def treePatternDir():
    ''' parse a trivial treePattern'''
    dName = yield treePatternDirWithSlash ^ treePatternDirWithoutSlash
    return TreePatternDir(dName)

@generate
def treePatternChild():
    ''' parse a tree pattern with children '''
    parent = yield dirItem
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
    return tPat



