from nose.tools import eq_, with_setup
import os
import io
import shutil
from semantics import run

os.chdir('../test/testdir4')

def checkEmpty(directory="./"):
    dirItems = os.listdir(directory)
    if os.listdir(directory) != []:
        assert False, "directory was not empty, contained " + str(dirItems)

def setup():
    """ run before each test to clean out the directory """
    eq_(os.path.basename(os.getcwd()), 'testdir4')
    for item in os.scandir():
        if os.path.isdir(item.path):
            shutil.rmtree(item.path)
        else:
            os.remove(item.path)


def teardown():
    """ run after each test to make sure there was nothing else in the dir"""
    checkEmpty()


@with_setup(setup, teardown)
def testDest():
    """ script to create parent with two children folders """
    prog = r"""
    dest parent/(child1/, child2/)
    """

    run(prog)
    os.rmdir("parent/child2")
    os.removedirs("parent/child1")


@with_setup(setup, teardown)
def test2():
    """
    See ideal syntax example 1
    """

    setupProg = r"""
    dest (src/(
            foo.cpp,
            bar.cpp),
          test/(
            foo_test.cpp,
            bar_test.cpp))
    """

    run(setupProg)

    prog = r"""
    match (src/srcfile=<pat=*>.cpp,
           test/testfile=<\pat>_test.cpp)
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

@with_setup(setup, teardown)
def test3():
    """ same set-up as above, but uses more variable naming as alternate syntax"""

    setupProg = r"""
    dest (src/(
            foo.cpp,
            bar.cpp),
          test/(
            foo_test.cpp,
            bar_test.cpp))
    """

    run(setupProg)

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

    # should not match with the dummy variable
    setupProg = r"""
    dest (foo/(foo.cpp,foo_test.cpp),
          bar/(bar.cpp,bar_test.cpp),
          dummy/(dummy1.cpp,dummy_test.cpp))
    """
    run(setupProg)

    prog = r"""
    match <pat=*>/(
            srcfile=<\pat>.cpp,
            testfile=<\pat>_test.cpp)
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

@with_setup(setup, teardown)
def test5():
    """ same as test3, but uses the 'file' attribute to create a README.txt"""

    setupProg = r"""
    dest (src/(foo.cpp, bar.cpp),
          test/(foo_test.cpp, bar_test.cpp))
    """

    run(setupProg)

    prog = r"""
    srcfile = <pat=*>.cpp
    testfile = <\pat>_test.cpp
    match (src/{srcfile}, test/{testfile})
    dest <\pat>/({srcfile}, {testfile}, README.txt)
    """

    run(prog)

    os.remove('foo/foo.cpp')
    os.remove('foo/foo_test.cpp')
    os.remove('foo/README.txt')
    os.rmdir('foo')

    os.remove('bar/bar.cpp')
    os.remove('bar/bar_test.cpp')
    os.remove('bar/README.txt')
    os.rmdir('bar')


@with_setup(setup, teardown)
def test6():
    """ only moves files, not folders """

    # creates folder1/(hey.txt, hi.txt, dont_move)
    os.mkdir("folder1")
    open('folder1/hey.txt', 'a').close()
    open('folder1/hi.txt', 'a').close()
    os.mkdir('folder1/dont_move')

    os.mkdir("folder2")

    prog = r"""
    match folder1/f=file:*
    dest folder2/{f}
    """
    # should move hey and hi into folder2, but keep dont_move in folder1
    run(prog)

    os.remove('folder2/hey.txt')
    os.remove('folder2/hi.txt')
    os.rmdir('folder2')

    os.removedirs('folder1/dont_move')

@with_setup(setup, teardown)
def test7():
    """ move file to a subdirectory in the same folder """
    os.mkdir("src")
    open('src/foo.txt', 'a').close()
    open('src/bar.txt', 'a').close()

    prog = r"""
    match src/f=file:<pat=*>.txt
    dest src/<\pat>/{f}
    """

    run(prog)

    os.remove('src/foo/foo.txt')
    os.remove('src/bar/bar.txt')
    os.rmdir('src/foo')
    os.removedirs('src/bar')

@with_setup(setup, teardown)
def test8():
    """
    move files based on parsing tokens, based on
    http://stackoverflow.com/questions/34297712/move-files-to-different-directories-based-on-file-name-tokens
    """

    open('DSLs_fall_2016.txt', 'a')
    open('PLs_fall_2016.txt', 'a')
    open('CS81_spring_2016.txt', 'a')
    open('LinAl_spring_2016.txt', 'a')
    open('STEMs_fall_2015.txt', 'a')

    prog = r"""
    match syllabus = <class=*>_<sem=*>_<year=[0-9]*>.txt
    dest <\year>/<\sem>/<\class>/{syllabus}
    """

    run(prog)

    os.remove('2016/fall/DSLs/DSLs_fall_2016.txt')
    os.remove('2016/fall/PLs/PLs_fall_2016.txt')
    os.remove('2016/spring/CS81/CS81_spring_2016.txt')
    os.remove('2016/spring/LinAl/LinAl_spring_2016.txt')
    os.remove('2015/fall/STEMs/STEMs_fall_2015.txt')

    os.rmdir('2016/fall/DSLs')
    os.rmdir('2016/fall/PLs')
    os.rmdir('2016/spring/CS81')
    os.rmdir('2016/spring/LinAl')
    os.rmdir('2015/fall/STEMs')

    os.rmdir('2016/fall')
    os.rmdir('2016/spring')
    os.rmdir('2015/fall')

    os.rmdir('2016')
    os.rmdir('2015')

