import Literals

class Rules:

    def __init__(self, premises, conclusion, isDefeasible, literal, weight=None):
        self.premises = premises
        self.conclusion = conclusion
        self.isDefeasible = isDefeasible
        
        if weight is None:
            if isDefeasible:
                if len(premises) == 0:
                    self.weight = 1
                else:
                    self.weight = 0
        else:
            self.weight = weight

        self.name : Literals = literal

    # Handle equality between objects.
    # We dont check equality for names so we can test rules with different names --> duplicate rules
    def __eq__(self, other):
        if not isinstance(other, Rules):
            return False
        return ((self.premises == other.premises 
                and self.conclusion == other.conclusion 
                and self.isDefeasible == other.isDefeasible
                and self.weight == other.weight))
    
    # handle print of the class
    def __str__(self):
        ruleName = "[" + str(self.name) + "] "
        rulePremises = ""
        ruleImplication = ""
        ruleConclusion = ""
        ruleWeight = ""

        for premise in self.premises:
            rulePremises += str(premise) + ","

        ruleConclusion += str(self.conclusion) + ","

        rulePremises = rulePremises[:-1] + " "
        ruleConclusion = ruleConclusion[:-1] + " "

        if self.isDefeasible:
            ruleImplication = "=> "
            ruleWeight = str(self.weight)
        else:
            ruleImplication = "->"

        return ruleName + rulePremises + ruleImplication + ruleConclusion + ruleWeight
    
    # handle hash of the class
    def __hash__(self):
        return hash((tuple(self.premises), self.conclusion, self.isDefeasible, self.name))

    def contraposition(self):
        newRules = set()
        newPremise = set()
        conclusion = self.conclusion
        
        for premise in self.premises:
            newConclusion = premise.negate()

            newPremise = self.premises.copy()
            newPremise.remove(premise)
            newPremise.add(conclusion.negate())

            newRules.add(Rules(newPremise, newConclusion, self.isDefeasible, self.name))

        return newRules

    def copy(self):
        """
        This method is used to create a copy of a rule object without incrementing the ruleCount.
        """

        Rules.ruleCount -=1 
        return Rules(self.premises.copy(), self.conclusion.copy(), self.isDefeasible, self.name)
