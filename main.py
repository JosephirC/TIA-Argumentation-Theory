class Literals :
        
    def __init__(self, name, neg):
        self.name = name
        self.neg = neg 
    
    def __str__(self):
        if self.neg:
            return "!" + self.name
        else:
            return self.name
    
    def __eq__(self, other):
        return (self.name == other.name and self.neg == other.neg)
    
    def op(self):
        return Literals(self.name, not self.neg)
        
class Rules:
    compt = 0

    def __init__(self, setLit, defeasible, concl):
        self.setLit = setLit
        self.defeasible = defeasible 
        self.concl = concl
        Rules.compt = Rules.compt + 1
        self.name = "r" + str(Rules.compt)

    def __str__(self):
        tabLit = ""
        for lit in self.setLit:
            tabLit = tabLit + str(lit) + ", "
        if(self.defeasible):
            return "[" + self.name + "]" + tabLit + "=>" + str(self.concl)
        else:
            return "[" + self.name + "]" + tabLit + "->" + str(self.concl)
        
    def __eq__(self, other):
        return (self.setLit == other.setLit and self.concl == other.concl and self.defeasible == other.defeasible)
    
    def contraposition(self):
        if(len(self.setLit) == 1):
            setList = Literals.op(self.concl)
            concl = Literals.op(self.setLit)
            print(setList)
            return Rules(setList, self.defeasible, concl)

class Arguments:

    def __init__(self, topRule, subArg, name):
        self.topRule = topRule
        self.subArg = subArg 
        self.name = name

    def __str__(self):
        if(self.subArg):
            tabArgName = ""
            for arg in self.subArg:
                tabArgName = tabArgName + arg.name + ", "
                for subArg in arg.subArg: 
                    tabArgName = tabArgName + subArg.name + ", "

            if self.topRule.defeasible:
                return  self.name  + ": " + tabArgName + "=>" + str(self.topRule.concl)
            else:
                return  self.name  + ": " + tabArgName + "->" + str(self.topRule.concl)
        else:
            return  self.name  + ": "  + str(self.topRule)    
    
    def __eq__(self, other):
        return (self.topRule == other.topRule and self.subArg == other.subArg)

def main():
    a = Literals("a", True)
    b = Literals("b", False)
    c = Literals("c", False)
    d = Literals("d", False)
    print(a)
    print(a == a)
    rule = Rules([a, b, c], True, d)
    rule2 = Rules([a], True, c)
    # a1 = Arguments(Rules(None, False, a), None, "A1")
    # a2 = Arguments(Rules([a], True, c), [a1], "A2")
    # print(a2)

    arguement1 = Arguments(rule, None, "A1")
    arguement2 = Arguments(rule2, [arguement1], "A2")

    arguement3 = Arguments(rule, [arguement2], "A3")
    arguement4 = Arguments(rule2, [arguement3], "A4")
    arguement5 = Arguments(rule, [arguement4, arguement3], "A5")
    print(arguement5)

    rule3 = Rules([a], False, c)
    rule4 = Rules.contraposition(rule3)
    print(rule4)

main()

