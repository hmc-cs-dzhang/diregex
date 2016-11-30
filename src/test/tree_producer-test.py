import sys
import os
from nose.tools import eq_
sys.path.append("../main")

from diregex_ir import *
from diregex_tree_producer import produceDirTree

os.chdir("testdir4")
testPath = os.getcwd()

def testTrivial():
    treeList = TreePatternDir(DirGlob("folder"))

    produceDirTree(treeList, testPath)
    os.rmdir("folder")

def testChildren():
    """ parent/child"""
    treeList = TreePatternChild(
        DirGlob("parent"),
        TreePatternDir(
            DirGlob("child")))

    produceDirTree(treeList, testPath)
    os.removedirs("parent/child")


def testSiblings():
    treeList = TreePatternList(
        [TreePatternDir(
            DirGlob("sib1")),
        TreePatternDir(
            DirGlob("sib2"))])

    produceDirTree(treeList, testPath)
    os.rmdir("sib1")
    os.rmdir("sib2")

def testChildrenSiblings():
    """
    parent/(sib1, sib2)
    """
    treeList = TreePatternChild(
        DirGlob("parent"),
        TreePatternList(
            [TreePatternDir(
                DirGlob("sib1")),
            TreePatternDir(
                DirGlob("sib2"))]))

    produceDirTree(treeList, testPath)
    os.rmdir("parent/sib1")
    os.removedirs("parent/sib2")

def testBig():
    """
    project/(main/(header, src), test)
    """
    treeList = TreePatternChild(
        DirGlob("project"),
        TreePatternList(
            [TreePatternChild(
                DirGlob("main"),
                TreePatternList(
                    [TreePatternDir(
                        DirGlob("header")),
                    TreePatternDir(
                        DirGlob("src"))])),
            TreePatternDir(
                DirGlob("test"))]))

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
        DirGlob("src"),
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
