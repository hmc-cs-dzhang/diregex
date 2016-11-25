import sys
from nose.tools import eq_
sys.path.append("../main")
from pprint import pprint
from parsec_parser import parse
from diregex_ir import *

''' test a simple directory '''
def testDirItem():
    ast = TreePatternDir(DirGlob("hello"))
    bst = parse('hello')
    eq_(ast, bst)

''' test a directory bound to a variable '''
def testNamedDirItem():
    ast = TreePatternDir(DirGlobWithVar("foo", "hello"))
    bst = parse('foo=hello')
    eq_(ast, bst)

''' a small path '''
def testPath():
    ast = TreePatternChild(
        DirGlob("foo"),
        TreePatternDir(
            DirGlob("bar*")))
    bst = parse('foo/bar*')
    eq_(ast, bst)

def testSiblings1():
    ast = TreePatternList([
        TreePatternDir(
            DirGlob("sib1")),
        TreePatternDir(
            DirGlob("sib2"))])
    bst = parse('(sib1, sib2)')
    eq_(ast, bst)

''' a parent with two children '''
def testSiblings2():
    ast = TreePatternChild(
        DirGlob("foo"),
        TreePatternList(
            [TreePatternDir(
                DirGlob("bar1")),
            TreePatternDir(
                DirGlob("bar2"))]))
    bst = parse('foo/(bar1, bar2)')

    eq_(ast, bst)

''' descendent '''
def testDescedent():
    ast = TreePatternChild(
        DirGlob("foo"),
        TreePatternDesc(
            TreePatternDir(
                DirGlobWithVar("myvar", "bar"))))
    bst = parse('foo/**/myvar=bar')
    eq_(ast, bst)

''' pattern '''
def testPattern():
    ast = TreePatternChild(
        DirGlob("foo"),
        TreePatternChild(
            DirGlobWithVar("hey", 'test<pat=d*[?][1-2]>*a'),
            TreePatternDir(
                DirGlobWithVar("hi", "child"))))
    bst = parse('foo/hey=test<pat=d*[?][1-2]>*a/hi=child')
    eq_(ast, bst)

def testVar():
    ast = TreePatternChild(
        DirGlob("foo"),
        TreePatternVar("var"))
    bst = parse(r'foo/{var}')
    eq_(ast, bst)
