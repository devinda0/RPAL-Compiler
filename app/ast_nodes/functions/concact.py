from .node_registry import register_node
from app.ast_nodes import ASTNode, Closure

@register_node()
class Conc(ASTNode):
    def __init__(self):
        """
        Represents the Conc function in the AST.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        return Closure(
            params=["x", "y"],
            body=ConcEvaluator(),
            env=env
        )

    def print(self, prefix: str = ""):
        """
        Print the Conc node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}Conc")


class ConcEvaluator(ASTNode):
    def __init__(self):
        """
        Represents the evaluation logic for the Conc function.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        x = env.get("x")
        y = env.get("y")

        if x is None or y is None:
            raise ValueError("ConcEvaluator requires both 'x' and 'y' to be defined in the environment.")

        if not isinstance(x, str) or not isinstance(y, str):
            raise TypeError(f"Expected both arguments to be strings, but got {type(x).__name__} and {type(y).__name__}.")

        return x + y  # Concatenate the two strings

    def print(self, prefix: str = ""):
        """
        Print the ConcEvaluator in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}ConcEvaluator:")