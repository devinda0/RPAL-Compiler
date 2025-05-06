import unittest
from app.lexer import Lexer

class TestLexer(unittest.TestCase):

    def test_identifier(self):
        lexer = Lexer("my_var1")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "IDENTIFIER")
        self.assertEqual(tokens[0].value, "my_var1")

    def test_integer(self):
        lexer = Lexer("12345")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "INTEGER")
        self.assertEqual(tokens[0].value, "12345")

    def test_operator(self):
        lexer = Lexer("+")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "OPERATOR")
        self.assertEqual(tokens[0].value, "+")

    def test_string(self):
        lexer = Lexer("'''Hello World'''")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "STRING")
        self.assertEqual(tokens[0].value, "Hello World")

    def test_punctuation(self):
        lexer = Lexer("( ) ; ,")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].value, "(")
        self.assertEqual(tokens[1].value, ")")
        self.assertEqual(tokens[2].value, ";")
        self.assertEqual(tokens[3].value, ",")

    def test_comment_deletion(self):
        lexer = Lexer("/// this is a comment\n123")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "INTEGER")
        self.assertEqual(tokens[0].value, "123")

    def test_spaces_are_deleted(self):
        lexer = Lexer("   \n  \t 456")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, "INTEGER")
        self.assertEqual(tokens[0].value, "456")

if __name__ == "__main__":
    unittest.main()
