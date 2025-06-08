# RPAL Compiler

## Project Information
- **Course:** Programming Languages
- **Project:** RPAL Compiler Implementation
- **Students:**
    - Devinda Dilshan (220126M)
    - W.A.K. Indunil (220240G)

## Overview
This project is an implementation of a compiler for the RPAL (Right-reference Pedagogical Algorithmic Language) developed in Python. It includes a lexical analyzer, a recursive descent parser, Abstract Syntax Tree (AST) construction, AST to Standardized Tree (ST) conversion, and a CSE (Control Stack Environment) machine for program execution.

## How to Run

The compiler is executed from the command line using the `myrpal.py` script.

**Prerequisites:**
- Python 3.x
- `make` (optional, if using the Makefile for convenience) - Can be installed via Git for Windows (Git Bash), MinGW, Chocolatey (`choco install make`), or WSL on Windows.

**Execution Commands:**

1.  **Basic Execution:**
    To run an RPAL file (e.g., `your_file.rpal` located in the `testCodes` directory):
    ```bash
    python .\myrpal.py testCodes/your_file.rpal
    ```

2.  **View Abstract Syntax Tree (AST):**
    To execute and also display the Abstract Syntax Tree:
    ```bash
    python .\myrpal.py -ast testCodes/your_file.rpal
    ```

3.  **View Standardized Tree (ST):**
    To execute and also display the Standardized Tree:
    ```bash
    python .\myrpal.py -st testCodes/your_file.rpal
    ```

**Using the Makefile (Optional):**

If you have `make` installed and are in a compatible terminal (like Git Bash on Windows):

-   Run a specific file:
    ```bash
    make test FILE=testCodes/your_file.rpal
    ```
-   Run with AST output:
    ```bash
    make ast FILE=testCodes/your_file.rpal
    ```
-   Run with ST output:
    ```bash
    make st FILE=testCodes/your_file.rpal
    ```
-   Clean Python cache files:
    ```bash
    make clean
    ```
-   See all Makefile options:
    ```bash
    make help
    ```

## Key Components
- **Lexer (`app/lexer.py`):** Tokenizes RPAL source code.
- **Parser (`app/parser.py`):** Builds an Abstract Syntax Tree (AST) from tokens.
- **AST Nodes (`app/ast_nodes/`):** Classes representing language constructs, each with `standardize()`, `evaluate()`, and `print()` methods.
- **Standardization:** Converts the AST to a Standardized Tree (ST) for simpler evaluation.
- **CSE Machine:** Implemented via the `evaluate()` methods in AST nodes, managing environments and closures.
- **Node Registry (`app/ast_nodes/functions/node_registry.py`):** Manages built-in functions.

---
This README provides a quick guide to getting the RPAL compiler running and understanding its basic operation. For detailed design and implementation, please refer to the full `Report.md`.