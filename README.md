# RPAL-Compiler 🧠⚙️

This project is a compiler for **RPAL (Right-reference Pure Applicative Language)** written in Python. It takes RPAL source code as input, lexes and parses it, builds an abstract syntax tree (AST), performs semantic analysis, and generates code.

## 🧩 Project Structure

```bash
RPAL-COMPILER/
├── app/
│   ├── ast_nodes/                  # Contains AST node definitions
│   │   ├── base.py                 # Base class for AST nodes
│   │   ├── bracket_node.py         # Represents bracket nodes
│   │   ├── comma_node.py           # Represents comma-separated nodes
│   │   ├── equal_node.py           # Represents equality expressions
│   │   ├── fcn_form_node.py        # Represents function forms
│   │   ├── gamma_node.py           # Represents function application nodes
│   │   ├── lambda_node.py          # Represents lambda expressions
│   │   ├── let_node.py             # Represents 'let' expressions
│   │   ├── operator_node.py        # Represents operator expressions
│   │   ├── rand_node.py            # Represents literals and identifiers
│   │   ├── rec_node.py             # Represents recursive definitions
│   │   ├── tau_node.py             # Represents tuples
│   │   ├── where_node.py           # Represents 'where' expressions
│   │   ├── within_node.py          # Represents 'within' expressions
│   │   ├── ystar_node.py           # Represents Y* combinator
│   │   └─- functions/              # Contains built-in functions
│   │       ├── concact.py          # Concatenation function
│   │       ├── is_function.py      # Checks if a value is a function
│   │       ├── is_integer.py       # Checks if a value is an integer
│   │       ├── is_string.py        # Checks if a value is a string
│   │       ├── is_truthvalue.py    # Checks if a value is a truth value
│   │       ├── is_tuple.py         # Checks if a value is a tuple
│   │       ├── node_registry.py    # Registry for AST nodes
│   │       ├── order.py            # Order function for tuples
│   │       ├── print.py            # Print function
│   │       ├── stem.py             # Stem function
│   │       └─- stern.py            # Stern function
│   ├── lexer.py                    # Lexical analyzer for tokenizing input
│   ├── parser.py                   # Syntactic parser to build the AST
│   ├── token.py                    # Token definitions
│   ├── main.py                     # Entry point for the compiler
│   └── __init__.py                 # Package initializer
│
├── tests/                          # Unit tests for the compiler
│   ├── test_lexer.py               # Tests for lexical analysis
│   ├── test_parser.py              # Tests for parsing
│   └─- test_interpreter.py         # Tests for interpreter functionality
│
├── test.rpal                       # Example RPAL source code
├── theory.md                       # RPAL theory and concepts
├── .gitignore                      # Git ignore file
└── README.md                       # Project documentation
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
python3 -m app.main <input.rpal>
```

### Optional Arguments

- `-st`: Prints the standardized tree.
- `-ast`: Prints the abstract syntax tree.


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


