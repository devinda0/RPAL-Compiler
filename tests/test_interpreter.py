import unittest
from io import StringIO
from unittest.mock import patch

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

    @patch('sys.stdout', new_callable=StringIO)
    def test_tau_element_accessing(self, mock_stdout):
        source_code = "let x = (1,2,3) in Print (x 1)"
        run_interpreter(source_code)
        self.assertEqual(mock_stdout.getvalue().strip(), "1")

    @patch('sys.stdout', new_callable=StringIO)
    def test_function_application(self, mock_stdout):
        source_codes = [
            ("let f x = x + 1 in Print (f 2)", "3"),
            ("Print((fn f. f 2) (fn x. x eq 1 -> 1 | x+2))", "4"),
            ("""
                Print( 
                    (fn f. f 'first letter missing in this sentence?') (fn x. Stern x) 
                )
            """, "irst letter missing in this sentence?"),
            ("""
                Print (   (fn x. x+1) ( (fn y. y+3) ( (fn z. z+4)7 ) ))
            """, "15"),
        ]

        for source_code, answer in source_codes:
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            run_interpreter(source_code)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, answer)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_function(self, mock_stdout):
        source_code = "Print(1 + 2)"
        run_interpreter(source_code)
        self.assertEqual(mock_stdout.getvalue().strip(), "3")

    @patch('sys.stdout', new_callable=StringIO)
    def test_infix_operations(self, mock_stdout):
        source_codes = [
            ("""
                let f x y z = x + y + z
                in Print ((3 @f 6) 4)
                """, "13"),
            ("""
                let f x y z t = x + y + z + t
                in Print (( 3 @f 4) 5 6 )
                ""","18")
        ]

        for source_code, answer in source_codes:
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            run_interpreter(source_code)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, answer)

    
    @patch('sys.stdout', new_callable=StringIO)
    def test_pairs(self, mock_stdout):
        source_codes = [
            ("""
                let rec Rev S =
                    S eq '' -> ''
                    | (Rev(Stern S)) @Conc (Stem S )
                within
                    Pairs (S1,S2) =
                    not (Isstring S1 & Isstring S2) -> 'both args not strings'
                    | P (Rev S1, Rev S2)
                    where rec P (S1, S2) =
                    S1 eq '' & S2 eq '' -> nil
                    | (Stern S1 eq '' & Stern S2 ne '') or
                    (Stern S1 ne '' & Stern S2 eq '')
                        -> 'bad strings'
                    | (P (Stern S1, Stern S2) aug ((Stem S1) @Conc (Stem S2)))
                in Print ( Pairs ('abc','def'))
             ""","(ad, be, cf)")
        ]

        for source_code, answer in source_codes:
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            run_interpreter(source_code)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, answer)


    @patch('sys.stdout', new_callable=StringIO)
    def test_is_string(self, mock_stdout):
        source_codes = [
            ("Print(Isstring('hello'))", "True"),
            ("Print(Isstring(123))", "False"),
            ("Print(Isstring(''))", "True")
        ]

        for source_code, answer in source_codes:
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            run_interpreter(source_code)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, answer)

    @patch('sys.stdout', new_callable=StringIO)
    def test_not_operator(self, mock_stdout):
        source_codes = [
            ("Print(not true)", "False"),
            ("Print(not false)", "True"),
            ("Print(not (1 + 1 eq 2))", "False"),
            ("Print(not (1 + 1 eq 3))", "True")
        ]

        for source_code, answer in source_codes:
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            run_interpreter(source_code)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, answer)

    @patch('sys.stdout', new_callable=StringIO)
    def test_and_operator(self, mock_stdout):
        source_codes = [
            ("Print(true & true)", "True"),
            ("Print(true & false)", "False"),
            ("Print(false & true)", "False"),
            ("Print(false & false)", "False"),
            ("Print((1 + 1 eq 2) & (2 + 2 eq 4))", "True"),
            ("Print((1 + 1 eq 2) & (2 + 2 eq 5))", "False")
        ]

        for source_code, answer in source_codes:
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            run_interpreter(source_code)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, answer)
