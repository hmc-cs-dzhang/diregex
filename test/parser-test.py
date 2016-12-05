from nose.tools import eq_
from parser import parse
from ir import *


''' test a directory bound to a variable '''
def testNamedDirItem():
    ast = Prog([Assign(
        TreePatternDir(DirGlob("hello"), "foo"))])
    bst = parse('foo=hello')
    eq_(ast, bst)

''' a small path '''
def testPath():
    ast = Prog([Assign(TreePatternChild(
            DirGlob("foo"),
            TreePatternDir(
                DirGlob("bar*")),
            "var"))])
    bst = parse('var = foo/bar*')
    eq_(ast, bst)

def testSiblings1():
    ast = Prog([Match(TreePatternList([
            TreePatternDir(
                DirGlob("sib1")),
            TreePatternDir(
                DirGlob("sib2"))]))])
    bst = parse('match (sib1, sib2)')
    eq_(ast, bst)

''' a parent with two children '''
def testSiblings2():
    ast = Prog([Match(TreePatternChild(
            DirGlob("foo"),
            TreePatternList(
                [TreePatternDir(
                    DirGlob("bar1")),
                TreePatternDir(
                    DirGlob("bar2"))])))])
    bst = parse('match foo/(bar1, bar2)')

    eq_(ast, bst)

''' descendent '''
def testDescedent():
    ast = Prog([Match(TreePatternChild(
            DirGlob("foo"),
            TreePatternDesc(
                TreePatternDir(
                    DirGlob("bar"), "myvar"))))])
    bst = parse('match foo/**/myvar=bar')
    eq_(ast, bst)

''' pattern '''
def testPattern():
    ast = Prog([Match(TreePatternChild(
            DirGlob("foo"),
            TreePatternChild(
                DirGlob('test<pat=d*[?][1-2]>*a'),
                TreePatternDir(
                    DirGlob("child"),
                    "hi"),
                "hey")))])
    bst = parse('''
        match foo/hey=test<pat=d*[?][1-2]>*a/hi=child

        ''')
    eq_(ast, bst)

def testVar():
    ast = Prog([Dest(TreePatternChild(
            DirName("foo"),
            TreePatternVar("var")))])
    bst = parse(r'dest foo/{var}')
    eq_(ast, bst)

def testAttrs():
    """ test 'file' and 'dir' attributes in match and dest """
    ast = Prog([
        Match(
            TreePatternList([
                TreePatternChild(
                    DirGlob("par"),
                    TreePatternDir(
                        DirGlob('d*?', 'dir'))),
                TreePatternDir(
                    DirGlob('s*', 'file'))])),
        Dest(
            TreePatternDir(
                DirName('test.cpp', 'file')))])

    bst = parse(r'''
        match (par/dir:d*?, file:s*)
        dest file:test.cpp
        ''')
    eq_(ast, bst)

def testAttrs2():
    """ test attributes in assignment statements """
    ast = Prog([
        Assign(
            TreePatternChild(
                DirGlob('par*', 'dir'),
                TreePatternDir(
                    DirGlob('chi*', 'file'),
                    'src'),
                'top'))])

    bst = parse(r'''
        top = dir:par*/src=file:chi*
        ''')

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
                DirName(r'<\pat>'),
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
        Assign(
            TreePatternDir(
                DirGlob('<pat=*>.cpp'),
                "srcfile")),
        Assign(
            TreePatternDir(
                DirGlob('<\pat>_test.cpp'),
                "testfile")),
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
                DirName(r'<\pat>'),
                TreePatternList([
                    TreePatternVar("srcfile"),
                    TreePatternVar("testfile"),
                    TreePatternDir(DirName("README.txt", 'file'))])))])

    bst = parse(r'''
        srcfile = <pat=*>.cpp
        testfile = <\pat>_test.cpp
        match (src/{srcfile}, test/{testfile})
        dest <\pat>/({srcfile}, {testfile}, file:README.txt)
        ''')

    eq_(ast,bst)


