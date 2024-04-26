burden = set()

def bur(arg, i):
    b = 0
    if i == 0:
        b = 1
    if i > 0:
        b = 1 + int(1/bur(arg, i-1))
    return b 

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

from collections import defaultdict

def rank_arguments(argument_base, rebuts):
    ranks = defaultdict(int)
    lowest_rank = 0

    # Initialize ranks
    for arg in argument_base:
        ranks[arg] = lowest_rank

    # Iterate until ranks stabilize
    stabilized = False
    while not stabilized:
        stabilized = True
        for arg in argument_base:
            attacking_args = rebuts.get(arg.topRule.conclusion, set())
            max_attacker_rank = max([ranks[attacker] for attacker, _ in attacking_args], default=-1)

            if max_attacker_rank > ranks[arg]:
                stabilized = False
                ranks[arg] = max_attacker_rank + 1

    # Sort arguments by rank
    sorted_arguments = sorted(argument_base, key=lambda arg: ranks[arg])

    return ranks