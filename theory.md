## theory facts:

## Lexical Analyzer = Regular Grammar + Input Characters → Tokens

## Parser = CFG + Tokens → Parse Tree
A parser takes the tokens from the Lexical Analyzer and checks whether those tokens follow the grammar rules of the language.
It builds a parse tree (or abstract syntax tree) based on those rules.






## TG and CFG. ##
The structure (shape) of the derivation tree is the same in TG and CFG.
But...

TG often shows only the translation output, not all the intermediate steps.
That’s why it looks shorter or more compact — because it focuses on the meaning, not just the syntax.

Think of it like this:
1. CFG Tree (Full syntax tree)
Shows:

css
Copy
Edit
E
├── E
│   └── i
├── +
└── T
    └── i
It includes every token and rule used in parsing.

2. TG Output (Translation tree or result)
Just gives you:

css
Copy
Edit
+
├── i
└── i
Cleaner, because it skips all the intermediate symbols and focuses on what the computation means (postfix or AST).


## parser:
top down parsing
recursive descent parsing methode