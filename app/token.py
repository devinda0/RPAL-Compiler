class Token:
    def __init__(self, value:str, type:str, line:int = None, column:int = None):
        self.value = value
        self.type = type
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.value}, {self.type}, {self.line}, {self.column})"
    
    def __str__(self):
        return f"Token({self.value}, {self.type}, {self.line}, {self.column})"
    


    