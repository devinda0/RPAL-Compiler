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
        # For unary operators, right might be None. Adapt as needed.
        # Current implementation assumes binary for most.
        # Example: if self.operator == 'neg' and self.right is None: return -self.left.evaluate(env)
        
        left_val = self.left.evaluate(env)
        right_val = self.right.evaluate(env) if self.right else None

        match self.operator:
            case "+":
                return left_val + right_val
            case "-":
                # Handle unary negation if right_val is None and operator is '-'
                if right_val is None: # Assuming '-' can be unary
                     # This depends on how your parser creates OperatorNode for unary minus.
                     # If it's always OperatorNode('neg', operand, None), then this case is not for '-'
                     # If parser makes OperatorNode('-', operand1, operand2) for binary and
                     # potentially OperatorNode('-', operand, None) for unary, this needs adjustment.
                     # For now, assuming binary for arithmetic ops.
                    raise ValueError("Unary minus should be handled differently, e.g. a 'neg' operator or specific node")
                return left_val - right_val
            case "*":
                return left_val * right_val
            case "/":
                return left_val / right_val
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
            # Add other operators like 'or', 'and', 'not' if they use OperatorNode
            # Or if they have their own specific nodes (e.g. AndNode, OrNode, NotNode)
            case _:
                raise ValueError(f"Unknown operator: {self.operator}")