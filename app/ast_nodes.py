class ASTNode:
    pass

class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
