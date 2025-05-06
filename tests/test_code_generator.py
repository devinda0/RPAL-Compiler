import unittest
from app.code_generator import CodeGenerator
from app.ast_nodes import IntNode, AddNode, VarNode, AssignNode  # just assuming

class TestCodeGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = CodeGenerator()

    def test_generate_int_node(self):
        ast = IntNode(5)
        code = self.generator.generate(ast)
        self.assertEqual(code.strip(), "PUSH 5")

    def test_generate_add_node(self):
        ast = AddNode(IntNode(2), IntNode(3))
        code = self.generator.generate(ast)
        expected = "PUSH 2\nPUSH 3\nADD"
        self.assertEqual(code.strip(), expected)

    def test_generate_variable_assignment(self):
        ast = AssignNode("x", IntNode(1))
        code = self.generator.generate(ast)
        expected = "PUSH 1\nSTORE x"
        self.assertEqual(code.strip(), expected)

    def test_generate_variable_reference(self):
        ast = VarNode("x")
        code = self.generator.generate(ast)
        self.assertEqual(code.strip(), "LOAD x")

if __name__ == '__main__':
    unittest.main()
