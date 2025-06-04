from .base import ASTNode, Closure
from .lambda_node import LambdaNode # Needed for type checking and accessing LambdaNode structure

class YStarNode(ASTNode):
    """
    Represents the Y* combinator (or a similar fixed-point combinator).
    Y* = lambda h . (lambda x . h (x x)) (lambda x . h (x x))
    Its evaluation will typically involve creating a recursive closure.
    """

    class YStarApplicator:
        """
        Helper object returned by YStarNode.evaluate().
        GammaNode will call the 'apply' method of this object.
        """
        def apply(self, h_eta_closure: Closure):
            """
            Applies the Y* combinator logic.
            h_eta_closure is the closure for (lambda f_placeholder . E_recursive_body_lambda_node)
            Returns the final recursive closure.
            """
            if not isinstance(h_eta_closure, Closure):
                raise TypeError("Y* combinator's argument must be a Closure.")
            if len(h_eta_closure.params) != 1:
                raise TypeError(
                    f"The function provided to Y* must take exactly one argument (the placeholder for the recursive function itself), "
                    f"but it takes {len(h_eta_closure.params)}."
                )

            f_placeholder_name: str = h_eta_closure.params[0]
            # E_recursive_body_ast_node is the ASTNode that is the body of h_eta_closure.
            # This ASTNode should itself be a LambdaNode representing the actual recursive function.
            E_recursive_body_ast_node: ASTNode = h_eta_closure.body
            env_h_eta: dict = h_eta_closure.env # Environment where h_eta was defined

            if not isinstance(E_recursive_body_ast_node, LambdaNode):
                raise TypeError(
                    "The body of the function provided to Y* must be a LambdaNode "
                    "(representing the actual recursive function's structure)."
                )
            
            # This E_recursive_body_ast_node is the (lambda actual_params . actual_body)
            # We need to create a closure for this.
            # The environment for this new closure (let's call it 'g_final_recursive_closure')
            # must be env_h_eta, but extended with f_placeholder_name bound to g_final_recursive_closure itself.

            # Prepare the environment for g_final_recursive_closure
            g_env = env_h_eta.copy()

            # Extract parameter names for g_final_recursive_closure from the LambdaNode's Vb list.
            # Assuming Vb elements are ASTNodes (e.g., RandNode) that have a 'value' attribute for the name.
            g_param_names = [vb.value for vb in E_recursive_body_ast_node.Vb]

            # Create the final recursive closure 'g'.
            # Its body AST node is E_recursive_body_ast_node.E
            # Its captured environment is g_env (which doesn't contain 'g' yet).
            g_final_recursive_closure = Closure(
                params=g_param_names,
                body=E_recursive_body_ast_node.E, # The actual body AST of the recursive function
                env=g_env
            )

            # "Tie the knot": Add g_final_recursive_closure to its own captured environment
            # under the placeholder name used in h_eta.
            g_env[f_placeholder_name] = g_final_recursive_closure

            return g_final_recursive_closure

    def __init__(self):
        super().__init__()

    def standerdize(self):
        # Y* is already in a standard form.
        return self

    def evaluate(self, env):
        """
        Evaluation of YStarNode returns an applicator object.
        The GammaNode will use this applicator to perform the actual Y-combinator logic
        when Y* is applied to a function.
        The 'env' parameter (environment where Y* is encountered) is not directly used
        by the Y* combinator itself, as its behavior is universal.
        """
        return YStarNode.YStarApplicator()

    def __repr__(self):
        return "YStarNode()"