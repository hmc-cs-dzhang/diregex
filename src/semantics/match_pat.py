from regex_env import RegexEnv

def matchPattern(params):

    regexEnv = RegexEnv()

    for regexGroups in matchPatternHelper(params):
        regexEnv.groupdict = regexGroups

        yield regexEnv

def matchPatternHelper(params):
    if params == []:

        yield {}
    else:
        for env in matchPatternHelper(params[1:]):
            currParam = params[0]

            for match in currParam.matches:
                env.update({currParam.name: match})
                yield env


