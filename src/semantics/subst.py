import src

from ir import *
from parser import parse
from pattern_parser import parsePattern

from copy import deepcopy


class Subst(object):
    '''
    This class iterates through the tree, and updates the regex Environment
    and variable environments with new named nodes
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
        ''' visit the current directory and the children ones '''
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
    ''' main method called by semantics.  Given a var environment and a
    regex environment, creates a Subst tree visitor, adds to these
    environments, and returns them '''
    subst = Subst()

    if not varEnv:
        varEnv = {}

    if not regexEnv:
        regexEnv = {}

    subst.visit(node, varEnv, regexEnv)
    return varEnv, regexEnv

