from app.ast_nodes.bracket_node import BracketNode
from app.ast_nodes.comma_node import CommaNode
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
        if self.Vb is None or len(self.Vb) == 0:
            raise ValueError("LambdaNode must have at least one variable binding (Vb).")
        
        node = self.E.standerdize()

        for i in range(len(self.Vb)-1, -1, -1):
            Vb = self.Vb[i].standerdize()

            node = LambdaNode(Vb=[Vb], E=node)

        return node

    def evaluate(self, env):
        # Assuming Vb elements have a 'value' attribute after standardization if they are identifiers
        if len(self.Vb) > 1 :
            return self.standerdize().evaluate()

        if isinstance(self.Vb[0], CommaNode):
            return Closure(
                params=[child.value for child in self.Vb[0].children], 
                body=self.E,
                env=env
            )
        
        if isinstance(self.Vb[0], BracketNode):
            return Closure(
                params=[self.Vb[0]], 
                body=self.E,
                env=env
            )

        return Closure(
            params=[self.Vb[0].value], 
            body=self.E,
            env=env
        )
    
    def print(self, prefix: str = ""):
        """
        Print the lambda node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}lambda")
        for vb in self.Vb:
            vb.print(prefix + ".")
        self.E.print(prefix + ".")
