fichier = open("exporting.txt", "a")

def exportArguments(argumentBase):
    for arg in argumentBase :
        fichier.write("arg("+arg.name+")\n")
    fichier.close()

