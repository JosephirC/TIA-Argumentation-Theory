import Literals
import Rules
import Arguments


# static bf to store all the arguments
bf = set()

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
        if len(rule.premises) == 0 and len(rule.conclusion) > 0:
            arg = Arguments.Arguments(rule, set())
            bf.add(arg)
            rulesCopy.remove(rule)
    
    return rulesCopy

#Idee debug
## faire sous des fonctions 
## déplacer le while de generateArgs pour faire un appel récursif dans generateArgsFromRules
## repenser a la logique de if premises in argtopruleccl (cas où on a 5 arg avec la même ccl)

def generateArgsFromRules(rules):
    argToAdd = set()
    for rule in rules:
        subArguments = set()
        for premise in rule.premises:
            for arg in bf:
                if premise in arg.topRule.conclusion:
                    subArguments.add(arg)
                    break

        if len(subArguments) == len(rule.premises):
            newArg = Arguments.Arguments(rule, subArguments)
            if newArg not in bf and newArg not in argToAdd:
                argToAdd.add(newArg)

    print("\n")
    for b in bf:
        print("current bf before update : ", b)
    
    for arg in argToAdd:
        print("current arg : ", arg)
    
    print("\n")
    bf.update(argToAdd)

    for b in bf:
        print("current bf after update : ", b)

    print("\n")
    print("E###################################")
    return len(argToAdd)

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
    # rulesWithNoArgs = generateInitialArguments(rules)
    
    countArg = generateArgsFromRules(rulesWithNoArgs)

    while countArg > 0:
        countArg = generateArgsFromRules(rulesWithNoArgs)
        # print("new count arg : ", countArg)
        break
        



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


    rule1 = Rules.Rules({}, {aF}, False)
    rule2 = Rules.Rules({bF, dF}, {cF}, False)
    rule3 = Rules.Rules({c}, {dF}, False)
    
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

    rule4 = Rules.Rules({aF}, {d}, True)
    rule5 = Rules.Rules({}, {bF}, True)
    rule6 = Rules.Rules({}, {c}, True)
    rule7 = Rules.Rules({}, {dF}, True)
    rule8 = Rules.Rules({cF}, {eF}, True)
    rule9 = Rules.Rules({c}, {rule4}, True)

    print(rule4)
    print(rule5)
    print(rule6)
    print(rule7)
    print(rule8)
    print(rule9)


    # Testing the generation of arguments
    print("\n")
    rules = {rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9}
    print("nbr of recursive calls : ", Arguments.Arguments.setOfArgs_call_count)

    generateArgs(rules)

if __name__ == "__main__":
    main()