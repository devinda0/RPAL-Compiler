from app.ast_nodes.bracket_node import BracketNode
from app.ast_nodes.comma_node import CommaNode
from .token import Token
from .ast_nodes import (
    ASTNode,  # Assuming you have a base ASTNode class in ast_nodes.py
    LetNode,
    LambdaNode,
    WhereNode,
    TauNode,
    AugNode,
    ArrowNode,
    OperatorNode,
    AtNode,
    GammaNode,
    RandNode,
    WithinNode,
    AndNode,
    RecNode,
    FcnFormNode,
    EqualNode,
)



class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token_index = 0
        self.ast_stack = [] # Using a list as a stack for AST nodes

    def _peek(self) -> Token | None:
        """Returns the current token without consuming it."""
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def _consume(self, expected_value: str = None, expected_type: str = None):
        """Consumes the current token, optionally checking its value or type."""
        token = self._peek()
        if token is None:
            # Adjusted error message for clarity
            expected_desc = ""
            if expected_value:
                expected_desc = f"'{expected_value}'"
            elif expected_type:
                expected_desc = f"a token of type {expected_type}"
            else:
                expected_desc = "more tokens"
            raise SyntaxError(f"Syntax error: Unexpected end of input. Expected {expected_desc}.")

        if expected_value is not None and token.value != expected_value:
            raise SyntaxError(f"Syntax error in line {token.line}: Expected '{expected_value}' but got '{token.value}'")
        if expected_type is not None and token.type != expected_type:
            raise SyntaxError(f"Syntax error in line {token.line}: Expected token type {expected_type} but got {token.type} ('{token.value}')")
        
        self.current_token_index += 1
        return token

    def parse(self):
        """Main parsing method. Starts parsing from the top-level rule."""
        if not self.tokens:
            # Handle empty token list if necessary, or let _peek handle it.
            # Depending on grammar, an empty token list might be a valid empty program or an error.
            # For many languages, it's an error or results in a specific "empty" AST node.
            # For now, let's assume an empty program is not valid and would be caught by _parse_E.
             pass

        return self._parse_E() # Start with the top-level grammar rule E

        if len(self.ast_stack) == 1:
            return self.ast_stack.pop()
        elif not self.ast_stack and not self.tokens: # Special case: empty input, empty stack
            return ASTNode("empty_program", []) # Or however you represent an empty AST
        elif len(self.ast_stack) > 1:
            raise Exception("Parser error: AST stack has multiple roots.")
        else: # len(self.ast_stack) == 0 but tokens might have been consumed
            # This case might occur if the grammar is empty or parsing failed silently
            # Or if the top rule doesn't build a node for some inputs.
            # If _parse_E is guaranteed to push a node for valid programs, this is an error.
            if self.current_token_index < len(self.tokens):
                 raise SyntaxError(f"Syntax error: Unexpected token '{self._peek().value}' at end of input.")
            # If all tokens consumed and stack is empty, it might mean an empty valid program
            # that doesn't produce a node, or an error in grammar/logic.
            # For now, let's assume a valid program always results in one root node.
            raise Exception("Parser error: AST stack is empty after parsing.")

    # --- Grammar Rule Parsing Methods ---
    # These methods correspond to the procedures in the provided code.
    # I've renamed them for clarity (e.g., procedure_E -> _parse_E)
    # and adapted them to use the class's methods and attributes.

    def _parse_E(self):      
        """ Parses an Expression (E).
        E -> 'let' D 'in' E 
           | 'fn' Vb+ '.' E    
           | Ew
        """
        token = self._peek()
        if token is None:
            raise SyntaxError("Syntax error: Unexpected end of input, expected an expression.")

        if token.value == "let":
            self._consume("let")
            D:ASTNode =self._parse_D()
            self._consume("in")
            E:ASTNode =self._parse_E()
            return LetNode(D, E)
        elif token.value == "fn":
            self._consume("fn")
            n = 0
            Vb:list[ASTNode] = []
            # Vb+ means one or more Vb
            while self._peek() and (self._peek().type == "IDENTIFIER" or self._peek().value == "("): 
                Vb.append(self._parse_Vb())
                n += 1
            if n == 0:
                err_token = self._peek()
                line = err_token.line if err_token else "N/A"
                raise SyntaxError(f"Syntax error in line {line}: At least one variable binding (IDENTIFIER or '(') expected after 'fn'")
            
            self._consume(".")
            E:ASTNode = self._parse_E()
            return LambdaNode(Vb, E) 
        else:
            return self._parse_Ew()

    def _parse_Ew(self):
        """ Parses Ew.
        Ew -> T ('where' Dr)?
        """
        T:ASTNode = self._parse_T()
        token = self._peek()
        if token and token.value == "where":
            self._consume("where")
            Dr:ASTNode = self._parse_Dr()
            return WhereNode(T, Dr)
        else:
            # If no 'where', just return T
            return T
        
    def _parse_T(self):     
        """ Parses T.
        T -> Ta (',' Ta)*
        """
        Tas:list[ASTNode] = []
        Tas.append(self._parse_Ta())
        n = 0
        while self._peek() and self._peek().value == ",":
            self._consume(",")
            Tas.append(self._parse_Ta())
            n += 1
        if n > 0:
            return TauNode(Tas)  # If multiple Tas, return a TauNode with the list of Tas
        else:
            return Tas[0]  # If only one Ta, return it directly
        
    def _parse_Ta(self):  
        """ Parses Ta.
        Ta -> Tc ('aug' Tc)*
        """
        Tcs:list[ASTNode] = []
        Tcs.append(self._parse_Tc())

        while self._peek() and self._peek().value == "aug":
            self._consume("aug")
            Tcs.append(self._parse_Tc())
        
        if len(Tcs) > 1:
            currentNode = OperatorNode("aug", Tcs[0], Tcs[1])
            Tcs = Tcs[2:]  # Remove the firs two nodes
            for Ta in Tcs:
                currentNode = OperatorNode("aug", currentNode, Ta)
            return currentNode  # Return the binary operation node for multiple Tcs
        elif len(Tcs) == 1:
            return Tcs[0]
        else:
            raise SyntaxError("Syntax error: Expected at least one Tc in Ta.")
        
    def _parse_Tc(self):   
        """ Parses Tc.
        Tc -> B ('->' Tc '|' Tc)?
        """
        B:ASTNode = self._parse_B()
        token = self._peek()
        if token and token.value == "->":  
            self._consume("->")
            true:ASTNode = self._parse_Tc()
            self._consume("|")
            false:ASTNode = self._parse_Tc()
            
            return ArrowNode(B, true, false)  # Return an ArrowNode with B, true, and false
        else:
            # If no '->', just return B
            return B
            
    def _parse_B(self):
        """ Parses B.
        B -> Bt ('or' Bt)*
        """
        Bts:list[ASTNode] = []
        Bts.append(self._parse_Bt())
        while self._peek() and self._peek().value == "or":
            self._consume("or")
            self._parse_Bt()
        
        if len(Bts) > 1:
            currentNode = OperatorNode("or", Bts[-2], Bts[-1])
            Bts = Bts[:-2]
            for B in reversed(Bts):
                currentNode = OperatorNode("or", B, currentNode)
            return currentNode  # Return the binary operation node for multiple Bts
        elif len(Bts) == 1:
            return Bts[0]
        else:
            raise SyntaxError("Syntax error: Expected at least one Bt in B.")

    def _parse_Bt(self):    
        """ Parses Bt.
        Bt -> Bs ('&' Bs)*
        """
        Bss:list[ASTNode] = []
        Bss.append(self._parse_Bs())
        while self._peek() and self._peek().value == "&":
            self._consume("&")
            Bss.append(self._parse_Bs())

        if len(Bss) > 1:
            currentNode = OperatorNode("&", Bss[-2], Bss[-1])
            Bss = Bss[:-2]
            for B in reversed(Bss):
                currentNode = OperatorNode("&", B, currentNode)
            return currentNode  # Return the binary operation node for multiple Bss
        elif len(Bss) == 1:
            return Bss[0]
        else:
            raise SyntaxError("Syntax error: Expected at least one Bs in Bt.")


    def _parse_Bs(self):
        """ Parses Bs.
        Bs -> 'not' Bp | Bp
        """
        token = self._peek()
        if token and token.value == "not":
            self._consume("not")
            Bp:ASTNode = self._parse_Bp()
            return OperatorNode("not", Bp, None)  # Return a unary 'not' operation node
        else:
            return self._parse_Bp()
        
    def _parse_Bp(self):           
        """ Parses Bp (Boolean with comparisons).
        Bp -> A (('gr' | '>') A | ('ge' | '>=') A | ... | 'ne' A)?
        """
        firstA:ASTNode = self._parse_A()
        token = self._peek()
        if token:
            op_value = None
            node_name = None
            if token.value == "gr" or token.value == ">":
                op_value = token.value
                node_name = "gr"
            elif token.value == "ge" or token.value == ">=":
                op_value = token.value
                node_name = "ge"
            elif token.value == "ls" or token.value == "<":
                op_value = token.value
                node_name = "ls"
            elif token.value == "le" or token.value == "<=":
                op_value = token.value
                node_name = "le"
            elif token.value == "eq":
                op_value = token.value
                node_name = "eq"
            elif token.value == "ne":
                op_value = token.value
                node_name = "ne"

            if op_value:
                self._consume(op_value) # Consume the specific operator token
                secondA:ASTNode = self._parse_A()
                return OperatorNode(node_name, firstA, secondA)  # Return a binary operation node
            else:
                # If no comparison operator, just return the first A
                return firstA
        else:
            return firstA

    def _parse_A(self):
        """ Parses A (Arithmetic expressions: +, -).
        A -> ('+' | '-')? At (('+' | '-') At)*
        """
        token = self._peek()
        is_negated = False
        if token:
            if token.value == "+":
                self._consume("+")
                # Positive unary plus often has no semantic meaning or AST node
            elif token.value == "-":
                self._consume("-")
                is_negated = True
                
        firstAt:ASTNode = self._parse_At()
        if is_negated:
            firstAt = OperatorNode("neg", firstAt, None)  # Negate the first At if unary minus was used
            
        Ats:list[tuple[ASTNode, str]] = [(firstAt, '+')]   # Start with the first At
        while self._peek() and (self._peek().value == "+" or self._peek().value == "-"):
            op_token = self._peek()
            if op_token.value == "+":
                self._consume("+")
                Ats.append((self._parse_At(), '+'))  # Append the next At with '+' operator
            elif op_token.value == "-":
                self._consume("-")
                Ats.append((self._parse_At(), '-'))  # Append the next At with '-' operator
        
        if len(Ats) == 1:
            return Ats[0][0]
        elif len(Ats) > 1:
            # If there are multiple Ats, we need to combine them into a binary operation tree
            current_node = Ats[0][0]
            for i in range(1, len(Ats), 1):
                if Ats[i][1] == '+':
                    current_node = OperatorNode("+", current_node, Ats[i][0])
                elif Ats[i][1] == '-':
                    current_node = OperatorNode("-", current_node, Ats[i][0])

            return current_node  # Return the combined binary operation node
        else:
            raise SyntaxError("Syntax error: Expected at least one At in A.")


    def _parse_At(self):
        """ Parses At (Arithmetic terms: *, /).
        At -> Af (('*' | '/') Af)*
        """
        Afs:list[tuple[ASTNode, str]] = []
        Afs.append((self._parse_Af(),''))  # Start with the first Af
        while self._peek() and (self._peek().value == "*" or self._peek().value == "/"):
            op_token = self._peek()
            if op_token.value == "*":
                self._consume("*")
                Afs.append((self._parse_Af(), '*'))  # Append the next Af with '*' operator
            elif op_token.value == "/":
                self._consume("/")
                Afs.append((self._parse_Af(), '/'))  # Append the next Af with '/' operator
            
        if len(Afs) == 1:
            return Afs[0][0]
        elif len(Afs) > 1:
            # If there are multiple Afs, we need to combine them into a binary operation tree
            current_node = Afs[0][0]
            for i in range(1, len(Afs), -1):
                if Afs[i][1] == '*':
                    current_node = OperatorNode("*", current_node, Afs[i][0])
                elif Afs[i][1] == '/':
                    current_node = OperatorNode("/", current_node, Afs[i][0])

            return current_node
        else:
            raise SyntaxError("Syntax error: Expected at least one Af in At.")

    def _parse_Af(self):    
        """ Parses Af (Arithmetic factors: exponentiation).
        Af -> Ap ('**' Af)?
        """
        firstAp:ASTNode = self._parse_Ap()
        if self._peek() and self._peek().value == "**":     
            self._consume("**")
            return OperatorNode("**", firstAp, self._parse_Ap())  # Return a binary operation node for exponentiation
        else:
            # If no exponentiation, just return the first Ap
            return firstAp
 
    def _parse_Ap(self):
        """ Parses Ap (Atomic power operand, function application with @).
        Ap -> R ('@' <IDENTIFIER> R)* 
        """
        firstR:ASTNode = self._parse_R()
        Ats:list[tuple[ASTNode, ASTNode|None]] = [(firstR, None)]  # Start with the first R, no identifier yet

        while self._peek() and self._peek().value == "@":
            self._consume("@")
            id_token = self._peek()
            if id_token and id_token.type == "IDENTIFIER":
                identifier = RandNode("IDENTIFIER", id_token.value)
                self._consume(expected_type="IDENTIFIER")
                R:ASTNode = self._parse_R()
                Ats.append((R, identifier))  # Append the next R with its identifier 
            else:
                err_token = self._peek()
                line = err_token.line if err_token else "N/A"
                raise SyntaxError(f"Syntax error in line {line}: IDENTIFIER expected after '@'")
            
        if len(Ats) == 1:
            return Ats[0][0]
        elif len(Ats) > 1:
            # If there are multiple Ats, we need to combine them into an AtNode
            current_node = Ats[0][0]
            for i in range(1, len(Ats)):
                if Ats[i][1] is not None:
                    # If there's an identifier, create an AtNode
                    current_node = AtNode(current_node, Ats[i][1], Ats[i][0])
            return current_node  # Return the combined AtNode
    
    def _parse_R(self):
        """ Parses R (Repeated applications/atoms).
        R -> Rn (Rn)* 
        """
        firstRn:ASTNode = self._parse_Rn()

        Rns:list[ASTNode] = [firstRn]  # Start with the first Rn

        # Check if next token can start an Rn (for function application)
        while self._peek() and \
              (self._peek().type in ["IDENTIFIER", "INTEGER", "STRING"] or \
               self._peek().value in ["true", "false", "nil", "(", "dummy"]): 
            Rns.append(self._parse_Rn())

        if len(Rns) == 1:
            return Rns[0]
        elif len(Rns) > 1:
            # If there are multiple Rns, we need to combine them into a single node
            current_node = Rns[0]
            for i in range(1, len(Rns)):
                current_node = GammaNode(current_node, Rns[i])  # Combine them into a GammaNode
            
            return current_node  # Return the combined GammaNode

    def _parse_Rn(self):   
        """ Parses Rn (Atomic operands).
        Rn -> <IDENTIFIER> | <INTEGER> | <STRING> 
            | 'true' | 'false' | 'nil' | 'dummy'    
            | '(' E ')'    
        """
        token = self._peek()
        if token is None:
            raise SyntaxError("Syntax error: Unexpected end of input, expected an operand.")

        value = token.value
        
        if token.type == "IDENTIFIER":
            self._consume(expected_type="IDENTIFIER")
            return RandNode("IDENTIFIER", value)  # Create a RandNode for IDENTIFIER
        elif token.type == "INTEGER":
            self._consume(expected_type="INTEGER")
            return RandNode("INTEGER", int(value))  # Create a RandNode for INTEGER
        elif token.type == "STRING":
            self._consume(expected_type="STRING")
            return RandNode("STRING", value)  # Create a RandNode for STRING
        elif value in ["true", "false", "nil", "dummy"]:
            self._consume(value)
            return RandNode(value.upper(), value)
        elif value == "(":
            self._consume("(")
            E:ASTNode = self._parse_E()
            self._consume(")")
            return E  # Return the parsed expression inside parentheses
            # No specific node for parentheses; the structure of E is preserved.
        else:
            raise SyntaxError(f"Syntax error in line {token.line}: Unexpected token '{value}'. Expected IDENTIFIER, INTEGER, STRING, keyword, or '('.")

    def _parse_D(self):
        """ Parses D (Definitions).
        D -> Da ('within' D)?
        """
        Da:ASTNode = self._parse_Da()
        if self._peek() and self._peek().value == "within":
            self._consume("within")
            return WithinNode(Da, self._parse_D())
        else:
            # If no 'within', just return Da
            return Da
    
    def _parse_Da(self):
        """ Parses Da.
        Da -> Dr ('and' Dr)*
        """
        firstDr:ASTNode =self._parse_Dr()
        Drs:list[ASTNode] = [firstDr]  # Start with the first Dr
        n = 0
        while self._peek() and self._peek().value == "and":
            self._consume("and")
            Drs.append(self._parse_Dr())  # Append the next Dr
            n += 1

        if n > 0:  
            return AndNode(Drs)  # If multiple Drs, return an AndNode with the list of Drs
        elif n == 0:
            return firstDr
    
    def _parse_Dr(self):
        """ Parses Dr.
        Dr -> 'rec' Db | Db
        """
        if self._peek() and self._peek().value == "rec":
            self._consume("rec")
            return RecNode(self._parse_Db())  # If 'rec', parse Db and return a RecNode
        else:
            return self._parse_Db()
    
    def _parse_Db(self):    
        """ Parses Db (Definition body).
        Db -> <IDENTIFIER> Vb+ '=' E       (function form)
           | <IDENTIFIER> '=' E            (simple variable binding, Vl handles this)
           | '(' D ')'
        """
        token = self._peek()
        if token is None:
            raise SyntaxError("Syntax error: Unexpected end of input, expected a definition.")

        if token.value == "(":
            self._consume("(")
            D:ASTNode = self._parse_D() # If it's a parenthesized definition, parse D inside parentheses
            self._consume(")")
            return D  # Return the parsed D, which is a child of the parentheses node
        elif token.type == "IDENTIFIER":
            identifier = token.value
            self._consume(expected_type="IDENTIFIER")

            peek = self._peek()

            if peek and peek.value == ",":
                self._consume(",")
                Vls:CommaNode = self._parse_Vl()  # Parse Vl for multiple identifiers
                if not Vls or not isinstance(Vls, CommaNode):
                    raise SyntaxError(f"Syntax error in line {token.line}: Expected a comma-separated list of identifiers after '{identifier}'.")
                Vls = CommaNode([RandNode("IDENTIFIER", identifier)] + Vls.children)  # Prepend the current identifier to the list
                self._consume("=")
                E:ASTNode = self._parse_E()
                return EqualNode(Vls, E)  # Return an EqualNode with the list of identifiers and the expression
            elif (peek and peek.type == "IDENTIFIER") or \
               (peek and peek.value == "("):  # If next is IDENTIFIER or '('
                # This indicates a function form with variable bindings
                # If next is IDENTIFIER, it might be a function form with Vb
                Vbs:list[ASTNode] = []
                while self._peek() and (self._peek().type == "IDENTIFIER" or self._peek().value == "("):
                    Vbs.append(self._parse_Vb())

                self._consume("=")
                E:ASTNode = self._parse_E()
                return FcnFormNode(RandNode("IDENTIFIER", identifier), Vbs, E)  # Return a function form node
            else:
                # If next is not a comma or IDENTIFIER, it's a simple variable binding
                self._consume("=")
                E:ASTNode = self._parse_E()
                return EqualNode(RandNode("IDENTIFIER", identifier), E)
        else:
            raise SyntaxError(f"Syntax error in line {token.line}: IDENTIFIER or '(' expected for a definition.")


    def _parse_Vb(self): 
        """ Parses Vb (Variable Binding in function definitions).
        Vb -> <IDENTIFIER>
           | '(' Vl? ')'  // Vl? means Vl is optional. If Vl is not present, it's '()'
        """
        token = self._peek()
        if token is None:
            raise SyntaxError("Syntax error: Unexpected end of input, expected a variable binding.")

        if token.type == "IDENTIFIER":
            self._consume(expected_type="IDENTIFIER")
            return RandNode("IDENTIFIER", token.value)  # Return a list with a single identifier node
        elif token.value == "(":
            self._consume("(")
            # Check if next is ')' for an empty tuple '()' or if it's a Vl
            if self._peek() and self._peek().value == ")":
                self._consume(")")
                return BracketNode()
            elif self._peek() and self._peek().type == "IDENTIFIER": 
                # This indicates the start of Vl
                Vls:CommaNode = self._parse_Vl() # Vl will build its own node(s)
                self._consume(")")
                return Vls  # Return the list of variable bindings from Vl
            else: # Content inside () but not IDENTIFIER and not ')'
                err_token = self._peek()
                line = err_token.line if err_token else "N/A"
                raise SyntaxError(f"Syntax error in line {line}: IDENTIFIER or ')' expected inside parameter list.")
        else:
            raise SyntaxError(f"Syntax error in line {token.line}: IDENTIFIER or '(' expected for a variable binding.")
    
    def _parse_Vl(self):
        """ Parses Vl (Variable List, typically in tuples or multiple assignments).
        Vl -> <IDENTIFIER> (',' <IDENTIFIER>)*   
        Pushes individual IDENTIFIER nodes. If a list node is needed, the caller of Vl should build it.
        The original code's Vl built a "," node. Here, we'll push IDs, and if Db needs a list, it can form it.
        However, for `(Vl)`, Vb expects Vl to potentially form a structure.
        Let's follow the original's intent: Vl creates a list node if multiple items.
        """
        
        # First identifier is mandatory for Vl
        first_id_token = self._peek()
        if not (first_id_token and first_id_token.type == "IDENTIFIER"):
            raise SyntaxError(f"Syntax error in line {first_id_token.line if first_id_token else 'N/A'}: IDENTIFIER expected at the start of variable list.")
        
        Vls:list[ASTNode] = [RandNode("IDENTIFIER", first_id_token.value)]  # Start with the first identifier
        self._consume(expected_type="IDENTIFIER")
        
        while self._peek() and self._peek().value == ",":
            self._consume(",")
            next_id_token = self._peek()
            if not (next_id_token and next_id_token.type == "IDENTIFIER"):
                line = next_id_token.line if next_id_token else "N/A"
                raise SyntaxError(f"Syntax error in line {line}: IDENTIFIER expected after ',' in variable list.")
            
            Vls.append(RandNode("IDENTIFIER", next_id_token.value))  # Append the next identifier
            self._consume(expected_type="IDENTIFIER") 
            
        return CommaNode(Vls)



