import ply.yacc as yacc
import diregex_lexer
from diregex_ir import *
tokens = diregex_lexer.tokens

# Parses the grammar into the abstract syntax, represented in ir.py

########################### PARSERS ########################

def p_treePatternDir(p):
    '''treePattern : dirItem '''
    p[0] = TreePatternDir(p[1])

def p_treePatternDirWithChildren(p):
    '''treePattern : dirItem SLASH treePattern'''
    p[0] = TreePatternChild(p[1], p[3])

def p_treePatternDescendant(p):
    '''treePattern : GT treePattern'''
    p[0] = TreePatternDescendant(p[2])

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

def p_dirItem(p):
    '''dirItem : dirName
               | GT dirName'''
    if len(p) == 2:
        p[0] = DirItem(p[1])
    else:
        p[0] = DirItem(p[2], p[1])

def p_dirName(p):
    '''dirName : REGEX
               | REGEX EQUALS VAR'''
    if len(p) == 2:
        p[0] = DirName(p[1].strip("\""))
    else:
        p[0] = DirName(p[1].strip("\""), p[3])

def p_error(p):
    print("cannot parse " + repr(p))

parser = yacc.yacc()

def parse(st):
    return parser.parse(st)
