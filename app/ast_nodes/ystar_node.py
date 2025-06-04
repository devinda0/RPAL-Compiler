from .base import ASTNode, Closure
from .gamma_node import GammaNode
from .rand_node import RandNode  
from .lambda_node import LambdaNode

class YStarNode(ASTNode):
    """
    Represents the Y* combinator (or a similar fixed-point combinator).
    Y* = lambda h . (lambda x . h (x x)) (lambda x . h (x x))
    Its evaluation will typically involve creating a recursive closure.
    """
    
    def __init__(self):
        super().__init__()

    def standerdize(self):
        """
        Standardize the Y* combinator.
        This will create a LambdaNode that represents the Y* combinator.
        """
        return self
    
    def evaluate(self, env):
        """
        Evaluate the Y* combinator.
        This will create a closure that can be used for recursive function calls.
        """
        # Create a closure for the Y* combinator

        # closure = Closure(
        #     params=["h"],
        #     body=GammaNode(
        #         left=LambdaNode(
        #             Vb=[RandNode("IDENTIFIER","x")],
        #             E=GammaNode(
        #                 left=RandNode("IDENTIFIER","h"),
        #                 right=LambdaNode(
        #                     Vb=[RandNode("IDENTIFIER","v")],
        #                     E=GammaNode(
        #                         left=RandNode("IDENTIFIER","x"),
        #                         right=RandNode("IDENTIFIER","x")
        #                     )
        #                 )
        #             )
        #         ),
        #         right=LambdaNode(
        #             Vb=[RandNode("IDENTIFIER","x")],
        #             E=GammaNode(
        #                 left=RandNode("IDENTIFIER","h"),
        #                 right=LambdaNode(
        #                     Vb=[RandNode("IDENTIFIER","v")],
        #                     E=GammaNode(
        #                         left=RandNode("IDENTIFIER","x"),
        #                         right=RandNode("IDENTIFIER","x")
        #                     )
        #                 )
        #             )
        #         )
        #     ),
        #     env=env
        # )

        inner_lambda = LambdaNode(
            Vb=[RandNode("IDENTIFIER", "x")],
            E=GammaNode(
                left=RandNode("IDENTIFIER", "f"),
                right=LambdaNode(
                    Vb=[RandNode("IDENTIFIER", "v")],
                    E=GammaNode(
                        left=GammaNode(
                            left=RandNode("IDENTIFIER", "x"),
                            right=RandNode("IDENTIFIER", "x")
                        ),
                        right=RandNode("IDENTIFIER", "v")
                    )
                )
            )
        )
        
        closure = Closure(
            params=["t"],
            body=GammaNode(
                left=RandNode("IDENTIFIER", "t"),
                right=RandNode("IDENTIFIER", "t")
            ),
            env=env
        )

        outer_lambda = LambdaNode(
            Vb=[RandNode("IDENTIFIER", "f")],
            E=GammaNode(
                left=inner_lambda,
                right=inner_lambda  # For actual Y, you apply it to itself
            )
        )

        z_combinator = LambdaNode(
            Vb=[RandNode("IDENTIFIER", "f")],
            E=GammaNode(
                left=inner_lambda,
                right=inner_lambda
            )
        )

        return z_combinator.evaluate(env)
    
    def print(self, prefix: str = ""):
        """
        Print the Y* node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}Y*")