from .base import ASTNode
from .node_registry import get_node_class

class RandNode(ASTNode):
    def __init__(self, type: str, value: str|int|bool|None): # Adjusted type hint for value
        """
        Represents an opeRand node in the AST (literals, identifiers).
        :param type: The type of the node (e.g., "IDENTIFIER", "INTEGER", "STRING", "TRUE", "FALSE", "NIL", "DUMMY").
        :param value: The value of the node.
        """
        self.type = type # e.g. "IDENTIFIER", "INTEGER", "STRING", "TRUE", "KEYWORD_NIL" etc.
        self.value = value # The actual string "x", or integer 10, or string "hello"

    def standerdize(self):
        # Literals and identifiers are typically already in their standard form.
        return self

    def evaluate(self, env):
        """
        Evaluate the operand node.
        """
        if self.type == "IDENTIFIER":
            if self.value in env:
                return env[self.value]
            elif get_node_class(self.value) is not None:
                # If the identifier corresponds to a registered node, return its class
                return get_node_class(self.value)().evaluate(env)
            else:
                raise NameError(f"Name '{self.value}' is not defined in the current environment.")
        elif self.type == "INTEGER" or self.type == "STRING":
            return self.value
        elif self.type == "TRUE": 
            return True
        elif self.type == "FALSE": 
            return False
        elif self.type == "NIL":
            return None
        elif self.type == "DUMMY":
            return "DUMMY" 
        else:
            raise ValueError(f"Unknown RandNode type for evaluation: {self.type} with value {self.value}")
        

    
    def print(self, prefix: str = ""):
        """
        Print the RandNode in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}{self.value}")