@with_setup(setup, teardown)
def test9():
    """
    move many files up a directory.  Inspired by:
    http://stackoverflow.com/questions/35554875/iterate-over-folders-and-move-files-up-one-level
    """

    setupProg = r"""
        dest (
            1/.temp/(
                image1.png,
                image2.png,
                image3.png),
            2/.temp/(
                image1.png,
                image2.png,
                image3.png))
    """
    run(setupProg)

    prog = r"""
    match <fldr=[0-9]>/.temp/img=image[0-9].png
    dest <\fldr>/{img}
    """

    run(prog)

    os.remove('1/image1.png')
    os.remove('1/image2.png')
    os.remove('1/image3.png')
    os.remove('2/image1.png')
    os.remove('2/image2.png')
    os.remove('2/image3.png')

    os.rmdir('1')
    os.rmdir('2')

@with_setup(setup, teardown)
def test10():
    """
    Search for PDFs matching their corresponding signed PDFS,
    move them into the same directory.  Inspired by
    http://stackoverflow.com/questions/15438347/find-match-variable-filenames-and-move-files-to-respective-directory
    """

    prog1 = r"""
        dest (
            signed/(
                PDF1_signed.pdf,
                PDF2_signed.pdf,
                PDF3_signed.pdf),

            top_level/(
                PDF1.pdf,
                next/(
                     PDF2.pdf,
                     deep/(
                        PDF3.pdf,
                        PDF4.pdf))))
    """

    run(prog1)

    prog = r"""
    match (signed/<name=PDF[0-9]>_signed.pdf,
            **/pdf=<\name>.pdf)
    dest signed/{pdf}
    """

    run(prog)


    os.remove('signed/PDF1_signed.pdf')
    os.remove('signed/PDF2_signed.pdf')
    os.remove('signed/PDF3_signed.pdf')
    os.remove('signed/PDF1.pdf')
    os.remove('signed/PDF2.pdf')
    os.remove('signed/PDF3.pdf')

    os.rmdir('signed')

    os.remove('top_level/next/deep/PDF4.pdf')

    os.removedirs('top_level/next/deep')


@with_setup(setup, teardown)
def test11():
    """ tests using shell commands """
    setupProg = r"dest (foo.txt, bar.txt)"

    run(setupProg)

    prog = r"""
    var = file:*
    match {var}
    !rm {var}
    """

    run(prog)

@with_setup(setup, teardown)
def test12():
    """ combining shell commands and dest trees """
    setupProg = r"""
    dest (foo/(
            foo_src.cpp,
            foo_test.cpp,
            delete.me),
          bar/(
            bar_src.cpp,
            bar_test.cpp,
            delete.me))
    """

    run(setupProg)

    prog = r"""
    match */(code=*_src.cpp, test=*_test.cpp, rem=delete.me)
    !rm {rem}
    dest new_folder/({code}, {test})
    """

    run(prog)

    os.remove('new_folder/foo_src.cpp')
    os.remove('new_folder/foo_test.cpp')
    os.remove('new_folder/bar_src.cpp')
    os.remove('new_folder/bar_test.cpp')

    os.rmdir('new_folder')

@with_setup(setup, teardown)
def test13():
    """ shell commands with patterns """
    setupProg = r"""
    dest foo/(joe.cpp, mike.cpp)
    """

    run(setupProg)

    prog = r"""
    match foo/name = <pat=*>.cpp
    !mkdir \pat
    !mv {name} \pat
    """

    run(prog)

    os.remove('joe/joe.cpp')
    os.remove('mike/mike.cpp')

    os.rmdir('joe')
    os.rmdir('mike')

    os.rmdir('foo')

@with_setup(setup, teardown)
def test14():
    """ produce a parameterized tree structure """
    prog = r"""
    matchpat src = [foo, bar]
    dest <\src>.txt
    """

    run(prog)

    os.remove('foo.txt')
    os.remove('bar.txt')

@with_setup(setup, teardown)
def test15():
    """ parameterized tree structure with different levels """

    prog = r"""
    matchpat class = [Math189, DSLs, PLs],
                subfolder = [Homework, Notes]
    dest <\class>/<\subfolder>/
    """

    run(prog)

    # a program to remove the files

    remProg = r"""
    match top=*/(hw = Homework, nt = Notes)
    !rm -r {top}
    """

    run(remProg)

