import os
import re
import itertools
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
        for var, name in self.visit(node.dirItem.dirName, path):
            if var:
                yield {var : os.path.join(path,name)}
            else:
                yield {}

    def visit_TreePattern_Child(self, node, path):
        # return node.dirItem matches with currNode and
        # visit tree pattern with child node
        parentMatches = self.visit(node.dirItem.dirName, path)
        for var, name in parentMatches:
            oneMatch = {}
            if var:
                oneMatch = {var : os.path.join(path,name)}

            # visit children
            newPath = os.path.join(path, name)
            children = self.visit(node.treePattern, newPath)

            for child in children:
                #if the node was named, it will be added to dict
                child.update(oneMatch)
                yield child


        # call visit for each of the children

    def visit_TreePattern_ListHelper(patterns, path, matches):
        if patterns == []:
            return
        for pattern in patterns:
            for match in self.visit(pattern, path, matches):
                yield visit_TreePattern_ListHelper(patterns[1:], path, matches)


    def visit_TreePattern_List(self, node, path):
        generators = [self.visit(treePattern, path) for treePattern in node.treePatterns]
        for result in itertools.product(*generators):
            matches = {}
            for match in result:
                matches.update(match)
            yield matches

    def visit_DirItem(self, node, currDir, matches):
        # call visit node.dirName to check that it matches the folder
        return self.visit(node.dirName, currDir)

    def visit_DirName(self, node, path):
        dirs = os.scandir(path)
        for d in dirs:
            match = re.fullmatch(node.regexPattern, d.name)
            if match:
                # if the variable is not null, add it to the dictionary
                yield node.var, match.string

