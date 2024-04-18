import itertools
import Arguments as Arguments
import Rules as Rules
import Literals as Literals

def find_combinations(dictionary, target_values):
    valid_combinations = set()
    keys = list(dictionary.keys())

    for r in range(1, len(keys) + 1):
        for combo in itertools.combinations(keys, r):
            values = set.union(*[dictionary[key] for key in combo])
            if len(tuple(combo)) == len(target_values) and set(values) == set(target_values):
                valid_combinations.add(tuple(combo))

    return valid_combinations

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
rule7 = Rules.Rules({}, {eF}, True)
arg1 = Arguments.Arguments(rule1, set())
arg2 = Arguments.Arguments(rule2, set())
arg3 = Arguments.Arguments(rule5, {arg1})
arg99 = Arguments.Arguments(rule7, set())
arg5 = Arguments.Arguments(rule6, {arg99, arg1, arg3})

rule99 = Rules.Rules({aF, bF, cF}, {eF}, True)

dictionary = {arg1: arg1.topRule.conclusion, arg2: arg2.topRule.conclusion, arg3: arg3.topRule.conclusion, arg5: arg5.topRule.conclusion}

target_values = rule99.premises

subArg = set()
combinations = find_combinations(dictionary, target_values)
for combination in combinations:
    narg = Arguments.Arguments(rule99, combination)
    print(narg)
