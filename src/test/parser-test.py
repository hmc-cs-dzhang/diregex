import sys
from nose.tools import eq_
sys.path.append("../main")
from pprint import pprint
from parsec_parser import parse
from diregex_ir import *

''' test a simple directory '''
def testDirItem():
    ast = Prog([TreePatternDir(DirGlob("hello"))])
    bst = parse('hello')
    eq_(ast, bst)

''' test a directory bound to a variable '''
def testNamedDirItem():
    ast = Prog([TreePatternDir(DirGlob("hello"), "foo")])
    bst = parse('foo=hello')
    eq_(ast, bst)

''' a small path '''
def testPath():
    ast = Prog([TreePatternChild(
            DirGlob("foo"),
            TreePatternDir(
                DirGlob("bar*")))])
    bst = parse('foo/bar*')
    eq_(ast, bst)

def testSiblings1():
    ast = Prog([TreePatternList([
            TreePatternDir(
                DirGlob("sib1")),
            TreePatternDir(
                DirGlob("sib2"))])])
    bst = parse('(sib1, sib2)')
    eq_(ast, bst)

''' a parent with two children '''
def testSiblings2():
    ast = Prog([TreePatternChild(
            DirGlob("foo"),
            TreePatternList(
                [TreePatternDir(
                    DirGlob("bar1")),
                TreePatternDir(
                    DirGlob("bar2"))]))])
    bst = parse('foo/(bar1, bar2)')

    eq_(ast, bst)

''' descendent '''
def testDescedent():
    ast = Prog([TreePatternChild(
            DirGlob("foo"),
            TreePatternDesc(
                TreePatternDir(
                    DirGlob("bar"), "myvar")))])
    bst = parse('foo/**/myvar=bar')
    eq_(ast, bst)

''' pattern '''
def testPattern():
    ast = Prog([TreePatternChild(
            DirGlob("foo"),
            TreePatternChild(
                DirGlob('test<pat=d*[?][1-2]>*a'),
                TreePatternDir(
                    DirGlob("child"),
                    "hi"),
                "hey"))])
    bst = parse('''
        foo/hey=test<pat=d*[?][1-2]>*a/hi=child

        ''')
    eq_(ast, bst)

def testVar():
    ast = Prog([TreePatternChild(
            DirGlob("foo"),
            TreePatternVar("var"))])
    bst = parse(r'foo/{var}')
    eq_(ast, bst)

def testMatchDest():
    ''' parses a program with src and dest trees '''
    ast = Prog([
        Match(
            TreePatternList([
                TreePatternChild(
                    DirGlob('src'),
                    TreePatternDir(
                        DirGlob(r'<pat=*>.cpp'),
                        'srcfile')),
                TreePatternChild(
                    DirGlob('test'),
                    TreePatternDir(
                        DirGlob(r'<\pat>_test.cpp'),
                        'testfile'))])),
        Dest(
            TreePatternChild(
                DirGlob(r'<\pat>'),
                TreePatternList([
                    TreePatternVar('srcfile'),
                    TreePatternVar('testfile')])))])

    bst = parse(r'''
    match (src/srcfile=<pat=*>.cpp, test/testfile=<\pat>_test.cpp)
    dest <\pat>/({srcfile}, {testfile})
    ''')
    eq_(ast, bst)

def testVarMatchDest():
    ''' parses a program with src, dest trees and other stmts '''
    ast = Prog([
        TreePatternDir(
            DirGlob('<pat=*>.cpp'),
            "srcfile"),
        TreePatternDir(
            DirGlob('<\pat>_test.cpp'),
            "testfile"),
        Match(
            TreePatternList([
                TreePatternChild(
                    DirGlob('src'),
                    TreePatternVar("srcfile")),
                TreePatternChild(
                    DirGlob('test'),
                    TreePatternVar("testfile"))])),
        Dest(
            TreePatternChild(
                DirGlob(r'<\pat>'),
                TreePatternList([
                    TreePatternVar("srcfile"),
                    TreePatternVar("testfile")])))])

    bst = parse(r'''
        srcfile = <pat=*>.cpp
        testfile = <\pat>_test.cpp
        match (src/{srcfile}, test/{testfile})
        dest <\pat>/({srcfile}, {testfile})
        ''')

    eq_(ast,bst)


