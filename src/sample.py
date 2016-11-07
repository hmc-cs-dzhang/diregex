import os

# starts in the current directory: prints
# /home/daniel/Documents/courses/cs111/diregex
print(os.getcwd())

os.chdir('/home/daniel')
print(os.getcwd())

# Use relative path
os.chdir('Documents')
print(os.getcwd())

# os.listdir lists the directories
# Can also take in a *file descriptor*
print(os.listdir("."))

#os.mkdir("testdir") will make a directory of called
#"testdir" in the current test directory.  If "testdir"
#exists, it will throw an error

#os.makedirs("parentdir/childdir") will recursively make
#the parent and child directories


#readlink will be necessary for symbolic links

#remove() will remove files, rmdir() for directories,
#removedirs() will recursively remove the child directory
#AND all the parent directories
# removedirs("foo/bar/baz") removes foo/bar/baz, then
# foo/bar, then foo
#

#scandir(path) returns an iterator

# prints all the files, with all their children in a
# nice tree-like format
def mywalk(dir, depth, maxdepth):
    if depth > maxdepth:
        return
    for entry in os.scandir(dir):
        if entry.is_file() and entry.name.endswith('.txt'):
            print_direntry(entry.name, depth)

        elif entry.is_dir() and not entry.name.startswith('.'):
            print_direntry(entry.name, depth)
            mywalk(dir + "/" + entry.name, depth + 1, maxdepth)

def print_direntry(name, depth):
    print(" "*3*depth + name)

#mywalk("courses/cs111/diregex", 0, 3)

from os.path import join, getsize

def walk(top):
    for root, dirs, files in os.walk(top):
        if ('.' not in root) and ('_' not in root):
            print(root)
            for dir in dirs:
                print("   " + dir)
            for file in files:
                print("   " + file)
        """
        print(root, "consumes", end=" ")
        print(sum(getsize(join(root, name)) for name in files), end=" ")
        print("bytes in", len(files), "non-directory files")
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories
"""
print(walk("courses/cs111/diregex/test"))

