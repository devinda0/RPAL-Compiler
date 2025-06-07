from app.ast_nodes import Closure
from ..base import ASTNode
from .node_registry import register_node

@register_node
class Print(ASTNode):
    def __init__(self):
        """
        Represents a print statement in the AST.
        :param expression: The expression to print.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        return Closure(
            params=["expression"],
            body=PrintExpression(),
            env=env
        )

    def print(self, prefix: str = ""):
        """
        Print the print node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}Print:")


class PrintExpression(ASTNode):
    def __init__(self,):
        """
        Represents an expression to be printed in the AST.
        :param expression: The expression to print.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        
        print(env.get("expression"))

    def print(self, prefix: str = ""):
        """
        Print the print expression in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}PrintExpression:")