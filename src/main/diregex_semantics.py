import os
import re
import itertools
from diregex_ir import *

## Use the visitor pattern, from Let's Build a Simple Interpreter
## Visits each node of the abstarct syntax tree to build up a
## candidate match, which is a dictionary mapping variable names to
## the directories that they match.

class NodeVisitor(object):

    def __init__(self):
        self.groupNames = {}
        self.groupNumber = 0

    def visit(self, node, currDir):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, currDir)

    def generic_visit(self, node, currDir):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Matcher(NodeVisitor):

    ''' Matches a TreePatternDir against a path.  Calls the visit method
        on the directory name.  If the pattern was bound to a variable, adds
        that variable to the list of matches.  Otherwise, just yields a match '''
    def visit_TreePatternDir(self, node, path):
        # return node.dirName matches with the current node
        for var, name in self.visit(node.dirName, path):
            if var:
                yield {var : os.path.join(path, name)}
            else:
                yield {}

    ''' matches against the parent and the children.  Combines the match
        dictionaries, and returns the result'''
    def visit_TreePatternChild(self, node, path):
        parentMatches = self.visit(node.dirName, path)

        for var, name in parentMatches:
            oneMatch = {}
            newPath = os.path.join(path, name)
            if var:
                oneMatch = {var : newPath}

            children = self.visit(node.treePattern, newPath)

            for child in children:
                # if the node was named, it will be added to child matches dictionary
                child.update(oneMatch)
                yield child


    ''' matches against a list of tree patterns.  For each pattern in the list,
        calls visit method to obtain a generator.  Then takes the product of all
        those generators to yield a result'''
    def visit_TreePatternList(self, node, path):
        generators = [self.visit(treePattern, path) for treePattern in node.treePatterns]
        for result in itertools.product(*generators):
            matches = {}
            for match in result:
                matches.update(match)
            yield matches

    def visit_TreePatternDescendant(self, node, path):
        for descPath, _, _ in os.walk(path):
            for match in self.visit(node.treePattern, descPath):
                yield match

    ''' Scans the directory in path, looking for something that matches the node's
        regex pattern.  Yields every match of the directory name and the node's
        variable '''
    def visit_DirName(self, node, path):
        for d in os.scandir(path):
            match = re.fullmatch(node.regexPattern, d.name)
            if match:
                yield node.var, match.string


def match(tree, path):
    matcher = Matcher()
    matches = matcher.visit(tree, path)
    matchset = []
    for match in matches:
        print(match)
        matchset.append(match)

    return matchset
