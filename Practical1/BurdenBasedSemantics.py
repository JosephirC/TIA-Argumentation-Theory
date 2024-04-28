from collections import defaultdict

tempDict = {}

def getAttack(arg, defeats):
    """
    Get the attack of an argument
    """
    attack = set()
    for key in defeats:
        for (arg1, arg2) in defeats[key]:
            if arg2.name == arg.name:
                attack.add(arg1)

    return attack

def init(argument_base):
    """
    Initialize the dictionary with burden value 1 for each argument
    """
    for arg in argument_base:
        tempDict[arg.name] = [1]

def burden(argument_base, defeats, i):
    """
    Compute the burden of each argument for the i-th iteration
    """
    if i == 0:
        init(argument_base)
    else:
        for arg in argument_base:
            attack = getAttack(arg, defeats)
            sum = 0
            for a in attack:
                sum = sum + (1 / tempDict[a.name][i-1])

            tempDict[arg.name].append(sum + 1)

def computeBurden(argBase, defeats, depth):
    """
    Compute the burden of each argument for a given depth
    """
    tempDict.clear()

    for i in range(depth): 
        burden(argBase, defeats, i)

    return tempDict


def compareArgRankings(burdenValues):
    """
    Compares the ranking of arguments
    """

    groupedRankings = {}

    for argument, scores in burdenValues.items():
        scores_tuple = tuple(scores)
        if scores_tuple not in groupedRankings:
            groupedRankings[scores_tuple] = []
        groupedRankings[scores_tuple].append(argument)

    sorted_scores = sorted(groupedRankings.keys())

    result = ""
    for scores in sorted_scores:
        arguments = ", ".join(groupedRankings[scores])
        if result:
            result += " > "
        result += arguments

    return result
