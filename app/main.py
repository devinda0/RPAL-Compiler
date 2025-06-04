from app.ast_nodes import GammaNode, RandNode
from .lexer import Lexer
from .parser import Parser
# from .semantic_analyzer import SemanticAnalyzer
# from .code_generator import Interpreter
from .token import Token

def run(source_code):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    # semantic = SemanticAnalyzer(ast)
    # semantic.analyze()

    interpreter = Interpreter(ast)
    result = interpreter.evaluate()
    print("Output:", result)

if __name__ == "__main__":
    # with open("input.rpal", "r") as f:
    #     code = f.read()
    # run(code)
    # test_code = "'''Hello, World!'''"
    # tokens = Lexer(test_code).tokenize()
    # for token in tokens:
    #     print(token)

    code = "let rec f x = x eq 0 -> 10 | f (x-1) in f 5"
    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    # ast.standerdize().print()  # Print the AST structure for debugging
    result = ast.evaluate({})
    print("Output:", result)
    # print(result.params, result.env)
    # result.body.print()  # Print the result of the evaluation