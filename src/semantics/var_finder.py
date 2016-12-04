from ir import *

class VarFinder(object):
    """ stores all the varsUsed referenced in a tree-pattern into a set """

    def visit(self, node, varEnv, varsUsed):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, varEnv, varsUsed)

    def generic_visit(self, node, varEnv, varsUsed):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_TreePatternDir(self, *_):
        pass

    def visit_TreePatternChild(self, node, varEnv, varsUsed):
        self.visit(node.treePattern, varEnv, varsUsed)

    def visit_TreePatternList(self, node, varEnv, varsUsed):
        for treePattern in node.treePatterns:
            self.visit(treePattern, varEnv, varsUsed)

    def visit_TreePatternDesc(self, *_):
        raise Exception("descendant pattern '**' cannot be in a dest tree")

    def visit_TreePatternVar(self, node, varEnv, varsUsed):
        """
        If we encounter a TreePatternVar, add the varname to the list of
        vars encountered, and continue to traverse through the var's ast
        """
        varsUsed.add(node.var)
        if node.var in varEnv:
            newNode = varEnv[node.var]
            self.visit(newNode, varEnv, varsUsed)

def findVars(ast, varEnv=None):
    if not varEnv:
        varEnv = {}

    varFinder = VarFinder()
    varsUsed = set()

    varFinder.visit(ast, varEnv, varsUsed)

    return varsUsed
