# Rules are objects which are referred by their premises (set of literals), its conclusion (a literal), a boolean which indicates if the rule is 
# defeasible or not, and a literal (e.g., $r_1$) which uniquely references it. 
# An object of this class would be used to represent: $r_1: a, \neg b, c \Rightarrow e$ or $r_2: \rightarrow \neg a$


class Rules:

    ruleCount = 0

    def __init__(self, premises, conclusion, isDefeasible):
        self.premises = premises
        self.conclusion = conclusion
        self.isDefeasible = isDefeasible
        Rules.ruleCount += 1
        self.name = "r" + str(Rules.ruleCount)

    # Handle equality between objects.
    # We dont check equality for names so we can test rules with different names --> duplicate rules
    def __eq__(self, other):
        return ((self.premises == other.premises 
                and self.conclusion == other.conclusion 
                and self.isDefeasible == other.isDefeasible ))

    # handle print of the class
    def __str__(self):
        ruleName = "[" + self.name + "] "
        rulePremises = ""
        ruleImplication = ""
        ruleConclusion = ""

        for premise in self.premises:
            rulePremises = rulePremises + str(premise) + ","

        for conclusion in self.conclusion:
            ruleConclusion = ruleConclusion + str(conclusion) + ","

        rulePremises = rulePremises[:-1] + " "
        ruleConclusion = ruleConclusion[:-1] + " "

        if(self.isDefeasible):
            ruleImplication = "=> "
        else :
            ruleImplication = "->"
        
        return ruleName + rulePremises + ruleImplication + ruleConclusion
        
    # handle hash of the class
    def __hash__(self):
        return hash((tuple(self.premises), tuple(self.conclusion), self.isDefeasible, self.name))

    # set rule literal reference
    def setLiteralReference(self, name):
        self.name = name


    # Write a function that creates contraposition rules for strict rules. Create the following rules and display them. 
    # You should obtain a prompt similar to what is displayed below.

    # Example : a,d -> b becomes d, ¬b -> ¬a    
        

    #### Prof : 
            # je cree un literal qui a la negation du premise courant -->   o  
            # je dois creer un ensemble de literal qui contient le nv literal 
            # tous les autres literaux de self.premise sauf premise   --> ensemble qui contient "o" qui contient tous les 
    
    
    ### ME : 
        # a,b ->d becomes { {a, ¬d -> ¬b}, {b, ¬d -> ¬a}} 

    def contraposition(self):
        newPremise = set()
        newConclusion = set()

        print("Self?" , self)


        if len(self.premises) == 1 and len(self.conclusion) == 1 :
            literal = next(iter(self.conclusion))
            newPremise.add(literal.negate())
            literal = next(iter(self.premises))
            newConclusion.add(literal.negate())

            return Rules(newPremise, newConclusion, self.isDefeasible)


        
    

    