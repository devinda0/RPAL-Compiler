from app.ast_nodes import GammaNode, RandNode
from app.ast_nodes.node_registry import get_node_class
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

    code = '''let Vec_sum (A,B) =
    Psum(A,B,Order A)
    where
      rec Psum(A,B,N) = 
	  N eq 0
	  ->  nil
	  |  (Psum(A,B,N-1) aug  A N + B N)

    in (Vec_sum (   (1,2,3),  (4,5,6)  ))
'''
    # code = "let rec f n = n eq 1 -> 0 | n eq 2 -> 1 | f (n-1) + f (n-2) in let rec fib n = n eq 0 -> nil | (fib (n-1) aug f (n)) in Print ( fib 6 )"
    # code = "let rec f x = x eq 0 -> 10 | f (x-1) in Print (f 5)"
    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    # ast.standerdize().print()  # Print the AST structure for debugging
    result = ast.evaluate({})
    # print(result.params, result.env)
    # result.body.print()  # Print the result of the evaluation
