from .base import ASTNode
from .equal_node import EqualNode # For type hint and usage
from .gamma_node import GammaNode
from .lambda_node import LambdaNode

class LetNode(ASTNode):
    def __init__(self, D: ASTNode, E: ASTNode):
        """
        Represents a 'let' expression in the AST.
        :param D: The declaration part of the let expression.
        :param E: The expression part of the let expression.
        """
        self.D = D
        self.E = E
    
    def standerdize(self):
        standardized_D: EqualNode = self.D.standerdize()
        standardized_E: ASTNode = self.E.standerdize()

        standardized_LetNode = GammaNode(
            left=LambdaNode(
                Vb = standardized_D.left, # Assuming standardized_D.left is compatible with LambdaNode Vb
                E = standardized_E
            ),
            right=standardized_D.right
        )
        return standardized_LetNode

    def evaluate(self, env):
        return self.standerdize().evaluate(env)
    

    def print(self, prefix = ""):
        """
        Print the 'let' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}LetNode:")
        self.D.print(prefix + "*")
        self.E.print(prefix + "*")