import unittest
from app import Lexer

class TestLexer(unittest.TestCase):

    def test_identifier(self):
        lexer = Lexer("my_var1")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "IDENTIFIER", "Expected IDENTIFIER token type for 'my_var1'")
        self.assertEqual(tokens[0].value, "my_var1", "Expected token value to be 'my_var1'")

    def test_integer(self):
        lexer = Lexer("12345")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "INTEGER", "Expected INTEGER token type for '12345'")
        self.assertEqual(tokens[0].value, "12345", "Expected token value to be '12345'")

    def test_operator(self):
        operators = "+-*<>&.@:=~|$!#%^_[]{}?"
        for operator in operators:
            lexer = Lexer(operator)
            tokens = lexer.tokenize()
            self.assertEqual(tokens[0].type, "OPERATOR", f"Expected OPERATOR token for '{operator}'")
            self.assertEqual(tokens[0].value, operator, f"Expected token value to be '{operator}'")

    def test_string(self):
        test_strings = [
            "\"Hello, World!\"",
            "\"This is a test string with spaces\"",
            "\"String with \\\"escaped quotes\\\" inside\"",
            "\"String with \\n new line\"",
            "'''Hello, World!'''",
            "'''This is a test string with spaces'''",
        ]
        for test_string in test_strings:
            lexer = Lexer(test_string)
            tokens = lexer.tokenize()
            self.assertEqual(tokens[0].type, "STRING", f"Expected STRING token for '{test_string}'")
            self.assertEqual(tokens[0].value, test_string[1:-1], f"Expected token value to be '{test_string[1:-1]}'")

    def test_punctuation(self):
        lexer = Lexer("( ) ; ,")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].value, "(", "Expected first punctuation token to be '('")
        self.assertEqual(tokens[1].value, ")", "Expected second punctuation token to be ')'")
        self.assertEqual(tokens[2].value, ";", "Expected third punctuation token to be ';'")
        self.assertEqual(tokens[3].value, ",", "Expected fourth punctuation token to be ','")

    def test_comment_deletion(self):
        lexer = Lexer("/// this is a comment\n123")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "INTEGER", f"Expected INTEGER token after comment but got : {tokens[0].type}")
        self.assertEqual(tokens[0].value, "123", "Expected token value to be '123' after comment")

    def test_spaces_are_deleted(self):
        lexer = Lexer("   \n  \t 456")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "INTEGER", "Expected INTEGER token after whitespace")
        self.assertEqual(tokens[0].value, "456", "Expected token value to be '456' after whitespace")

if __name__ == "__main__":
    unittest.main()