'''

**Key Changes and Considerations:**

1.  **Class Structure:** The parsing logic is now within the `Parser` class.
2.  **Token Handling:**
    *   Uses `self.tokens` and `self.current_token_index` to manage the token stream.
    *   `_peek()` looks at the current token.
    *   `_consume()` advances the token stream and can validate the token's value or type. It replaces the `read()` function.
    *   Assumes your `Token` objects have `value`, `type`, and `line` attributes.
3.  **AST Building:**
    *   `self.ast_stack` (a Python list) is used to hold intermediate AST nodes.
    *   `_build_node(value, num_children)` creates a node (assuming a generic `ASTNode(value, children)` from `app.ast_nodes.py`) and pushes it to `self.ast_stack`. **You MUST ensure `app.ast_nodes.py` provides a suitable base `ASTNode` or you'll need to modify the `_build_node` calls in each parsing method to use your specific AST node classes.**
    *   Node values like `<ID:name>`, `<INT:value>`, `<STR:value>` are used for identifiers and literals.
4.  **Error Handling:** Uses `raise SyntaxError(...)` for parsing errors, which is more Pythonic than `print` and `exit`.
5.  **Function Naming:** Procedures are renamed (e.g., `procedure_E` to `_parse_E`) to indicate they are internal methods.
6.  **Comments:** Added comments explaining the grammar rule each method parses.
7.  **`_parse_Db` and `_parse_Vl`:** The logic for definitions, especially function forms vs. variable assignments, and tuple parameters, can be quite complex. I've tried to interpret the original intent and adapt it. You might need to refine this based on the exact semantics of RPAL your compiler supports. The original `Db` had a path for `Vl` directly for assignments like `x,y = E`, which is not explicitly handled in this refactoring as `Vl` is primarily used within `Vb` for function parameters. If RPAL supports `let x,y = (1,2) in ...`, you'd need to adjust `_parse_Db` or `_parse_D`.
8.  **`print_ast`:** Added a basic tree printing utility for debugging.
9.  **Assumptions on Lexer Output:** This parser assumes your lexer produces token types like `"IDENTIFIER"`, `"INTEGER"`, `"STRING"`, and keywords as their string value (e.g., token value `"let"` with type `"LET"` or just value `"let"` and type `"KEYWORD"` which then `_consume` checks by value). The code primarily checks `token.value` for keywords and `token.type` for generic categories. Adjust as needed.
'''