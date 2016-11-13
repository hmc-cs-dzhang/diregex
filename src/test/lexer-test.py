import sys
from nose.tools import eq_
sys.path.append("../main")

from diregex_lexer import lexer

def testDirName():
    toks = lexer("\"hello\"")
    eq_(toks, [('REGEX', "\"hello\"")])

def testLinearPath():
    toks = lexer("\"parent\"/\"child\"")
    eq_(toks, [('REGEX', "\"parent\""),
               ('SLASH', "/"),
               ('REGEX', "\"child\"")])

def testTree():
    toks = lexer("\"parent\"/(\"child1\", \"chil*\"=match)")
    eq_(toks, [('REGEX', "\"parent\""),
               ('SLASH', "/"),
               ('LPAREN', "("),
               ('REGEX', "\"child1\""),
               ('COMMA', ","),
               ('REGEX', "\"chil*\""),
               ('EQUALS', "="),
               ('VAR', "match"),
               ('RPAREN', ")")])


