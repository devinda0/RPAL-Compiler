import unittest
from app.semantic_analyzer import SemanticAnalyzer
from app.ast_nodes import VarNode, AssignNode, IntNode, AddNode  # Just guessing structure

class TestSemanticAnalyzer(unittest.TestCase):

    def test_valid_assignment(self):
        analyzer = SemanticAnalyzer()

        # x = 5;
        ast = AssignNode("x", IntNode(5))

        try:
            analyzer.analyze(ast)
        except Exception:
            self.fail("analyze() raised Exception unexpectedly!")

    def test_undeclared_variable(self):
        analyzer = SemanticAnalyzer()

        # y = x + 5;  (but x is undeclared)
        ast = AssignNode("y", AddNode(VarNode("x"), IntNode(5)))

        with self.assertRaises(Exception) as context:
            analyzer.analyze(ast)

        self.assertIn("undeclared variable", str(context.exception).lower())

    def test_type_mismatch(self):
        analyzer = SemanticAnalyzer()

        # x = 5;
        # y = x + "hello";  (mixing int and string)
        x_assign = AssignNode("x", IntNode(5))
        y_assign = AssignNode("y", AddNode(VarNode("x"), VarNode("str_hello")))

        # Let's pretend analyzer uses some scope tracking
        analyzer.analyze(x_assign)
        analyzer.symbol_table["str_hello"] = "string"  # manually faking the symbol

        with self.assertRaises(Exception) as context:
            analyzer.analyze(y_assign)

        self.assertIn("type mismatch", str(context.exception).lower())

if __name__ == "__main__":
    unittest.main()
