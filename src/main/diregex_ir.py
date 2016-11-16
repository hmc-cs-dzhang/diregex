## Intermediate Representation for Diregex
## Used this as guide:
##  https://ruslanspivak.com/lsbasi-part7/



''' My current grammar (subject to change)
<program> : <tree-pattern>

<tree-pattern> : <dir-name>
               | <dir-name> SLASH <tree-pattern>
               | LPAREN <tree-pattern-list> RPAREN



<dir-name> : <regex-pattern>
           | <regex-pattern> EQUALS <var>
'''
'''
<tree-pattern-list> : | <tree-pattern>
                      | <tree-pattern> COMMA <tree-pattern-list>
(ignore)
<dir-item> : <dir-name>
           | GT <dir-name>
'''
# abstact class for a node of the AST
class Node(object):

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        st = ""
        for key in self.__dict__:
            st += repr(key) + ": " + repr(self.__dict__[key])
            st += "\n"
        return st

# abstract class, representing the three cases of tree patterns
class TreePattern(Node):
    pass

class TreePatternDir(TreePattern):
    def __init__(self, dirName):
        self.dirName = dirName

class TreePatternChild(TreePattern):
    def __init__(self, dirName, treePattern):
        self.dirName = dirName
        self.treePattern = treePattern

''' Like a TreePatternChild, but matches in current directory
    or any descendant'''
class TreePatternDescendant(TreePattern):
    def __init__(self, treePattern):
        self.treePattern = treePattern

class TreePatternList(TreePattern):
    # takes in a list of tree patterns
    def __init__(self, treePatterns):
        self.treePatterns = treePatterns

class DirName(Node):
    def __init__(self, regexPattern, var=None):
        self.regexPattern = regexPattern
        self.var = var

