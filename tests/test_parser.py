import unittest
from app.parser import Parser
from token import Token  # Assuming your tokens are like Token(type, value)

class TestParser(unittest.TestCase):

    def test_simple_integer_expression(self):
        tokens = [Token("INTEGER", "5")]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(ast.type, "INTEGER")
        self.assertEqual(ast.value, "5")

    def test_addition_expression(self):
        tokens = [
            Token("INTEGER", "2"),
            Token("OPERATOR", "+"),
            Token("INTEGER", "3")
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(ast.type, "ADD")
        self.assertEqual(ast.left.value, "2")
        self.assertEqual(ast.right.value, "3")

    def test_nested_expression(self):
        tokens = [
            Token("INTEGER", "2"),
            Token("OPERATOR", "+"),
            Token("INTEGER", "3"),
            Token("OPERATOR", "*"),
            Token("INTEGER", "4")
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(ast.type, "ADD")
        self.assertEqual(ast.left.value, "2")
        self.assertEqual(ast.right.type, "MUL")
        self.assertEqual(ast.right.left.value, "3")
        self.assertEqual(ast.right.right.value, "4")

if __name__ == "__main__":
    unittest.main()
