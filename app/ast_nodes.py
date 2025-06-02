from abc import ABC, abstractmethod

class ASTNode(ABC):
    """
    Base class for all AST nodes.
    This class can be extended to create specific types of AST nodes.
    """
    def __init__(self):
        pass

    @abstractmethod
    def standerdize():
        pass


class LetNode(ASTNode):
    def __init__(self, D: ASTNode, E: ASTNode):
        """
        Represents a 'let' expression in the AST.
        :param D: The declaration part of the let expression.
        :param E: The expression part of the let expression.
        """
        self.D = D
        self.E = E
    
    def standerdize():
        pass

class LambdaNode(ASTNode):
    def __init__(self, Vb:list[ASTNode], E: ASTNode):
        """
        Represents a lambda expression in the AST.
        :param Vb: The variable binding part of the lambda expression.
        :param E: The expression body of the lambda expression.
        """
        self.Vb = Vb
        self.E = E
    
    def standerdize():
        pass

class WhereNode(ASTNode):
    def __init__(self, T: ASTNode, Dr: ASTNode):
        """
        Represents a 'where' expression in the AST.
        :param condition: The condition part of the where expression.
        :param body: The body part of the where expression.
        """
        self.T = T
        self.Dr = Dr
    
    def standerdize():
        pass

class TauNode(ASTNode):
    def __init__(self, Tas:list[ASTNode]):
        """
        Represents a 'tau' expression in the AST.
        :param Tas: A list of AST nodes representing the tau expressions.
        """
        self.T = Tas
    
    def standerdize():
        pass

class AugNode(ASTNode):
    def __init__(self, Ta: ASTNode, Tc: ASTNode):
        """
        Represents an 'aug' expression in the AST.
        :param Ta: The first part of the aug expression.
        :param Tc: The second part of the aug expression.
        """
        self.Ta = Ta
        self.Tc = Tc
    
    def standerdize():
        pass

class ArrowNode(ASTNode):
    def __init__(self, B: ASTNode, true: ASTNode, false: ASTNode):
        """
        Represents an 'arrow' expression in the AST.
        :param B: The condition part of the arrow expression.
        :param true: The expression to evaluate if B is true.
        :param false: The expression to evaluate if B is false.
        """
        self.B = B
        self.true = true
        self.false = false
    
    def standerdize():
        pass

class OperatorNode(ASTNode):
    def __init__(self, operator: str, left: ASTNode, right: ASTNode|None = None):
        """
        Represents an operator expression in the AST.
        :param operator: The operator to apply.
        :param left: The left operand.
        :param right: The right operand.
        """
        self.operator = operator
        self.left = left
        self.right = right

    def standerdize():
        pass

class AtNode(ASTNode):
    def __init__(self, Ap: ASTNode, identifier : ASTNode, R:ASTNode):
        """
        Represents an 'at' expression in the AST.
        :param Ap: The first part of the at expression.
        :param identifier: The identifier to apply the at expression to.
        :param R: The second part of the at expression.
        """
        self.Ap = Ap
        self.identifier = identifier
        self.R = R
    
    def standerdize():
        pass

class GammaNode(ASTNode):
    def __init__(self, left:ASTNode, right: ASTNode):
        """
        Represents a 'gamma' expression in the AST.
        :param left: The left part of the gamma expression.
        :param right: The right part of the gamma expression.
        """
        self.left = left
        self.right = right
    
    def standerdize():
        pass

class RandNode(ASTNode):
    def __init__(self, type: str, value: str|int):
        """
        Represents a random node in the AST.
        :param type: The type of the random node (e.g., "IDENTIFIER", "INTEGER", etc.).
        :param value: The value of the random node.
        """
        self.type = type
        self.value = value

    def standerdize():
        pass


class WithinNode(ASTNode):
    def __init__(self, Da:ASTNode, D:ASTNode):
        """
        Represents a 'within' expression in the AST.
        :param Da: The first part of the within expression.
        :param D: The second part of the within expression.
        """
        self.Da = Da
        self.D = D

    def standerdize():
        pass


class AndNode(ASTNode):
    def __init__(self, Drs:list[ASTNode]):
        """
        Represents an 'and' expression in the AST.
        :param Drs: A list of AST nodes representing the 'and' expressions.
        """
        self.Drs = Drs

    def standerdize():
        pass

class RecNode(ASTNode):
    def __init__(self, Db:ASTNode):
        """
        Represents a 'rec' expression in the AST.
        :param Db: The body of the 'rec' expression.
        """
        self.Db = Db

    def standerdize():
        pass


class FcnFormNode(ASTNode):
    def __init__(self, identifier: ASTNode, Vbs:list[ASTNode], E: ASTNode):
        """
        Represents a function form in the AST.
        :param identifier: The identifier of the function.
        :param Vbs: A list of variable bindings for the function.
        :param E: The expression body of the function.
        """
        self.identifier = identifier
        self.Vbs = Vbs
        self.E = E

    def standerdize():
        pass

class EqualNode(ASTNode):
    def __init__(self, left:list[ASTNode], right: ASTNode):
        """
        Represents an equality expression in the AST.
        :param left: The left operand of the equality.
        :param right: The right operand of the equality.
        """

        if isinstance(left, list) and len(left) == 0:
            raise ValueError("Left operand cannot be an empty list")

        self.left = left
        self.right = right

    def standerdize():
        pass




