from .base import ASTNode
from .gamma_node import GammaNode
# Assuming identifier in AtNode is a RandNode or similar that has a 'value'
# from .rand_node import RandNode 

class AtNode(ASTNode):
    def __init__(self, Ap: ASTNode, identifier : ASTNode, R:ASTNode):
        """
        Represents an 'at' (@) expression in the AST.
        :param Ap: The expression on the left of @ identifier.
        :param identifier: The identifier node (e.g., a RandNode for an ID).
        :param R: The expression on the right of @ identifier.
        """
        self.Ap = Ap
        self.identifier = identifier # This should be the <ID:foo> node
        self.R = R
    
    def standerdize(self):
        standerdized_Ap = self.Ap.standerdize()
        standerdized_R = self.R.standerdize()
        # Identifier itself is usually a terminal, e.g. RandNode, already standardized.
        # If identifier can be complex, it might need .standerdize() too.
        # For now, assuming identifier is simple (like a RandNode for ID).

        return GammaNode(
            left=GammaNode(
                left = self.identifier, # The identifier node itself
                right = standerdized_Ap
            ),
            right=standerdized_R
        )

    def evaluate(self,env):
        return self.standerdize().evaluate(env)
    

    def print(self, prefix: str = ""):
        """
        Print the 'at' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}@")
        self.Ap.print(prefix + ".")
        self.identifier.print(prefix + ".")
        self.R.print(prefix + ".")