undercuts = set()

def getRulesNames(rules):
    rulesNames = set()
    for rule in rules:
        rulesNames.add(rule.name.name)
    return rulesNames

def getAllDefeasibleRulesNames(argument):
    defeasibleRulesNames = set()
    argumentAllDefeasibles = argument.getAllDefeasible()
    for rule in argumentAllDefeasibles:
        defeasibleRulesNames.add(rule.name.name)

    return defeasibleRulesNames

def generateUndercuts(argumentBase, rules):
    rulesNames = getRulesNames(rules)
    for arg in argumentBase:
        if arg.topRule.premises:
            if arg.topRule.conclusion.name in rulesNames:
                for otherArg in argumentBase:
                    currentArgRuleConclusion = arg.topRule.conclusion
                    defeasibleRulesNames = getAllDefeasibleRulesNames(otherArg)
                    currentArgRuleConclusionCopy = currentArgRuleConclusion.copy()
                    if currentArgRuleConclusionCopy.name in defeasibleRulesNames:
                        argTuple = (arg.name, otherArg.name)
                        undercuts.add(argTuple)

    return undercuts
