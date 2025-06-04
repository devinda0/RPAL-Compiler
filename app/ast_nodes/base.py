from abc import ABC, abstractmethod

class ASTNode(ABC):
    """
    Base class for all AST nodes.
    This class can be extended to create specific types of AST nodes.
    """
    def __init__(self):
        pass

    @abstractmethod
    def standerdize(self):
        pass

    @abstractmethod
    def evaluate(self, env):
        """
        Evaluate the AST node.
        This method should be implemented by subclasses to provide specific evaluation logic.
        """
        pass

    @abstractmethod
    def print(self, prefix:str = ""):
        """
        Print the AST node in a readable format.
        :param indent: The indentation level for pretty printing.
        """
        pass

class Closure:
    def __init__(self, params: list[str], body: ASTNode, env: dict):
        """
        Represents a closure in the AST.
        :param params: A list of parameters for the closure.
        :param body: The body of the closure.
        :param env: The environment in which the closure was created.
        """
        self.params = params
        self.body = body
        self.env = env