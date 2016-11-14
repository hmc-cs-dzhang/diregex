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

def testRegex():
    toks = lexer("\"A*[A-z0-9]\"")
    eq_(toks, [('REGEX', "\"A*[A-z0-9]\"")])

def testTree():
    toks = lexer("\"parent\"/(\"child1\", >\"chil*\"=match)")
    eq_(toks, [('REGEX', "\"parent\""),
               ('SLASH', "/"),
               ('LPAREN', "("),
               ('REGEX', "\"child1\""),
               ('COMMA', ","),
               ('GT', ">"),
               ('REGEX', "\"chil*\""),
               ('EQUALS', "="),
               ('VAR', "match"),
               ('RPAREN', ")")])


