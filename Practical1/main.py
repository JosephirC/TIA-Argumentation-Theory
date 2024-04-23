import Literals
import Rules
import Arguments
import itertools
import time

# static bf to store all the arguments
# bf = set()
bf = {

}

undercut = {

}

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
            bf[arg] = arg.topRule.conclusion
         
def generateInitialArguments(rules):
    rulesCopy = rules.copy()
    for rule in rules:
        if len(rule.premises) == 0 :
            arg = Arguments.Arguments(rule, set())
            bf[arg] = arg.topRule.conclusion
            rulesCopy.remove(rule)
    
    return rulesCopy

def find_combinations(target_values):
    valid_combinations = set()
    keys = list(bf.keys())

    for r in range(1, len(keys) + 1):
        for combo in itertools.combinations(keys, r):
            values = set()
            for key in combo:
                values.add(bf[key])
            if len(tuple(combo)) == len(target_values) and set(values) == set(target_values):
                valid_combinations.add(tuple(combo))

    return valid_combinations

def generateArgsFromRules(rules):
    argToAdd = set()
    for rule in rules:
        combination = find_combinations(rule.premises) 
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
        bf[key] = key.topRule.conclusion
    
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

# def generateAttacks(bf):
#     undercuts = {}
#     for cleArg in bf.keys():
#         print(cleArg.name)
#         if(cleArg.topRule.premises is not None and not(isinstance(cleArg.topRule.conclusion, Literals.Literals))) :
#             top = cleArg.topRule
#             for autrecleArg in bf.keys():
#                 if cleArg != autrecleArg: # vérifier que cleArg et autrecleArg sont différents
#                     autreTop = autrecleArg.topRule
#                     if top.conclusion == autreTop.premises:
#                         # print("in if : conclusion == premises", autreTop.name)
#                         undercuts[cleArg.name] = autrecleArg.name
#                     else:
#                         if isinstance(cleArg, Arguments.Arguments):
#                             for subArgument in cleArg.subArguments:
#                                 if(subArgument.topRule.conclusion == autreTop.conclusion):
#                                     if(top == autreTop):
#                                         # print("subArg", cleArg.name, ": ", top.conclusion)
#                                         undercuts[cleArg.name] = subArgument.topRule.name
#                             # if top.premises and autreTop.conclusion in top.premises:
#                             #     undercut[cleArg.name] = autrecleArg.name

#     return undercuts

# def generateAttacks(bf):
#     undercuts = {}
#     for cleArg in bf.keys():
#         if cleArg.topRule.premises : 
#             # if isinstance(cleArg.topRule.conclusion, Rules.Rules) :
#             #     print("les arguments du premier for ", cleArg.name, ": ", cleArg.topRule.conclusion)
#             #     top = cleArg.topRule
#             #     for autrecleArg in bf.keys():
#             #         if cleArg != autrecleArg: # vérifier que cleArg et autrecleArg sont différents
#             #             autreTop = autrecleArg.topRule
#             #             autreConclusion = autreTop.conclusion
#             #             if isinstance(autreConclusion, Literals.Literals) :
#             #                 if top.conclusion == autreConclusion.negate(): 
#             #                     undercuts[cleArg.name] = autrecleArg.name
#             #                 else:
#             #                     for subArgument in cleArg.subArguments:
#             #                         if(subArgument.topRule.conclusion.negate() == autreTop.conclusion):
#             #                             undercuts[cleArg.name] = autrecleArg.name
#             #             elif isinstance(autreConclusion, Rules.Rules) :
#             #                 if autreConclusion == top.conclusion.negate() and top.notRule(top.name) == autreTop:
#             #                     undercuts[autrecleArg.name] = cleArg.name
#             #             # else:
#             #             #     if isinstance(cleArg, Arguments.Arguments):
#             #             #         if autrecleArg in cleArg.subArguments:
#             #             #             undercuts[autrecleArg.name] = cleArg.name
#             #             #         else:
#             #             #             for subArgument in cleArg.subArguments:
#             #             #                 if(subArgument.topRule.conclusion == autreTop.conclusion):
#             #             #                     if(top == autreTop):
#             #             #                         undercuts[cleArg.name] = subArgument.topRule.name
#             # else :
#             top = cleArg.topRule
#             print("les arguments du premier for ", cleArg.name, ": ", cleArg.topRule.conclusion)
#             for autrecleArg in bf.keys():
#                 if cleArg != autrecleArg:
#                     autreTop = autrecleArg.topRule
#                     autreConclusion = autreTop.conclusion
#                     print("les arguments du 2e for ", autrecleArg.name, ": ", autreConclusion)
#                     ##TODO ne rentre pas dans les if... => isinstance ne marche pas...
#                     if isinstance(autreConclusion, Literals.Literals) :
#                         print("ccl instance of Literals : ", autrecleArg.name)
#                         if top.conclusion == autreConclusion.negate(): #autreConclusion.negate(): #marche pas car set...
#                             print("ccl = autreccl.negate()", top.conclusion.name, autreConclusion.negate())
#                             undercuts[cleArg.name] = autrecleArg.name
#                         else:
#                             for subArgument in cleArg.subArguments:
#                                 if(subArgument.topRule.conclusion.negate() == autreTop.conclusion):
#                                     undercuts[cleArg.name] = autrecleArg.name
#                     elif isinstance(autreConclusion, Rules.Rules) :
#                         print("ccl instance of Rules : ", autrecleArg.name)
#                         if autreConclusion == top.conclusion.negate() or top.notRule(top.name) == autreTop:
#                             print("ccl = autreccl.negate()", top.conclusion.name, autreConclusion.negate())
#                             undercuts[autrecleArg.name] = cleArg.name
#                         else:
#                             for subArgument in cleArg.subArguments:
#                                 print("subArg: ", subArgument.name)
#                                 if(subArgument.topRule.conclusion.negate() == autreTop.conclusion or top.notRule(top.name) == autreTop):
#                                     print("ccl = autreccl.negate()", top.conclusion.name, autreConclusion.negate())
#                                     undercuts[cleArg.name] = autrecleArg.name


