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