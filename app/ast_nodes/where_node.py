from .base import ASTNode
from .gamma_node import GammaNode
from .lambda_node import LambdaNode
# from .equal_node import EqualNode # If standerdized_Dr is known to be EqualNode

class WhereNode(ASTNode):
    def __init__(self, T: ASTNode, Dr: ASTNode):
        """
        Represents a 'where' expression in the AST.
        :param T: The main expression part. (Changed from 'condition' based on usage)
        :param Dr: The definition part. (Changed from 'body' based on usage)
        """
        self.T = T
        self.Dr = Dr
    
    def standerdize(self):
        standerdized_T = self.T.standerdize()
        standerdized_Dr = self.Dr.standerdize() 

        return GammaNode(
            left=LambdaNode(
                Vb=[standerdized_Dr.left], 
                E=standerdized_T
            ),
            right=standerdized_Dr.right
        )

    def evaluate(self, env):
        return self.standerdize().evaluate(env)
    

    def print(self, prefix: str = ""):
        """
        Print the 'where' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}where")
        self.T.print(prefix + ".")
        self.Dr.print(prefix + ".")