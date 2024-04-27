def makePreferred(rules):
    preferred = {}
    for rule in rules:
        if rule.isDefeasible:
            preferred[rule] = str(rule.weight)
        else:
            preferred[rule] = ""
    return preferred

def comparePreferred(preferred):
    sortedRules = set()
    fiilteredRules = set()

    for ruleKey in preferred:
        if preferred[ruleKey] != "":
            fiilteredRules.add(ruleKey)

    sortedRules = sorted(fiilteredRules, key=lambda rule: int(preferred[rule]), reverse=True)

    groupedWeights = {}
    for rule in sortedRules:
        weight = int(preferred[rule])
        if weight not in groupedWeights:
            groupedWeights[weight] = []
        groupedWeights[weight].append(rule.name.name)

    result = ""
    for weight in sorted(groupedWeights.keys(), reverse=True):
        rules = ", ".join(groupedWeights[weight])
        if result:
            result += " > "
        result += rules

    return result

def findOppositeArgs(arg1, arg2):
    
    if arg1.topRule.conclusion == arg2.topRule.conclusion.negate():
        return (arg1, arg2)
    elif arg2.subArguments:
        for subarg2 in arg2.subArguments:
            result = findOppositeArgs(arg1, subarg2)
            if result:
                return result
    return None

def findOppositeArgsFromTuple(arg1, arg2):
    result = findOppositeArgs(arg1, arg2)
    if result:
        return result
    elif arg2.subArguments:
        for subarg2 in arg2.subArguments:
            result = findOppositeArgs(arg1, subarg2)
            if result:
                return result
    return None

def democraticWeakestLink(arg1, arg2):
    
    result = findOppositeArgsFromTuple(arg1, arg2)
    arg1AttacerArgs = [ result[0] ]
    arg2AttacerArgs = [ result[1] ]
    
    allDefeasible1 = []
    allDefeasible2 = []

    for arg in arg1AttacerArgs:
        for attack in arg.getAllDefeasible():
            allDefeasible1.append(attack)

    for arg in arg2AttacerArgs:
        for attack in arg.getAllDefeasible():
            allDefeasible2.append(attack)

    if not allDefeasible1:
        return True
    
    if not allDefeasible2:
        return False

    for ruleArg2 in allDefeasible2:
        comparisonCounter = 0
        for ruleArg1 in allDefeasible1:
            if ruleArg1.weight >= ruleArg2.weight:
                comparisonCounter += 1

            if comparisonCounter == len(allDefeasible1):
                return True

    return False

def democraticLastLink(arg1, arg2):
    
    result = findOppositeArgsFromTuple(arg1, arg2)
    arg1AttacerArgs = [ result[0] ]
    arg2AttacerArgs = [ result[1] ]

    allDefeasible1 = []
    allDefeasible2 = []

    for arg in arg1AttacerArgs:
        for attack in arg.getLastDefeasible():
            allDefeasible1.append(attack)

    for arg in arg2AttacerArgs:
        for attack in arg.getLastDefeasible():
            allDefeasible2.append(attack)

    if not allDefeasible1:
        return True
    
    if not allDefeasible2:
        return False
    
    for ruleArg2 in allDefeasible2:
        comparisonCounter = 0
        for ruleArg1 in allDefeasible1:
            if ruleArg1.weight >= ruleArg2.weight:
                comparisonCounter += 1

            if comparisonCounter == len(allDefeasible1):
                return True
        
    return False

def elitistWeakestLink(arg1, arg2):

    result = findOppositeArgsFromTuple(arg1, arg2)
    arg1AttacerArgs = [ result[0] ]
    arg2AttacerArgs = [ result[1] ]

    allDefeasible1 = []
    allDefeasible2 = []

    for arg in arg1AttacerArgs:
        for attack in arg.getAllDefeasible():
            allDefeasible1.append(attack)

    for arg in arg2AttacerArgs:
        for attack in arg.getAllDefeasible():
            allDefeasible2.append(attack)

    if not allDefeasible1:
        return True
    
    if not allDefeasible2:
        return False
    
    for ruleArg1 in allDefeasible1:
        comparisonCounter = 0
        for ruleArg2 in allDefeasible2:
            if ruleArg1.weight >= ruleArg2.weight:
                comparisonCounter += 1

        if comparisonCounter == len(allDefeasible2):
            return True
        
    return False

def elitistLastLink(arg1, arg2):

    result = findOppositeArgsFromTuple(arg1, arg2)
    arg1AttacerArgs = [ result[0] ]
    arg2AttacerArgs = [ result[1] ]

    allDefeasible1 = []
    allDefeasible2 = []

    for arg in arg1AttacerArgs:
        for attack in arg.getLastDefeasible():
            allDefeasible1.append(attack)

    for arg in arg2AttacerArgs:
        for attack in arg.getLastDefeasible():
            allDefeasible2.append(attack)

    if not allDefeasible1:
        return True
    
    if not allDefeasible2:
        return False
    
    for ruleArg1 in allDefeasible1:
        comparisonCounter = 0
        for ruleArg2 in allDefeasible2:
            if ruleArg1.weight >= ruleArg2.weight:
                comparisonCounter += 1

        if comparisonCounter == len(allDefeasible2):
            return True
        
    return False    

def defeat(arg1, arg2, method, principal):

    if method == "democratic" and principal == "weakest-link":
        if (democraticWeakestLink(arg1, arg2)):
            return (arg1, arg2)
    elif method == "democratic" and principal == "last-link":
        if (democraticLastLink(arg1, arg2)):
            return (arg1, arg2)
    elif method == "elitist" and principal == "weakest-link":
        if (elitistWeakestLink(arg1, arg2)):
            return (arg1, arg2)
    elif method == "elitist" and principal == "last-link":
        if (elitistLastLink(arg1, arg2)):
            return (arg1, arg2)
    return None
