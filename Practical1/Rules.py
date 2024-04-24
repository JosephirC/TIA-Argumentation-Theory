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
        if not isinstance(other, Rules):
            return False
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
        """
        This method is used to create a negated rule object.
        """

        if "¬" in name:
            self.name = name[1:]
            self.premises = {literal.negate() for literal in self.premises}
            self.conclusion = self.conclusion.negate()
            return self
        else:    
            self.name = "¬" + name 
            self.premises = {literal.negate() for literal in self.premises}
            self.conclusion = self.conclusion.negate()
            return self
    
    def copy(self):
        """
        This method is used to create a copy of a rule object without incrementing the ruleCount.
        """

        Rules.ruleCount -=1 
        return Rules(self.premises.copy(), self.conclusion.copy(), self.isDefeasible)
