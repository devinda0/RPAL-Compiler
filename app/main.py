from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import Interpreter

def run(source_code):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    semantic = SemanticAnalyzer(ast)
    semantic.analyze()

    interpreter = Interpreter(ast)
    result = interpreter.evaluate()
    print("Output:", result)

if __name__ == "__main__":
    with open("input.rpal", "r") as f:
        code = f.read()
    run(code)
