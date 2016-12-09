from lexemes import *
from ir import *
from parsec import *

@generate
def matchPattern():
    patternList = yield matchpat_tok >> sepBy(params, comma)
    return patternList

@generate
def params():
    name = yield ident
    yield equals
    matches = yield lbrack >> sepBy(dirname, comma) << rbrack
    return Params(name, matches)
