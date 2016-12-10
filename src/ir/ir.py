
# abstact class for a node of the AST
class Node(object):

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return self.prettyPrint(0)

    def prettyPrint(self, n):
        ''' pretty print on new lines for debugging purposes '''
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
    ''' a program consists of a set of statements '''
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
    '''
    A statement is either a Match, a Dest, Assign, Shell, or MatchPat
    Match, Dest, and Assign all primarily hold tree patterns.
    MatchPat holds params, and are meant for iterating through lists to create
    a destination tree.
    A shell merely holds the string to be executed by the commad line.
    '''
    pass

class Match(Stmt):
    ''' a match tree '''
    def __init__(self, tree):
        self.tree = tree

class Dest(Stmt):
    ''' a destination tree '''
    def __init__(self, tree):
        self.tree = tree

class Assign(Stmt):
    ''' The variable name is stored in the root node of the tree '''
    def __init__(self, tree):
        self.tree = tree

class Shell(Stmt):
    ''' contains the string to be executed on the command line'''
    def __init__(self, command):
        self.command = command

class MatchPat(Stmt):
    def __init__(self, params):
        self.params = params

class Params(Node):
    def __init__(self, name, matches):
        self.name = name
        self.matches = matches



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
    """ Either a DirGlob or a DirName """
    pass

class DirGlob(DirItem):
    """ A dirItem specified by a glob.  Used in matches and assignments"""
    def __init__(self, glob, attr=None):
        self.glob = glob
        self.attr = attr

    def __repr__(self):
        return "DirGlob(%s)" % self.glob

class DirName(DirItem):
    """ A dirItem specified by a name, as opposed to a glob or a regular
    expression.  Used in dest trees"""
    def __init__(self, name, attr=None):
        self.name = name
        self.attr = attr

    def __repr__(self):
        return "DirName(%s, %s)" % (self.name, self.attr)
