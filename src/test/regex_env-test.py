from nose.tools import eq_
import sys

sys.path.append("../main")
from regex_env import RegexEnv
'''
def testTrivial():
    pattern = r"(.+) \1 "
    string = "the the "
    regexEnv = RegexEnv()
    regexEnv = regexEnv.match(pattern, string)

    eq_(regexEnv.groups, ['the'])

def testNumbers():
    regexEnv = RegexEnv()

    regexEnv1 = regexEnv.match(r"([a-z]+)1", "child1")
    regexEnv2 = regexEnv1.match(r"\1[2]", "child2")

    eq_(regexEnv2.groups, ['child'])

def testNames():
    strings = ["child1", "child2"]
    patterns = [r"(?P<c>[a-z]+)1", r"(?P=c)2"]

    regexEnv = RegexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['child'])

def testNumbersAndNames():
    patterns = [r"(hi) \1 (?P<name>yo) (?P=name)", r"\1 (?P=name) (bye) \3 (?P<ayy>later) (?P=ayy)"]
    strings = ["hi hi yo yo", "hi yo bye bye later later"]

    regexEnv = RegexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['hi', 'yo', 'bye', 'later'])
    eq_(regexEnv.groupdict, {'name':'yo', 'ayy':'later'})
'''
def testGlob():
    patterns = [r'<*>.cpp']
    strings = ["foo.cpp"]
    regexEnv = RegexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['foo'])

def testGlob2():
    patterns = [r'<*>.cpp', r'\1.hpp']
    strings = ["foo.cpp", "foo.hpp"]
    regexEnv = RegexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['foo'])

def testGlob3():
    patterns = [r'<*>\1.txt']
    strings = ['haha.txt']
    regexEnv = RegexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['ha'])

def testGlob4():
    '''
    a very contrived example, that tests backreferencing to previous patterns
    and the same pattern
    '''
    patterns = [r'<hey*>.c', r'<hi*>\1\2.h']
    strings = ['heyo.c', 'hiThereheyohiThere.h']
    regexEnv = RegexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['heyo', 'hiThere'])

def testGlob5():
    patterns = ['<c*[1-5]>.h', r'\1']
    strings = ['carrot4.h', 'carrot4']
    regexEnv = RegexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['carrot4'])

def testGlob6():
    patterns = ['<child*>.h', r'\1.cpp']
    strings = ['child1.h', 'child1.cpp']
    regexEnv = RegexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['child1'])


