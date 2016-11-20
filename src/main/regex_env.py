import re
from copy import deepcopy

class RegexEnv(object):

    def __init__(self):
        self.groupdict = {} # contains the named groups
        self.groups = [] # contains all the groups, in order

    def deepcopy(self):
        other = RegexEnv()
        other.groupdict = deepcopy(self.groupdict)
        other.groups = deepcopy(self.groups)
        return other

    def matchAll(patterns, strings):
        regexEnv = RegexEnv()

        for pattern, string in zip(patterns, strings):
            regexEnv = regexEnv.match(pattern, string)

        return regexEnv

    def match(self, pattern, string):
        # translate from globbing to python regex
        regexPattern = RegexEnv.translate(pattern)

        newPattern = self.replaceBackreferences(regexPattern)

        # fullmatch only matches if the entire string is match
        # Add option for not full match?
        m = re.fullmatch(newPattern, string)
        if m:
            newRegexEnv = self.deepcopy()

            newRegexEnv.groups += list(m.groups())
            newRegexEnv.groupdict.update(m.groupdict())

            return newRegexEnv
        # return nothing (?)

    def translate(pat):
        """
        Translate a shell PATTERN to a regular expression. There is no way to
        quote meta-characters. Adapted from Python3's fnmatch.translate().
        Allows capture groups specified by <...>

        @param      pat   The pattern

        @return     the regex pattern
        """

        i, n = 0, len(pat)
        res = ''
        while i < n:
            c = pat[i]
            i = i+1
            if c == '*':
                res = res + '.*'
            elif c == '?':
                res = res + '.'
            elif c == '<':
                res = res + '('
            elif c == '>':
                res = res + ')'
            elif c == '\\':
                res = res + '\\'
            elif c == '[':
                j = i
                if j < n and pat[j] == '!':
                    j = j+1
                if j < n and pat[j] == ']':
                    j = j+1
                while j < n and pat[j] != ']':
                    j = j+1
                if j >= n:
                    res = res + '\\[' # open didn't match close bracket
                else:
                    stuff = pat[i:j].replace('\\','\\\\')
                    i = j+1
                    if stuff[0] == '!':
                        stuff = '^' + stuff[1:]
                    elif stuff[0] == '^':   # what is this for? just escaping ^?
                        stuff = '\\' + stuff
                    res = '%s[%s]' % (res, stuff)
            else:
                res = res + re.escape(c)
        return res + '\Z(?ms)'



    '''
    @return     string
    @brief      Creates a pattern to identify backreferences, then
                replaces them, as specified in replFunc
    '''
    def replaceBackreferences(self, p):
        numberedBackreference = r"(\\[1-9][0-9]?)"

        # no mechanism for named backreferences with globbing yet
        #namedBackreference = r"\(\?P\=([A-z_][A-z0-9_]*)\)"
        #backreferencePattern = "{}|{}".format(numberedBackreference, namedBackreference)

        newPattern = re.sub(numberedBackreference, self.replFunc, p)

        return newPattern

    '''
    param[in]   matchobj A match object, returned by re.match
    @return     string
    @details    Replacement function used for parsing regex patterns.
                Given an environment of existing groups, with matching patterns,
                replaces all backreferenced numbers and pattern names.  If it
                encounters \k (k is an int) and there have already been n
                patterns where k < n, then replaes \k with the existing match.
                If k > n, then replaces k with n - k.  If it encounters
                (?P=name), if name refers to a previous pattern, then it
                replaces that text with the content of the pattern.  Otherwise,
                leaves it blank.
    '''
    def replFunc(self, matchobj):
        # returns a number if it was a numbered backreference
        # otherwise returns None
        number = RegexEnv.numberedBackreference(matchobj)
        if number:
            if number <= len(self.groups):
                return self.groups[number-1]
            else:
                return "\\" + str(number - len(self.groups))
        # No way to make named backreferences with globbing, so this code is useless
        '''
        else:
            rawName = RegexEnv.namedBackreference(matchobj)
            name = RegexEnv.extractName(rawName)
            if name in self.groupdict:
                return self.groupdict[name]
            else:
                return rawName      # don't replace it, return the original pattern
        '''
    ''' If matchobj matches a numbered backreference \n, extracts the number '''

    def numberedBackreference(matchobj):
        n = matchobj.group(0).strip(r"\\")
        if n.isdigit():
            return int(n)
        else:
            return None

    ''' If matchobj matches a named backreference (?P=name), extracts the name'''
    def namedBackreference(matchobj):
        return matchobj.group(0)

    ''' extracts name from (?P=name) '''
    def extractName(name):
        return name[4:-1]



