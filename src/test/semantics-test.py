# copied from diregex_semantics.py.
# Add imports and change directory

def test():
    matcher = Matcher()

    treeList = TreePattern_List(
        [TreePattern_Child(
            DirItem(
                DirName("[A-z0-9]*")),
            TreePattern_Dir(
                DirItem(
                    DirName("[A-z0-9\.]*")))),
        TreePattern_Dir(
            DirItem(
                DirName("[A-z0-9]*")))])

    simple = TreePattern_Child(
        DirItem(
            DirName("[A-z0-9]*")),
        TreePattern_Child(
            DirItem(
                DirName("[A-z0-9]*1")),
            TreePattern_Dir(
                DirItem(
                    DirName("[A-z0-9\.]*")))))

    matches = matcher.visit(treeList, os.getcwd())
    for match in matches:
        print(match)

test()
