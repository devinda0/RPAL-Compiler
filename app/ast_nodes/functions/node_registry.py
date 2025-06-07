from app.ast_nodes import ASTNode


NODE_REGISTRY = {}

def register_node(cls):
    """
    Decorator to register a class as an AST node.
    :param cls: The class to register.
    :return: The registered class.
    """
    if not issubclass(cls, ASTNode):
        raise TypeError(f"{cls.__name__} must be a subclass of ASTNode")
    
    NODE_REGISTRY[cls.__name__] = cls
    return cls

def get_node_class(name: str):
    """
    Retrieve a registered AST node class by its name.
    :param name: The name of the AST node class.
    :return: The class if found, otherwise None.
    """
    return NODE_REGISTRY.get(name, None)