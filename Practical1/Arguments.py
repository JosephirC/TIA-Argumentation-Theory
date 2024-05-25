class Arguments:
    nameCount = 0

    def __init__(self, topRule, subArguments):
        self.topRule = topRule
        self.subArguments = subArguments
        Arguments.nameCount += 1
        self.name = "A" + str(Arguments.nameCount)

    def __eq__(self, other):
        if not isinstance(other, Arguments):
            return False
        return (self.topRule.conclusion == other.topRule.conclusion
                and self.subArguments == other.subArguments)

    def __str__(self):
        argumentName = self.name + ": "
        argumentSubArgumentsList = []
        argumentSubArguments = ""
        argumentTopRule = self.topRule
        argumentImplication = ""
        argumentTopRuleConclusion = ""

        for subArgument in self.subArguments:
            argumentSubArgumentsList.append(subArgument)

        for argument in argumentSubArgumentsList:
            argumentSubArguments = argumentSubArguments + argument.name + ","

        argumentSubArguments = argumentSubArguments[:-1] + " "

        if(argumentTopRule.isDefeasible):
            argumentImplication = "=> "
        else :
            argumentImplication = "-> "

        argumentTopRuleConclusion = argumentTopRule.conclusion
            
        return argumentName + argumentSubArguments + argumentImplication + str(argumentTopRuleConclusion)

    def __hash__(self):
        return hash((self.topRule, tuple(self.subArguments), self.name))
    
    def getAllDefeasible(self):
        """
        Return all the defeasible rules of the argument
        """
        rulesDefeasible = set()

        if (self.topRule.isDefeasible):
            rulesDefeasible.add(self.topRule)
        for arg in self.subArguments:
                rulesDefeasible = rulesDefeasible.union(arg.getAllDefeasible())
                
        return rulesDefeasible

    def getLastDefeasible(self):
        """
        Return the last defeasible rule of the argument
        """
        rulesDefeasible = set()
        if(self.topRule.isDefeasible):
            rulesDefeasible.add(self.topRule)
        elif self.topRule.isDefeasible == False:
            for arg in self.subArguments:
                rulesDefeasible = rulesDefeasible.union(arg.getLastDefeasible())

        return rulesDefeasible
    
    def getAllSubArgs(self):
        """
        Return all the sub arguments of the argument
        """
        allSubArgs = set()
        for arg in self.subArguments:
            allSubArgs.add(arg)
            allSubArgs = allSubArgs.union(arg.getAllSubArgs())
        return allSubArgs
    