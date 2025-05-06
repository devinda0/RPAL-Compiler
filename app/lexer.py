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

    def __init__(self, source_code):
        self.__source = source_code
        self.__tokens: list[Token] = []

    def __extract_identifier_or_keyword(self, start: int):
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
    

    def __extract_integer(self, start: int):
        end = start
        while end < len(self.__source) and self.__source[end] in self.__digits:
            end += 1
        token_value = self.__source[start:end]
        self.__tokens.append(Token(token_value, "INTEGER"))
        return end
    

    def __extract_operator(self, start: int):
        end = start
        while end < len(self.__source) and self.__source[end] in self.__operators:
            end += 1
        token_value = self.__source[start:end]
        self.__tokens.append(Token(token_value, "OPERATOR"))
        return end
    

    def __extract_string(self, start: int):
        end = start
        if self.__source[start] == '"':
            end += 1
            while end < len(self.__source) and self.__source[end] != '"':
                if self.__source[end] == "\\":
                    end += 2
                else:
                    end += 1
            token_value = self.__source[start + 1:end]
            self.__tokens.append(Token(token_value, "STRING"))
            end += 1
            return end
        else:
            raise ValueError("Invalid string literal")
        
    def __extract_punction(self, start: int):
        end = start
        if self.__source[start] in self.__punction:
            end += 1
            token_value = self.__source[start:end]
            self.__tokens.append(Token(token_value, "PUNCTION"))
            return end
        else:
            raise ValueError("Invalid punctuation")
        
    
    def __delete_comment(self, start: int):
        end = start
        while end < len(self.__source) and self.__source[end] != "\n":
            end += 1
        return end
    
    def tokenize(self):
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
