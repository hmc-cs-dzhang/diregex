from lexemes import *

@generate
def nonPat():
    '''
    matches with parts of the glob that are not patterns
    '''
    yield many(none_of('<'))

@generate
def namedPattern():
    '''
    parse a pattern, add the varname and glob to an environment.
    TODO: create another pattern parser for python regex '''
    yield nonPat
    name = yield string('<') >> ident << string('=')
    pat = yield glob << string('>')
    return (name, pat)

@generate
def backreference():
    '''
    parse a backreference, which we will ignore for now
    '''
    yield nonPat
    yield lt >> backslash >> ident >> gt

@generate
def globWithPatterns():
    ''' parse a glob with patterns '...<name=p*at?>...<...>...' '''
    pats = yield many(namedPattern ^ backreference)
    yield nonPat << eof

    # get rid of NoneType values produced by backreference
    pats = [e for e in pats if e]
    return pats

def parsePattern(pat):
    return globWithPatterns.parse(pat)