#     return undercuts


# def generateAttacks(bf):
#     undercut = {}
#     for arg1 in bf:
#         for arg2 in bf:
#             print(bf[arg2])
#             lit = bf[arg2]
#             if arg1 != arg2 and bf[arg1] == lit.negate():
#                 undercut[arg1] = arg2
#     return undercut


# def generateAttacks(arguments):
#     undercuts = {}

#     for arg1 in arguments.keys():
#         for arg2 in arguments.keys():
#             if arg1 != arg2 and arg1.topRule.conclusion != arg2.topRule.conclusion:
#                 for conclusion in arg1.topRule.conclusion:
#                     lit = conclusion
#                     if lit.negate() in arg2.topRule.conclusion:
#                         undercuts[arg1] = arg2

#     return undercuts

# def generateAttacks(bf):
#     undercuts = {}

#     for arg1, conclusion1 in bf.items():
#         for arg2, conclusion2 in bf.items():
#             if arg1 != arg2:
#                 is_contradictory = False
#                 for lit1 in conclusion1:
#                     if isinstance(lit1, Literals.Literals):
#                         if lit1.negate() in conclusion2:
#                             is_contradictory = True
#                             break
#                         else :
#                             for subArg in arg2.subArguments:
#                                 for lit in subArg.topRule.conclusion: 
#                                     if isinstance(lit1, Literals.Literals):
#                                         if lit.negate() in conclusion2:
#                                             is_contradictory = True
#                                             break
#                     elif isinstance(lit1, Rules.Rules):
#                         for lit2 in conclusion2:
#                             if isinstance(lit2, Literals.Literals) and lit2.negate() in lit1.conclusion:
#                                 is_contradictory = True
#                                 break
#                         if is_contradictory:
#                             break
#                 if is_contradictory:
#                     if arg1 not in undercuts:
#                         undercuts[arg1.name] = set()
#                     undercuts[arg1.name].add(arg2.name)

#     return undercuts

def generateAttacks(bf):
    undercuts = {}

    for arg in bf.keys():
        if arg.topRule.premises:
            for conclusion in other_arg.topRule.conclusion:
                if isinstance(conclusion, Rules.Rules):
                    print("arg : ", arg.topRule.name, "other arg: ", other_arg.topRule.name, conclusion.name)
                    for other_arg in bf.keys():
                        if arg != other_arg and arg.topRule == conclusion.notRule(conclusion.name):
                            print("dans le if:", other_arg.name)
                            conflicting_rules = set(arg.topRule.premises) & set(other_arg.topRule.premises)
                            if conflicting_rules and arg.topRule.conclusion != conclusion:
                                if arg in undercuts:
                                    undercuts[arg.name].add(other_arg.name)
                                else:
                                    undercuts[arg.name] = {other_arg.name}

    return undercuts

# def generateAttacks(bf):
#     undercuts = {}
#     for cleArg in bf.keys():
#         print(cleArg.name)
#         if(cleArg.topRule.premises is not None) :
#             top = cleArg.topRule
#             for autrecleArg in bf.keys():
#                 if cleArg != autrecleArg: # vérifier que cleArg et autrecleArg sont différents
#                     autreTop = autrecleArg.topRule
#                     print(autreTop.name)
#                     if(top == autreTop):
#                         if(top.conclusion == autreTop.conclusion) :
#                             undercut[cleArg.name] = autrecleArg.name
#                     else:
#                         if isinstance(cleArg, Arguments.Arguments):
#                             for subArgument in cleArg.subArguments:
#                                 print("subArg", subArgument.name)
#                                 if(top == autreTop):
#                                     if(subArgument.topRule.conclusion == autreTop.conclusion) :
#                                         undercut[cleArg.name] = subArgument.topRule.name
#     return undercut
            

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

    contrapositionRules = rule1.contraposition()
    for rule in contrapositionRules:
        print(rule)
    
    contrapositionRules = rule2.contraposition()
    for rule in contrapositionRules:
        print(rule)

    contrapositionRules = rule3.contraposition()
    for rule in contrapositionRules:
        print(rule)

    rule4 = Rules.Rules({aF}, d, True)
    rule5 = Rules.Rules({}, bF, True)
    rule6 = Rules.Rules({}, c, True)
    rule7 = Rules.Rules({}, dF, True)
    rule8 = Rules.Rules({cF}, eF, True)
    notRule4:Rules.Rules = rule4.copy()
    rule9 = Rules.Rules({c}, notRule4.notRule(rule4.name), True)

    print(rule4)
    print(rule5)
    print(rule6)
    print(rule7)
    print(rule8)

    print(rule9, notRule4)


    # Testing the generation of arguments
    print("\n")
    rules = {rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9}
    print("nbr of recursive calls : ", Arguments.Arguments.setOfArgs_call_count)
    deb  = time.time()
    generateArgs(rules)
    fin = time.time()
    print("temp", fin-deb)

    for cleArg in bf.keys():
        print(cleArg)

    for cle in bf.keys():
        print(cle)
        defeasibleRules = cle.getAllDefeasible()
        print("Les règles defeasibles: ")
        for rules in defeasibleRules:
            print(rules.name)
        print("\n")

    undercuts = generateAttacks(bf)
    print(undercuts)

if __name__ == "__main__":
    main()