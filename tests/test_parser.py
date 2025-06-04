import unittest
from app.parser import Parser
from app.token import Token  # Assuming your tokens are like Token(type, value)
from app.ast_nodes import (
    ASTNode,  # Assuming you have a base ASTNode class in ast_nodes.py
    LetNode,
    LambdaNode,
    WhereNode,
    TauNode,
    AugNode,
    ArrowNode,
    OperatorNode,
    AtNode,
    GammaNode,
    RandNode,
    WithinNode,
    AndNode,
    RecNode,
    FcnFormNode,
    EqualNode,
)

class TestParser(unittest.TestCase):

    def test_simple_integer_expression(self):
        tokens = [Token(5, "INTEGER")]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertIsInstance(ast, RandNode, "Expected ASTNode type for simple integer expression")
        self.assertEqual(ast.value, 5, "Expected value to be '5'")
        self.assertEqual(ast.type, "INTEGER", "Expected type to be 'INTEGER'")
    
    def test_binary_operation(self):
        tokens = [
            Token(3, "INTEGER"),
            Token("+", "OPERATOR"),
            Token(4, "INTEGER")
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertIsInstance(ast, OperatorNode, "Expected ASTNode type for binary operation")
        self.assertEqual(ast.left.value, 3, "Expected left operand to be '3'")
        self.assertEqual(ast.right.value, 4, "Expected right operand to be '4'")
        self.assertEqual(ast.operator, "+", "Expected operator to be '+'")

    def test_let_expression(self):
        tokens = [
            Token("let", "KEYWORD"),
            Token("x", "IDENTIFIER"),
            Token("=", "OPERATOR"),
            Token(10, "INTEGER"),
            Token("in", "KEYWORD"),
            Token("x", "IDENTIFIER")
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertIsInstance(ast, LetNode, "Expected ASTNode type for let expression")
        self.assertIsInstance(ast.E, RandNode, "Expected expression in let to be a RandNode")
        self.assertIsInstance(ast.D, EqualNode, "Expected D in let to be an OperatorNode")
        self.assertEqual(len(ast.D.left),1, "Expected D.left to be a single identifier")
        self.assertEqual(ast.D.left[0].value, "x", "Expected identifier in let expression to be 'x'")
        self.assertEqual(ast.D.right.value, 10, "Expected value in let expression to be '10'")
        self.assertEqual(ast.E.value, "x", "Expected expression in let to be 'x'")

if __name__ == "__main__":
    unittest.main()
