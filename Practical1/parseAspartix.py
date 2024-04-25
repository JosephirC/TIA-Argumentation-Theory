import os
from GenerateArguments import generateContrapositonRules

"""
parse and write in the file aspartix.txt
"""
def parseAttacks(defeats):
    if os.path.exists('aspartix.txt'):
        #open and erase the file content
        fichier = open('aspartix.txt', 'w')
        pass
    fichier = open('aspartix.txt', 'a')
    for rule in defeats:
        for (arg1, arg2) in defeats[rule]:
            fichier.write("att(" + arg1.name + "," + arg2.name + ")" + "\n")
    fichier.close()

def parseRules(rules):
    if os.path.exists('KB.txt'):
        fichier = open('KB.txt', 'w')
        pass
    fichier = open('KB.txt', 'a')
    rules = generateContrapositonRules(rules)
    for rule in rules:
        print(rule)
    for rule in rules:
        if rule.isDefeasible:
            chaine = rule.name.name + " "
            for p in rule.premises:
                if p.isNeg:
                    chaine += "!" + p.name + ","
                else:
                    chaine += p.name + ","
            chaine = chaine[:-1]
            chaine += "=>"
            if rule.conclusion.isNeg:
                chaine += "!" + rule.conclusion.name
            else:
                chaine += rule.conclusion.name
            if rule.weight is not None:
                chaine += " " + str(rule.weight)
            fichier.write(chaine + "\n")             
        else:
            chaine = rule.name.name + " "
            for p in rule.premises:
                if p.isNeg:
                    chaine += "!" + p.name + ","
                else:
                    chaine += p.name + ","
            chaine = chaine[:-1]
            chaine += "->"
            if rule.conclusion.isNeg:
                chaine += "!" + rule.conclusion.name
            else:
                chaine += rule.conclusion.name
            fichier.write(chaine + "\n")             
    fichier.close()