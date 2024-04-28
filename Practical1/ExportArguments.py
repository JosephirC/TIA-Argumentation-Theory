fichier = open("exporting.txt", "a")

def exportArguments(argumentBase):
    """
    Exports the arguments to a file.
    """
    for arg in argumentBase :
        fichier.write("arg("+arg.name+")\n")
    fichier.close()

