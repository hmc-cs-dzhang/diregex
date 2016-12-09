import src

import re
import os
import functools

from parser import parse
from matcher import Matcher
from ir import *
from regex_env import RegexEnv

#os.chdir('../test/testdir3')

def findVarsExec(command):
    return set(re.findall(r"\{(\w+)\}", command))

def execCommand(command, varEnv, regexEnv):

    matchedEnvs = []

    #for varEnv, regexEnv in matcher.visit(ast, os.getcwd(), emptyEnv):

    #    if newEnv(varEnv, regexEnv, matchedEnvs):

    matchedEnvs.append((varEnv, regexEnv))
    parsedCommand = replVarsAndRegex(varEnv, regexEnv, command)
    os.system(parsedCommand)

def newEnv(varEnv, regexEnv, envs):
    ''' returns true if the current environment is not in the list of old envs'''
    for otherVarEnv, otherRegexEnv in envs:
        if varEnv == otherVarEnv and regexEnv == otherRegexEnv:
            return False
    return True

def replVarsAndRegex(varEnv, regexEnv, command):

    replacedVars = re.sub(r"\{\w+\}", functools.partial(replVars, varEnv), command)
    replacedRegex = re.sub(r"\\[1-9A-Za-z_]+", functools.partial(replRegex, regexEnv), replacedVars)
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
        return regexEnv.groupdict[newvar]

'''
diregex = 'parent/child[1-2]/*=c'
command = r"subl {c}"
test(diregex, command)
'''

