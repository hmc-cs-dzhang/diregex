from nose.tools import eq_
import sys

sys.path.append("../main")
from regex_env import RegexEnv

def testTrivial():
    pattern = r"(.+) \1"
    string = "the the "
    regexEnv = RegexEnv()
    regexEnv.match(pattern, string)

    eq_(regexEnv.groups, ['the'])

def testNumbers():
    regexEnv = RegexEnv()

    regexEnv.match(r"([a-z]+)1", "child1")
    regexEnv.match(r"\1[2]", "child2")

    eq_(regexEnv.groups, ['child'])

def testNames():
    strings = ["child1", "child2"]
    patterns = [r"(?P<c>[a-z]+)1", r"(?P=c)2"]

    regexEnv = RegexEnv()
    regexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['child'])

def testNumbersAndNames():
    regexEnv = RegexEnv()
    patterns = [r"(hi) \1 (?P<name>yo) (?P=name)", r"\1 (?P=name) (bye) \3 (?P<ayy>later) (?P=ayy)"]
    strings = ["hi hi yo yo", "hi yo bye bye later later"]

    regexEnv.matchAll(patterns, strings)

    eq_(regexEnv.groups, ['hi', 'yo', 'bye', 'later'])
    eq_(regexEnv.groupdict, {'name':'yo', 'ayy':'later'})

