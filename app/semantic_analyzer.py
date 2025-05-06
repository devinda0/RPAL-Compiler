class SemanticAnalyzer:
    def __init__(self, ast_root):
        self.ast_root = ast_root
        self.symbol_table = {}

    def analyze(self):
        # Walk the tree and validate scope, types
        self._analyze_node(self.ast_root)

    def _analyze_node(self, node):
        # Example for variable use
        if isinstance(node, VariableNode):
            if node.name not in self.symbol_table:
                raise Exception(f"Undeclared variable '{node.name}'")
        # Recurse for children
        for child in node.children:
            self._analyze_node(child)
