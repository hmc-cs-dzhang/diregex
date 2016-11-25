import sys
from nose.tools import eq_
sys.path.append("../main")
from pprint import pprint
from parsec_parser import parse
from diregex_ir import *

''' test a simple directory '''
def testDirItem():
    ast = TreePatternDir(DirName("hello"))
    bst = parse('hello')
    eq_(ast, bst)

''' test a directory bound to a variable '''
def testNamedDirItem():
    ast = TreePatternDir(DirName("hello", "foo"))
    bst = parse('hello=foo')
    eq_(ast, bst)

''' a small path '''
def testPath():
    ast = TreePatternChild(
        DirName("foo"),
        TreePatternDir(
            DirName("bar*")))
    bst = parse('foo/bar*')
    eq_(ast, bst)

def testSiblings1():
    ast = TreePatternList([
        TreePatternDir(
            DirName("sib1")),
        TreePatternDir(
            DirName("sib2"))])
    bst = parse('(sib1, sib2)')
    eq_(ast, bst)

''' a parent with two children '''
def testSiblings2():
    ast = TreePatternChild(
        DirName("foo"),
        TreePatternList(
            [TreePatternDir(
                DirName("bar1")),
            TreePatternDir(
                DirName("bar2"))]))
    bst = parse('foo/(bar1, bar2)')

    eq_(ast, bst)

''' descendent '''
def testDescedent():
    ast = TreePatternChild(
        DirName("foo"),
        TreePatternDescendant(
            TreePatternDir(
                DirName("bar", "myvar"))))
    bst = parse('foo/**/bar=myvar')
    eq_(ast, bst)

''' pattern '''
def testPattern():
    ast = TreePatternChild(
        DirName("foo"),
        TreePatternChild(
            DirName('test<pat=d*[?][1-2]>*a', "hey"),
            TreePatternDir(
                DirName("child", "hi"))))
    bst = parse('foo/test<pat=d*[?][1-2]>*a=hey/child=hi')
    eq_(ast, bst)
