## Intermediate Representation for Diregex
## Used this as guide:
##  https://ruslanspivak.com/lsbasi-part7/

import ply.yacc as yacc
import lexer
tokens = lexer.tokens

# abstact class for a node of the AST
class Node(object):
    pass

class TreePattern(Node):
    def __init__(self, item, relation=None):
        self.item = item
        self.relation = relation

    def __repr__(self):
        return "(TreePattern: " + item + " " + relation + ")"

class Expression(Node):
    pass

class BinaryExpression(Expression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class LeafExpression(Expression):
    def __init__(self, relation):
        self.relation = relation

class Relation(Expression):
    def __init__(self, op, treePattern):
        self.op = op
        self.treePattern = treePattern

    def __repr__(self):
        return "(Relation: " + op + " " + treePattern + ")"

class DirItem(Node):
    def __init__(self, regex, var=None):
        self.regex = regex
        self.var = var

############################ PARSERS ########################

def p_treePattern(p):
    '''treePattern : dirItem expression
                   | dirItem '''
    if len(p) == 3:
        p[0] = TreePattern(p[1], p[2])
    else:
        p[0] = TreePattern(p[1])

def p_expression_binary(p):
    '''expression : LPAREN expression binop expression RPAREN'''
    p[0] = BinaryExpression(p[3], p[2], p[4])

def p_expression_leaf(p):
    '''expression : relation'''
    p[0] = LeafExpression(p[1])

def p_relation(p):
    '''relation : SLASH treePattern
                | DOUBLE_SLASH treePattern
                | TILDE treePattern'''
    p[0] = Relation(p[1], p[2])

def p_dirItem(p):
    '''dirItem : REGEX EQUALS VAR
               | REGEX'''
    if len(p) == 4:
        p[0] = DirItem(p[1], p[3])
    else:
        p[0] = DirItem(p[1])

def p_binop(p):
    ''' binop : AND
              | OR'''
    p[0] = p[1]

yacc.yacc()
print(yacc.parse("\"abc*d\" = myvar"))
