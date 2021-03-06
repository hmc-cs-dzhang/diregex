import os
import shutil
from matcher import *
from ir import *
from regex_env import RegexEnv

"""
Creates a tree based on a Dest statement's tree pattern.
"""

class Producer(object):

    def visit(self, node, path, varEnv, regexEnv):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, path, varEnv, regexEnv)

    def generic_visit(self, node, path, varEnv, regexEnv):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_TreePatternDir(self, node, path, varEnv, regexEnv):
        return self.visit(node.dirItem, path, varEnv, regexEnv)

    def visit_TreePatternChild(self, node, path, varEnv, regexEnv):
        newPath = self.visit(node.dirItem, path, varEnv, regexEnv)
        return self.visit(node.treePattern, newPath, varEnv, regexEnv)

    def visit_TreePatternList(self, node, path, varEnv, regexEnv):
        for treePattern in node.treePatterns:
            self.visit(treePattern, path, varEnv, regexEnv)
        return path

    def visit_TreePatternVar(self, node, path, varEnv, regexEnv):
        var = node.var
        if var in varEnv:
            # move whatever the old file to the current location
            shutil.move(varEnv[var], path)

            # remove parent directory if it is empty
            parent = os.path.abspath(os.path.join(varEnv[var], os.pardir))
            try:
                os.rmdir(parent)
            except OSError:
                pass

            return varEnv[var]
        else:
            raise FooError("Variable '%s' does not exist" % var)

    def visit_DirName(self, node, path, varEnv, regexEnv):

        name = regexEnv.replaceBackreferences(RegexEnv.translateOnlyBackrefs(node.name))

        if name not in os.listdir(path):
            # create a new directory
            if not node.attr or node.attr == 'dir':
                os.mkdir(os.path.join(path, name))

            # create a new file
            elif node.attr == 'file':
                newFilePath = os.path.join(path, name)
                open(newFilePath, 'a').close()

        return os.path.join(path, name)



def produceDirTree(tree, path, varEnv=None, regexEnv=None):
    if not varEnv:
        varEnv = {}

    if not regexEnv:
        regexEnv = RegexEnv()

    producer = Producer()

    producer.visit(tree, path, varEnv, regexEnv)

class FooError(Exception):

    def __init__(self, err):
        self.err = err

