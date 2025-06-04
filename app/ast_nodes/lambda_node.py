from .base import ASTNode, Closure

class LambdaNode(ASTNode):
    def __init__(self, Vb:list[ASTNode], E: ASTNode):
        """
        Represents a lambda expression in the AST.
        :param Vb: The variable binding part of the lambda expression.
        :param E: The expression body of the lambda expression.
        """
        self.Vb = Vb
        self.E = E
    
    def standerdize(self):
        self.Vb = [vb.standerdize() for vb in self.Vb]
        self.E = self.E.standerdize()
        return self

    def evaluate(self, env):
        # Assuming Vb elements have a 'value' attribute after standardization if they are identifiers
        return Closure(
            params=[vb.value for vb in self.Vb], 
            body=self.E,
            env=env
        )
    
    def print(self, prefix: str = ""):
        """
        Print the lambda node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}LambdaNode:")
        for vb in self.Vb:
            vb.print(prefix + "*")
        self.E.print(prefix + "*")
