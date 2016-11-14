import os
import re
from diregex_ir import *

## Use the visitor pattern, from Let's Build a Simple Interpreter

class NodeVisitor(object):
    def visit(self, node, currDir):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, currDir)

    def generic_visit(self, node, currDir):
        #print(node)
        #print(currDir)
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Matcher(NodeVisitor):

    def visit_TreePattern_Dir(self, node, path):
        # return node.dirItem matches with the current node
        return self.visit(node.dirItem.dirName, path)

    def visit_TreePattern_Child(self, node, path):
        # return node.dirItem matches with currNode and
        # visit tree pattern with child node
        names = self.visit(node.dirItem.dirName, path)
        for name in names:
            newPath = os.path.join(path, name)
            children = self.visit(node.treePattern, newPath)
            for child in children:
                yield name + ", " + repr(child)


    def visit_TreePattern_List(self, node, path):
        patterns = []
        for pattern in node.treePatterns:
            match = self.visit(pattern, path)
            thisMatch = []
            for m in match:
                thisMatch += [m]
            patterns += [thisMatch]

        return patterns

        # call visit for each of the children

    def visit_DirItem(self, node, currDir):
        # call visit node.dirName to check that it matches the folder
        return self.visit(node.dirName, currDir)

    def visit_DirName(self, node, path):
        dirs = os.scandir(path)
        for d in dirs:
            match = re.fullmatch(node.regexPattern, d.name)
            if match:
                yield match.string

