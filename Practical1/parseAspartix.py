fichier = open('aspartix.txt', 'a')

def parseAttacks(defeats) :
    for rule in defeats:
        for (arg1, arg2) in defeats[rule]:
            fichier.write("att(" + arg1.name + "," + arg2.name + ")" + "\n")
    fichier.close()