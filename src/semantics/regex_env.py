import re
from copy import deepcopy

class RegexEnv(object):

    def __init__(self):
        self.groupdict = {} # contains the named groups
        self.groups = [] # contains all the groups, in order

    def __eq__(self, other):
        return self.groups == other.groups

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



    def replaceBackreferences(self, p):
        '''
        @return     string
        @brief      Creates a pattern to identify backreferences, then
                    replaces them, as specified in replFunc
        '''
        numberedBackreference = r"(\\[1-9][0-9]?)"
        namedBackreference = r"\(\?P\=([A-z_][A-z0-9_]*)\)"

        p = re.sub(numberedBackreference, self.replNums, p)
        p = re.sub(namedBackreference, self.replNames, p)

        # no mechanism for named backreferences with globbing yet
        #namedBackreference = r"\(\?P\=([A-z_][A-z0-9_]*)\)"
        #backreferencePattern = "{}|{}".format(numberedBackreference, namedBackreference)
        return p

    def replNums(self, matchobj):
        """
        @param[in]  A match object, returned by re.match
        @return     string
        @details    Called by re.sub, replaces backreferencing numbers to refer
                    to the proper match in the environment.
        """
        n = RegexEnv.numberedBackreference(matchobj)
        if n > 0 and n <= len(self.groups):
            return self.groups[n - 1]
        else:
            return "\\" + str(n - len(self.groups))

    def replNames(self, matchobj):
        """
        @param[in]  A match object, returned by re.match
        @return     string
        @details    Called by re.sub, replaces backreferencing names with the
                    proper name from the environment
        """
        name = RegexEnv.namedBackreference(matchobj)
        # name is of the form (?P<name>).
        name = name[4:-1]

        if name in self.groupdict:
            return self.groupdict[name]
        else:
            return "(?P={})".format(name)

    def numberedBackreference(matchobj):
        '''
        If matchobj matches a numbered backreference \n, extracts the number
        '''
        n = matchobj.group(0).strip(r"\\")
        if n.isdigit():
            return int(n)
        else:
            return None

    def namedBackreference(matchobj):
        '''
        If matchobj matches a named backreference (?P=name),
        extracts the name
        '''
        return matchobj.group(0)

    def translateName(pat, i):
        """
        Replaces <some*pattern> with (...) and <name=p*a> with (?P<name>...)
        """
        if pat[i] == '\\':
            name, i = RegexEnv.translateBackRef(pat, i+1)
            return name[:-1], i

        j = i
        name = ''
        while True:
            if pat[j] == '=': # it was a named pattern
                name = '(?P<%s>' % name
                i = j + 1
                break
            elif pat[j] == '>': # it was just a numbered pattern
                name = '('
                break;
            name += pat[j]
            j += 1

        return name, i

    def translateBackRef(pat, i):
        if pat[i].isdigit():
            return '\\', i

        name = ''
        while i < len(pat) and (pat[i].isalnum() or pat[i] == '_'):
            name += pat[i]
            i += 1

        name = '(?P=%s)' % name
        return name, i

    def translateOnlyBackrefs(pat):
        """ Used in tree_producer, only replaces backreferences, and keeps
        the rest of the directory name the same """
        i, n = 0, len(pat)
        res = ''
        while i < n:
            c = pat[i]
            i = i+1
            if c == '<':
                name, i = RegexEnv.translateName(pat, i)
                res += name
            elif c == '>':
                res += ')'
            elif c == '\\':
                name, i = RegexEnv.translateBackRef(pat, i)
                res += name
            elif c.isalnum() or c == '_' or c == '.':
                res += c
            else:
                raise Exception("Unrecognized character '%s'" % c)
        return res

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
                name, i = RegexEnv.translateName(pat, i) # converting glob capture groups into regex ones
                res += name
            elif c == '>':
                res = res + ')'
            elif c == '\\':
                name, i = RegexEnv.translateBackRef(pat, i)
                res += name
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



