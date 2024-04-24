import Literals
import Rules
import Arguments
import time
from GenerateArguments import generateArgs
from GenerateAttacks import generateUndercuts, generateRebuts
from Defeats import makePreferred, comparePreferred, defeat
from collections import defaultdict
from parseAspartix import parseAttacks, parseRules
from BurdenBasedSemantics import bur, addset

def printSorted(argumentBase):
    sortedArgs = sorted(argumentBase, key=lambda arg: int(arg.name[1:]))
    for arg in sortedArgs:
        print(arg)

def main():
    # a = Literals.Literals("a", False)
    # b = Literals.Literals("b", False)
    # c = Literals.Literals("c", True)
    # d = Literals.Literals("d", True)
    # e = Literals.Literals("e3", False)

    # print("literal a : ", a)

    # newRule = Rules.Rules({a, b, c, d, e}, {e}, True)

    # print("new rule " , newRule)

    # rule1 = Rules.Rules({a}, {b}, True)
    # print(rule1.name)
    # rule2 = Rules.Rules({a}, {b}, True)
    # print(rule2.name)
    # print(rule1 == rule2)
    # rule3 = Rules.Rules({a}, {b}, True)
    # print(rule1.name + " " + rule3.name)
    # print(rule1 == rule3)

    # print("\n")

    # # Testing Arguments
    # arguement1 = Arguments.Arguments(rule1, set())
    # arguement2 = Arguments.Arguments(rule2, {arguement1})
    # print(arguement2)

    # arguement3 = Arguments.Arguments(rule1, {arguement2})
    # arguement4 = Arguments.Arguments(rule2, {arguement3})
    # arguement5 = Arguments.Arguments(rule1, {arguement4, arguement3})

    # print(arguement5.setOfArguemnts())
    # print(arguement5)

    # l1 = Literals.Literals("test", True)
    # print(l1)
    # print(l1.negate())

    # # Testing contraposition
    a = Literals.Literals("a", True)
    aF = Literals.Literals("a", False)
    b = Literals.Literals("b", True)
    bF = Literals.Literals("b", False)
    c = Literals.Literals("c", True)
    cF = Literals.Literals("c", False)
    d = Literals.Literals("d", True)
    dF = Literals.Literals("d", False)
    eF = Literals.Literals("e", False)

    r1 = Literals.Literals("r1", False)
    r2 = Literals.Literals("r2", False)
    r3 = Literals.Literals("r3", False)
    r4 = Literals.Literals("r4", False)
    r5 = Literals.Literals("r5", False)
    r6 = Literals.Literals("r6", False)
    r7 = Literals.Literals("r7", False)
    r8 = Literals.Literals("r8", False)
    r9 = Literals.Literals("r9", False)

    rule1 = Rules.Rules({}, aF, False, r1)
    rule2 = Rules.Rules({bF, dF}, cF, False, r2)
    rule3 = Rules.Rules({c}, dF, False, r3)
    
    rule4 = Rules.Rules({aF}, d, True, r4)
    rule5 = Rules.Rules({}, bF, True, r5, 1)
    rule6 = Rules.Rules({}, c, True, r6, 1)
    rule7 = Rules.Rules({}, dF, True, r7, 0)
    rule8 = Rules.Rules({cF}, eF, True, r8)
    rule9 = Rules.Rules({c}, r4.negate(), True, r9)
    
    print(rule1)
    print(rule2)
    print(rule3)
    print(rule4)
    print(rule5)
    print(rule6)
    print(rule7)
    print(rule8)
    print(rule9)

    # Testing the generation of arguments
    print("\n")
    rules = {rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9}
    deb  = time.time()
    argumentBase = generateArgs(rules)
    parseRules(rules)
    fin = time.time()
    print("temp", fin-deb)

    printSorted(argumentBase)    

    defeasibleRules = set()
    for arg in argumentBase:
        print(f"argument {arg}")
        defeasibleRules.update(arg.getAllDefeasible())
        print("The defeasible rules : ")

    undercuts = generateUndercuts(argumentBase, rules)
    print("undercuts are : ", undercuts)

    # for arg in bf:
    #     print(arg)
    #     defeasibleRules = arg.getAllDefeasible()
    #     print("Les règles defeasibles: ")
    #     for rules in defeasibleRules:
    #         print(rules.name)

    print()

    print("\nundercuts done \n")

    for arg in argumentBase:
        print(arg)
        # defeasibleRules = arg.getAllDefeasible()
        defeasibleRules = arg.getLastDefeasible()
        print("Les règles defeasibles: ")
        for rules in defeasibleRules:
            print(rules.name)
        print("\n")


    print("\n")
    print("REBUTS:")
    rebuts = generateRebuts(argumentBase)
    for key in rebuts:
        print(f'For {key.isNeg} {key.name} len {len(rebuts[key])} :')
        for (arg1, arg2) in rebuts[key]:
            print(f'{arg1.name} -> {arg2.name}')
        print()
    
    print("\n")
    # rules = {rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9}
    
    # preferred = makePreferred(rules)
    # for key in preferred:   
    #     print(f"key: {key} value: {preferred[key]}")

    # weightComparison = comparePreferred(preferred)
    # print("weightComparison: ", weightComparison)
    print("DEFEATS:")
    defeatWeakLink = defaultdict(set)

    for rebut in rebuts:
        for (arg1, arg2) in rebuts[rebut]:
            defeatTuple = defeat(arg1, arg2, "elitist", "weakest-link")
            if defeatTuple is not None:
                defeatWeakLink[arg1.topRule.conclusion].add(defeatTuple)
    
    for key in defeatWeakLink:
        print(f'For {key.isNeg} {key.name} len {len(defeatWeakLink[key])} :')
        for (arg1, arg2) in defeatWeakLink[key]:
            print(f'{arg1.name} -> {arg2.name}')
        print()

    parseAttacks(defeatWeakLink)
    # rules = {rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9}
    

    bur = addset(argumentBase, rebuts, 5)
    for b in bur:
        print(b)

    

if __name__ == "__main__":
    main()
