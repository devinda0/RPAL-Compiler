from .node_registry import register_node
from app.ast_nodes import ASTNode, Closure

@register_node
class Istuple(ASTNode):
    """
    Represents a tuple in the AST.
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Evaluates the tuple by evaluating each of its elements.
        """
        return Closure(
            params=["tuple"],
            body=IstupleEvaluator(),
            env=env,
        )
    
    def standerdize(self):
        return self
    
    def print(self, prefix = ""):
        return f"{prefix}Istuple)"
    
class IstupleEvaluator(ASTNode):
    """
    Evaluates if the given value is a tuple.
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Returns True if the value is a tuple, otherwise False.
        """
        value = env.get("tuple")
        return isinstance(value, tuple)
    
    def standerdize(self):
        return self
    
    def print(self, prefix = ""):
        return f"{prefix}IstupleEvaluator)"