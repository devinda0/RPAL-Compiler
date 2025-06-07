from app.ast_nodes import Closure
from .base import ASTNode

class TauNode(ASTNode):
    def __init__(self, Tas:list[ASTNode]):
        """
        Represents a 'tau' expression (tuple) in the AST.
        :param Tas: A list of AST nodes representing the elements of the tuple.
        """
        self.T = Tas # Renamed Tas to T to match usage in evaluate
    
    def standerdize(self): # Corrected method name from standerdize() to standerdize(self)
        # Assuming elements need to be standardized
        self.T = [ta.standerdize() for ta in self.T]
        return self

    def evaluate(self, env):
        """
        Evaluate the tau node.
        For a TauNode, this typically means evaluating each of its child nodes.
        """

        return TauClosure(env, self.T)
    
    def print(self, prefix: str = ""):
        """
        Print the 'tau' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}tau")
        for ta in self.T:
            ta.print(prefix + ". ")

    def __str__(self):
        return f"({', '.join(ta for ta in self.T)})"
    

class TauClosure(Closure):
    def __init__(self, env, T:list[ASTNode]):
        """
        Represents a closure for a tuple type.
        :param env: The environment in which the closure is defined.
        :param tau_node: The TauNode representing the tuple.
        """
        super().__init__(
            params=["index"],  # The closure expects an index to access tuple elements
            body=TauNodeGetter(T),  # The body is a TauNodeGetter that will handle tuple access
            env=env  # The environment in which the closure was created
        )
        self.T = T  # Store the tuple elements
    
    def get(self):
        return [elem.evaluate(self.env) for elem in self.T]
    
    def __str__(self):
        return f"({', '.join(str(ta.evaluate(self.env)) for ta in self.T)})"
    
class TauNodeGetter(ASTNode):
    def __init__(self, Tas:list[ASTNode]):
        """
        Represents a 'tau' type (tuple type) in the AST.
        :param Tas: A list of AST nodes representing the types of the elements in the tuple.
        """
        self.T = Tas # Renamed Tas to T to match usage in evaluate
    
    def standerdize(self): # Corrected method name from standerdize() to standerdize(self)
        # Assuming elements need to be standardized
        self.T = [ta.standerdize() for ta in self.T]
        return self
    
    def evaluate(self, env):
        """
        Evaluate the tau type node.
        For a TauNodeGetter, this typically means evaluating each of its child nodes.
        """
        index = env['index']
        if index is None:
            return tuple([ta.evaluate(env) for ta in self.T])
        elif 0 < index <= len(self.T):
            return self.T[index - 1].evaluate(env)
        else:
            raise IndexError(f"Index {index} out of bounds for tuple of length {len(self.T)}")
        
    def print(self, prefix: str = ""):
        """
        Print the 'tau' type node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}TauNodeType:")
        for ta in self.T:
            ta.print(prefix + ". ")