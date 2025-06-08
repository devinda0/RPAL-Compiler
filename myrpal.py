import argparse
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.lexer import Lexer
from app.parser import Parser

def main():
    parser = argparse.ArgumentParser(description="RPAL Compiler/Interpreter")
    parser.add_argument("file", type=str, help="The RPAL file to process.")
    parser.add_argument("-ast", action="store_true", help="Print the Abstract Syntax Tree.")
    parser.add_argument("-st", action="store_true", help="Print the Standardized Abstract Syntax Tree.")

    args = parser.parse_args()

    try:
        with open(args.file, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File not found at path: {args.file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {args.file}: {e}")
        sys.exit(1)

    try:
        tokens = Lexer(code).tokenize()
        parser_instance = Parser(tokens)
        ast_tree = parser_instance.parse()

        if args.ast:
            # Removed header and separator for AST
            ast_tree.print()

        # Standardize the AST. This step ineeded for evaluation and -st.
        # If -ast was the only flag, standardized_ast won't be printed unless -st is also present.
        standardized_ast = ast_tree.standerdize() 

        if args.st:
            # Removed header and separator for ST
            standardized_ast.print()
        
        # The evaluate method in AST nodes are handling actual printing 
        standardized_ast.evaluate({}) # Evaluate the standardized AST

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        #import traceback
        # traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()