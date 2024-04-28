from Arguments import Arguments
import time

argumentBase = set()

def emptyArgumentsBase():
    """
    Empties the argument base.
    """
    global argumentBase
    argumentBase = set()

def generateInitialArguments(rules):
    """
    Extracts the rules with no premises and generates the initial arguments. 
    """
    rulesCopy = rules.copy()
    for rule in rules:
        if len(rule.premises) == 0 :
            arg = Arguments(rule, set())
            argumentBase.add(arg)
            rulesCopy.remove(rule)
    
    return rulesCopy

def findCombinations(targetValues):
    """
    Finds the combinations of arguments that lead to the target values.
    This function was inspired by the DFS algorithm but it doesnt use a stack.
    """
    if not targetValues:
        return set([frozenset([])])
    else:
        validCombinations = set()
        
        for arg in argumentBase:    
            if arg.topRule.conclusion in targetValues:
                validSubCombination = findCombinations(targetValues - {arg.topRule.conclusion})
                
                for combination in validSubCombination:
                    validCombinations.add(frozenset([arg]) | combination)

        return validCombinations

def generateArgsFromRules(rules):
    """
    Generates the arguments from the rules and populates the argument base.
    """
    argToAdd = set()
    for rule in rules:
        # timeStart = time.time()
        combination = findCombinations(rule.premises) 
        # timeEnd = time.time()
        # print("time to find combinations : ", timeEnd - timeStart)
        for subArg in combination:
            arg = Arguments(rule, subArg)
            compt = 0
            for elem in argumentBase:
                if elem.subArguments != arg.subArguments:
                    compt = compt + 1

            if len(argumentBase) == compt:
                argToAdd.add(arg)
            else:
                Arguments.nameCount = Arguments.nameCount - 1
    
    for key in argToAdd:
        argumentBase.add(key)
    
    if(len(argToAdd)) > 0:
        generateArgsFromRules(rules)

def generateContrapositonRules(rules):
    """
    Generates the contraposition rules and makes sure there are no duplicates.
    """
    sortedRules = []
    rulesToAdd = set()
    for rule in rules:
        if not rule.isDefeasible :
            ruleContraposition = rule.contraposition()
            rulesToAdd.update(ruleContraposition)

    for rule in rulesToAdd:
        exists = False
        for existingRule in rules:
            if rule.premises == existingRule.premises and rule.conclusion == existingRule.conclusion:
                exists = True
                break
        if not exists:
            rules.update(rulesToAdd)

    sortedRules = sorted(rules, key=lambda rule: int(rule.literalReference.name[1:]))
    
    return sortedRules

def generateArgs(rules):
    """
    Calls all the functions to generate the arguments.
    """
    rulesWithContraposition = generateContrapositonRules(rules)
    rulesWithNoArgs = generateInitialArguments(rulesWithContraposition)
    generateArgsFromRules(rulesWithNoArgs)
    return argumentBase
