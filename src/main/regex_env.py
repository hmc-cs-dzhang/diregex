import re

class RegexEnv(object):

    def __init__(self):
        self.groupdict = {} # contains the named groups
        self.groups = [] # contains all the groups, in order

    def matchAll(self, patterns, strings):
        for pattern, string in zip(patterns, strings):
            self.match(pattern, string)

    def match(self, pattern, string):
        newPattern = self.replaceBackreferences(pattern)
        m = re.match(newPattern, string)
        if m:
            self.groups += list(m.groups())
            self.groupdict.update(m.groupdict())

        return m

    '''
    @return     string
    @brief      Creates a pattern to identify backreferences, then
                replaces them, as specified in replFunc
    '''
    def replaceBackreferences(self, p):
        numberedBackreference = r"(\\[1-9][0-9]?)"
        namedBackreference = r"\(\?P\=([A-z_][A-z0-9_]*)\)"

        backreferencePattern = "{}|{}".format(numberedBackreference, namedBackreference)

        newPattern = re.sub(backreferencePattern, self.replFunc, p)

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
        else:
            rawName = RegexEnv.namedBackreference(matchobj)
            name = RegexEnv.extractName(rawName)
            if name in self.groupdict:
                return self.groupdict[name]
            else:
                return rawName      # don't replace it, return the original pattern

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






