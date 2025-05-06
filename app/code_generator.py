class Interpreter:
    def __init__(self, ast_root):
        self.ast_root = ast_root

    def evaluate(self):
        return self._eval(self.ast_root)

    def _eval(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, BinaryOpNode):
            left = self._eval(node.left)
            right = self._eval(node.right)
            if node.op == '+':
                return left + right
            elif node.op == '*':
                return left * right
        elif isinstance(node, VariableNode):
            return node.value  # assuming already set
