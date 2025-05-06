class Token:
    def __init__(self, token:str, type:str, line:int = None, column:int = None):
        self.token = token
        self.type = type
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.token}, {self.type}, {self.line}, {self.column})"
    
    def __str__(self):
        return f"Token({self.token}, {self.type}, {self.line}, {self.column})"