import os
import re
import itertools
from functools import partialmethod
from diregex_ir import *
from regex_env import RegexEnv

## Use the visitor pattern, from Let's Build a Simple Interpreter
## Visits each node of the abstarct syntax tree to build up a
## candidate match, which is a dictionary mapping variable names to
## the directories that they match.

class NodeVisitor(object):

    def visit(self, node, currDir, regexEnv):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, currDir, regexEnv)

    def generic_visit(self, node, currDir):
        raise Exception('No visit_{} method'.format(type(node).__name__))

'''
Each function takes in a regex environment, which contains the expression
variables that have been matched so far.  They then output a new variable
environment, containing the variables that matched with entire directory
names, and a regexEnv if there was a match.
'''
class Matcher(NodeVisitor):

    def visit(self, node, currDir, regexEnv):
        return NodeVisitor.visit(self, node, currDir, regexEnv)

    ''' Matches a TreePatternDir against a path.  Calls the visit method
        on the directory name.  If the pattern was bound to a variable, adds
        that variable to the list of matches.  Otherwise, just yields a match '''
    def visit_TreePatternDir(self, node, path, regexEnv):
        # return node.dirItem matches with the current node
        for varEnv, newRegexEnv, _ in self.visit(node.dirItem, path, regexEnv):
            yield varEnv, newRegexEnv

    ''' matches against the parent and the children.  Combines the match
        dictionaries, and returns the result'''
    def visit_TreePatternChild(self, node, path, regexEnv):
        parentMatches = self.visit(node.dirItem, path, regexEnv)

        # calls visit_DirGlob, which in addition returns the path to child
        # found in the match, so that you can search the child directory
        for varEnv, regexEnv, pathToChild, in parentMatches:

            # receive generators from each of the children
            childrenMatches = self.visit(node.treePattern, pathToChild, regexEnv)

            for newVarEnv, newRegexEnv in childrenMatches:
                # merge the two varEnvs
                newVarEnv.update(varEnv)
                # regexEnv already merged when regex match happened
                yield newVarEnv, newRegexEnv


    ''' matches against a list of tree patterns.  For each pattern in the list,
        calls visit method to obtain a generator.  Then takes the product of all
        those generators to yield a result'''
    def visit_TreePatternList(self, node, path, regexEnv):
        visit_method = getattr(self, 'visit')
        visitData = [(tree, path) for tree in node.treePatterns]
        for varEnv, newRegexEnv in self.lazyProduct(visitData, regexEnv):
            yield varEnv, newRegexEnv

    '''
    Finds the cartesian product of the results of the different elements in the
    list.  This is different from taking the `Product` of generators, which
    calls each function once to build up a list, and then takes the product of
    that list.  Instead, lazyProduct will make a function call again instead of
    storing the result in a list, which is needed because the regex environment
    changes
    '''
    def lazyProduct(self, visitData, regexEnv):
        if len(visitData) == 0:
            raise Exception("Can't have an empty list")

        firstNode = visitData[0][0]
        firstPath = visitData[0][1]

        if len(visitData) == 1:

            for varEnv, regexEnv in self.visit(firstNode, firstPath, regexEnv):
                yield varEnv, regexEnv

        else:

            for varEnv1, regexEnv1 in self.visit(firstNode, firstPath, regexEnv):
                for varEnv2, regexEnv2 in self.lazyProduct(visitData[1:], regexEnv1):
                    varEnv2.update(varEnv1)
                    yield varEnv2, regexEnv2


    def visit_TreePatternDesc(self, node, path, regexEnv):

        for descPath, _, _ in os.walk(path):
            for varEnv, newRegexEnv in self.visit(node.treePattern, descPath, regexEnv):
                yield varEnv, newRegexEnv

    ''' Scans the directory in path, looking for something that matches the node's
        regex pattern.  Yields every match of the directory name and the node's
        variable '''
    def visit_DirGlob(self, node, path, regexEnv):

        for dirItem in os.scandir(path):
            newRegexEnv = regexEnv.match(node.glob, dirItem.name)
            if newRegexEnv: # got a match, return the updated regex env
                newPath = os.path.join(path, dirItem.name)
                varEnv = {}
                yield varEnv, newRegexEnv, newPath

    def visit_DirGlobWithVar(self, node, path, regexEnv):
        for dirItem in os.scandir(path):
            newRegexEnv = regexEnv.match(node.glob, dirItem.name)
            if newRegexEnv:
                newPath = os.path.join(path, dirItem.name)
                varEnv = {node.var: newPath}
                yield varEnv, newRegexEnv, newPath

    def visit_DirVar(self, node, path, regexEnv):
        raise NotImplementedError("Var not implemented yet")


def match(tree, path):
    matcher = Matcher()
    regexEnv = RegexEnv()
    matches = matcher.visit(tree, path, regexEnv)

    varEnvs = []

    for varEnv, _ in matches:
        # don't print duplicates
        if newEnv(varEnv, varEnvs):
            varEnvs += [varEnv]
            yield varEnv

def newEnv(varEnv, varEnvs):
    for otherVarEnv in varEnvs:
        if varEnv == otherVarEnv:
            return False
    return True

def allMatches(tree, path):

    matchList = []
    for varEnv in match(tree, path):
        baseVarEnv = {v: os.path.basename(p) for v, p in varEnv.items()}
        matchList.append(baseVarEnv)
        '''
        for var in varEnv:
            path = varEnv[var]
            if var in varSets:
                varSets[var] = {path}
            else:
                varSets[var].add(path)
        '''
    return matchList
