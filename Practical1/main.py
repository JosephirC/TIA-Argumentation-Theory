import Literals
import Rules
import Arguments
import itertools
import time
from collections import defaultdict

# static bf to store all the arguments
bf =  set()

undercuts = set()

rebuts = defaultdict(set)

# 1. contraposition on strict rules
# 2. search for the rules with conclusions only and generate their respective arguments (verify if the rule has a conclusion?)
# 2.1 add the arguments in the bf
# 3. in a different function have a list of all the rules minus the rules for the intial arguments
# 3.1 for each rule in the list of rules, generate the arguments
# 3.2 add the respective arguments in the bf
# 4. during this step we will try to generate the remaining arguments
# 4.1 go through all the rules once and again and for each rule iterate over the bf and check if you can genereate a new argument for it and add it to the bf
# 4.2. iterate over the whole bf once again and check if you can generate a new argument and then move to the next rule
# 4.3 repeate 4.1 and 4.2 until no new arguments are generated

def addArgsToBF(setOfArguments):
    for arg in setOfArguments:
        if isinstance(arg, Arguments):
            bf.add(arg)
         
def generateInitialArguments(rules):
    rulesCopy = rules.copy()
    for rule in rules:
        if len(rule.premises) == 0 :
            arg = Arguments.Arguments(rule, set())
            bf.add(arg)
            rulesCopy.remove(rule)
    
    return rulesCopy

def find_combinations(target_values):
    if not target_values:
        return set([frozenset([])])
    else:
        valid_combinations = set()
        
        for arg in bf:    
            if arg.topRule.conclusion in target_values:
                sub_valid_combinations = find_combinations(target_values - {arg.topRule.conclusion})
                
                for combination in sub_valid_combinations:
                    valid_combinations.add(frozenset([arg]) | combination)

        return valid_combinations

def generateArgsFromRules(rules):
    argToAdd = set()
    for rule in rules:
        time_start = time.time()
        combination = find_combinations(rule.premises) 
        time_end = time.time()
        for subArg in combination:
            arg = Arguments.Arguments(rule, subArg)
            compt = 0
            for elem in bf:
                if elem.subArguments != arg.subArguments:
                    compt = compt + 1

            if len(bf) == compt:
                argToAdd.add(arg)
            else:
                Arguments.Arguments.nameCount = Arguments.Arguments.nameCount - 1
    
    for key in argToAdd:
        bf.add(key)
    
    if(len(argToAdd)) > 0:
        generateArgsFromRules(rules)

def generateContrapositonRules(rules):
    rulesToAdd = set()
    for rule in rules:
        if not rule.isDefeasible :
            rulesToAdd.update(rule.contraposition())

    rules.update(rulesToAdd)
    return rules

def generateArgs(rules):
    rulesWithContraposition = generateContrapositonRules(rules)
    rulesWithNoArgs = generateInitialArguments(rulesWithContraposition)
    generateArgsFromRules(rulesWithNoArgs)

def print_sorted(bf):
    sorted_args = sorted(bf, key=lambda arg: int(arg.name[1:]))
    for arg in sorted_args:
        print(arg)

def generateUndercuts(bf):
    undercuts = {}
    conflict_arg = []

    for arg in bf:
        if arg.topRule.premises:
            if isinstance(arg.topRule.conclusion, Rules.Rules):
                for other_arg in bf:
                    other_rule = other_arg.topRule
                    arg_rule = arg.topRule.conclusion
                    other_defeasible = other_arg.getAllDefeasible()
                    arg_ruleCopy = arg_rule.copy()
                    if arg_ruleCopy.notRule(arg_rule.name) in other_defeasible:
                        notArg = arg
                        print(other_arg.name)
                        if other_arg.name not in conflict_arg:
                            conflict_arg.append(other_arg.name)
                    undercuts[arg.name] = conflict_arg

    return undercuts

def generateUndercutsWithSet(bf):
    for arg in bf:
        if arg.topRule.premises:
            if isinstance(arg.topRule.conclusion, Rules.Rules):
                for other_arg in bf:
                    arg_rule = arg.topRule.conclusion
                    other_defeasible = other_arg.getAllDefeasible()
                    arg_ruleCopy = arg_rule.copy()
                    if arg_ruleCopy.notRule(arg_rule.name) in other_defeasible:
                        tupe = (arg.name, other_arg.name)
                        undercuts.add(tupe)

    return undercuts

