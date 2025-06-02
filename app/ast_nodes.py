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


class LetNode(ASTNode):
    def __init__(self, D: ASTNode, E: ASTNode):
        """
        Represents a 'let' expression in the AST.
        :param D: The declaration part of the let expression.
        :param E: The expression part of the let expression.
        """
        self.D = D
        self.E = E
    
    def standerdize(self):
        standardized_D:EqualNode = self.D.standerdize()
        standardized_E:ASTNode = self.E.standerdize()

        standardized_LetNode = GammaNode(
            left=LambdaNode(
                Vb = standardized_D.left,
                E = standardized_E
            ),
            right=standardized_D.right
        )
        return standardized_LetNode

    def evaluate(self, env):
        return self.standerdize().evaluate(env)

class LambdaNode(ASTNode):
    def __init__(self, Vb:list[ASTNode], E: ASTNode):
        """
        Represents a lambda expression in the AST.
        :param Vb: The variable binding part of the lambda expression.
        :param E: The expression body of the lambda expression.
        """
        self.Vb = Vb
        self.E = E
    
    def standerdize(self):
        self.Vb = [vb.standerdize() for vb in self.Vb]
        self.E = self.E.standerdize()
        return self

    def evaluate(self, env):
        return Closure(
            params=[vb.value for vb in self.Vb],
            body=self.E,
            env=env
        )

class WhereNode(ASTNode):
    def __init__(self, T: ASTNode, Dr: ASTNode):
        """
        Represents a 'where' expression in the AST.
        :param condition: The condition part of the where expression.
        :param body: The body part of the where expression.
        """
        self.T = T
        self.Dr = Dr
    
    def standerdize(self):
        standerdized_T = self.T.standerdize()
        standerdized_Dr = self.Dr.standerdize()

        return GammaNode(
            left=LambdaNode(
                Vb=standerdized_Dr.left,
                E=standerdized_T
            ),
            right=standerdized_Dr.right
        )

    def evaluate(self, env):
        return self.standerdize().evaluate(env)

class TauNode(ASTNode):
    def __init__(self, Tas:list[ASTNode]):
        """
        Represents a 'tau' expression in the AST.
        :param Tas: A list of AST nodes representing the tau expressions.
        """
        self.T = Tas
    
    def standerdize():
        pass

    def evaluate(self, env):
        """
        Evaluate the tau node.
        For a TauNode, this typically means evaluating each of its child nodes.
        """
        return [ta.evaluate(env) for ta in self.T]

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

    def evaluate(self, env):
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
    
    def standerdize(self):
        self.B = self.B.standerdize()
        self.true = self.true.standerdize()
        self.false = self.false.standerdize()
        self

    def evaluate(self, env):
        if self.B.evaluate():
            return self.true.evaluate(env)
        else:
            return self.false.evaluate(env)

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

    def standerdize(self):
        self.left = self.left.standerdize()
        self.right = self.right.standerdize() if self.right else None
        return self

    def evaluate(self, env):
        match self.operator:
            case "+":
                return self.left.evaluate(env) + self.right.evaluate(env)
            case "-":
                return self.left.evaluate(env) - self.right.evaluate(env)
            case "*":
                return self.left.evaluate(env) * self.right.evaluate(env)
            case "/":
                return self.left.evaluate(env) / self.right.evaluate(env)
            case "%":
                return self.left.evaluate(env) % self.right.evaluate(env)
            case "==":
                return self.left.evaluate(env) == self.right.evaluate(env)
            case "!=":
                return self.left.evaluate(env) != self.right.evaluate(env)
            case "<":
                return self.left.evaluate(env) < self.right.evaluate(env)
            case ">":
                return self.left.evaluate(env) > self.right.evaluate(env)
            case "<=":
                return self.left.evaluate(env) <= self.right.evaluate(env)
            case ">=":
                return self.left.evaluate(env) >= self.right.evaluate(env)
            case _:
                raise ValueError(f"Unknown operator: {self.operator}")

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
    
    def standerdize(self):
        standerdized_Ap = self.Ap.standerdize()
        standerdized_R = self.R.standerdize()

        return GammaNode(
            left=GammaNode(
                left = self.identifier,
                right = standerdized_Ap
            ),
            right=standerdized_R
        )

    def evaluate(self,env):
        self.standerdize().evaluate(env)

