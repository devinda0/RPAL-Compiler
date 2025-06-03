from .base import ASTNode
from .equal_node import EqualNode
from .lambda_node import LambdaNode

class FcnFormNode(ASTNode):
    def __init__(self, identifier: ASTNode, Vbs:list[ASTNode], E: ASTNode):
        """
        Represents a function form (e.g., f x y = E) in the AST.
        :param identifier: The identifier (name) of the function (e.g., a RandNode for 'f').
        :param Vbs: A list of variable bindings (parameters) for the function.
        :param E: The expression body of the function.

                function_form                   =
                 /   |    \                    / \
                P    Vb+    E     =>           P   +lambda
                                                   /   \
                                                  Vb    .E  
        """
        self.identifier = identifier
        self.Vbs = Vbs
        self.E = E

    def standerdize(self): # Corrected method name
        # Standardize 'f Vb1 Vb2 ... = E' to 'f = lambda Vb1 . lambda Vb2 . ... E'
        # Or 'f = lambda (Vb1, Vb2, ...) . E' if Vbs are treated as a single tuple param list
        
        # Assuming Vbs is a list of parameter nodes (e.g., RandNodes for identifiers)
        # And E is the body.
        
        # Standardize body first
        standardized_E = self.E.standerdize()
        
        # Standardize parameters (they are likely simple identifiers, e.g., RandNodes)
        standardized_Vbs = [vb.standerdize() for vb in self.Vbs]

        # Create the nested lambda structure or a single lambda with multiple params
        # If LambdaNode takes a list of Vbs directly:
        lambda_expression = LambdaNode(Vb=standardized_Vbs, E=standardized_E)
        
        # Or, if currying:
        # current_expr = standardized_E
        # for vb in reversed(standardized_Vbs):
        #     current_expr = LambdaNode(Vb=[vb], E=current_expr)
        # lambda_expression = current_expr
            
        return EqualNode(left=self.identifier.standerdize(), right=lambda_expression)
        # pass # Original was pass

    def evaluate(self, env):
        # This node should be standardized away into an EqualNode assigning a LambdaNode.
        # So, direct evaluation of FcnFormNode might not be typical.
        return self.standerdize().evaluate(env)
        #pass