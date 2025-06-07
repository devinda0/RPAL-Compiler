from .node_registry import register_node
from app.ast_nodes import ASTNode, Closure


@register_node()
class Stem(ASTNode):
    def __init__(self):
        """
        Represents the Stem function in the AST.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        return Closure(
            params=["x"],
            body=StemEvaluator(),
            env=env
        )

    def print(self, prefix: str = ""):
        """
        Print the Stem node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}Stem:")


class StemEvaluator(ASTNode):
    def __init__(self):
        """
        Represents the evaluation logic for the Stem function.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        x = env.get("x")
        
        if x is None:
            raise ValueError("StemEvaluator requires argument to be defined in the environment.")
        
        if not isinstance(x, str):
            raise TypeError(f"Expected argument to be a string, but got {type(x).__name__}.")
        
        if len(x) == 0:
            raise ValueError("StemEvaluator requires a non-empty string argument.")
        
        return x[0]  # Example logic: return the string without the first character

    def print(self, prefix: str = ""):
        print(f"{prefix}StemEvaluator:")