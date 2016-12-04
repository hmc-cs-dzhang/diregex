## Intermediate Representation for Diregex
## Used this as guide:
##  https://ruslanspivak.com/lsbasi-part7/

# See diregex_parser for grammar details


# abstact class for a node of the AST
class Node(object):

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    '''
    def __repr__(self):
        import pprint
        return pprint.pprint(self)
    '''
    def __repr__(self):
        return self.prettyPrint(0)

    def prettyPrint(self, n):
        tab = "  "
        name = type(self).__name__
        st = tab*n + "%s" % name + "(\n"

        for val in self.__dict__.values():
            if issubclass(type(val), TreePattern):
                st += val.prettyPrint(n + 1)
                st += '\n'
            else:
                st += tab*(n + 1) + "%s\n" % repr(val)
        st += tab*n + ")"
        return st

class Prog(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def __eq__(self, other):
        if len(self.stmts) != len(other.stmts):
            return False
        for i in range(len(self.stmts)):
            if self.stmts[i] != other.stmts[i]:
                 return False
        return True

class Stmt(Node):
    pass

class Match(Stmt):
    def __init__(self, tree):
        self.tree = tree

class Dest(Stmt):
    def __init__(self, tree):
        self.tree = tree

class Assign(Stmt):
    # The variable name is stored in the root node of the tree
    def __init__(self, tree):
        self.tree = tree

# abstract class, representing the three cases of tree patterns
class TreePattern(Stmt):
    pass

class TreePatternDir(TreePattern):
    def __init__(self, dirItem, var=None):
        self.dirItem = dirItem
        self.var = var

class TreePatternChild(TreePattern):
    def __init__(self, dirItem, treePattern, var=None):
        self.dirItem = dirItem
        self.treePattern = treePattern
        self.var = var

''' Like a TreePatternChild, but matches in current directory
    or any descendant'''
class TreePatternDesc(TreePattern):
    def __init__(self, treePattern, var=None):
        self.treePattern = treePattern
        self.var = var

class TreePatternList(TreePattern):
    # takes in a list of tree patterns
    def __init__(self, treePatterns, var=None):
        self.treePatterns = treePatterns
        self.var = var

class TreePatternVar(TreePattern):
    '''refers to an existing var in the ast'''
    def __init__(self, var):
        self.var = var

class DirItem(Node):
    pass

class DirGlob(DirItem):
    def __init__(self, glob):
        self.glob = glob

    def __repr__(self):
        return "DirGlob(%s)" % self.glob

class DirName(DirItem):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "DirName(%s)" % self.name
