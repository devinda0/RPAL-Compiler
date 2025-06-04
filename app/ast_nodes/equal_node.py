from .base import ASTNode

class EqualNode(ASTNode):
    def __init__(self, left: ASTNode | list[ASTNode], right: ASTNode | list[ASTNode]): # Made left/right more flexible
        """
        Represents an equality (assignment) expression in the AST.
        :param left: The left operand(s) of the equality (variable or list of variables for tuple assignment).
        :param right: The right operand(s) of the equality (expression or list of expressions for tuple assignment).
        """

        # Original check:
        # if isinstance(left, list) and len(left) == 0:
        #     raise ValueError("Left operand cannot be an empty list")
        # This check might be too restrictive if `left` can be a single ASTNode.
        # For `let x = E`, left would be a single RandNode.
        # For `let (x,y) = E`, left would be a list [RandNode_x, RandNode_y] (or a TauNode).

        self.left = left
        self.right = right

    def standerdize(self):
        # Assignment nodes are often already in a standard form or are terminals for standardization.
        # However, their right-hand side might need standardization.
        # And if left is a complex pattern, it might also need standardization.
        
        # Standardize the right-hand side expression
        standardized_right = self.right.standerdize() if isinstance(self.right, ASTNode) else [r.standerdize() for r in self.right]


        # Standardize the left-hand side (if it's not just simple identifiers)
        # If self.left is a list of identifiers (RandNodes), they are already standard.
        # If self.left can be a pattern, it would need its own standardization.
        standardized_left = self.left.standerdize() if isinstance(self.left, ASTNode) else [l.standerdize() for l in self.left]


        # Return a new EqualNode or modify in place
        self.left = standardized_left
        self.right = standardized_right
        return self

    def evaluate(self, env):
        """
        Evaluate an assignment. This typically means updating the environment.
        The EqualNode itself might not "return" a value in the same way an expression does,
        but its side effect is to modify the environment.
        The overall 'let' or 'where' construct that uses this EqualNode will then use the modified env.
        """
        # This evaluation is complex and depends on the structure of 'left' and 'right'.
        # Case 1: Simple assignment: x = E
        #   var_name = self.left.value (if self.left is RandNode for ID)
        #   value = self.right.evaluate(env)
        #   env[var_name] = value
        # Case 2: Tuple assignment: (x, y) = (E1, E2) or (x,y) = E_tuple
        #   If self.left is a list of var names (RandNodes) and self.right evaluates to a list/tuple:
        #   evaluated_right = self.right.evaluate(env)
        #   if isinstance(self.left, list) and isinstance(evaluated_right, list) and len(self.left) == len(evaluated_right):
        #       for i, var_node in enumerate(self.left):
        #           env[var_node.value] = evaluated_right[i]
        #   else:
        #       raise TypeError("Pattern matching failed for assignment")
        
        # For the purpose of a 'let' or 'where' construct, the EqualNode's evaluation
        # might be more about preparing bindings rather than direct execution.
        # The 'let' or 'where' node would handle the environment extension.
        
        # If this node is directly evaluated as part of a sequence of operations,
        # it would modify the passed 'env'.
        # The original code raised NotImplementedError.
        raise NotImplementedError("EqualNode evaluation is context-dependent (e.g., within let/where) and typically modifies environment rather than returning a value directly.")
