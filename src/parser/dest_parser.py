from lexemes import *
from ir import *
from parsec import *

""" parses a destination tree.  Similar to a match tree with a couple notable exceptions:
    1) Uses DirNames instead of DirGlobs, since you shouldn't specify a
      destination with a glob
    2) foo/ specifies a directory, foo is a folder.  In the other parser,
      you need the attributes dir: and file:, otherwise its ambiguous
    3) The descendant pattern **/ is invalid

"""

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



