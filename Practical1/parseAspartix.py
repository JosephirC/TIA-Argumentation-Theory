import os
import Rules

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
    # rules = generateContrapositonRules(rules)
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

def readKB(parsedRules):
    if os.path.exists('KB.txt'):
        fichier = open('KB.txt', 'r')
        for f in fichier:
            [text, premises, conclusion, fleche] = element(f)
            # print(text, premises, fleche, conclusion)
            if fleche == "=>":
                if len(premises) > 1:
                    if len(conclusion) > 1:
                        parsedRules.add(Rules.Rules({premises[0], premises[1]}, conclusion[0], True, text[0], conclusion[1]))
                    if len(conclusion) == 1:
                        parsedRules.add(Rules.Rules({premises[0], premises[1]}, conclusion[0], True, text[0]))
                if len(premises) == 1:
                    if len(conclusion) > 1:
                        parsedRules.add(Rules.Rules(premises[0], conclusion[0], True, text[0], conclusion[1]))
                    if len(conclusion) == 1:
                        parsedRules.add(Rules.Rules(premises[0], conclusion[0], True, text[0]))
            if fleche == '->':
                if len(premises) > 1:
                    if len(conclusion) > 1:
                        parsedRules.add(Rules.Rules({premises[0], premises[1]}, conclusion[0], False, text[0], conclusion[1]))
                    if len(conclusion) == 1:
                        parsedRules.add(Rules.Rules({premises[0], premises[1]}, conclusion[0], False, text[0]))
                if len(premises) == 1:
                    if len(conclusion) > 1:
                        parsedRules.add(Rules.Rules(premises[0], conclusion[0], False, text[0], conclusion[1]))
                    if len(conclusion) == 1:
                        parsedRules.add(Rules.Rules(premises[0], conclusion[0], False, text[0]))
        return parsedRules
    else :
        print("pas de fichier KB.txt")

def element(f):
    regle = f.strip()
    text = []
    sous = []
    premises = []
    conclusion = []
    fleche = ''
    elements = regle.split(' ', 1)
    if len(elements) > 1:
        text.append(elements[0])
        if '=>' in elements[1]:
            sous = elements[1].split('=>',1)
            fleche = '=>'
        else:
            sous = elements[1].split('->',1)
            fleche = '->'
        if len(sous) > 1:
            premises = [sous[0].split(',')]
            conclusion = sous[1].split(' ')
        
    return text, premises, conclusion, fleche