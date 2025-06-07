from .base import ASTNode

class ArrowNode(ASTNode):
    def __init__(self, B: ASTNode, true_branch: ASTNode, false_branch: ASTNode): # Renamed true/false for clarity
        """
        Represents an 'arrow' (conditional) expression in the AST.
        :param B: The condition part of the arrow expression.
        :param true_branch: The expression to evaluate if B is true.
        :param false_branch: The expression to evaluate if B is false.
        """
        self.B = B
        self.true_branch = true_branch
        self.false_branch = false_branch
    
    def standerdize(self):
        self.B = self.B.standerdize()
        self.true_branch = self.true_branch.standerdize()
        self.false_branch = self.false_branch.standerdize()
        return self # Added return self

    def evaluate(self, env):
        if self.B.evaluate(env): # Pass env to condition evaluation
            return self.true_branch.evaluate(env)
        else:
            return self.false_branch.evaluate(env)
        
    def print(self, prefix: str = ""):
        """
        Print the 'arrow' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}->")
        self.B.print(prefix + ". ")
        self.true_branch.print(prefix + ". ")
        self.false_branch.print(prefix + ". ")