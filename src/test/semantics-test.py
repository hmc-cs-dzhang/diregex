import sys
import os
from nose.tools import eq_
sys.path.append("../main")

from diregex_ir import *
from diregex_semantics import allMatches

# copied from diregex_semantics.py.
# Add imports and change directory

''' current testdir looks like:
parent
    child1
        file1a.txt
        file1b.txt
    child2
        file2.txt
    kid3
        file3.txt
'''

# testpath is path to testdir
testpath = os.getcwd()

''' child1/file1[a-b].*=var2/[a-z]*2=var3 '''
def testTreeList():
    treeList = TreePatternDescendant(TreePatternList(
        [TreePatternChild(
            DirGlob(r"child1"),
            TreePatternDir(
                DirGlobWithVar("var2", r"file1[a-b]*"))),
        TreePatternDir(
            DirGlobWithVar("var3", r"*2"))]))

    matchList = allMatches(treeList, testpath)

    expectedMatches = [{'var3': 'child2', 'var2': 'file1b.txt'},
        {'var3': 'child2', 'var2': 'file1a.txt'}]

    eq_(matchList, expectedMatches)

def testNoDuplicates():
    treeList=  TreePatternDescendant(
        TreePatternChild(
            DirGlobWithVar("var", "parent"),
            TreePatternDir(
                DirGlob(r'*'))))
    matchList = allMatches(treeList, testpath)

    expectedMatches = [{'var': 'parent'}]
    eq_(matchList, expectedMatches)

''' parent=p/child1/file1[a-b]=f'''
def testTreeChildren():
    simple = TreePatternChild(
        DirGlobWithVar('p', r"[a-z]*"),
        TreePatternChild(
            DirGlob(r"[A-z0-9]*1"),
            TreePatternDir(
                DirGlobWithVar('f', r"[A-z0-9\.]*"))))

    matches = allMatches(simple, testpath + "/testdir")
    expectedMatches = [{'p': 'parent', 'f': 'file1b.txt'},
        {'p': 'parent','f': 'file1a.txt'}]
    eq_(matches, expectedMatches)

''' test backreferencing between patterns with lists '''
def testTreeBackreferencing():
    tree = TreePatternDescendant(TreePatternList([
        TreePatternDir(
            DirGlobWithVar("f1", r"<*>a.txt")),
        TreePatternDir(
            DirGlobWithVar("f2", r"\1b.txt"))]))

    matches = allMatches(tree, testpath + "/testdir")
    expectedMatches = [{'f1': 'file1a.txt', 'f2': 'file1b.txt'}]
    eq_(matches, expectedMatches)

''' test backreferencing with parents/children '''
def testTreeBackreferencing2():
    tree = TreePatternChild(
        DirGlobWithVar("f1", r"<*>"),
        TreePatternDir(
            DirGlobWithVar("f2", r"\1.cpp")))

    matches = allMatches(tree, testpath + "/testdir2")
    expectedMatches = [{'f1': 'foo', 'f2': 'foo.cpp'}]
    eq_(matches, expectedMatches)


