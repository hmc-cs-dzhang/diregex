from lexemes import *
from ir import *
from parsec import *

""" Parser for MatchPats (denoted by the keyword matchname)
These are of the form

matchname person = [Joe, Bob, Tim], year = [2012, 2013]
"""

@generate
def matchPattern():
    """ splits the pattern into a list of params """
    patternList = yield matchname_tok >> sepBy(params, comma)
    return patternList

@generate
def params():
    """ parses a params, which contains the name and a list of matches """
    name = yield ident
    yield equals
    matches = yield lbrack >> sepBy(dirname, comma) << rbrack
    return Params(name, matches)
