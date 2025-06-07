from app.ast_nodes import GammaNode, RandNode
from app.ast_nodes.node_registry import get_node_class
from .lexer import Lexer
from .parser import Parser
# from .semantic_analyzer import SemanticAnalyzer
# from .code_generator import Interpreter
from .token import Token
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="The file to parse and evaluate")
    parser.add_argument("--ast", action="store_true", help="Print the AST structure")
    parser.add_argument("--st", action="store_true", help="Print the standardized AST")
    args = parser.parse_args()
    
    with open("test.rpal", 'r') as file:
        code = file.read()

    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    if args.ast:
        print()
        ast.print()  # Print the AST structure for debugging
        print()

    if args.st:
        print()
        ast.standerdize().print()
        print()

    ast.evaluate({})


    