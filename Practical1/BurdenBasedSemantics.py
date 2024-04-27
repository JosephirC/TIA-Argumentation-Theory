from collections import defaultdict
burden = set()
dico_temp = {

}
# def bur(arg, i):
#     b = 0
#     if i == 0:
#         b = 1
#     if i > 0:
#         b = 1 + int(1/bur(arg, i-1))
#     return b 

# def addset(bf, rebuts, n):
#     cpt = 0
#     dejaVu = []
#     while n != 0:
#         # print(n)
#         for arg in bf:
#             if arg not in dejaVu:
#                 cpt = 0
#                 dejaVu.append(arg)
#             else: 
#                 cpt += 1
#             if cpt == 0:
#                 burden.add(bur(arg, 0))
#             else:
#                 for arg2 in bf:
#                     i = 0
#                     # print(arg.name, arg2.name)
#                     if (arg, arg2) in rebuts:
#                         i+=1
#                 burden.add(bur(arg, i))
#         n -= 1
#     return burden


# def rank_arguments(argument_base, rebuts):
#     ranks = defaultdict(int)
#     lowest_rank = 0

#     # Initialize ranks
#     for arg in argument_base:
#         ranks[arg] = lowest_rank

#     # Iterate until ranks stabilize
#     stabilized = False
#     while not stabilized:
#         stabilized = True
#         for arg in argument_base:
#             attacking_args = rebuts.get(arg.topRule.conclusion, set())
#             max_attacker_rank = max([ranks[attacker] for attacker, _ in attacking_args], default=-1)

#             if max_attacker_rank > ranks[arg]:
#                 stabilized = False
#                 ranks[arg] = max_attacker_rank + 1

#     # Sort arguments by rank
#     sorted_arguments = sorted(argument_base, key=lambda arg: ranks[arg])

#     return sorted_arguments, ranks

# Il me fait boucle infinie
# def bur(arg, i, rebuts):
#     if i == 0:
#         return 1.0
#     else:
#         attacking_args = rebuts.get(arg.topRule.conclusion, set())
#         attacking_args = [reb for reb in attacking_args if reb[1] != arg]  # Make sure the argument is not rebutting itself
#         print(f"Argument: {arg.name}, Attacking args: {[reb[1].name for reb in attacking_args]}")
#         return 1.0 + sum(1.0 / bur(reb[1], i - 1, rebuts) for reb in attacking_args)

# caluculate the burden value
def burden(argument_base, arg, i, defeats):
    if i == 0:
        return 1
    else:
        attacking_args = defeats.get(arg.topRule.conclusion, [])
        burned_values = []
        for reb in attacking_args:
            burned_value = burden(argument_base, reb[1], i - 1, defeats)
            burned_values.append(burned_value)
        burned_value = 1 + sum(1 / v for v in burned_values)

        return burned_value

def get_attack(arg, defeats):
    attack = set()
    for key in defeats:
        for (arg1, arg2) in defeats[key]:
            if arg2.name == arg.name:
                attack.add(arg1)

    return attack

def init(argument_base):
    for arg in argument_base:
        dico_temp[arg.name] = [1]

def burden2(argument_base, defeats, i):
    if i == 0:
        init(argument_base)
    else:
        for arg in argument_base:
            attack = get_attack(arg, defeats)
            somme = 0
            for a in attack:
                somme = somme + (1 / dico_temp[a.name][i-1])

            dico_temp[arg.name].append(somme + 1)

def custom_compare(entry):
    return entry[1:]

def calculate_bur_values1(argument_base, defeats, depth):
    dico_temp.clear()

    for i in range(depth): 
        burden2(argument_base, defeats, i)

    sorted_dico_temp = sorted(dico_temp.items(), key=custom_compare)

    for s in sorted_dico_temp:
        print(s)

    return sorted_dico_temp


# result not sorted
# def calculate_bur_values1(argument_base, defeats, depth):
#     bur_values = {}

#     for arg in argument_base:
#         bur_value = burden(argument_base, arg, depth, defeats)
#         bur_values[arg] = bur_value

#     return bur_values

# sort the result
def calculate_bur_values(argument_base, defeats, depth):
    bur_values = defaultdict(set)

    for arg in argument_base:
        bur_value = burden(argument_base, arg, depth, defeats)
        bur_values[arg].add(bur_value)

    # sort the args according to their burden value
    sorted_bur_values = defaultdict(set)
    for arg, bur_set in bur_values.items():
        for bur_value in bur_set:
            sorted_bur_values[bur_value].add(arg)

    sorted_keys = sorted(sorted_bur_values.keys())

    final_bur_values = defaultdict(set)
    for key in sorted_keys:
        final_bur_values[key] = sorted_bur_values[key]

    return final_bur_values
