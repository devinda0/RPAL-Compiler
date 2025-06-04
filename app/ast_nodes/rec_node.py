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
        if not isinstance(self.Db, EqualNode):
            # Or if self.Db is not standardized yet, standardize it first.
            # For this transformation, self.Db is expected to be X = E.
            # If self.Db could be something else that *becomes* X=E after its own standardization,
            self.Db = self.Db.standerdize() 
            # Assuming self.Db is already an EqualNode as per typical parsing of 'rec X = E'.
            #raise TypeError("RecNode expects Db to be an EqualNode (X = E)")

        # X is the identifier (function name) being defined
        # E is the body of the function
        # These come from the EqualNode child of RecNode
        X_node = self.Db.left  # This should be an identifier node (e.g., RandNode)
        E_node = self.Db.right # This is the expression for the function body

        # Standardize the body E, as it might contain other constructs
        standardized_E = E_node.standerdize()
        
        # X_node is an identifier, typically already standard. If it could be complex, standardize it too.
        # For 'rec f = ...', f is usually a simple identifier.
        standardized_X_node = X_node.standerdize()


        # Create lambda X . E
        # The Vb (bound variable) for the lambda is X_node itself.
        lambda_for_recursion = LambdaNode(Vb=[standardized_X_node], E=standardized_E)

        # Create Y* node
        y_star = YStarNode()

        # Create gamma node: Y* (lambda X . E)
        gamma_application = GammaNode(left=y_star, right=lambda_for_recursion)

        # Create the final EqualNode: X = gamma_application
        standardized_rec_definition = EqualNode(left=standardized_X_node, right=gamma_application)
        
        return standardized_rec_definition

    def evaluate(self, env):
        # After standardization, a RecNode should have been transformed.
        # Direct evaluation of a RecNode might not occur if standardization is always applied.
        # If it can be evaluated, it means the standardization to Y* form is evaluated.
        return self.standerdize().evaluate(env)

    def __repr__(self):
        return f"RecNode(Db={repr(self.Db)})"