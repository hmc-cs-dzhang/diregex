import sys
import os
from nose.tools import eq_
sys.path.append("../main")

from diregex_ir import *
from diregex_semantics import match

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
            DirName(r"child1"),
            TreePatternDir(
                DirName(r"file1[a-b].*", "var2"))),
        TreePatternDir(
            DirName(r"[a-z]*2", "var3"))]))

    matchList = match(treeList, testpath)

    expectedMatches = [{'var3': 'child2', 'var2': 'file1b.txt'},
        {'var3': 'child2', 'var2': 'file1a.txt'}]

    eq_(matchList, expectedMatches)

''' parent=p/child1/file1[a-b]=f'''
def testTreeChildren():
    simple = TreePatternChild(
        DirName(r"[a-z]*", 'p'),
        TreePatternChild(
            DirName(r"[A-z0-9]*1"),
            TreePatternDir(
                DirName(r"[A-z0-9\.]*", 'f'))))

    matches = match(simple, testpath + "/testdir")
    expectedMatches = [{'p': 'parent', 'f': 'file1b.txt'},
        {'p': 'parent','f': 'file1a.txt'}]
    eq_(matches, expectedMatches)

''' test backreferencing between patterns with lists '''
def testTreeBackreferencing():
    tree = TreePatternDescendant(TreePatternList([
        TreePatternDir(
            DirName(r"([a-z0-9]*)a\.txt", "f1")),
        TreePatternDir(
            DirName(r"\1b\.txt", "f2"))]))

    matches = match(tree, testpath + "/testdir")
    expectedMatches = [{'f1': 'file1a.txt', 'f2': 'file1b.txt'}]
    eq_(matches, expectedMatches)

''' test backreferencing with parents/children '''
def testTreeBackreferencing2():
    tree = TreePatternChild(
        DirName(r"([a-z0-9]*)", "f1"),
        TreePatternDir(
            DirName(r"\1\.cpp", "f2")))

    matches = match(tree, testpath + "/testdir2")
    expectedMatches = [{'f1': 'foo', 'f2': 'foo.cpp'}]
    eq_(matches, expectedMatches)


