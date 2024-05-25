from Literals import Literals
from Rules import Rules
import time
from GenerateArguments import generateArgs
from GenerateAttacks import generateUndercuts, generateRebuts
from Defeats import makePreferred, comparePreferred, defeat, genHisto
from collections import defaultdict
from parseAspartix import parseAttacks, parseRules
from ExportArguments import exportArguments
from parseAspartix import parseAttacks, readKB
from BurdenBasedSemantics import computeBurden, compareArgRankings
from GenerateAttacks import generateRebuts
import matplotlib.pyplot as plt

def printSorted(argumentBase):
    sortedArgs = sorted(argumentBase, key=lambda arg: int(arg.name[1:]))
    for arg in sortedArgs:
        print(arg)

def main():

    a = Literals("a", True)
    aF = Literals("a", False)
    b = Literals("b", True)
    bF = Literals("b", False)
    c = Literals("c", True)
    cF = Literals("c", False)
    d = Literals("d", True)
    dF = Literals("d", False)
    eF = Literals("e", False)

    r1 = Literals("r1", False)
    r2 = Literals("r2", False)
    r3 = Literals("r3", False)
    r4 = Literals("r4", False)
    r5 = Literals("r5", False)
    r6 = Literals("r6", False)
    r7 = Literals("r7", False)
    r8 = Literals("r8", False)
    r9 = Literals("r9", False)

    rule1 = Rules({}, aF, False, r1)
    rule2 = Rules({bF, dF}, cF, False, r2)
    rule3 = Rules({c}, dF, False, r3)
    
    rule4 = Rules({aF}, d, True, r4)
    rule5 = Rules({}, bF, True, r5, 1)
    rule6 = Rules({}, c, True, r6, 1)
    rule7 = Rules({}, dF, True, r7, 0)
    rule8 = Rules({cF}, eF, True, r8)
    rule9 = Rules({c}, r4.negate(), True, r9)

    rules = {rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9}
    
    for rule in rules:
        print(rule)
    
    print("\n")
    print("GENERATING ARGUMENTS")
    deb  = time.time()
    argumentBase = generateArgs(rules)
    fin = time.time()
    print("Total time to generate arguments: ", fin-deb)
    printSorted(argumentBase)    

    print("\n")
    print("UNDERCUTS")
    undercuts = generateUndercuts(argumentBase, rules)
    print("Undercuts are : ", undercuts)

    print("\n")
    print("ALL DEFEASIBLE RULES:")
    defeasibleRules = set()
    defeasibleRulesSize = 0
    for arg in argumentBase:
        defeasibleRules = arg.getAllDefeasible()
        defeasibleRuleNames = []
        for rule in defeasibleRules:
            defeasibleRulesSize += 1
            defeasibleRuleNames.append(rule.literalReference.name)
        print(arg.name + " : " + ", ".join(defeasibleRuleNames))
    print("Length of all defeasible rules: ", defeasibleRulesSize)
    
    print("\n")
    print("LAST DEFEASIBLE RULES:")
    defeasibleRules.clear()
    defeasibleRulesSize = 0
    for arg in argumentBase:
        defeasibleRules = arg.getLastDefeasible()
        defeasibleRuleNames = []
        for rule in defeasibleRules:
            defeasibleRulesSize += 1
            defeasibleRuleNames.append(rule.literalReference.name)
        print(arg.name + " : " + ", ".join(defeasibleRuleNames))
    print("Length of last defeasible rules: ", defeasibleRulesSize)


    print("\n")
    print("REBUTS:")
    rebuts = generateRebuts(argumentBase)
    for key in rebuts:
        print(f'For {key.isNeg} {key.name} len {len(rebuts[key])} :')
        for (arg1, arg2) in rebuts[key]:
            print(f'{arg1.name} -> {arg2.name}')
        print()
    
    print("\n")
    print("PREFERRED:")
    rules = {rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9}
    
    preferred = makePreferred(rules)
    for key in preferred:   
        print(f"key: {key} value: {preferred[key]}")

    weightComparison = comparePreferred(preferred)
    print("WeightComparison: ", weightComparison)

    print("\n")
    print("DEFEATS:")
    defeatsDict = defaultdict(list)

    for rebut in rebuts:
        for (arg1, arg2) in rebuts[rebut]:
            defeatTuple = defeat(arg1, arg2, "democratic", "weakest-link")
            if defeatTuple is not None:
                defeatsDict[arg1.topRule.conclusion].append(defeatTuple)
    
    for key in defeatsDict:
        print(f'For {not key.isNeg} {key.name} : {len(defeatsDict[key])}')
        for (arg1, arg2) in defeatsDict[key]:
            print(f'{arg1.name} -> {arg2.name}')
        print()

    parseAttacks(defeatsDict)
    parsedRules = set()
    readKB(parsedRules)
    print("Parsed rules:")
    for rule in parsedRules:
        print(rule)
    
    print("\n")
    print("SORTED RANKED ARGUMENTS")

    burnedValues = computeBurden(argumentBase, defeatsDict, 4)
    argRanking = compareArgRankings(burnedValues)
    print("Ranking: ", argRanking)

    # Constuct the histogram with matplotlib
    genHisto(defeatsDict, len(argumentBase))


if __name__ == "__main__":
    main()
