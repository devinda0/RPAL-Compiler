from .base import ASTNode


class CommaNode(ASTNode):
    def __init__(self, children: list[ASTNode]):
        """
        Represents a comma-separated list of AST nodes.
        :param children: A list of AST nodes that are separated by commas.
        """
        self.children = children

    def standerdize(self):
        """
        Standardize the comma-separated nodes.
        This method will standardize each child node in the list.
        """
        standardized_children = [child.standerdize() for child in self.children]
        return CommaNode(standardized_children)
    
    def evaluate(self, env):
        """
        Evaluate each child node in the environment.
        This method will evaluate each child node and return a list of their results.
        """
        return [child.evaluate(env) for child in self.children]
    
    def print(self, prefix: str = ""):
        """
        Print the comma node in a readable format.
        :param prefix: The indentation level for pretty printing.
        """
        print(f"{prefix},")
        for child in self.children:
            child.print(prefix + ". ")