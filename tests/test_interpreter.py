import unittest

from app import Lexer, Parser
from app.ast_nodes import ASTNode

def run_interpreter(source_code):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast:ASTNode = parser.parse()
    ast.evaluate({})
    return ast

class TestInterpreter(unittest.TestCase):
    def test_simple_expression(self):
        source_code = "let x = (1,2,3) in Print (x 1)"
        ast = run_interpreter(source_code)