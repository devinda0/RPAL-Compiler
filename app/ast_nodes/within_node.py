from .base import ASTNode
from .equal_node import EqualNode
from .gamma_node import GammaNode
from .lambda_node import LambdaNode

class WithinNode(ASTNode):
    def __init__(self, Da:ASTNode, D:ASTNode): # Parameters named as in original code
        """
        Represents a 'within' expression in the AST.
        :param Da: The first (outer) definition.
        :param D: The second (inner) definition that uses the outer one.
        """
        self.Da = Da
        self.D = D

    def standerdize(self):
        standardized_Da = self.Da.standerdize() # Should be an EqualNode: X1 = E1
        standardized_D = self.D.standerdize()   # Should be an EqualNode: X2 = E2

        return EqualNode(
            left=standardized_D.left, # X2
            right=GammaNode(
                left=LambdaNode(
                    Vb=[standardized_Da.left], # X1 (parameter)
                    E=standardized_D.right   # E2 (body, uses X1)
                ),
                right=standardized_Da.right  # E1 (argument)
            )
        )

    def evaluate(self, env):
        return self.standerdize().evaluate(env)
    

    def print(self, prefix: str = ""):
        """
        Print the 'within' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}within")
        self.Da.print(prefix + ". ")
        self.D.print(prefix + ". ")