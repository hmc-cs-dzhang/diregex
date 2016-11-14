import os
from diregex_semantics import Matcher
from diregex_parser import parse
import diregex_lexer
from diregex_ir import *

print(os.getcwd())
os.chdir('../test/testdir')

def match(diregex):
    ast = parse(diregex)

    matcher = Matcher()
    matches = matcher.visit(ast, os.getcwd())
    for match in matches:
        print(match)


print("----Example 1------")
match("\"parent\"=p")

print("----Example 2------")
match("\"[a-z]*\"=foo/\"[a-z0-9]*\"=bar")

print("----Example 3------")
match("\"parent\"/(\"ch[a-z0-9]*\", \"[a-z0-9]*\")")

