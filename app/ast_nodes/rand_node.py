from .base import ASTNode

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
            else:
                raise NameError(f"Name '{self.value}' is not defined in the current environment.")
        elif self.type == "INTEGER" or self.type == "STRING":
            return self.value
        elif self.type == "TRUE": # Assuming parser creates type "TRUE" for 'true' keyword
            return True
        elif self.type == "FALSE": # Assuming parser creates type "FALSE" for 'false' keyword
            return False
        elif self.type == "NIL": # Changed from NILL to NIL
            return None
        elif self.type == "DUMMY": # Assuming parser creates type "DUMMY"
            return "DUMMY" # Or a special Dummy object if needed
        else:
            # This case should ideally not be reached if the parser correctly assigns types.
            # Or, if 'value' itself is the token value for keywords like 'true', 'false', 'nil'.
            # The original code had self.type == "TRUE", etc.
            raise ValueError(f"Unknown RandNode type for evaluation: {self.type} with value {self.value}")