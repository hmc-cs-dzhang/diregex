import os
from diregex_semantics import Matcher
from diregex_parser import parse
import diregex_lexer
from diregex_ir import *
from regex_env import RegexEnv

print(os.getcwd())
os.chdir('../test/testdir')

def match(diregex):
    ast = parse(diregex)
    #print(ast)
    matcher = Matcher()
    emptyEnv = RegexEnv()

    for match, regexEnv in matcher.visit(ast, os.getcwd(), emptyEnv):
        shortenedMatch = {key:os.path.basename(val) for key, val in match.items()}
        print(shortenedMatch)
        #print(regexEnv.groups)


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

