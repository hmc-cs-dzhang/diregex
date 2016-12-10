import src

from matcher import match
from subst import updateEnv
from tree_producer import produceDirTree
from parser import parse, parseAssign, parseMatch, parseDest
from ir import *
from regex_env import RegexEnv
from var_finder import findVars
from exec_shell import findVarsExec, execCommand
from match_pat import matchPattern


def run(program, path):
    """ The semantics function.  Runs a diregex program by parsing it, and then
    calling the various visitor methods."""

    varEnv = {}
    regexEnv = RegexEnv()

    # parse the program and extract the list of statements
    stmts = parse(program).stmts

    # There are three main semantic patterns:
    # 1) Match, followed by a Dest or shell command
    # 2) MatchPat, followed by a dest or shell command
    # 3) Dest, just a 'script' to create a directory tree
    i = 0
    while i < len(stmts):

        stmt = stmts[i]

        # Read in assignments, and add them to the environment
        if type(stmt) is Assign:
            varEnv, regexEnv = updateEnv(stmt.tree, varEnv, regexEnv)

        # Once we hit a match, iterate through all the matches, and
        # perform the action specified in the destination tree
        elif type(stmt) is Match:

            # find all the remaining variables used to know what to match with
            usedVars = set()
            for j in range(i + 1, len(stmts)):
                if type(stmts[j]) is Dest:
                    usedVars.update(findVars(stmts[j].tree, varEnv))

                elif type(stmts[j]) is Shell:
                    usedVars.update(findVarsExec(stmts[j].command))

                else:
                    raise TypeError("Type %s cannot be used after match" \
                        % type(stmts[j]).__name__)

            # Once we've gathered all the variables needed for the match,
            # perform the match.  Iterate through the dest and exec shell statements,
            # repeating each time there is a new match
            for newVars, newRegex in match(stmt.tree, path, usedVars, varEnv, regexEnv):

                for j in range(i + 1, len(stmts)):
                    if type(stmts[j]) is Dest:
                        produceDirTree(stmts[j].tree, path, newVars, newRegex)
                    elif type(stmts[j]) is Shell:
                        execCommand(stmts[j].command, newVars, newRegex)

            break

        # A MatchPat statement
        elif type(stmt) is MatchPat:

            for newRegex in matchPattern(stmt.params):

                for j in range(i + 1, len(stmts)):
                    if type(stmts[j]) is Dest:
                        produceDirTree(stmts[j].tree, path, {}, newRegex)
                    elif type(stmts[j]) is Shell:
                        execCommand(stmts[j].command, {}, newRegex)

            break
            # in case there were no matches
            print("nothing found")

        # Just a dest statement
        elif type(stmt) is Dest:
            produceDirTree(stmt.tree, path, varEnv, regexEnv)

        else:
            raise TypeError("Unknown type %s" % type(stmt).__name__)

        i += 1

