from Literals import Literals

class Rules:

    ruleCount = 0

    def __init__(self, premises, conclusion, isDefeasible, literalReference, weight=0):
        self.premises = premises
        self.conclusion = conclusion
        self.isDefeasible = isDefeasible
        Rules.ruleCount += 1
        self.literalReference : Literals = literalReference
        self.weight = weight

    def __eq__(self, other):
        if not isinstance(other, Rules):
            return False
        else:
            return ((self.premises == other.premises 
                and self.conclusion == other.conclusion 
                and self.isDefeasible == other.isDefeasible
                and self.literal == other.literal
                and self.weight == other.weight))

    def __str__(self):
        if "[" in str(self.literalReference) and "]" in str(self.literalReference):
            ruleName = self.literalReference
        else: 
            ruleName = "[" + str(self.literalReference) + "] "
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
            ruleImplication = "⇒ "
            ruleWeight = str(self.weight)
        else:
            ruleImplication = "→ "

        return ruleName + rulePremises + ruleImplication + ruleConclusion + ruleWeight
    
    # handle hash of the class
    def __hash__(self):
        return hash((tuple(self.premises), self.conclusion, self.isDefeasible, self.literalReference, self.weight))

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
            rX = Literals("r" + str(compt), self.literalReference.isNeg)
            newRules.add(Rules(newPremise, newConclusion, self.isDefeasible, rX))

        return newRules

    def copy(self):
        """
        This method is used to create a copy of a rule object.
        """
        return Rules(self.premises.copy(), self.conclusion.copy(), self.isDefeasible, self.literalReference)
