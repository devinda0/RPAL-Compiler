from .base import ASTNode

class EqualNode(ASTNode):
    def __init__(self, left: ASTNode , right: ASTNode): # Made left/right more flexible
        """
        Represents an equality (assignment) expression in the AST.
        :param left: The left operand(s) of the equality (variable or list of variables for tuple assignment).
        :param right: The right operand(s) of the equality (expression or list of expressions for tuple assignment).
        """

        self.left = left
        self.right = right

    def standerdize(self):
        standardized_right = self.right.standerdize() 
        standardized_left = self.left.standerdize()

        # Return a new EqualNode or modify in place
        node =  EqualNode(standardized_left, standardized_right)
        
        return node

    def evaluate(self, env):
        """
        Evaluate an assignment. This typically means updating the environment.
        The EqualNode itself might not "return" a value in the same way an expression does,
        but its side effect is to modify the environment.
        The overall 'let' or 'where' construct that uses this EqualNode will then use the modified env.
        """
        raise NotImplementedError("EqualNode evaluation is context-dependent (e.g., within let/where) and typically modifies environment rather than returning a value directly.")

    def print(self, prefix: str = ""):
        """
        Print the equality node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}=")
        if isinstance(self.left, list):
            print(f"{prefix}.,")
            for l in self.left:
                l.print(prefix + "..")
        else:
            self.left.print(prefix + ".")
        
        if isinstance(self.right, list):
            print(f"{prefix}.,")
            for r in self.right:
                r.print(prefix + "..")
        else:
            self.right.print(prefix + ".")

