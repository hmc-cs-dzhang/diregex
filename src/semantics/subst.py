import sys
sys.path.append("../ir")
sys.path.insert(0, "../parser")

from ir import *
from parser import parse
from copy import deepcopy


class Subst(object):
    '''
    All this class does is iterate through the tree, and update the environment
    with new named nodes
    '''

    def visit(self, node, env):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def generic_visit(self, node, currDir):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_TreePatternDir(self, node, env):
        ''' Go through the tree, vars with items in the environment '''
        self.visit(node.dirItem, env)
        if node.var:
            env.update({node.var: node})

    def visit_TreePatternChild(self, node, env):
        self.visit(node.treePattern, env)
        self.visit(node.dirItem, env)
        if node.var:
            env.update({node.var: node})

    def visit_TreePatternList(self, node, env):

        for tpat in node.treePatterns:
            # visit each child, which will update the environment
            self.visit(tpat, env)

        if node.var:
            env.update({node.var: node})

    def visit_TreePatternDesc(self, node, env):
        self.visit(node.treePattern, env)
        if node.var:
            env.update({node.var, node})

    def visit_TreePatternVar(self, node, env):
        var = node.var
        if not var in env:
            raise Exception("variable %s has not been declared" % var)
        else:
            return env[var], env


    ############## Visiting DirItems ######################

    def visit_DirGlob(self, dirItem, env):
        #todo: update a regex env
        pass

def updateEnv(node, env = None):
    subst = Subst()

    if not env:
        env = {}

    subst.visit(node, env)
    return env
'''
def test():
    subst = Subst()

    ast = parse("srcfile=<pat=*>.cpp")

    env = {}
    subst.visit(ast, env)

    bst = parse("testfile=<\pat>_test.cpp")
    subst.visit(bst, env)

    cst = parse(r"list=(src/{srcfile}, test/{testfile})")
    subst.visit(cst, env)
    print(env)

test()
'''
