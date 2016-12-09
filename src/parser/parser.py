import src

from ir import *
from parsec import *
from lexemes import *
from match_parser import matchTreePattern
from dest_parser import destTreePattern
from assign_parser import assignment
from matchpat_parser import matchPattern

""" Parse a diregex program, calls the individual statement parsers """

@generate
def program():
    yield whitespace
    prog = yield many1(statement) << eof
    return Prog(prog)

@generate
def statement():
    ''' parse a statement, which is either a match tree, destination tree,
    or an assignment.'''
    stmt = yield matchpat ^ match ^ dest ^ shell ^ assign
    return stmt

@generate
def match():
    m = yield match_tok >> matchTreePattern
    return Match(m)

@generate
def matchpat():
    m = yield matchPattern
    return MatchPat(m)

@generate
def dest():
    d = yield dest_tok >> destTreePattern
    return Dest(d)

@generate
def shell():
    s = yield bang >> regex(r'''[^\n$]+''') << (eol | eof)
    return Shell(s)

@generate
def assign():
    ''' an assignment is just a specific type of tree pattern '''
    a = yield assignment
    return Assign(a)

def parse(st):
    return program.parse(st)

def parseAssign(st):
    return assign.parse(st)

def parseMatch(st):
    return match.parse(st)

def parseDest(st):
    return dest.parse(st)

