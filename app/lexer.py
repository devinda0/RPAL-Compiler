from app.token import Token

class Lexer:
    __letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    __digits = "0123456789"
    __operators = "+-*<>&.@:=~|$!#%^_[]{}?"  # ' , " , / are not included
    __whitespace = " \t\n\r"
    __punction = ",;()"
    __keywords = {
        "let": "LET",
        "in" : "IN",
        "fn" : "FN",
        "where" : "WHERE",
        "aug" : "AUG",
        "or" : "OR",
        "not": "NOT",
        "gr" : "GR",
        "ge" : "GE",
        "ls" : "LS",
        "le" : "LE",
        "eq" : "EQ",
        "ne" : "NE",
        "true" : "TRUE",
        "false" : "FALSE",
        "nil" : "NIL",
        "dummy" : " DUMMY",
        "within" : "WITHIN",
        "and" : "AND",
        "rec" : "REC",
    }

    def __init__(self, source_code): # Initializes the lexer with the source code.
        self.__source = source_code
        self.__tokens: list[Token] = []

    def __extract_identifier_or_keyword(self, start: int): # Extracts an identifier or a keyword token.
        end = start
        while end < len(self.__source) and (self.__source[end] in self.__letters or \
                                             self.__source[end] in self.__digits or self.__source[end] == "_"):
            end += 1
        token_value = self.__source[start:end]
        if token_value in self.__keywords:
            token_type = self.__keywords[token_value]
        else:
            token_type = "IDENTIFIER"
        self.__tokens.append(Token(token_value, token_type))
        return end
    

    def __extract_integer(self, start: int): # Extracts an integer token.
        end = start
        while end < len(self.__source) and self.__source[end] in self.__digits:
            end += 1
        token_value = self.__source[start:end]
        self.__tokens.append(Token(token_value, "INTEGER"))
        return end
    

    def __extract_operator(self, start: int): # Extracts an operator token.
        end = start
        while end < len(self.__source) and self.__source[end] in self.__operators:
            end += 1
        token_value = self.__source[start:end]
        self.__tokens.append(Token(token_value, "OPERATOR"))
        return end
    

    def __extract_string(self, start: int): # Extracts a string literal token.
        end = start
        extracted_string = ""
        if self.__source[start] == '"':
            end += 1
            while end < len(self.__source) and self.__source[end] != '"':
                if self.__source[end] == "\\":
                    end += 1
                    if end < len(self.__source):
                        if self.__source[end] == "n":
                            extracted_string += "\n"
                        elif self.__source[end] == "t":
                            extracted_string += "\t"
                        elif self.__source[end] == "\\":
                            extracted_string += "\\"
                        elif self.__source[end] == '"':
                            extracted_string += '"'
                        else:
                            extracted_string += self.__source[end]
                else:
                    extracted_string += self.__source[end]
                end += 1
            self.__tokens.append(Token(extracted_string, "STRING"))
            end += 1
            return end
        else:
            raise ValueError("Invalid string literal")
        
    def __extract_punction(self, start: int): # Extracts a punctuation token.
        end = start
        if self.__source[start] in self.__punction:
            end += 1
            token_value = self.__source[start:end]
            self.__tokens.append(Token(token_value, "PUNCTION"))
            return end
        else:
            raise ValueError("Invalid punctuation")
        
    
    def __delete_comment(self, start: int): # Skips over a single-line comment.
        end = start
        while end < len(self.__source) and self.__source[end] != "\n":
            end += 1
        return end
    
    def tokenize(self): # Processes the source code and returns a list of tokens.
        index = 0
        while index < len(self.__source):
            char = self.__source[index]
            if char in self.__whitespace:
                index += 1
            elif char in self.__letters:
                index = self.__extract_identifier_or_keyword(index)
            elif char in self.__digits:
                index = self.__extract_integer(index)
            elif char in self.__operators:
                index = self.__extract_operator(index)
            elif char == '"':
                index = self.__extract_string(index)
            elif char in self.__punction:
                index = self.__extract_punction(index)
            elif char == "/":
                if index + 1 < len(self.__source) and self.__source[index + 1] == "/":
                    index = self.__delete_comment(index)
                else:
                    raise ValueError("Invalid comment")
            else:
                raise ValueError(f"Invalid character: {char}")
        return self.__tokens

  

'''The lexer.py file defines a `Lexer` class. This class is responsible for taking a string of source code and breaking it down into a list of "tokens". Think of tokens as the basic building blocks or "words" of the programming language.

The lexer scans the input character by character and groups them into meaningful units like:
-   **Keywords**: `let`, `in`, `fn`, etc.
-   **Identifiers**: Variable names like `x`, `myVar`.
-   **Integers**: Numbers like `10`, `0`, `123`.
-   **Operators**: `+`, `-`, `*`, `=`, `gr`, `ge`, etc.
-   **Strings**: Text enclosed in double quotes like `"hello"`.
-   **Punctuation**: `(`, `)`, `,`, `;`.

It also handles:
-   Skipping **whitespace** (spaces, tabs, newlines).
-   Ignoring **comments** (lines starting with ).

**Intuitive Explanation:**

Imagine you're reading a sentence. A lexer does something similar for code. It doesn't understand the *meaning* of the sentence (that's the parser's job later), but it can identify the individual words and punctuation marks.

**Simple Example:**

If the input source code is:
```
let answer = 42 // this is the answer
```

The `Lexer` would process this and produce a list of `Token` objects, something like this (ignoring line/column numbers for simplicity here):

1.  `Token("let", "LET")`
2.  `Token("answer", "IDENTIFIER")`
3.  `Token("=", "OPERATOR")`
4.  `Token("42", "INTEGER")`

The comment `// this is the answer` would be ignored. Each of these `Token` objects would be an instance of the `Token` class defined in token.py.'''