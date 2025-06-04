from .base import ASTNode

class TauNode(ASTNode):
    def __init__(self, Tas:list[ASTNode]):
        """
        Represents a 'tau' expression (tuple) in the AST.
        :param Tas: A list of AST nodes representing the elements of the tuple.
        """
        self.T = Tas # Renamed Tas to T to match usage in evaluate
    
    def standerdize(self): # Corrected method name from standerdize() to standerdize(self)
        # Assuming elements need to be standardized
        self.T = [ta.standerdize() for ta in self.T]
        return self

    def evaluate(self, env):
        """
        Evaluate the tau node.
        For a TauNode, this typically means evaluating each of its child nodes.
        """
        return [ta.evaluate(env) for ta in self.T]
    
    def print(self, prefix: str = ""):
        """
        Print the 'tau' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}TauNode:")
        for ta in self.T:
            ta.print(prefix + "*")