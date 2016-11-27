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

# abstract class, representing the three cases of tree patterns
class TreePattern(Node):
    pass

class TreePatternDir(TreePattern):
    def __init__(self, dirItem):
        self.dirItem = dirItem

class TreePatternChild(TreePattern):
    def __init__(self, dirItem, treePattern):
        self.dirItem = dirItem
        self.treePattern = treePattern

''' Like a TreePatternChild, but matches in current directory
    or any descendant'''
class TreePatternDesc(TreePattern):
    def __init__(self, treePattern):
        self.treePattern = treePattern

class TreePatternList(TreePattern):
    # takes in a list of tree patterns
    def __init__(self, treePatterns):
        self.treePatterns = treePatterns

class TreePatternVar(TreePattern):
    def __init__(self, var):
        self.var = var

class DirItem(Node):
    pass

class DirGlob(DirItem):
    def __init__(self, glob):
        self.glob = glob

    def __repr__(self):
        return "DirGlob(%s)" % self.glob

class DirVar(DirItem):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return "DirVar(%s)" % self.var

class DirGlobWithVar(DirItem):
    def __init__(self, var, glob):
        self.var = var
        self.glob = glob

    def __repr__(self):
        return "DirGlobWithVar(%s, %s)" % (self.var, self.glob)

ast = TreePatternDesc(
    TreePatternChild(
        DirGlob("*hi"),
        TreePatternDir(
            DirGlobWithVar("var", "*hey"))))

print(ast.prettyPrint(0))
