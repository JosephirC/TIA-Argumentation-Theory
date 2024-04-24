# Literals are objects which are referred by a name (string) and a boolean which indicates if the literal is in its negative form or not. 
# An object of this class can represent an atom (e.g., $x$) or the negation of an atom (e.g., $\neg x$).

class Literals:
    def __init__(self, name, isNeg):
        self.name = name
        self.isNeg = isNeg

    def __eq__(self, other):
        return (self.name == other.name 
                and self.isNeg == other.isNeg)

    def __str__(self):

        literalName = str(self.name)

        if(not self.isNeg):
            literalName = literalName
        else:
            literalName = "¬" + literalName

        return literalName
    

    def __hash__(self):
        return hash((self.name, self.isNeg))
    
    # negate the class instance through the isNeg attribute
    def negate(self):
        return Literals(self.name, not self.isNeg)
    
    def copy(self):
        return Literals(self.name, self.isNeg)
    
    def contradicts(self, other):
        return (self.name == other.name and self.isNeg != other.isNeg)