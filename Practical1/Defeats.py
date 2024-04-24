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
