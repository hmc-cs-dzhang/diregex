import ply.yacc as yacc
import diregex_lexer
from diregex_ir import *
tokens = diregex_lexer.tokens

# Parses the grammar into the abstract syntax, represented in ir.py

########################### PARSERS ########################

def p_treePattern_dir(p):
    '''treePattern : dirItem '''
    p[0] = TreePattern_Dir(p[1])

def p_treePattern_dir_with_children(p):
    '''treePattern : dirItem SLASH treePattern'''
    p[0] = TreePattern_Child(p[1], p[3])

def p_treePattern_many(p):
    '''treePattern : LPAREN treePatternList RPAREN'''
    p[0] = TreePattern_List(p[2])

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
