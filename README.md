# RPAL-Compiler 🧠⚙️

This project is a compiler for **RPAL (Right-reference Pure Applicative Language)** written in Python. It takes RPAL source code as input, lexes and parses it, builds an abstract syntax tree (AST), performs semantic analysis, and generates code.

## 🧩 Project Structure

```bash
RPAL-COMPILER/
├── app/
│ ├── ast_nodes.py # Defines AST node structures
│ ├── code_generator.py # Translates AST to target code
│ ├── lexer.py # Lexical analyzer for tokenizing input
│ ├── main.py # Entry point for the compiler
│ ├── parser.py # Syntactic parser to build the AST
│ ├── semantic_analyzer.py # Checks semantic rules
│ ├── token.py # Token definitions
│ └── init.py
│
├── tests/
│ ├── test_code_generator.py
│ ├── test_lexer.py
│ ├── test_parser.py
│ └── test_semantic.py 
│
├── .gitignore
└── README.md
```



## 🚀 How to Run

Make sure you have Python 3 installed. Then:

1. Clone the repo:
```bash
git clone https://github.com/your-username/rpal-compiler.git
cd rpal-compiler
```

2. Run the compiler:
```bash
python3 app/main.py input.rpal
```


## 🛠️ Features

Lexical Analysis — Converts source code into tokens.
Parsing — Constructs an AST from token stream.
Semantic Analysis — Ensures type rules and bindings.
Code Generation — Outputs intermediate or target code.

## 📦 Dependencies

This project uses pure Python. No external libraries are required.

## 🧪 Testing

Unit tests are included for all major components:

- Lexer
- Parser
- Code Generator
- Semantic Analyzer

Run them using:
```bash
python3 -m unittest discover tests
```