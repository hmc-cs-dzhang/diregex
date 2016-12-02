import os
import shutil
from semantics import *
from ir import *

class Producer(object):

    def visit(self, node, path, env):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, path, env)

    def generic_visit(self, node, path, env):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_TreePatternDir(self, node, path, env):
        return self.visit(node.dirItem, path, env)

    def visit_TreePatternChild(self, node, path, env):
        newPath = self.visit(node.dirItem, path, env)
        return self.visit(node.treePattern, newPath, env)

    def visit_TreePatternList(self, node, path, env):
        for treePattern in node.treePatterns:
            self.visit(treePattern, path, env)
        return path

    def visit_TreePatternVar(self, node, path, env):
        var = node.var
        if var in env:
            # move whatever the old file to the current location
            shutil.move(env[var], path)
            return env[var]
        else:
            raise Exception('Variable %s does not exist' % var)

    def visit_DirGlob(self, node, path, env):
        name = node.glob
        if name in os.listdir(path):
            print("directory " + name + " already exists")
        else:
            os.mkdir(os.path.join(path, name))

        return os.path.join(path, name)



def produceDirTree(tree, path, env=None):
    if not env:
        env = {}

    producer = Producer()

    producer.visit(tree, path, env)

