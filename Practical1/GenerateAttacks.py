from Literals import Literals
from collections import defaultdict

undercuts = set()
rebuts = defaultdict(set)

def getRulesNames(rules):
    """
    Gets the rules names from the rules.
    """
    rulesNames = set()
    for rule in rules:
        rulesNames.add(rule.literalReference.name)
    return rulesNames

def getAllDefeasibleRulesNames(argument):
    """
    Gets all the defeasible rules names from the argument.
    """
    defeasibleRulesNames = set()
    argumentAllDefeasibles = argument.getAllDefeasible()
    for rule in argumentAllDefeasibles:
        defeasibleRulesNames.add(rule.literalReference.name)

    return defeasibleRulesNames

def generateUndercuts(argumentBase, rules):
    """
    Generates the undercuts from the argument base.
    """
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

def generateRebuts(argumentBase):
    """
    Generates the rebuts from the argument base.
    """

    sortedArgBase = sorted(argumentBase, key=lambda arg: int(arg.name[1:]))

    for arg in sortedArgBase:
        for other_arg in sortedArgBase:
            conclusionCopy = arg.topRule.conclusion.copy()
            conclusionCopy = conclusionCopy.negate()
            if conclusionCopy.name == other_arg.topRule.conclusion.name and conclusionCopy == other_arg.topRule.conclusion:
                paire = (arg, other_arg)
                rebuts[arg.topRule.conclusion].add(paire)
            else:
                subArgs = subArgConclusion(other_arg.subArguments)
                for s in subArgs:
                    if conclusionCopy == s.topRule.conclusion:
                        paire = (arg, other_arg)
                        rebuts[arg.topRule.conclusion].add(paire)
                        break

    sortedRebuts = defaultdict(list)
    sorted_keys = sorted(rebuts.keys(), key=lambda arg: arg.name)

    for key in sorted_keys:
        sortedRebuts[key] = sorted(rebuts[key], key=lambda x: (int(x[0].name[1:]), int(x[1].name[1:])))

    return sortedRebuts


def subArgConclusion(args):
    """
    Gets the sub arguments conclusions.
    """
    subConclusion = set()
    for arg in args:
        subConclusion.add(arg)
        subConclusion = subConclusion.union(subArgConclusion(arg.subArguments))
    return subConclusion