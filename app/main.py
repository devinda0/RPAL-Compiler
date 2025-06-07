from .ast_nodes.functions.node_registry import get_node_class
from .lexer import Lexer
from .parser import Parser
import argparse


if __name__ == "__main__": # Corrected from _name

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="The file to parse and evaluate")
    parser.add_argument("-ast", action="store_true", help="Print the AST structure")
    parser.add_argument("-st", action="store_true", help="Print the standardized AST")
    args = parser.parse_args()
    
    # Use the file path provided as a command-line argument
    try:
        with open(args.file, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File not found at path: {args.file}")
        exit(1)
    except Exception as e:
        print(f"Error reading file {args.file}: {e}")
        exit(1)

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