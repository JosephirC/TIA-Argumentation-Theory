import Arguments
import time

argumentBase = set()

def generateInitialArguments(rules):
    rulesCopy = rules.copy()
    for rule in rules:
        if len(rule.premises) == 0 :
            arg = Arguments.Arguments(rule, set())
            argumentBase.add(arg)
            rulesCopy.remove(rule)
    
    return rulesCopy

def findCombinations(targetValues):
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
    argToAdd = set()
    for rule in rules:
        timeStart = time.time()
        combination = findCombinations(rule.premises) 
        timeEnd = time.time()
        print("time to find combinations : ", timeEnd - timeStart)
        for subArg in combination:
            arg = Arguments.Arguments(rule, subArg)
            compt = 0
            for elem in argumentBase:
                if elem.subArguments != arg.subArguments:
                    compt = compt + 1

            if len(argumentBase) == compt:
                argToAdd.add(arg)
            else:
                Arguments.Arguments.nameCount = Arguments.Arguments.nameCount - 1
    
    for key in argToAdd:
        argumentBase.add(key)
    
    if(len(argToAdd)) > 0:
        generateArgsFromRules(rules)

def generateContrapositonRules(rules):
    sortedRules = []
    rulesToAdd = []
    for rule in rules:
        if not rule.isDefeasible :
            rulesToAdd.extend(rule.contraposition())

    sortedRules = sorted(rules, key=lambda rule: rule.name.name)
    sortedRules.extend(sorted(rulesToAdd, key=lambda rule: rule.name.name))

    return sortedRules

def generateArgs(rules):
    rulesWithContraposition = generateContrapositonRules(rules)
    rulesWithNoArgs = generateInitialArguments(rulesWithContraposition)
    generateArgsFromRules(rulesWithNoArgs)
    return argumentBase