"""
def generateRebuts(bf):
    for arg in bf:
        for other_arg in bf:
            if arg != other_arg:
                if isinstance(arg.topRule.conclusion, Literals.Literals):
                    conclusionCopy = arg.topRule.conclusion.copy()
                    conclusionCopy = conclusionCopy.negate()
                    # if conclusionCopy.name == other_arg.topRule.conclusion.name and conclusionCopy == other_arg.topRule.conclusion:
                    # # if arg.topRule.conclusion.name == other_arg.topRule.conclusion.name and arg.topRule.conclusion != other_arg.topRule.conclusion:
                    #     # print("(", arg.name, ", ", other_arg.name, ")")
                    #     paire = (arg.name, other_arg.name)
                    #     rebuts.add(paire)
                    # else:
                    subArgs = subArgConclusion(other_arg.subArguments)
                    for s in subArgs:
                        if conclusionCopy == s.topRule.conclusion:
                        # if arg.topRule.conclusion.name == s.topRule.conclusion.name and arg.topRule.conclusion != s.topRule.conclusion:
                            paire = (arg.name, s.name)
                            rebuts.add(paire)
                            paire = (arg.name, other_arg.name)
                            rebuts.add(paire)
                if isinstance(arg.topRule.conclusion, Rules.Rules):
                    conclusionCopy = arg.topRule.conclusion.conclusion.copy()
                    conclusionCopy = conclusionCopy.negate()
                    # if conclusionCopy.name == other_arg.topRule.conclusion.name and conclusionCopy == other_arg.topRule.conclusion:
                    # if arg.topRule.conclusion.conclusion.name == other_arg.topRule.conclusion.name and arg.topRule.conclusion.conclusion != other_arg.topRule.conclusion:
                        # print("(", arg.name, ", ", other_arg.name, ")")
                    #     paire = (arg.name, other_arg.name)
                    #     rebuts.add(paire)
                    # else:
                    subArgs = subArgConclusion(other_arg.subArguments)
                    for s in subArgs:
                        if conclusionCopy == s.topRule.conclusion:
                        # if arg.topRule.conclusion.name == s.topRule.conclusion.name and arg.topRule.conclusion != s.topRule.conclusion:
                            # paire = (arg.name, s.name)
                            # rebuts.add(paire)
                            paire = (arg.name, other_arg.name)
                            rebuts.add(paire)

    return rebuts
"""

def generateRebuts(bf):
    for arg in bf:
        for other_arg in bf:
            if arg != other_arg:
                if isinstance(arg.topRule.conclusion, Literals.Literals):
                    conclusionCopy = arg.topRule.conclusion.copy()
                    conclusionCopy = conclusionCopy.negate()
                    if conclusionCopy.name == other_arg.topRule.conclusion.name and conclusionCopy == other_arg.topRule.conclusion:
                        print("(", arg.name, ", ", other_arg.name, ")")
                        paire = (arg, other_arg)
                        rebuts[arg.topRule.conclusion].add(paire)
                    else:
                        subArgs = subArgConclusion(other_arg.subArguments)
                        for s in subArgs:
                            if conclusionCopy == s.topRule.conclusion:
                                paire = (arg, s)
                                rebuts[arg.topRule.conclusion].add(paire)
                                paire = (arg, other_arg)
                                rebuts[arg.topRule.conclusion].add(paire)
                if isinstance(arg.topRule.conclusion, Rules.Rules):
                    conclusionCopy = arg.topRule.conclusion.conclusion.copy()
                    conclusionCopy = conclusionCopy.negate()
                    # if conclusionCopy.name == other_arg.topRule.conclusion.name and conclusionCopy == other_arg.topRule.conclusion:
                    #     print("(", arg.name, ", ", other_arg.name, ")")
                    #     paire = (arg, other_arg)
                    #     rebuts[arg.topRule.conclusion.conclusion].add(paire)
                    subArgs = subArgConclusion(other_arg.subArguments)
                    for s in subArgs:
                        # if conclusionCopy == s.topRule.conclusion:
                        if isinstance(s.topRule.conclusion, Rules.Rules):
                            if arg.topRule.conclusion == s.topRule.conclusion:
                                paire = (arg, s)
                                rebuts[arg.topRule.conclusion.conclusion].add(paire)

    return rebuts

def subArgConclusion(args):
    subConclusion = set()
    for arg in args:
        if isinstance(arg.topRule.conclusion, Literals.Literals):
            subConclusion.add(arg)
        if isinstance(arg.topRule.conclusion, Rules.Rules):
            subConclusion.add(arg)
        
        subConclusion = subConclusion.union(subArgConclusion(arg.subArguments))
    return subConclusion


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

    rule1 = Rules.Rules({}, aF, False)
    rule2 = Rules.Rules({bF, dF}, cF, False)
    rule3 = Rules.Rules({c}, dF, False)
    
    print(rule1)
    print(rule2)
    print(rule3)

    rule4 = Rules.Rules({aF}, d, True)
    rule5 = Rules.Rules({}, bF, True)
    rule6 = Rules.Rules({}, c, True)
    rule7 = Rules.Rules({}, dF, True)
    rule8 = Rules.Rules({cF}, eF, True)
    notRule4 = rule4.copy()
    rule9 = Rules.Rules({c}, notRule4.notRule(rule4.name), True)

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
    generateArgs(rules)
    fin = time.time()
    print("temp", fin-deb)

    print_sorted(bf)    

    # defeasibleRules = set()
    # for arg in bf:
    #     print(f"argument {arg}")
    #     defeasibleRules.update(arg.getAllDefeasible())
    #     print("The defeasible rules : ")

    print()
    undercuts = generateUndercutsWithSet(bf)
    print("undercuts are : ", undercuts)

    # for arg in bf:
    #     print(arg)
    #     defeasibleRules = arg.getAllDefeasible()
    #     print("Les règles defeasibles: ")
    #     for rules in defeasibleRules:
    #         print(rules.name)

    print()
    generateRebuts(bf)
    for key in rebuts:
        print(f'For {key.isNeg} {key.name} len {len(rebuts[key])} :')
        for (arg1, arg2) in rebuts[key]:
            print(f'{arg1.name} -> {arg2.name}')
        print()
    print(len(rebuts))

if __name__ == "__main__":
    main()
    