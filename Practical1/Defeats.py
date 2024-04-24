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


"""
une fonction qui prend arg1 et arg2 et le method (democratic ou elitist) et le principal (last link ou weakest link)
selon ces parametres je fais le calcul des defeats
il faut utiliser les fonctions de la classe Arguments : getAllDefeasible, getLastDefeasible

"""

def democraticWeakestLink(arg1, arg2):
    allDefeasible1 = arg1.getAllDefeasible()
    allDefeasible2 = arg2.getAllDefeasible()

    for ruleArg2 in allDefeasible2:
        comparisonCounter = 0
        for ruleArg1 in allDefeasible1:
            
            if ruleArg1.isDefeasible and ruleArg2.isDefeasible:
                if ruleArg1.weight >= ruleArg2.weight:
                    comparisonCounter += 1
            
            elif not (ruleArg1.isDefeasible) and ruleArg2.isDefeasible:
                comparisonCounter += 1
            
            elif ruleArg1.isDefeasible and not (ruleArg2.isDefeasible):
                continue

            elif not (ruleArg1.isDefeasible) and not (ruleArg2.isDefeasible):
                comparisonCounter += 1

        if comparisonCounter == len(allDefeasible1):
            return True
        
    return False
        
    
def democraticLastLink(arg1, arg2):
    pass

def elitistWeakestLink(arg1, arg2):
    pass

def elitistLastLink(arg1, arg2):
    pass

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