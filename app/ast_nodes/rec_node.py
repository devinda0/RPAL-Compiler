from .base import ASTNode
from .equal_node import EqualNode # If Db standardizes to EqualNode
from .gamma_node import GammaNode
from .lambda_node import LambdaNode
from .ystar_node import YStarNode # If using Y-combinator explicitly

class RecNode(ASTNode):
    def __init__(self, Db:ASTNode):
        """
        Represents a 'rec' (recursive) definition in the AST.
        :param Db: The definition body, usually an EqualNode (e.g., f = lambda ... f ...).
        """
        self.Db = Db

    def standerdize(self): 
        '''
                    rec             =
                     |             / \
                     =     =>     X   gamma
                    / \               /   \
                   X   E            Y* lambda
                                          /    \
                                         X      E
        
        Transforms: rec (X = E)  into  X = (Y* (lambda X . E))
        '''
        standardized_Db:EqualNode = self.Db.standerdize()

        if len(standardized_Db.left) != 1:
            raise ValueError("RecNode's Db must have exactly one left-hand side variable.")
        


        lambda_for_recursion = LambdaNode(Vb=standardized_Db.left, E=standardized_Db.right)

        y_star = YStarNode()
        gamma_application = GammaNode(left=y_star, right=lambda_for_recursion)

        standardized_rec_definition = EqualNode(left=standardized_Db.left, right=gamma_application)
        
        return standardized_rec_definition

    def evaluate(self, env):
        # After standardization, a RecNode should have been transformed.
        # Direct evaluation of a RecNode might not occur if standardization is always applied.
        # If it can be evaluated, it means the standardization to Y* form is evaluated.
        return self.standerdize().evaluate(env)

    def __repr__(self):
        return f"RecNode(Db={repr(self.Db)})"
    

    def print(self, prefix: str = ""):
        """
        Print the 'rec' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}RecNode:")
        self.Db.print(prefix + "*")