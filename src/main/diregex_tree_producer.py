import os
import shutil
from diregex_semantics import *
from diregex_ir import *

class Producer(object):

    def visit(self, node, path, env):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, path, env)

    def generic_visit(self, node, path, env):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_TreePatternDir(self, node, path, env):
        return self.visit(node.dirName, path, env)

    def visit_TreePatternChild(self, node, path, env):
        newPath = self.visit(node.dirName, path, env)
        return self.visit(node.treePattern, newPath, env)

    def visit_TreePatternList(self, node, path, env):
        for treePattern in node.treePatterns:
            self.visit(treePattern, path, env)
        return path


    def visit_DirName(self, node, path, env):
        name = node.regexPattern
        if name:
            if name in os.listdir(path):
                print("directory " + name + " already exists")
            else:
                os.mkdir(os.path.join(path, name))

            return os.path.join(path, name)

        else:
            var = node.var
            if var in env:
                # create the new file
                shutil.move(env[var], path)
                return env[var]
            else:
                raise Exception('Variable %s does not exist' % var)




def produceDirTree(tree, path, env={}):
    producer = Producer()

    producer.visit(tree, path, env)

