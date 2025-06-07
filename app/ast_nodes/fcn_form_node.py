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
        """
        self.identifier = identifier
        self.Vbs = Vbs
        self.E = E

    def standerdize(self):
        standardized_identifier = self.identifier.standerdize()
        
        lambda_expression = LambdaNode(Vb=self.Vbs, E=self.E).standerdize()
            
        return EqualNode(left=[standardized_identifier], right=lambda_expression)

    def evaluate(self, env):
        raise NotImplementedError("FcnFormNode evaluation is context-dependent and typically modifies environment rather than returning a value directly.")
    

    def print(self, prefix: str = ""):
        """
        Print the function form node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}fcn_form:")
        self.identifier.print(prefix + ". ")
        for vb in self.Vbs:
            vb.print(prefix + ". ")
        self.E.print(prefix + ". ")

