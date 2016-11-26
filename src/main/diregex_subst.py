from diregex_ir import *
from parsec_parser import parse
from copy import deepcopy


class Subst(object):
    def visit(self, node, env):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def generic_visit(self, node, currDir):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visitDir(self, node, env, tree):
        ''' abstract method for visiting a directory '''
        method_name = 'visitDir_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env, tree)

    ''' Go through the tree, vars with items in the environment '''
    def visit_TreePatternDir(self, node, env):
        newDirItem, newEnv = self.visitDir(node.dirItem, env, node)
        return TreePatternDir(newDirItem), newEnv

    def visit_TreePatternChild(self, node, env):
        # for now, assume that you cannot have {var}/child
        children, env1 = self.visit(node.treePattern, env)
        newTPat = TreePatternChild(node.dirItem, children)

        # must pass in the new tree pattern to update the environment,
        # in case any of children were variables that needed substituting
        # and node.dirItem must store the absyn
        dirItem, env2 = self.visitDir(node.dirItem, env, newTPat)
        env2.update(env1)
        return TreePatternChild(dirItem, children), env2

    def visit_TreePatternList(self, node, env):
        env2 = {}
        treePatterns = []

        for tpat in node.treePatterns:
            # for each child, aggregate the new tpats and update the environment
            newTPat, newEnv = self.visit(tpat, env)
            treePatterns.append(newTPat)
            env2.update(newEnv)

        # update env2 with the original environment
        env2.update(env)
        return TreePatternList(treePatterns), env2

    def visit_TreePatternDesc(self, node, env):
        newTPat, newEnv = self.visit(node.treePattern, env)
        return TreePatternDesc(newTPat), newEnv

    def visit_TreePatternVar(self, node, env):
        var = node.var
        if not var in env:
            raise Exception("variable %s is not been declared" % var)
        else:
            return env[var], env


    ############## Visiting DirItems ######################

    def visitDir_DirGlob(self, dirItem, env, _):
        return dirItem, env

    def visitDir_DirGlobWithVar(self, dirItem, env, node):
        ''' return a new environment, with the added variable '''
        if dirItem.var in env:
            raise Exception("variable %s has already been declared" % dirItem.var)

        env.update({dirItem.var: node})
        return dirItem, env

def test():
    subst = Subst()

    ast = parse("srcfile=<pat=*>.cpp")

    env = {}
    _, env = subst.visit(ast, env)

    bst = parse("testfile=<\pat>_test.cpp")
    _, env = subst.visit(bst, env)

    cst = parse(r"(src/{srcfile}, test/{testfile})")
    res, env = subst.visit(cst, env)

    '''
    ast = TreePatternChild(
        DirGlobWithVar("var1", "*glob*"),
        TreePatternChild(
            DirGlobWithVar("var2", "*glob2"),
            TreePatternVar("var")))

    entry = TreePatternDir(DirGlob("*hihi*"))

    env = {"var": entry}

    result, newEnv = subst.visit(ast, env)

    print(result)
    print("env:")
    print(newEnv)
    '''
test()

