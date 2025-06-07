from .node_registry import register_node
from app.ast_nodes import ASTNode, Closure

@register_node()
class Stern(ASTNode):
    def __init__(self):
        """
        Represents the Stern function in the AST.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        # The Stern function is a recursive function that computes the Stern's diatomic series.
        return Closure(
            params=["x"],
            body=SternEvaluator(),
            env=env
        )

    def print(self, prefix: str = ""):
        """
        Print the Stern node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}Stern:")

class SternEvaluator(ASTNode):
    def __init__(self):
        """
        Represents the evaluation logic for the Stern function.
        """
        pass

    def standerdize(self):
        return self

    def evaluate(self, env):
        x = env.get("x")
        if x is None:
            raise ValueError("SternEvaluator requires argument to be defined in the environment.")
        
        if x is not type(str) == str:
            raise TypeError(f"Expected argument to be a string, but got {type(x).__name__}.")
        
        if len(x) == 0:
            raise ValueError("SternEvaluator requires a non-empty string argument.")
        
        return x[1:]  # Example logic: return the string without the first character

    def print(self, prefix: str = ""):
        print(f"{prefix}SternEvaluator:")

    