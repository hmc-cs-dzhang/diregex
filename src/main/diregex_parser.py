import ply.yacc as yacc
import diregex_lexer
from diregex_ir import *
tokens = diregex_lexer.tokens



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
'''


# Parses the grammar into the abstract syntax, represented in ir.py

########################### PARSERS ########################

def p_treePatternDir(p):
    '''treePattern : dirName '''
    p[0] = TreePatternDir(p[1])

def p_treePatternDirWithChildren(p):
    '''treePattern : dirName SLASH treePattern'''
    p[0] = TreePatternChild(p[1], p[3])

def p_treePatternDescendant(p):
    '''treePattern : DOUBLE_STAR SLASH treePattern'''
    p[0] = TreePatternDescendant(p[3])

def p_treePatternMany(p):
    '''treePattern : LPAREN treePatternList RPAREN'''
    p[0] = TreePatternList(p[2])

def p_treePatternList(p):
    '''treePatternList : treePattern
                       | treePattern COMMA treePatternList'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_dirName(p):
    '''dirName : GLOB
               | IDENT
               | GLOB EQUALS IDENT'''
    if len(p) == 2:
        p[0] = DirName(p[1])
    else:
        p[0] = DirName(p[1], p[3])

def p_error(p):
    print("cannot parse " + repr(p))

parser = yacc.yacc()

def parse(st):
    return parser.parse(st)
