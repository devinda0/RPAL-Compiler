from .token import Token
# Assuming you have a generic Node class in ast_nodes.py
# If not, you'll need to create one or adapt _build_node and its calls.
# Example:
# class Node:
#     def __init__(self, value, children=None):
#         self.value = value
#         self.children = children if children is not None else []
#     def __repr__(self):
#         return f"Node({self.value}, {self.children})"
from .ast_nodes import ASTNode # Or your specific base/generic node class

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

    def _build_node(self, value: str, num_children: int):
        """Builds an AST node and pushes it onto the AST stack."""
        children = []
        for _ in range(num_children):
            if not self.ast_stack:
                raise Exception("Parser error: AST stack underflow during node construction.")
            children.insert(0, self.ast_stack.pop()) # Pop children in reverse order of parsing
        
        # This assumes a generic ASTNode(value, children_list) constructor.
        # Adapt this if your ast_nodes.py has different structures.
        node = ASTNode(value, children) 
        self.ast_stack.append(node)

    def parse(self):
        """Main parsing method. Starts parsing from the top-level rule."""
        if not self.tokens:
            # Handle empty token list if necessary, or let _peek handle it.
            # Depending on grammar, an empty token list might be a valid empty program or an error.
            # For many languages, it's an error or results in a specific "empty" AST node.
            # For now, let's assume an empty program is not valid and would be caught by _parse_E.
             pass

        self._parse_E() # Start with the top-level grammar rule E

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
            self._parse_D()
            self._consume("in")
            self._parse_E()
            self._build_node("let", 2)
        elif token.value == "fn":
            self._consume("fn")
            n = 0
            # Vb+ means one or more Vb
            while self._peek() and (self._peek().type == "IDENTIFIER" or self._peek().value == "("): 
                self._parse_Vb()
                n += 1
            if n == 0:
                err_token = self._peek()
                line = err_token.line if err_token else "N/A"
                raise SyntaxError(f"Syntax error in line {line}: At least one variable binding (IDENTIFIER or '(') expected after 'fn'")
            
            self._consume(".")
            self._parse_E()
            self._build_node("lambda", n + 1)
        else:
            self._parse_Ew()

    def _parse_Ew(self):
        """ Parses Ew.
        Ew -> T ('where' Dr)?
        """
        self._parse_T()
        token = self._peek()
        if token and token.value == "where":
            self._consume("where")
            self._parse_Dr()
            self._build_node("where", 2)  
        
    def _parse_T(self):     
        """ Parses T.
        T -> Ta (',' Ta)*
        """
        self._parse_Ta()
        n = 0
        while self._peek() and self._peek().value == ",":
            self._consume(",")
            self._parse_Ta()
            n += 1
        if n > 0:
            self._build_node("tau", n + 1)
        
    def _parse_Ta(self):  
        """ Parses Ta.
        Ta -> Tc ('aug' Tc)*
        """
        self._parse_Tc()
        while self._peek() and self._peek().value == "aug":
            self._consume("aug")
            self._parse_Tc()
            self._build_node("aug", 2)  
        
    def _parse_Tc(self):   
        """ Parses Tc.
        Tc -> B ('->' Tc '|' Tc)?
        """
        self._parse_B()
        token = self._peek()
        if token and token.value == "->":  
            self._consume("->")
            self._parse_Tc()
            self._consume("|")
            self._parse_Tc()
            self._build_node("->", 3)
            
    def _parse_B(self):
        """ Parses B.
        B -> Bt ('or' Bt)*
        """
        self._parse_Bt()
        while self._peek() and self._peek().value == "or":
            self._consume("or")
            self._parse_Bt()
            self._build_node("or", 2) 

    def _parse_Bt(self):    
        """ Parses Bt.
        Bt -> Bs ('&' Bs)*
        """
        self._parse_Bs()
        while self._peek() and self._peek().value == "&":
            self._consume("&")
            self._parse_Bs()
            self._build_node("&", 2)
        
    def _parse_Bs(self):
        """ Parses Bs.
        Bs -> 'not' Bp | Bp
        """
        token = self._peek()
        if token and token.value == "not":
            self._consume("not")
            self._parse_Bp()
            self._build_node("not", 1)
        else:
            self._parse_Bp()
        
    def _parse_Bp(self):           
        """ Parses Bp (Boolean with comparisons).
        Bp -> A (('gr' | '>') A | ('ge' | '>=') A | ... | 'ne' A)?
        """
        self._parse_A()
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
                self._parse_A()
                self._build_node(node_name, 2)

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
        
        self._parse_At()
        if is_negated:
            self._build_node("neg", 1) # Unary negation
            
        while self._peek() and (self._peek().value == "+" or self._peek().value == "-"):
            op_token = self._peek()
            if op_token.value == "+":
                self._consume("+")
                self._parse_At()
                self._build_node("+", 2)
            elif op_token.value == "-":
                self._consume("-")
                self._parse_At()
                self._build_node("-", 2)
    
    def _parse_At(self):
        """ Parses At (Arithmetic terms: *, /).
        At -> Af (('*' | '/') Af)*
        """
        self._parse_Af()
        while self._peek() and (self._peek().value == "*" or self._peek().value == "/"):
            op_token = self._peek()
            if op_token.value == "*":
                self._consume("*")
                self._parse_Af()
                self._build_node("*", 2)
            elif op_token.value == "/":
                self._consume("/")
                self._parse_Af()
                self._build_node("/", 2)

    def _parse_Af(self):    
        """ Parses Af (Arithmetic factors: exponentiation).
        Af -> Ap ('**' Af)?
        """
        self._parse_Ap()
        if self._peek() and self._peek().value == "**":     
            self._consume("**")
            self._parse_Af()
            self._build_node("**", 2)
 
    def _parse_Ap(self):
        """ Parses Ap (Atomic power operand, function application with @).
        Ap -> R ('@' <IDENTIFIER> R)* 
        """
        self._parse_R()
        while self._peek() and self._peek().value == "@":
            self._consume("@")
            id_token = self._peek()
            if id_token and id_token.type == "IDENTIFIER":
                # Build node for the identifier being applied
                self._build_node(f"<ID:{id_token.value}>", 0)
                self._consume(expected_type="IDENTIFIER")
                self._parse_R()
                self._build_node("@", 3) # Pops R, ID, and the R before @           
            else:
                err_token = self._peek()
                line = err_token.line if err_token else "N/A"
                raise SyntaxError(f"Syntax error in line {line}: IDENTIFIER expected after '@'")
    
    def _parse_R(self):
        """ Parses R (Repeated applications/atoms).
        R -> Rn (Rn)* 
        """
        self._parse_Rn()
        # Check if next token can start an Rn (for function application)
        while self._peek() and \
              (self._peek().type in ["IDENTIFIER", "INTEGER", "STRING"] or \
               self._peek().value in ["true", "false", "nil", "(", "dummy"]): 
            self._parse_Rn()
            self._build_node("gamma", 2) # Represents function application

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
            self._build_node(f"<ID:{value}>", 0)
        elif token.type == "INTEGER":
            self._consume(expected_type="INTEGER")
            self._build_node(f"<INT:{value}>", 0)
        elif token.type == "STRING":
            self._consume(expected_type="STRING")
            self._build_node(f"<STR:{value}>", 0)
        elif value in ["true", "false", "nil", "dummy"]:
            self._consume(value)
            # Standardize node names for keywords if needed, e.g., "true" instead of "<true>"
            self._build_node(value, 0) # Or self._build_node(f"<{value}>", 0) if you prefer
        elif value == "(":
            self._consume("(")
            self._parse_E()
            self._consume(")")
            # No specific node for parentheses; the structure of E is preserved.
        else:
            raise SyntaxError(f"Syntax error in line {token.line}: Unexpected token '{value}'. Expected IDENTIFIER, INTEGER, STRING, keyword, or '('.")

    def _parse_D(self):
        """ Parses D (Definitions).
        D -> Da ('within' D)?
        """
        self._parse_Da()
        if self._peek() and self._peek().value == "within":
            self._consume("within")
            self._parse_D()
            self._build_node("within", 2)
    
    def _parse_Da(self):
        """ Parses Da.
        Da -> Dr ('and' Dr)*
        """
        self._parse_Dr()
        n = 0
        while self._peek() and self._peek().value == "and":
            self._consume("and")
            self._parse_Dr()
            n += 1
        if n > 0:  
            self._build_node("and", n + 1)
    
    def _parse_Dr(self):
        """ Parses Dr.
        Dr -> 'rec' Db | Db
        """
        if self._peek() and self._peek().value == "rec":
            self._consume("rec")
            self._parse_Db()
            self._build_node("rec", 1)
        else:
            self._parse_Db()
    
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
            self._parse_D()
            self._consume(")")
            # Parenthesized definition, D's node is already on stack.
        elif token.type == "IDENTIFIER":
            identifier_node_value = f"<ID:{token.value}>"
            self._consume(expected_type="IDENTIFIER")
            # We push the identifier now, it will be a child of 'function_form' or '='
            self._build_node(identifier_node_value, 0) 

            # Check if it's a function form (IDENTIFIER Vb+ = E) or simple assignment (IDENTIFIER = E)
            # Vb starts with IDENTIFIER or '('. If next is '=', it's simple assignment.
            # If next is IDENTIFIER or '(', it's function form.
            
            # This part needs to distinguish between `f x = E` and `f = E`
            # The original code structure for Db was a bit complex.
            # Let's try to simplify based on common patterns.
            
            # If next is '=' directly, it's a simple var assignment.
            # If next is Vb (IDENTIFIER or '('), it's a function.
            
            n_vbs = 0
            # Look ahead for Vb+
            # A Vb is an IDENTIFIER or '(' ... ')'
            # This loop collects Vbs for function_form
            while self._peek() and (self._peek().type == "IDENTIFIER" or self._peek().value == "("):
                self._parse_Vb()
                n_vbs += 1

            if self._peek() and self._peek().value == "=":
                self._consume("=")
                self._parse_E()
                if n_vbs > 0: # It was f Vb+ = E
                    # Children: E, Vb_n, ..., Vb_1, f_identifier
                    self._build_node("function_form", n_vbs + 2) 
                else: # It was f = E
                    # Children: E, f_identifier
                    self._build_node("=", 2)
            else:
                err_token = self._peek()
                line = err_token.line if err_token else "N/A"
                # If n_vbs > 0 but no '=', it's an error.
                # If n_vbs == 0 and no '=', it means IDENTIFIER was followed by something unexpected.
                if n_vbs > 0:
                    raise SyntaxError(f"Syntax error in line {line}: '=' expected after function parameters.")
                else: # This case means IDENTIFIER was not followed by Vb or '='.
                      # This might be an incomplete definition or a different construct not covered by Db.
                      # The original code's Db logic for IDENTIFIER was:
                      # elif tokens[0].type == "<IDENTIFIER>":
                      #   read(value)
                      #   build_tree("<ID:" + value + ">", 0)  
                      #   if tokens[0].content in [",", "="]:  // This implies Vl for simple assignment
                      #       procedure_Vl() // This seems to be for tuple assignment like x,y = E
                      #       read("=")
                      #       procedure_E()
                      #       build_tree("=", 2)
                      #   else: // This is for function form
                      #       ... procedure_Vb() ... build_tree("function_form", n + 2)
                      # This suggests Vl might be for multiple assignment targets, which is not explicitly in Db here.
                      # For now, we assume Db is either `ID Vb* = E` or `( D )`.
                      # If `Vl` is for `x,y,z = E`, that's a different rule.
                      # The current logic handles `ID = E` and `ID Vb+ = E`.
                    raise SyntaxError(f"Syntax error in line {line}: '=' or function parameters expected after identifier in definition.")
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
            self._build_node(f"<ID:{token.value}>", 0)     
        elif token.value == "(":
            self._consume("(")
            # Check if next is ')' for an empty tuple '()' or if it's a Vl
            if self._peek() and self._peek().value == ")":
                self._consume(")")
                self._build_node("()", 0) # Node for empty parameter tuple
            elif self._peek() and self._peek().type == "IDENTIFIER": 
                # This indicates the start of Vl
                self._parse_Vl() # Vl will build its own node(s)
                self._consume(")")
                # If Vl builds a single node for the list, that node is already on stack.
                # If Vl builds multiple ID nodes, they are on stack.
                # The original `build_tree(",", n+1)` in Vl suggests it creates a list node.
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
            line = first_id_token.line if first_id_token else "N/A"
            raise SyntaxError(f"Syntax error in line {line}: IDENTIFIER expected in variable list.")
        
        self._consume(expected_type="IDENTIFIER")
        self._build_node(f"<ID:{first_id_token.value}>", 0)    
        n_additional_ids = 0
        
        while self._peek() and self._peek().value == ",":
            self._consume(",")
            next_id_token = self._peek()
            if not (next_id_token and next_id_token.type == "IDENTIFIER"):
                line = next_id_token.line if next_id_token else "N/A"
                raise SyntaxError(f"Syntax error in line {line}: IDENTIFIER expected after ',' in variable list.")
            
            self._consume(expected_type="IDENTIFIER")
            self._build_node(f"<ID:{next_id_token.value}>", 0)    
            n_additional_ids += 1
            
        if n_additional_ids > 0:
            # Children are: ID_last, ..., ID_second, ID_first
            self._build_node(",", n_additional_ids + 1) # Build a tuple/list like node

    # --- Utility for printing the tree (optional) ---
    def _print_tree_recursive(self, node, prefix="", is_last=True):
        """ Helper for printing the tree. """
        if node is None: return
        print(prefix + ("└── " if is_last else "├── ") + str(node.value))
        
        children = node.children if hasattr(node, 'children') and node.children else []
        
        for i, child in enumerate(children):
            new_prefix = prefix + ("    " if is_last else "│   ")
            self._print_tree_recursive(child, new_prefix, i == len(children) - 1)

    def print_ast(self, root_node):
        """ Prints the AST in a tree-like format. """
        if root_node:
            self._print_tree_recursive(root_node)
        else:
            print("AST is empty or not generated.")

# Example Usage (typically in your main.py or a test file):
# from app.lexer import Lexer
# from app.parser import Parser
#
# source = "let x = 10 in x + 5"
# lexer = Lexer(source)
# tokens = lexer.tokenize()
#
# parser = Parser(tokens)
# try:
#     ast_root = parser.parse()
#     print("Parsing successful!")
#     parser.print_ast(ast_root)
# except SyntaxError as e:
#     print(e)
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")

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