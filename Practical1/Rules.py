from Literals import Literals

class Rules:

    ruleCount = 0

    def __init__(self, premises, conclusion, isDefeasible, literal, weight=0):
        self.premises = premises
        self.conclusion = conclusion
        self.isDefeasible = isDefeasible
        Rules.ruleCount += 1
        self.weight = weight
        self.name : Literals = literal

    # Handle equality between objects.
    # We dont check equality for names so we can test rules with different names --> duplicate rules
    def __eq__(self, other):
        if not isinstance(other, Rules):
            return False
        if self.weight is not None:
            return ((self.premises == other.premises 
                and self.conclusion == other.conclusion 
                and self.isDefeasible == other.isDefeasible
                and self.weight == other.weight))
        else :
            return ((self.premises == other.premises 
                and self.conclusion == other.conclusion 
                and self.isDefeasible == other.isDefeasible))
    
    # handle print of the class
    def __str__(self):
        if "[" in str(self.name) and "]" in str(self.name):
            ruleName = self.name
        else: 
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
            ruleImplication = "=>"
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

            compt = Rules.ruleCount
            compt = compt + 1
            rX = Literals("r" + str(compt), self.name.isNeg)
            newRules.add(Rules(newPremise, newConclusion, self.isDefeasible, rX))

        return newRules

    def copy(self):
        """
        This method is used to create a copy of a rule object without incrementing the ruleCount.
        """

        # Rules.ruleCount -=1 
        return Rules(self.premises.copy(), self.conclusion.copy(), self.isDefeasible, self.name)
