from app.ast_nodes import TauNode
from app.ast_nodes.comma_node import CommaNode
from .base import ASTNode
from .equal_node import EqualNode

class AndNode(ASTNode):
    def __init__(self, Drs:list[ASTNode]):
        """
        Represents an 'and' expression for parallel definitions in the AST.
        :param Drs: A list of AST nodes representing the definitions (usually EqualNodes).
        """
        self.Drs = Drs

    def standerdize(self):
        standardized_Drs = [dr.standerdize() for dr in self.Drs]
        
        left = CommaNode([dr.left for dr in standardized_Drs])
        right = TauNode([dr.right for dr in standardized_Drs])

        return EqualNode(left, right)


    def evaluate(self, env):
        # This node is typically standardized away.
        raise NotImplementedError("Cannot evaluate 'and' node directly. Use standerdize() method.")
    
    def print(self, prefix: str = ""):
        """
        Print the 'and' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}and")
        for dr in self.Drs:
            dr.print(prefix + ". ")