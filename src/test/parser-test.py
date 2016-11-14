import sys
from nose.tools import eq_
sys.path.append("../main")

from diregex_parser import parse
from diregex_ir import *

''' test a simple directory '''
def testDirItem():
    ast = TreePattern_Dir(DirItem(DirName("hello")))
    bst = parse("\"hello\"")
    eq_(ast, bst)

''' test a directory bound to a variable '''
def testNamedDirItem():
    ast = TreePattern_Dir(DirItem(DirName("hello", "foo")))
    bst = parse("\"hello\"=foo")
    eq_(ast, bst)

''' a small path '''
def testPath():
    ast = TreePattern_Child(
        DirItem(
            DirName("foo")),
        TreePattern_Dir(
            DirItem(
                DirName("bar*"))))
    bst = parse("\"foo\"/\"bar*\"")
    eq_(ast, bst)

''' a parent with two children '''
def testSiblings():
    ast = TreePattern_Child(
        DirItem(
            DirName("foo")),
        TreePattern_List(
            [TreePattern_Dir(
                DirItem(
                    DirName("bar1"))),
            TreePattern_Dir(
                DirItem(
                    DirName("bar2")))]))
    bst = parse("\"foo\"/(\"bar1\", \"bar2\")")
    eq_(ast, bst)
