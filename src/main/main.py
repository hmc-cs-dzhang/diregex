import sys
sys.path.append("../semantics")

import os
import io
from matcher import match
from subst import updateEnv
from tree_producer import produceDirTree
from semantics import run



def main():
    path = '../../test/testdir4'
    os.chdir(path)
    if 'src' not in [p.name for p in os.scandir()]:
        os.mkdir('src')
    if 'test' not in [p.name for p in os.scandir()]:
        os.mkdir('test')

    open('src/foo.cpp', 'a').close()
    open('test/foo_test.cpp', 'a').close()

    open('src/bar.cpp', 'a').close()
    open('test/bar_test.cpp', 'a').close()

    open('src/baz.cpp', 'a').close()
    open('test/baz_test.cpp', 'a')

    program = r'''
    srcfile = <pat=*>.cpp
    testfile = <\pat>_test.cpp
    match (src/{srcfile}, test/{testfile})
    dest <\pat>/({srcfile}, {testfile})
    '''

    run(program)



main()



'''
srcfile = <pat=*>.cpp
        testfile = <\pat>_test.cpp
        match (src/{srcfile}, test/{testfile})
        dest <\pat>/({srcfile}, {testfile})
'''
