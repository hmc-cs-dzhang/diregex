import sys
sys.path.append("../semantics")
sys.path.append("../ir")
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

    varEnv = {}
    regexEnv = RegexEnv()

    stmts = parse(program).stmts
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

            print("used vars is %s" % usedVars)

            '''
            if type(stmts[i + 1]) is Dest:
                usedVars = findVars(stmts[i + 1].tree, varEnv)

            elif type(stmts[i + 1]) is Shell:
                usedVars = findVarsExec(stmts[i + 1].command)

            else:
            '''

            for newVars, newRegex in match(stmt.tree, path, usedVars, varEnv, regexEnv):

                for j in range(i + 1, len(stmts)):
                    if type(stmts[j]) is Dest:
                        produceDirTree(stmts[j].tree, path, newVars, newRegex)
                    elif type(stmts[j]) is Shell:
                        execCommand(stmts[j].command, newVars, newRegex)

            break

        elif type(stmt) is Dest:
            produceDirTree(stmt.tree, path, varEnv, regexEnv)

        elif type(stmt) is MatchPat:

            for newRegex in matchPattern(stmt.params):

                for j in range(i + 1, len(stmts)):
                    if type(stmts[j]) is Dest:
                        produceDirTree(stmts[j].tree, path, {}, newRegex)
                    elif type(stmts[j]) is Shell:
                        execCommand(stmts[j].command, {}, newRegex)

            break
            print("nothing found")

        else:
            raise TypeError("Unknown type %s" % type(stmt).__name__)

        i += 1


class Interpreter(object):

    def visit(self, node, path, env):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, path, env)

    def generic_visit(self, node, path, env):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_Prog(self, node, path, env):
        for stmt in node.stmts:
            env = self.visit(stmt, path, env)
        return env

    def visit_Match(self, node, path, env):
        return match(node.tree, path, env)

    def visit_Dest(self, node, path, env):
        return produceDirTree(node.tree, path, env)

    def visit_Assign(self, node, path, env):
        env = updateEnv(node.tree, env)
        #print(env)
        return env

'''
def run(ast, path, env):
    interpreter = Interpreter()
    interpreter.visit(ast, path, env)
    print("done")
'''
