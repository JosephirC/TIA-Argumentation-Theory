import itertools
import Arguments as Arguments
import Rules as Rules
import Literals as Literals

def find_combinations(dictionary, target_values):
    valid_combinations = set()
    keys = list(dictionary.keys())

    for r in range(1, len(keys) + 1):
        for combo in itertools.combinations(keys, r):
            values = set()
            for key in combo:
                values.update(dictionary[key])
            if len(tuple(combo)) == len(target_values) and set(values) == set(target_values):
                valid_combinations.add(tuple(combo))

    return valid_combinations


# Créer des objets Argument
a = Literals.Literals("a", True)
aF = Literals.Literals("a", False)
b = Literals.Literals("b", True)
bF = Literals.Literals("b", False)
c = Literals.Literals("c", True)
cF = Literals.Literals("c", False)
d = Literals.Literals("d", True)
dF = Literals.Literals("d", False)
eF = Literals.Literals("e", False)

rule1 = Rules.Rules({}, {aF}, False)
rule2 = Rules.Rules({}, {aF}, False)
rule5 = Rules.Rules({}, {bF}, True)
rule6 = Rules.Rules({}, {cF}, True)
arg1 = Arguments.Arguments(rule1, set())
arg2 = Arguments.Arguments(rule2, set())
arg3 = Arguments.Arguments(rule5, {arg1})
arg4 = Arguments.Arguments(rule6, {arg1, arg2})

rule99 = Rules.Rules({aF, bF, cF}, {eF}, True)

argTest = Arguments.Arguments(rule6, {arg2, arg1})
print("equal ?", arg1 == arg2)
print("equal ?", arg1 == arg1)
print("equal ?", arg4 == argTest)


dictionary = {arg1: arg1.topRule.conclusion, arg2: arg2.topRule.conclusion, arg3: arg3.topRule.conclusion, arg4: arg4.topRule.conclusion}

target_values = rule99.premises

combinations = find_combinations(dictionary, target_values)
for combination in combinations:
    for combination_key in combination:
        narg = Arguments.Arguments(rule99, combination)
        print(narg)

