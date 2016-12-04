import sys
sys.path.append("../ir")

import os
import re
import itertools
from functools import partialmethod
from ir import *
from regex_env import RegexEnv

## Use the visitor pattern, from Let's Build a Simple Interpreter
## Visits each node of the abstarct syntax tree to build up a
## candidate match, which is a dictionary mapping variable names to
## the directories that they match.

class NodeVisitor(object):

    def visit(self, node, currDir, varEnv, regexEnv):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, currDir, varEnv, regexEnv)

    def generic_visit(self, node, currDir, varEnv, regexEnv):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Matcher(NodeVisitor):
    '''
    Each function takes in a regex environment, which contains the expression
    variables that have been matched so far.  They then output a new variable
    environment, containing the variables that matched with entire directory
    names, and a regexEnv if there was a match.
    '''

    def visit(self, node, currDir, varEnv, regexEnv):
        return NodeVisitor.visit(self, node, currDir, varEnv, regexEnv)


    def visit_TreePatternDir(self, node, path, varEnv, regexEnv):
        '''
        Matches a TreePatternDir against a path.  If the pattern was named,
        returns a new environment mapping the variable name to the path.
        Otherwise, returns and empty environment.  Also returns the updated
        RegexEnv so that future patterns can refer back to it.
        '''
        for newPath, newRegexEnv in self.visit(node.dirItem, path, varEnv, regexEnv):
            yield ({node.var: newPath} if node.var else {}), newRegexEnv

    def visit_TreePatternChild(self, node, path, varEnv, regexEnv):
        '''
        Matches against the parent and the children.  Combines the match
        dictionaries, and returns the result
        '''

        # calls visit_DirGlob, which in addition returns the path to child
        # found in the match, so that you can search the child directory
        for newPath, regexEnv in self.visit(node.dirItem, path, varEnv, regexEnv):

            # if this is a named node
            newVarEnv = ({node.var: newPath} if node.var else {})

            # receive generators from each of the children
            childrenMatches = self.visit(node.treePattern, newPath, varEnv, regexEnv)

            for childVarEnv, newRegexEnv in childrenMatches:
                # merge the two varEnvs
                childVarEnv.update(newVarEnv)
                # regexEnv already merged when regex match happened
                yield childVarEnv, newRegexEnv


    def visit_TreePatternList(self, node, path, varEnv, regexEnv):
        '''
        Matches against a list of tree patterns.  For each pattern in the list,
        calls visit method to obtain a generator.  Then takes the product of all
        those generators to yield a result
        '''
        visit_method = getattr(self, 'visit')
        visitData = [(tree, path, varEnv) for tree in node.treePatterns]
        for newVarEnv, newRegexEnv in self.lazyProduct(visitData, regexEnv):
            # if the node is named, add a tuple of the values to the environment
            if node.var:
                newEntry = {node.var: tuple(varEnv.values())}
                newVarEnv.update(newEntry)

            yield newVarEnv, newRegexEnv


    def lazyProduct(self, visitData, regexEnv):
        '''
        Finds the cartesian product of the results of the different elements in
        the list.  This is different from taking the `Product` of generators,
        which calls each function once to build up a list, and then takes the
        product of that list.  Instead, lazyProduct will make a function call
        again instead of storing the result in a list, which is needed because
        the regex environment changes
        '''
        if len(visitData) == 0:
            raise Exception("Can't have an empty list")

        (firstNode, firstPath, firstVarEnv) = visitData[0]

        if len(visitData) == 1:

            for varEnv, regexEnv in self.visit(firstNode, firstPath, firstVarEnv, regexEnv):
                yield varEnv, regexEnv

        else:

            for varEnv1, regexEnv1 in self.visit(firstNode, firstPath, firstVarEnv, regexEnv):
                for varEnv2, regexEnv2 in self.lazyProduct(visitData[1:], regexEnv1):
                    varEnv2.update(varEnv1)
                    yield varEnv2, regexEnv2


    def visit_TreePatternDesc(self, node, path, varEnv, regexEnv):
        '''
        Visits a treePattern descendant, of the form `**/`.
        '''
        if node.var:
            raise Exception("Cannot name TreePatternDesc")
        for descPath, _, _ in os.walk(path):
            for newVarEnv, newRegexEnv in self.visit(node.treePattern, descPath, varEnv, regexEnv):
                yield newVarEnv, newRegexEnv

    def visit_TreePatternVar(self, node, path, varEnv, regexEnv):
        '''
        Visits a treePattern variable of the form {var}, which looks it up and
        the varEnv and continuous to traverse down that tree
        '''
        var = node.var
        if var not in varEnv:
            raise Exception("variable %s has not be declared" % var)
        else:
            newNode = varEnv[var]
            for newVarEnv, newRegexEnv in self.visit(newNode, path, varEnv, regexEnv):
                yield newVarEnv, newRegexEnv


    def visit_DirGlob(self, node, path, _, regexEnv):
        '''
        Scans the directory in path, looking for something that matches the node's
        regex pattern.  Yields every match of the directory name and the node's
        variable
        '''
        for dirItem in os.scandir(path):
            newRegexEnv = regexEnv.match(node.glob, dirItem.name)
            if newRegexEnv: # got a match, return the updated regex env
                newPath = os.path.join(path, dirItem.name)
                yield newPath, newRegexEnv

def match(tree, path, varEnv = None):
    if not varEnv:
        varEnv = {}

    matcher = Matcher()
    regexEnv = RegexEnv()
    matches = matcher.visit(tree, path, varEnv, regexEnv)

    varEnvs = []

    for newVarEnv, _ in matches:
        # don't print duplicates
        if newEnv(newVarEnv, varEnvs):
            varEnvs += [newVarEnv]
            yield newVarEnv

def newEnv(varEnv, varEnvs):
    for otherVarEnv in varEnvs:
        if varEnv == otherVarEnv:
            return False
    return True

def allMatches(tree, path, varEnv = None):
    if not varEnv:
        varEnv = {}

    matchList = []
    for varEnv in match(tree, path, varEnv):
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