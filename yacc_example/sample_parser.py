import sys
sys.path.insert(0, "../..")

import ply.yacc as yacc
import sample_lexer # Import lexer information
tokens = sample_lexer.tokens # Need token list

if sys.version_info[0] >= 3:
    raw_input = input

def p_assign(p):
 '''assign : NAME EQUALS expr'''
 p[0] = ('ASSIGN',p[1],p[3])
def p_expr_plus(p):
 '''expr : expr PLUS term'''
 p[0] = ('+',p[1],p[3])
def p_term_mul(p):
 '''term : term TIMES factor'''
 p[0] = ('*',p[1],p[3])
def p_term_factor(p):
 '''term : factor'''
 p[0] = p[1]
def p_factor(p):
 '''factor : NUMBER'''
 p[0] = ('NUM',p[1])
yacc.yacc()


yacc.parse("x = 3 + 4 - 2")
