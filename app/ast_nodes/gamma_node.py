from .base import ASTNode, Closure
from .ystar_node import YStarNode # Import YStarNode to access YStarNode.YStarApplicator

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
        evaluated_left = self.left.evaluate(env)
        
        if isinstance(evaluated_left, YStarNode.YStarApplicator):
            # Handle Y* application
            h_eta_closure_arg = self.right.evaluate(env) # Evaluate the function (lambda f. E)
            # The YStarApplicator.apply method expects h_eta_closure_arg to be a Closure
            return evaluated_left.apply(h_eta_closure_arg)
            
        elif isinstance(evaluated_left, Closure):
            # Standard closure application
            closure_to_call: Closure = evaluated_left
            arguments = self.right.evaluate(env) # Arguments could be a single value or a list (if TauNode)

            new_env = closure_to_call.env.copy()  # Start with the closure's captured environment

            # --- Existing logic for binding arguments to parameters ---
            if len(closure_to_call.params) == 1:
                if isinstance(arguments, list) and len(arguments) == 1 and len(closure_to_call.params) == 1 :
                     new_env[closure_to_call.params[0]] = arguments[0]
                elif not isinstance(arguments, list) and len(closure_to_call.params) == 1:
                     new_env[closure_to_call.params[0]] = arguments
                elif isinstance(arguments, list) and len(closure_to_call.params) == 1 and len(arguments) != 1:
                     raise ValueError(f"Function expected 1 argument, got a list of {len(arguments)}")
                else: 
                     new_env[closure_to_call.params[0]] = arguments 
            elif len(closure_to_call.params) == 0:
                if arguments is not None and not (isinstance(arguments, list) and len(arguments) == 0):
                     pass 
            elif not isinstance(arguments, list) or len(closure_to_call.params) != len(arguments):
                raise ValueError(
                    f"Function '{closure_to_call.params}' expected {len(closure_to_call.params)} arguments, "
                    f"got {len(arguments) if isinstance(arguments, list) else '1 (non-list)'}. Arguments: {arguments}"
                )
            else: # Multiple parameters, arguments is a list
                for i in range(len(closure_to_call.params)):
                    new_env[closure_to_call.params[i]] = arguments[i]
            # --- End of existing argument binding logic ---
            
            return closure_to_call.body.evaluate(new_env)
        else:
            raise TypeError(f"Cannot apply non-function: {type(evaluated_left)}. Left expression was: {self.left}")