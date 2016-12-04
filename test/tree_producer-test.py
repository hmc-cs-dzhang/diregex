import os
from nose.tools import eq_

from ir import *
from tree_producer import produceDirTree

os.chdir("testdir4")
testPath = os.getcwd()

def testTrivial():
    treeList = TreePatternDir(DirName("folder"))

    produceDirTree(treeList, testPath)
    os.rmdir("folder")

def testChildren():
    """ parent/child"""
    treeList = TreePatternChild(
        DirName("parent"),
        TreePatternDir(
            DirName("child")))

    produceDirTree(treeList, testPath)
    os.removedirs("parent/child")


def testSiblings():
    treeList = TreePatternList(
        [TreePatternDir(
            DirName("sib1")),
        TreePatternDir(
            DirName("sib2"))])

    produceDirTree(treeList, testPath)
    os.rmdir("sib1")
    os.rmdir("sib2")

def testChildrenSiblings():
    """
    parent/(sib1, sib2)
    """
    treeList = TreePatternChild(
        DirName("parent"),
        TreePatternList(
            [TreePatternDir(
                DirName("sib1")),
            TreePatternDir(
                DirName("sib2"))]))

    produceDirTree(treeList, testPath)
    os.rmdir("parent/sib1")
    os.removedirs("parent/sib2")

def testBig():
    """
    project/(main/(header, src), test)
    """
    treeList = TreePatternChild(
        DirName("project"),
        TreePatternList(
            [TreePatternChild(
                DirName("main"),
                TreePatternList(
                    [TreePatternDir(
                        DirName("header")),
                    TreePatternDir(
                        DirName("src"))])),
            TreePatternDir(
                DirName("test"))]))

    produceDirTree(treeList, testPath)

    os.rmdir("project/main/header")
    os.rmdir("project/main/src")
    os.rmdir("project/main")
    os.removedirs("project/test")

def testVar():
    """
    src/{srcfile}
    """
    open('newfile.cpp', 'a').close()

    env = {'srcfile' : './newfile.cpp'}

    treeList = TreePatternChild(
        DirName("src"),
        TreePatternVar("srcfile"))

    produceDirTree(treeList, testPath, env)

    os.remove("src/newfile.cpp")
    os.rmdir("src")
'''
def testManyVars():
    """
    project/({var1}, {var2})
    """

    os.mkdir("src")
    open("src/srcfile.cpp", "a").close()

    os.mkdir("test")
    open("test/testfile.cpp", "a").close()

    env = {'var1' : './src', 'var2' : './test'}

    treeList = TreePatternChild(
        DirGlob("project"),
        TreePatternList(
            [TreePatternDir(
                TreePatternVar('var1')),
            TreePatternDir(
                TreePatternVar('var2'))]))

    produceDirTree(treeList, testPath, env)

    os.remove("project/src/srcfile.cpp")
    os.remove("project/test/testfile.cpp")

    os.removedirs("project/src")
    os.removedirs("project/test")
'''
