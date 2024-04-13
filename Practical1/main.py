import Literals
import Rules
import Arguments

def main():
    a = Literals.Literals("a", False)
    b = Literals.Literals("b", False)
    c = Literals.Literals("c", True)
    d = Literals.Literals("d", True)
    e = Literals.Literals("e3", False)

    print("literal a : ", a)

    newRule = Rules.Rules({a, b, c, d, e}, {e}, True)

    print("new rule " , newRule)

    rule1 = Rules.Rules({a}, {b}, True)
    print(rule1.name)
    rule2 = Rules.Rules({a}, {b}, True)
    print(rule2.name)
    print(rule1 == rule2)
    rule3 = Rules.Rules({a}, {b}, True)
    rule3.setLiteralReference("r12")
    print(rule1.name + " " + rule3.name)
    print(rule1 == rule3)

    print("\n")

    # Testing Arguments
    arguement1 = Arguments.Arguments(rule1, set())
    arguement2 = Arguments.Arguments(rule2, {arguement1})
    print(arguement2)

    arguement3 = Arguments.Arguments(rule1, {arguement2})
    arguement4 = Arguments.Arguments(rule2, {arguement3})
    arguement5 = Arguments.Arguments(rule1, {arguement4, arguement3})

    print(arguement5.setOfArguemnts())
    print(arguement5)

    l1 = Literals.Literals("test", True)
    print(l1)
    print(l1.negate())

    # Testing contraposition
    contrapositionRules = rule1.contraposition()
    print("TESTING CONTRAPOSITION, LEN 1")
    print("Rule 1 before contraposition " , rule1)
    print("Rule 1 after contraposition ")
    for rule in contrapositionRules:
        print(rule)

    print("\n")
    print("TESTING CONTRAPOSITION, LEN > 1")
    rule4 = Rules.Rules({a, d}, {b}, True)
    contrapositionRules = rule4.contraposition()
    print("Rule 4 before contraposition " , rule4)
    print("Rule 4 after contraposition ")
    for rule in contrapositionRules:
        print(rule)


if __name__ == "__main__":
    main()