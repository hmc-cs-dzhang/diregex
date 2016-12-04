from ir import *
from parsec import *
from lexemes import *
from match_parser import matchTreePattern
from dest_parser import destTreePattern
from assign_parser import assignment

""" Parse a diregex program, calls the individual statement parsers """

@generate
def program():
    prog = yield whitespace >> many1(statement) << eof
    return Prog(prog)

@generate
def statement():
    ''' parse a statement, which is either a match tree, destination tree,
    or an assignment.
    TODO: add option to execute shell commands '''
    stmt = yield match ^ dest ^ assign
    return stmt

@generate
def match():
    m = yield match_tok >> matchTreePattern
    return Match(m)

@generate
def dest():
    d = yield dest_tok >> destTreePattern
    return Dest(d)

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
