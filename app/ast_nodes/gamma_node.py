from .base import ASTNode, Closure
from .tau_node import TauClosure

class GammaNode(ASTNode):
    def __init__(self, left:ASTNode, right: ASTNode):
        """
        Represents a 'gamma' (function application) expression in the AST.
        :param left: The function (often a LambdaNode or identifier evaluating to a Closure).
        :param right: The argument(s) to the function.
        """
        self.left = left
        self.right = right
    
    def standerdize(self):
        self.left = self.left.standerdize()
        self.right = self.right.standerdize()
        return self # Added return self

    def evaluate(self, env):
        closure:Closure = self.left.evaluate(env)
        if not isinstance(closure, Closure):
            raise TypeError(f"Expected a Closure, but got {type(closure).__name__}.")
        arguments = self.right.evaluate(env)

        new_env = closure.env.copy()  # Start with the closure's captured environment

        if len(closure.params) == 0:
            if arguments is not None:
                raise ValueError("Closure with no parameters should not receive any arguments.")
            return closure.body.evaluate(new_env)  # Evaluate the body with the captured environment
        elif len(closure.params) == 1:
            if isinstance(arguments, list):
                if len(arguments) != 1:
                    raise ValueError(f"Expected a single argument for closure, but got {len(arguments)}.")
                arguments = arguments[0]
            new_env[closure.params[0]] = arguments
            return closure.body.evaluate(new_env)
        elif len(closure.params) > 1:
            if not isinstance(arguments, TauClosure):
                new_env[closure.params[0]] = arguments
                return Closure(closure.params[1:], closure.body, new_env)  # Return a new closure with the remaining parameters
            if len(arguments.get()) != len(closure.params):
                raise ValueError(f"Expected {len(closure.params)} arguments for closure, but got {len(arguments)}.")
            for i, param in enumerate(closure.params):
                new_env[param] = arguments.get()[i].evaluate(arguments.env)
            return closure.body.evaluate(new_env)
        else:
            raise ValueError(f"Unexpected number of parameters in closure: {len(closure.params)}.")
    

    def print(self, prefix: str = ""):
        """
        Print the 'gamma' node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}GammaNode:")
        self.left.print(prefix + "*")
        self.right.print(prefix + "*")
