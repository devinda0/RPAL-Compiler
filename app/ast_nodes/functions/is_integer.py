from .node_registry import register_node
from app.ast_nodes import ASTNode, Closure

@register_node
class Isinteger(ASTNode):
    """
    Represents an integer check in the AST.
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Evaluates if the given value is an integer.
        """
        return Closure(
            params=["value"],
            body=IsintegerEvaluator(),
            env=env,
        )
    
    def standerdize(self):
        return self
    
    def print(self, prefix = ""):
        return f"{prefix}Isinteger)"
    

class IsintegerEvaluator(ASTNode):
    """
    Evaluates if the given value is an integer.
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Returns True if the value is an integer, otherwise False.
        """
        value = env.get("value")
        return isinstance(value, int)
    
    def standerdize(self):
        return self
    
    def print(self, prefix = ""):
        return f"{prefix}IsintegerEvaluator)"