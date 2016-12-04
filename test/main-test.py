from nose.tools import eq_, with_setup
import os
import io
import shutil
from semantics import run

os.chdir('../test/testdir4')

def checkEmpty(directory="./"):
    if os.listdir(directory) != []:
        assert False, "directory was not empty"

def setup():
    """ run before each test to clean out the directory """
    eq_(os.path.basename(os.getcwd()), 'testdir4')
    for item in os.scandir():
        shutil.rmtree(item.path)

def teardown():
    """ run after each test to make sure there was nothing else in the dir"""
    checkEmpty()


'''
def testDest():
    """ script to create parent with two children folders """
    prog = r"""
    dest parent/(child1, child2)
    """

    run(prog)
    os.rmdir("parent/child2")
    os.removedirs("parent/child1")

    checkEmpty()
'''
@with_setup(setup, teardown)
def test2():
    """
    See ideal syntax example 1
    """
    os.mkdir("src")
    open('src/foo.cpp' ,'a').close()
    open('src/bar.cpp' ,'a').close()

    os.mkdir("test")
    open('test/foo_test.cpp', 'a').close()
    open('test/bar_test.cpp', 'a').close()

    prog = r"""
    match (src/srcfile=<pat=*>.cpp, test/testfile=<\pat>_test.cpp)
    dest <\pat>/({srcfile}, {testfile})

    """

    run(prog)

    os.remove('foo/foo.cpp')
    os.remove('foo/foo_test.cpp')
    os.rmdir('foo')

    os.remove('bar/bar.cpp')
    os.remove('bar/bar_test.cpp')
    os.rmdir('bar')

    checkEmpty()


def test3():
    """ same set-up as above, but uses more variable naming as alternate syntax"""
    os.mkdir("src")
    open('src/foo.cpp' ,'a').close()
    open('src/bar.cpp' ,'a').close()

    os.mkdir("test")
    open('test/foo_test.cpp', 'a').close()
    open('test/bar_test.cpp', 'a').close()

    prog = r"""
    srcfile = <pat=*>.cpp
    testfile = <\pat>_test.cpp
    match (src/{srcfile}, test/{testfile})
    dest <\pat>/({srcfile}, {testfile})
    """

    run(prog)

    os.remove('foo/foo.cpp')
    os.remove('foo/foo_test.cpp')
    os.rmdir('foo')

    os.remove('bar/bar.cpp')
    os.remove('bar/bar_test.cpp')
    os.rmdir('bar')

def test4():
    """ does the opposite of the above test """
    os.mkdir("foo")
    open('foo/foo.cpp', 'a').close()
    open('foo/foo_test.cpp', 'a').close()

    os.mkdir("bar")
    open('bar/bar.cpp', 'a').close()
    open('bar/bar_test.cpp', 'a').close()

    # shouldn't copy dummy, since dummy1 doesn't match the pattern
    os.mkdir("dummy")
    open('dummy/dummy1.cpp', 'a').close()
    open('dummy/dummy_test.cpp', 'a').close()

    prog = r"""
    match <pat=*>/(srcfile=<\pat>.cpp, testfile=<\pat>_test.cpp)
    dest (src/{srcfile}, test/{testfile})
    """

    run(prog)

    os.remove('src/foo.cpp')
    os.remove('src/bar.cpp')
    os.rmdir('src')

    os.remove('test/foo_test.cpp')
    os.remove('test/bar_test.cpp')
    os.rmdir('test')

    os.remove('dummy/dummy1.cpp')
    os.remove('dummy/dummy_test.cpp')
    os.rmdir('dummy')


