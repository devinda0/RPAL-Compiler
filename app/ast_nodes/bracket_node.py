from .base import ASTNode

class BracketNode(ASTNode):
    def __init__(self):
        super().__init__()

    def standerdize(self):
        """
        Standardize the bracket node.
        This method currently does nothing as the BracketNode is a placeholder.
        """
        return self
    
    def evaluate(self, env):
        """
        Evaluate the bracket node in the given environment.
        This method currently does nothing as the BracketNode is a placeholder.
        """
        return None
    
    def print(self, prefix: str = ""):
        """
        Print the bracket node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}()")