class GammaNode(ASTNode):
    def __init__(self, left:ASTNode, right: ASTNode):
        """
        Represents a 'gamma' expression in the AST.
        :param left: The left part of the gamma expression.
        :param right: The right part of the gamma expression.
        """
        self.left = left
        self.right = right
    
    def standerdize(self):
        self.left = self.left.standerdize()
        self.right = self.right.standerdize()
        self

    def evaluate(self, env):
        closure:Closure = self.left.evaluate(env)
        arguments = self.right.evaluate(env)

        if len(closure.params) == 1:
            # If there's only one parameter, we can directly evaluate it
            new_env = closure.env.copy()
            new_env[closure.params[0]] = arguments
        elif len(closure.params) == 0:
            # If there are no parameters, we can directly evaluate the body
            new_env = closure.env.copy()
        elif len(closure.params) != len(arguments):
            raise ValueError(f"Expected {len(closure.params)} arguments, got {len(arguments)}")
        else:
            new_env = closure.env.copy()  # Create a new environment based on the closure's environment
            
            for i in range(len(closure.params)):
                new_env[closure.params[i]] = arguments[i]
        return closure.body.evaluate(new_env)  # Evaluate the body of the closure in the new environment

class RandNode(ASTNode):
    def __init__(self, type: str, value: str|int):
        """
        Represents a random node in the AST.
        :param type: The type of the random node (e.g., "IDENTIFIER", "INTEGER", etc.).
        :param value: The value of the random node.
        """
        self.type = type
        self.value = value

    def standerdize(self):
        return self

    def evaluate(self, env):
        """
        Evaluate the random node.
        For a RandNode, this typically means returning its value.
        """
        if self.type == "IDENTIFIER":
            return env.get(self.value, None)
        elif self.type in ["INTEGER", "STRING"]:
            return self.value
        elif self.type == "TRUE":
            return True
        elif self.type == "FALSE":
            return False
        elif self.type == "NILL":
            return None
        elif self.type == "DUMMY":
            return "DUMMY"
        else:
            raise ValueError(f"Unknown type: {self.type}")


class WithinNode(ASTNode):
    def __init__(self, Da:ASTNode, D:ASTNode):
        """
        Represents a 'within' expression in the AST.
        :param Da: The first part of the within expression.
        :param D: The second part of the within expression.
        """
        self.Da = Da
        self.D = D

    def standerdize(self):
        standardized_Da = self.Da.standerdize()
        standardized_D = self.D.standerdize()

        return EqualNode(
            left=standardized_D.left,
            right=GammaNode(
                left=LambdaNode(
                    Vb=standardized_Da.left,
                    E=standardized_D.right
                ),
                right=standardized_Da.right
            )
        )

    def evaluate(self, env):
        return self.standerdize().evaluate(env)


class AndNode(ASTNode):
    def __init__(self, Drs:list[ASTNode]):
        """
        Represents an 'and' expression in the AST.
        :param Drs: A list of AST nodes representing the 'and' expressions.
        """
        self.Drs = Drs

    def standerdize(self):
        standardized_Drs = [dr.standerdize() for dr in self.Drs]
        return EqualNode(
            left=[dr.left for dr in standardized_Drs],
            right=[dr.right for dr in standardized_Drs]
        )

    def evaluate(self, env):
        raise NotImplementedError("Cannot evaluate 'and' node directly. Use standerdize() method to convert it to an equality node.")

class RecNode(ASTNode):
    def __init__(self, Db:ASTNode):
        """
        Represents a 'rec' expression in the AST.
        :param Db: The body of the 'rec' expression.
        """
        self.Db = Db

    def standerdize():
        pass

    def evaluate(self, env):
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

    def evaluate(self, env):
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

    def standerdize(self):
        return self

    def evaluate(self, env):
        """
        Cannot evaluate equality node
        """
        raise NotImplementedError("Cannot evaluate equality node directly")


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



