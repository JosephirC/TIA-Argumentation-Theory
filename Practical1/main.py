import Literals
import Rules
import Arguments
import time
from GenerateArguments import generateArgs, getArgumentBase
from GenerateAttacks import generateUndercuts

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

    argumentBase = getArgumentBase()

    printSorted(argumentBase)    

    defeasibleRules = set()
    for arg in argumentBase:
        print(f"argument {arg}")
        defeasibleRules.update(arg.getAllDefeasible())
        print("The defeasible rules : ")

    undercuts = generateUndercuts(argumentBase)
    print("undercuts are : ", undercuts)
    print()

    print("\nundercuts done \n")

    for arg in argumentBase:
        print(arg)
        defeasibleRules = arg.getAllDefeasible()
        print("Les règles defeasibles: ")
        for rules in defeasibleRules:
            print(rules.name)
        print("\n")

if __name__ == "__main__":
    main()
