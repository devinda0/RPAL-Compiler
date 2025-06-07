from .node_registry import register_node
from app.ast_nodes import ASTNode, Closure

@register_node()
class Istruthvalue(ASTNode):
    """
    Represents a truth value check in the AST.
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Evaluates if the given value is a truth value (True or False).
        """
        return Closure(
            params=["value"],
            body=IstruthvalueEvaluator(),
            env=env,
        )
    
    def standerdize(self):
        return self
    
    def print(self, prefix=""):
        return f"{prefix}Istruthvalue)"
    

class IstruthvalueEvaluator(ASTNode):
    """
    Evaluates if the given value is a truth value (True or False).
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Returns True if the value is a truth value, otherwise False.
        """
        value = env.get("value")
        return isinstance(value, bool)
    
    def standerdize(self):
        return self
    
    def print(self, prefix=""):
        return f"{prefix}IstruthvalueEvaluator)"