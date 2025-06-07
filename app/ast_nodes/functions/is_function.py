from .node_registry import register_node
from app.ast_nodes import ASTNode, Closure

@register_node
class Isfunction(ASTNode):
    """
    Represents a function check in the AST.
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Evaluates if the given value is a function.
        """
        return Closure(
            params=["value"],
            body=IsfunctionEvaluator(),
            env=env,
        )
    
    def standerdize(self):
        return self
    
    def print(self, prefix=""):
        return f"{prefix}Isfunction)"
    

class IsfunctionEvaluator(ASTNode):
    """
    Evaluates if the given value is a function.
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Returns True if the value is a function, otherwise False.
        """
        value = env.get("value")
        return isinstance(value, Closure)
    
    def standerdize(self):
        return self
    
    def print(self, prefix=""):
        return f"{prefix}IsfunctionEvaluator)"