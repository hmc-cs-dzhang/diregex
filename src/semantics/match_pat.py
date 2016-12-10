from regex_env import RegexEnv

""" Uses generators to iterate through every possibility listed in the matchname
statement """

def matchPattern(params):

    regexEnv = RegexEnv()

    for regexGroups in matchPatternHelper(params):
        regexEnv.groupdict = regexGroups

        yield regexEnv

def matchPatternHelper(params):
    """ Recursively calls on smaller inputs, iterates through all the,
    each time returning a new regex environment """
    if params == []:

        yield {}
    else:
        for env in matchPatternHelper(params[1:]):
            currParam = params[0]

            for match in currParam.matches:
                env.update({currParam.name: match})
                yield env


