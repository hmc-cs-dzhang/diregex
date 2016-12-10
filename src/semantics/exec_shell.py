import src

import re
import os
import functools
from parser import parse
from matcher import Matcher
from ir import *
from regex_env import RegexEnv


def findVarsExec(command):
    """ like findVars, but for ExecShell strings.  Finds the variables that were
    referenced in a shell statement, so that match knows what to look for
    """
    return set(re.findall(r"\{(\w+)\}", command))

def execCommand(command, varEnv, regexEnv):
    """ execute a command by first replacing the variables and regex with values
    from the environment, then calling os.system"""

    parsedCommand = replVarsAndRegex(varEnv, regexEnv, command)
    os.system(parsedCommand)

def replVarsAndRegex(varEnv, regexEnv, command):
    """ Uses the regular expression sub method to replacement functions to
    replace variables and regular expressions from the respective environments"""

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
        raise NameError("variable {} does not exist".format(newvar))

def replRegex(regexEnv, matchobj):
    var = matchobj.group(0)
    newvar = var.strip("\\")
    if newvar.isdigit():
        n = int(newvar)
        if n > 0 and n <= len(regexEnv.groups):
            return regexEnv.groups[n-1]
        else:
            raise IndexError("numbered pattern is out of bounds")
    else:
        return regexEnv.groupdict[newvar]


