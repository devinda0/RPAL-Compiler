from app.ast_nodes.tau_node import TauClosure
from .node_registry import register_node
from app.ast_nodes import ASTNode, Closure

@register_node
class Order(ASTNode):
    """
    Represents an order operation in the AST.
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Evaluates the order operation by returning a closure.
        """
        return Closure(
            params=["value"],
            body=OrderEvaluator(),
            env=env,
        )
    
    def standerdize(self):
        return self
    
    def print(self, prefix=""):
        return f"{prefix}Order)"
    

class OrderEvaluator(ASTNode):
    """
    Evaluates the order operation.
    """

    def __init__(self):
        pass

    def evaluate(self, env):
        """
        Returns the order of the value.
        """
        value = env.get("value")
        
        if not isinstance(value, TauClosure):
            raise TypeError("Order can only be applied to a tuples.")
        
        return len(value.get())
    
    def standerdize(self):
        return self
    
    def print(self, prefix=""):
        return f"{prefix}OrderEvaluator)"