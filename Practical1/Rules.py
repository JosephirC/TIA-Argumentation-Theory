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
        self.literalReference = "r" + str(Rules.ruleCount)

    # Handle equality between objects.
    # We dont check equality for names so we can test rules with different names --> duplicate rules
    def __eq__(self, other):
        return ((self.premises == other.premises 
                and self.conclusion == other.conclusion 
                and self.isDefeasible == other.isDefeasible ))

    # handle print of the class
    def __str__(self):
        ruleLiteralReference = "[" + self.literalReference + "] "
        rulePremises = ""
        ruleImplication = ""
        ruleConclusion = str(self.conclusion)

        for premise in self.premises:
            rulePremises = rulePremises + str(premise) + ","

        rulePremises = rulePremises[:-1] + " "

        if(self.isDefeasible):
            ruleImplication = "=> "
        else :
            ruleImplication = "->"
        
        return ruleLiteralReference + rulePremises + ruleImplication + ruleConclusion
        
    # handle hash of the class
    def __hash__(self):
        return hash((tuple(self.premises), self.conclusion, self.isDefeasible, self.literalReference))

    # set rule literal reference
    def setLiteralReference(self, literalReference):
        self.literalReference = literalReference




        
    

    