import Rules

class Arguments:

    setOfArgs_call_count = 0
    nameCount = 0

    def __init__(self, topRule, subArguments):
        self.topRule = topRule
        self.subArguments = subArguments
        Arguments.nameCount += 1
        self.name = "A" + str(Arguments.nameCount)

    def __eq__(self, other):
        return (self.topRule.conclusion == other.topRule.conclusion
                and self.subArguments == other.subArguments)

    # arguemtn example : $A_1: \rightarrow a$ == A1: -> a
    # argument example : $A_2: A_1 \Rightarrow c$ == A2: A2, A1 => c
    def __str__(self):
        argumentName = self.name + ": "
        argumentSubArgumentsList = []
        argumentSubArguments = ""
        argumentTopRule = self.topRule
        argumentImplication = ""
        argumentTopRuleConclusion = ""

        # Extracting all sub arguments and putting them in a list
        for subArgument in self.subArguments:
            for argument in subArgument.setOfArguemnts():
                argumentSubArgumentsList.append(argument)

        # Extracting unique arguments from the list
        argumentSubArgumentsList = self.extractUniqueArguments(argumentSubArgumentsList)

        # Creating the string of unique sub arguments
        for argument in argumentSubArgumentsList:
            argumentSubArguments = argumentSubArguments + argument + ","

        if(argumentTopRule.isDefeasible):
            argumentImplication = "=> "
        else :
            argumentImplication = "->"

        if isinstance(argumentTopRule.conclusion, Rules.Rules):
            argumentTopRuleConclusion = argumentTopRule.conclusion.name
        else:
            argumentTopRuleConclusion = argumentTopRule.conclusion
            
        return argumentName + argumentSubArguments + argumentImplication + str(argumentTopRuleConclusion)

    def __hash__(self):
        return hash((self.topRule, tuple(self.subArguments), self.name))

    @staticmethod
    def extractUniqueArguments(arguments):
        uniqueArguments = []

        for argument in arguments:
            if argument not in uniqueArguments:
                uniqueArguments.append(argument)

        return uniqueArguments

    def setOfArguemnts(self):
        Arguments.setOfArgs_call_count += 1

        allArguments = [self.name]

        for subArgument in self.subArguments:
            for argument in subArgument.setOfArguemnts():
                allArguments.append(argument)

        return self.extractUniqueArguments(allArguments)
    
    def getAllDefeasible(self):
        rulesDefeasible = set()
        if(self.topRule.isDefeasible):
            rulesDefeasible.add(self.topRule)
        for arg in self.subArguments:
                rulesDefeasible = rulesDefeasible.union(arg.getAllDefeasible())
        return rulesDefeasible

    def getLastDefeasible(self):
        rulesDefeasible = set()
        if(self.topRule.isDefeasible):
            rulesDefeasible.add(self.topRule)
        return rulesDefeasible

    def getAllSubArg(self):
        rulesDefeasible = set()
        for arg in self.subArguments:
            rulesDefeasible.add(arg)
        return rulesDefeasible
