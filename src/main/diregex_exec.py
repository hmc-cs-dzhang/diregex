import re
import os
import functools

from diregex_parser import parse
from diregex_semantics import Matcher
import diregex_ir
from regex_env import RegexEnv

#os.chdir('../test/testdir3')

def test(diregex, command):
    ast = parse(diregex)
    matcher = Matcher()
    emptyEnv = RegexEnv()

    matchedEnvs = []

    for varEnv, regexEnv in matcher.visit(ast, os.getcwd(), emptyEnv):

        if newEnv(varEnv, regexEnv, matchedEnvs):
            matchedEnvs.append((varEnv, regexEnv))
            parsedCommand = exec(varEnv, regexEnv, command)
            print(parsedCommand)
            os.system(parsedCommand)

def newEnv(varEnv, regexEnv, envs):
    ''' returns true if the current environment is not in the list of old envs'''
    for otherVarEnv, otherRegexEnv in envs:
        if varEnv == otherVarEnv and regexEnv == otherRegexEnv:
            return False
    return True

def exec(varEnv, regexEnv, command):

    replacedVars = re.sub(r"\{\w+\}", functools.partial(replVars, varEnv), command)
    replacedRegex = re.sub(r"\\[1-9]", functools.partial(replRegex, regexEnv), replacedVars)
    return replacedRegex

def replVars(varEnv, matchobj):
    var = matchobj.group(0)
    newvar = var.strip(r"\{\}")
    path = varEnv[newvar]
    if path:
        return path
    else:
        raise Exception("variable {} does not exist".format(newvar))

def replRegex(regexEnv, matchobj):
    var = matchobj.group(0)
    newvar = var.strip("\\")
    if newvar.isdigit():
        n = int(newvar)
        if n > 0 and n <= len(regexEnv.groups):
            return regexEnv.groups[n-1]
        else:
            raise Exception("numbered pattern is out of bounds")
    else:
        raise Exception("named patterns are not supported")

'''
diregex = 'parent/child[1-2]/*=c'
command = r"subl {c}"
test(diregex, command)
'''
diregex = r'(src/<*>.cpp=srcfile, test/\1_test.cpp=testfile)'
command = r'''mkdir \1_dir
mv {srcfile} {testfile} \1_dir'''
test(diregex, command)
