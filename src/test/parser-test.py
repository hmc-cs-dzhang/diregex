import sys
sys.path.append("../main")

from diregex_parser import parse
from diregex_ir import *

def testDirItem():
    ast = TreePattern_Dir(DirItem(DirName("\"hello\"")))
    bst = parse("\"hello\"")
    print(parse("\"hello\""))
    assert ast == bst #parser.parse("hello")

#doctest
