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

def testTrivial():
    ''' p=parent '''
    tree = TreePatternDir(
        DirGlob("par*t"),
        "p")

    matchList = allMatches(tree, os.path.join(testpath, "testdir"))
    print(testpath)
    expectedMatches = [{'p': 'parent'}]

    eq_(matchList, expectedMatches)

def testTreeList():
    ''' child1/file1[a-b].*=var2/[a-z]*2=var3 '''
    treeList = TreePatternDesc(TreePatternList(
        [TreePatternChild(
            DirGlob(r"child1"),
            TreePatternDir(
                DirGlob(r"file1[a-b]*"),
                "var2")),
        TreePatternDir(
            DirGlob(r"*2"),
            "var3")]))

    matchList = allMatches(treeList, testpath)

    expectedMatches = [{'var3': 'child2', 'var2': 'file1b.txt'},
        {'var3': 'child2', 'var2': 'file1a.txt'}]

    eq_(matchList, expectedMatches)

def testNoDuplicates():
    ''' **/var=parent/* '''
    treeList =  TreePatternDesc(
        TreePatternChild(
            DirGlob("parent"),
            TreePatternDir(
                DirGlob(r'*')),
            "var"))
    matchList = allMatches(treeList, testpath)

    expectedMatches = [{'var': 'parent'}]
    eq_(matchList, expectedMatches)

def testTreeChildren():
    ''' parent=p/child1/file1[a-b]=f'''
    simple = TreePatternChild(
        DirGlob(r"[a-z]*"),
        TreePatternChild(
            DirGlob(r"[A-z0-9]*1"),
            TreePatternDir(
                DirGlob(r"[A-z0-9\.]*"),
                "f")),
        "p")

    matches = allMatches(simple, testpath + "/testdir")
    expectedMatches = [{'p': 'parent', 'f': 'file1b.txt'},
        {'p': 'parent','f': 'file1a.txt'}]
    eq_(matches, expectedMatches)

def testTreeBackreferencing():
    ''' test backreferencing between patterns with lists '''
    tree = TreePatternDesc(TreePatternList([
        TreePatternDir(
            DirGlob(r"<*>a.txt"),
            "f1"),
        TreePatternDir(
            DirGlob(r"\1b.txt"),
            "f2")]))

    matches = allMatches(tree, testpath + "/testdir")
    expectedMatches = [{'f1': 'file1a.txt', 'f2': 'file1b.txt'}]
    eq_(matches, expectedMatches)

def testTreeBackreferencing2():
    ''' test backreferencing with parents/children '''
    tree = TreePatternChild(
        DirGlob(r"<*>"),
        TreePatternDir(
            DirGlob(r"\1.cpp"),
            "f2"),
        "f1")

    matches = allMatches(tree, testpath + "/testdir2")
    expectedMatches = [{'f1': 'foo', 'f2': 'foo.cpp'}]
    eq_(matches, expectedMatches)

def testVar():
    parentAst = TreePatternDir(
        DirGlob('par*t'),
        "p")

    varEnv = {"p": parentAst}

    ast = TreePatternVar("p")

    matchList = allMatches(ast, os.path.join(testpath, "testdir"), varEnv)
    expectedMatches = [{'p': 'parent'}]

    eq_(matchList, expectedMatches)
