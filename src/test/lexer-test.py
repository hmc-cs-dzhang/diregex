import sys
from nose.tools import eq_
sys.path.append("../main")

from diregex_lexer import lexer

# reserved symbols: < > ( ) { } / , = ** :

def testGlob():
    toks = lexer("*/")
    eq_(toks, [('GLOB', '*'),
               ('SLASH', '/')])

def testDoubleStar():
    toks = lexer("**/*")
    eq_(toks, [('DOUBLE_STAR', '**'),
               ('SLASH', '/'),
               ('GLOB', '*')])

def testDirName():
    toks = lexer("hello")
    eq_(toks, [('IDENT', "hello")])

def testLinearPath():
    toks = lexer(r"p<pat:*>arent/{child}")
    eq_(toks, [('GLOB', "p<pat:*>arent"),
               ('SLASH', "/"),
               ('LBRACE', "{"),
               ('GLOB', "child"),
               ('RBRACE', "}")])

def testLinearPath2():
    toks = lexer("*=mydir/**/file/_a?[1-5]*=hi/yo=hi2")
    eq_(toks, [('GLOB', '*'),
               ('EQUALS', '='),
               ('IDENT', 'mydir'),
               ('SLASH', '/'),
               ('DOUBLE_STAR', '**'),
               ('SLASH', '/'),
               ('IDENT', 'file'), # could/should be GLOB
               ('SLASH', '/'),
               ('GLOB', '_a?[1-5]*'),
               ('EQUALS', '='),
               ('IDENT', 'hi'),
               ('SLASH', '/'),
               ('GLOB', 'yo'),
               ('EQUALS', '='),
               ('IDENT', 'hi2')])

def testRegex():
    toks = lexer("A*[A-z0-9]")
    eq_(toks, [('GLOB', "A*[A-z0-9]")])

def testTree():
    toks = lexer("parent/(child1, **/chil*=match)")
    eq_(toks, [('IDENT', "parent"), # could be GLOB
               ('SLASH', "/"),
               ('LPAREN', "("),
               ('IDENT', "child1"), # could be GLOB
               ('COMMA', ","),
               ('DOUBLE_STAR', "**"),
               ('SLASH', "/"),
               ('GLOB', "chil*"),
               ('EQUALS', "="),
               ('IDENT', "match"),
               ('RPAREN', ")")])

def testBackreference():
    toks = lexer(r"<*.h>/\1=foo")
    eq_(toks, [('GLOB', '<*.h>'),
               ('SLASH', '/'),
               ('GLOB', '\\1'),
               ('EQUALS', '='),
               ('IDENT', 'foo')])
