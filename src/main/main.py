from diregex_semantics import match
from parsec_parser import parse
from diregex_subst import updateEnv
from diregex_tree_producer import produceDirTree
import os

def main():

    os.chdir('../test/testdir4')
    os.mkdir('src')
    os.mkdir('test')
    open('src/foo.cpp').close()
    open('test/foo_test.cpp').close()

    program = r'''
        srcfile = <pat=*>.cpp
        testfile = <\pat>_test.cpp
        match (src/{srcfile}, test/{testfile})
        dest <\pat>/({srcfile}, {testfile})
        '''

    ast = parse(program)

    env = updateEnv(ast.stmts[0])
    env = updateEnv(ast.stmts[1], env)

    matches = match(ast.stmts[2], path, env)
    for match in matches:
        produceDirTree(ast.stmts[3], path, env)

main()
