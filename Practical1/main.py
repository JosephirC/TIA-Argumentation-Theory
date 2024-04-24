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

def generateUndercuts(bf):
    undercuts = {}
    conflict_arg = []

    for arg in bf.keys():
        if arg.topRule.premises:
            if isinstance(arg.topRule.conclusion, Rules.Rules):
                for other_arg in bf.keys():
                    other_rule = other_arg.topRule
                    arg_rule = arg.topRule.conclusion
                    other_defeasible = other_arg.getAllDefeasible()
                    arg_ruleCopy = arg_rule.copy()
                    if arg_ruleCopy.notRule(arg_rule.name) in other_defeasible:
                        notArg = arg
                        print(other_arg.name)
                        if other_arg.name not in conflict_arg:
                            conflict_arg.append(other_arg.name)
                    if arg not in undercuts:
                        undercuts[arg.name] = conflict_arg
                    else:
                        undercuts[arg.name] = conflict_arg

    return undercuts


def compare_arguments(arg1, arg2):
    return arg1.name != arg2.name

def generate_rebuts(bf):
    rebuts = {}
    print("Rebuts:")
    for arg in bf:
        contradicting_args = []
        for other_arg in bf:
            if compare_arguments(arg, other_arg):
                if arg.topRule.conclusion.contradicts(other_arg.topRule):
                    contradicting_args.append(other_arg.name)
        if contradicting_args:
            rebuts[arg.name] = contradicting_args
            print("affichage de rebuts")
            print("arg.name is", arg.name)
            print("OTHER_arg.name is", contradicting_args)

    return rebuts



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
        print(cleArg, cleArg.topRule)
    print()

    undercuts = generateUndercuts(bf)
    for undercut in undercuts:
        print(undercuts)
    print()

    rebuts = generate_rebuts(bf)
    
    for rebut in rebuts:
        print(rebuts)

    for cle in bf.keys():
        print(cle)
        defeasibleRules = cle.getAllDefeasible()
        print("Les règles defeasibles: ")
        for rules in defeasibleRules:
            print(rules.name)
        print("\n")

if __name__ == "__main__":
    main()