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
            rulePremises += str(premise) + ","

        # for conclusion in self.conclusion:
        if(isinstance(self.conclusion, Rules)):
            ruleConclusion += self.conclusion.name + ","
        else :
            ruleConclusion += str(self.conclusion) + ","

        rulePremises = rulePremises[:-1] + " "
        ruleConclusion = ruleConclusion[:-1] + " "

        if self.isDefeasible:
            ruleImplication = "=> "
        else:
            ruleImplication = "->"

        return ruleName + rulePremises + ruleImplication + ruleConclusion
    
    # handle hash of the class
    def __hash__(self):
        return hash((tuple(self.premises), self.conclusion, self.isDefeasible, self.name))

    def contraposition(self):
        newRules = set()
        newPremise = set()

        if len(self.premises) == 1:
            conclusion = self.conclusion
            newPremise.add(conclusion.negate())

            literal = next(iter(self.premises))
            newRules.add(Rules(newPremise, literal.negate(), self.isDefeasible))

            return newRules
        
        else:
            conclusion = self.conclusion
            
            for premise in self.premises:
                currentLiteral = premise.negate()

                newPremise = self.premises.copy()
                newPremise.remove(premise)
                newPremise.add(conclusion.negate())

                newRules.add(Rules(newPremise, currentLiteral, self.isDefeasible))

            return newRules

    def notRule(self, name):
        if "¬" in name:
            self.name = name[1:] #pour garder le même nom de la règle
            self.premises = {literal.negate() for literal in self.premises}
            self.conclusion = self.conclusion.negate()
            return self
        else:    
            self.name = "¬" + name #pour garder le même nom de la règle
            self.premises = {literal.negate() for literal in self.premises}
            self.conclusion = self.conclusion.negate()
            return self
    
    def copy(self):
        Rules.ruleCount -=1 #pour ne pas rajouter une nouvelle règle dans la base
        return Rules(self.premises.copy(), self.conclusion.copy(), self.isDefeasible)
        

    def contradicts(self, other):
        return self.conclusion.contradicts(other.conclusion)
