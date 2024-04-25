import os
import Rules
import Literals

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
            chaine = "[" + rule.name.name + "] "
            if rule.premises:
                for p in rule.premises:
                    if p.isNeg:
                        chaine += "!" + p.name + ","
                    else:
                        chaine += p.name + ","
            else:
                chaine += ' '
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
            chaine = "[" + rule.name.name + "] "
            if rule.premises:
                for p in rule.premises:
                    if p.isNeg:
                        chaine += "!" + p.name + ","
                    else:
                        chaine += p.name + ","
            else :
                chaine += ' '
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
        tmpPreLit1 = Literals.Literals("tmp2", False)
        tmpPreLit2 = Literals.Literals("tmp1", False)
        tmpCclLit = Literals.Literals("ccl1", False)
        for f in fichier:
            [text, premises, conclusion, fleche] = element(f)
            print(text, premises, fleche, conclusion)
            if fleche == "=>":
                if len(premises) > 1:
                    if '!' in premises[0]:
                        print(premises[0][0][1], "test")
                        tmpPreLit1 = Literals.Literals(premises[0][1:], True)
                    else:
                        print(premises[0][0])
                        tmpPreLit1 = Literals.Literals(premises[0], True)
                    if '!' in premises[1]:
                        print(premises[1][0])
                        tmpPreLit2 = Literals.Literals(premises[0][1:], True)
                    else:
                        print(premises[1][0])
                        tmpPreLit2 = Literals.Literals(premises[0], False)
                    if '!' in conclusion[0]:
                        print(conclusion[0][0])
                        tmpCclLit = Literals.Literals(conclusion[0], True)
                    else:
                        print(conclusion[0][0])
                        tmpCclLit = Literals.Literals(conclusion[0], False)
                    if len(conclusion) > 1:
                        parsedRules.add(Rules.Rules({tmpPreLit1, tmpPreLit2}, tmpCclLit, True, text[0], conclusion[1]))
                    if len(conclusion) == 1:
                        parsedRules.add(Rules.Rules({tmpPreLit1, tmpPreLit2}, tmpCclLit, True, text[0]))
                if len(premises) == 1 and premises[0] != '':
                    if '!' in premises[0]:
                        tmpPreLit1 = Literals.Literals(premises[0][1:], True)
                    else:
                        tmpPreLit1 = Literals.Literals(premises[0], False)
                    if '!' in conclusion[0]:
                        tmpCclLit = Literals.Literals(conclusion[0], True)
                    else:
                        tmpCclLit = Literals.Literals(conclusion[0], False)
                    if len(conclusion) > 1:
                        # print(tmpPreLit1)
                        parsedRules.add(Rules.Rules(tmpPreLit1, tmpCclLit, True, text[0], conclusion[1]))
                    if len(conclusion) == 1 and conclusion[0] != '':
                        parsedRules.add(Rules.Rules(tmpPreLit1, tmpCclLit, True, text[0]))
            if fleche == '->':
                if len(premises) > 1:
                    if '!' in premises[0]:
                        tmpPreLit1 = Literals.Literals(premises[0][1:], True)
                    else :
                        tmpPreLit1 = Literals.Literals(premises[0], False)
                    if '!' in premises[1]:
                        tmpPreLit1 = Literals.Literals(premises[1][1:], True)
                    else :
                        tmpPreLit1 = Literals.Literals(premises[1], False)
                    if '!' in conclusion[0]:
                        tmpCclLit = Literals.Literals(conclusion[0], True)
                    else:
                        tmpCclLit = Literals.Literals(conclusion[0], False)
                    if len(conclusion) > 1:
                        parsedRules.add(Rules.Rules({tmpPreLit1, tmpPreLit2}, tmpCclLit, False, text[0], conclusion[1]))
                    if len(conclusion) == 1:
                        parsedRules.add(Rules.Rules({tmpPreLit1, tmpPreLit2}, tmpCclLit, False, text[0]))
                if len(premises) == 1 and premises[0] != '':
                    if '!' in premises[0]:
                        tmpPreLit1 = Literals.Literals(premises[0][1:], True)
                    else:
                        tmpPreLit1 = Literals.Literals(premises[0], False)
                    if '!' in conclusion[0]:
                        tmpCclLit = Literals.Literals(conclusion[0], True)
                    else:
                        tmpCclLit = Literals.Literals(conclusion[0], False)
                    if len(conclusion) > 1:
                        parsedRules.add(Rules.Rules(tmpPreLit1, tmpCclLit, False, text[0], conclusion[1]))
                    if len(conclusion) == 1 and conclusion[0] != '':
                        print(tmpPreLit1)
                        parsedRules.add(Rules.Rules(tmpPreLit1, tmpCclLit, False, text[0]))
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


# [r1] ->a
# [r2] d,b->c
# [r3] !c->d
# [r10] !c,b->!d
# [r11] !c,d->!b
# [r12] !d->c
# [r4] a=>!d 0
# [r5] =>b 1
# [r6] =>!c 1
# [r7] =>d 0
# [r8] c=>e 0
# [r9] !c=>!r4 0