from .node_registry import register_node
from app.ast_nodes import ASTNode, Closure

@register_node
class Isstring(ASTNode):
    def __init__(self):
        """
        Represents the 'is_string' function in the AST.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        return Closure(
            params=["x"],
            body=IsStringEvaluator(),
            env=env
        )

    def print(self, prefix: str = ""):
        """
        Print the is_string node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}IsString:")


class IsStringEvaluator(ASTNode):
    def __init__(self):
        """
        Represents the evaluation logic for the 'is_string' function.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        x = env.get("x")
        
        if x is None:
            raise ValueError("IsStringEvaluator requires argument to be defined in the environment.")
        
        return isinstance(x, str)

    def print(self, prefix: str = ""):
        """
        Print the is_string evaluator in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}IsStringEvaluator:")