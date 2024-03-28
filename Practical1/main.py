import Literals
import Rules
import Arguments



def main():
    # Your code here
    # rule = Rules.Rules(["a", "b", "c"], "e", True, "r1")
    # print(rule.name)

    a = Literals.Literals("a", False)
    b = Literals.Literals("b", False)
    c = Literals.Literals("c", True)
    d = Literals.Literals("d", True)
    e = Literals.Literals("e3", False)

    newRule = Rules.Rules({a, b, c, d, e}, "e", True)

    print(newRule)

    # Equality test between rules
    a = Literals.Literals("a", False)

    rule1 = Rules.Rules({a}, "b", True)
    print(rule1.literalReference)
    rule2 = Rules.Rules({a}, "b2", True)
    print(rule2.literalReference)
    print(rule1 == rule2)
    rule3 = Rules.Rules({a}, "b", True)
    rule3.setLiteralReference("r12")
    print(rule1.literalReference + " " + rule3.literalReference)
    print(rule1 == rule3)


    # Testing Arguments
    arguement1 = Arguments.Arguments(rule1, set())
    arguement2 = Arguments.Arguments(rule2, {arguement1})
    print(arguement2)

    arguement3 = Arguments.Arguments(rule1, {arguement2})
    arguement4 = Arguments.Arguments(rule2, {arguement3})
    arguement5 = Arguments.Arguments(rule1, {arguement4, arguement3})

    print(arguement5.setOfArguemnts())
    print(arguement5)


if __name__ == "__main__":
    main()