import sys
sys.path.append("../ir")
sys.path.insert(0, "../parser")

from ir import *
from parser import parse
from pattern_parser import parsePattern

from copy import deepcopy


class Subst(object):
    '''
    All this class does is iterate through the tree, and update the environment
    with new named nodes
    '''

    def visit(self, node, varEnv, regexEnv):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, varEnv, regexEnv)

    def generic_visit(self, node, *_):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_TreePatternDir(self, node, varEnv, regexEnv):
        ''' Go through the tree, vars with items in the var environment '''
        self.visit(node.dirItem, varEnv, regexEnv)
        if node.var:
            varEnv.update({node.var: node})

    def visit_TreePatternChild(self, node, varEnv, regexEnv):
        self.visit(node.treePattern, varEnv, regexEnv)
        self.visit(node.dirItem, varEnv, regexEnv)
        if node.var:
            varEnv.update({node.var: node})

    def visit_TreePatternList(self, node, varEnv, regexEnv):

        for tpat in node.treePatterns:
            # visit each child, which will update the varEnvironment
            self.visit(tpat, varEnv, regexEnv)

        if node.var:
            varEnv.update({node.var: node})

    def visit_TreePatternDesc(self, node, varEnv, regexEnv):
        self.visit(node.treePattern, varEnv, regexEnv)
        if node.var:
            varEnv.update({node.var, node})

    def visit_TreePatternVar(self, node, varEnv, regexEnv):
        if node.var not in varEnv:
            raise KeyError("variable '%s' does not exist" % node.var)
        pass

    ############## Visiting DirItems ######################

    def visit_DirGlob(self, dirItem, _, regexEnv):
        for name, pat in parsePattern(dirItem.glob):

            if name in regexEnv.groupdict:
                raise KeyError("pattern name '%s' already exists" % name)

            regexEnv.groupdict[name] = pat



def updateEnv(node, varEnv=None, regexEnv=None):
    subst = Subst()

    if not varEnv:
        varEnv = {}

    if not regexEnv:
        regexEnv = {}

    subst.visit(node, varEnv, regexEnv)
    return varEnv, regexEnv
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
