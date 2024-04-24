import Rules

undercuts = set()

def generateUndercuts(bf):
    for arg in bf:
        if arg.topRule.premises:
            if isinstance(arg.topRule.conclusion, Rules.Rules):
                for otherArg in bf:
                    currentArgRule = arg.topRule.conclusion
                    otherArgDefeasibles = otherArg.getAllDefeasible()
                    currentArgRuleCopy = currentArgRule.copy()
                    if currentArgRuleCopy.notRule(currentArgRule.name) in otherArgDefeasibles:
                        print(otherArg.name)
                        tupe = (arg.name, otherArg.name)
                        undercuts.add(tupe)

    return undercuts