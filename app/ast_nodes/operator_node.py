from app.ast_nodes import TauNode
from app.ast_nodes.tau_node import TauClosure
from .base import ASTNode

class OperatorNode(ASTNode):
    def __init__(self, operator: str, left: ASTNode, right: ASTNode|None = None):
        """
        Represents an operator expression in the AST.
        :param operator: The operator to apply.
        :param left: The left operand.
        :param right: The right operand (optional for unary operators).
        """
        self.operator = operator
        self.left = left
        self.right = right

    def standerdize(self):
        self.left = self.left.standerdize()
        if self.right:
            self.right = self.right.standerdize()
        return self

    def evaluate(self, env):
        
        left_val = self.left.evaluate(env)
        right_val = self.right.evaluate(env) if self.right else None

        match self.operator:
            case "+":
                return left_val + right_val
            case "-":
                # Handle unary negation if right_val is None and operator is '-'
                if right_val is None: 
                    raise ValueError("Unary minus should be handled differently, e.g. a 'neg' operator or specific node")
                return left_val - right_val
            case "*":
                return left_val * right_val
            case "**":  # Assuming '**' is for exponentiation
                return left_val ** right_val
            case "/":
                return left_val // right_val
            case "%": # Added from original code
                return left_val % right_val
            case "gr" | ">": # Assuming 'gr' and '>' are equivalent
                return left_val > right_val
            case "ge" | ">=":
                return left_val >= right_val
            case "ls" | "<":
                return left_val < right_val
            case "le" | "<=":
                return left_val <= right_val
            case "eq" | "==": # Assuming 'eq' and '==' are equivalent
                return left_val == right_val
            case "ne" | "!=":
                return left_val != right_val
            case "&":
                return left_val and right_val
            case "or":
                return left_val or right_val
            case "not":
                return not left_val  # Assuming 'not' is a unary 
            case "neg":  # Assuming 'neg' is a unary negation operator
                return -left_val if right_val is None else -right_val
            case "aug": 
                if left_val is None:
                    return TauNode([right_val]).evaluate(env)
                if not isinstance(left_val, TauClosure):
                    raise TypeError(f"Left operand for 'aug' must be a tuple, got {type(left_val).__name__}.")
                return TauNode([i for i in left_val.get()] + [right_val]).evaluate(env)
            case _:
                raise ValueError(f"Unknown operator: {self.operator}")
            


    def print(self, prefix: str = ""):
        """
        Print the operator node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix}{self.operator}")
        self.left.print(prefix + ".")
        if self.right:
            self.right.print(prefix + ".")