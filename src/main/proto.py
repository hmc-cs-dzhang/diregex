import os
from diregex_semantics import Matcher
from diregex_parser import parse
import diregex_lexer
from diregex_ir import *
from regex_env import RegexEnv

print(os.getcwd())
os.chdir('../test/testdir4')

def match(diregex):
    ast = parse(diregex)
    #print(ast)
    matcher = Matcher()
    emptyEnv = RegexEnv()

    for match, regexEnv in matcher.visit(ast, os.getcwd(), emptyEnv):
        shortenedMatch = {key:os.path.basename(val) for key, val in match.items()}
        print(shortenedMatch)
        #print(regexEnv.groups)

def run(prog):
    raise NotImplementedError("run is not yet implemented")

def test1():
    """ script to create parent with two children folders """
    prog = r"""
    dest parent/(child1, child2)
    """

    run(prog)
    os.rmdir("parent/child2")
    os.removedirs("parent/child1")

def test2():
    """
    See ideal syntax example 1
    """
    os.mkdir("src")
    os.open('src/foo.cpp' ,'a').close()
    os.open('src/bar.cpp' ,'a').close()

    os.mkdir("test")
    os.open('test/foo_test.cpp', 'a').close()
    os.open('test/bar_test.cpp', 'a').close()

    prog = r"""
    match (src/srcfile=<pat=*>, test/testfile=<\pat>_test.cpp)
    dest <\pat>/({srcfile}, {testfile})

    """

    run(prog)

    os.remove('foo/foo.cpp')
    os.removedirs('foo/foo_test.cpp')

    os.remove('bar/bar.cpp')
    os.removedirs('bar/bar_test.cpp')

    os.rmdir('src')
    os.rmdir('test')

def test3():
    """ same set-up as above, but uses more variable naming as alternate syntax"""
    os.mkdir("src")
    os.open('src/foo.cpp' ,'a').close()
    os.open('src/bar.cpp' ,'a').close()

    os.mkdir("test")
    os.open('test/foo_test.cpp', 'a').close()
    os.open('test/bar_test.cpp', 'a').close()

    prog = r"""
    srcfile = <pat=*>.cpp
    testfile = <\pat>_test.cpp
    match (src/{srcfile}, test/{testfile})
    dest <\pat>/({srcfile}, {testfile})
    """

    run(prog)

    os.remove('foo/foo.cpp')
    os.removedirs('foo/foo_test.cpp')

    os.remove('bar/bar.cpp')
    os.removedirs('bar/bar_test.cpp')

    os.rmdir('src')
    os.rmdir('test')


"""
print("----Example 1------")
match('parent=p/child[1-2]')

print("----Example 2------")
match('**/*[0-9]=foo/*=bar')

print("----Example 3------")
match('parent=foo/child[1-2]*=bar/*')

print("----Example 4------")
match('parent/(ch*=c1, *[0-9]=c2)')

print("----Example 5------")
match('parent=p/**/file?[a-z0-9].txt=q')

print("----Example 6------")
match('*[!0-9]/(**/*=var1, child[a-z0-9]*=var2)')

# should return nothing
print("----Example 7------")
match('butt')

os.chdir('../testdir2')

print("----Example 8------")
match(r'<*>=top/\1.cpp=bottom')
"""
