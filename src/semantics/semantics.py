import sys
sys.path.append("../semantics")
sys.path.append("../ir")
sys.path.insert(0, "../parser")

from matcher import match
from subst import updateEnv
from tree_producer import produceDirTree
from parser import parse, parseAssign, parseMatch, parseDest
from ir import *
from regex_env import RegexEnv


def run(program):

    path = "../../test/testdir4"
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
            dest = stmts[i + 1]
            if not type(dest) is Dest:
                raise TypeError("Match must be followed by a Dest")

            for newVars, newRegex in match(stmt.tree, path, varEnv, regexEnv):
                produceDirTree(dest.tree, path, newVars, newRegex)

            break

        elif type(stmt) is Dest:
            raise TypeError("Dest must be preceded by Match")

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
            #print(env)
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
