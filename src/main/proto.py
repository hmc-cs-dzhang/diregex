import os
from diregex_semantics import Matcher
from diregex_parser import parse
import diregex_lexer
from diregex_ir import *

print(os.getcwd())
os.chdir('../test/testdir')

def match(diregex):
    ast = parse(diregex)
    print(ast)
    matcher = Matcher()
    matches = {}

    for match in matcher.visit(ast, os.getcwd()):
        print(match)


print("----Example 1------")
match('"parent"=p/"child[1-2]"')

print("----Example 2------")
match('"[a-z]*"=foo/"[a-z0-9]*"=bar')

print("----Example 3------")
match('"parent"=foo/"child[1-2]*"=bar/"[a-z0-9.]*"')

print("----Example 4------")
match('"parent"/("ch[a-z0-9]*"=c1, "[a-z0-9]*"=c2)')

print("----Example 5------")
match('"parent"=p/>"file[a-z0-9]*.txt"=q')

print("----Example 6------")
match('"[a-z]*"/(>"[a-z0-9\.]*"=var1, "child[a-z0-9]*"=var2)')

# should return nothing
print("----Example 7------")
match('"butt"')

