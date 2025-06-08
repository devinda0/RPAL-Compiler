# Makefile for RPAL Compiler project

# Variables
PYTHON ?= python  # Allows overriding with 'make PYTHON=python3'
RPAL_SCRIPT = myrpal.py
TEST_DIR = testCodes
# Assuming test1.rpal is in the root directory as per your attachment.
# If it's in testCodes, change to $(TEST_DIR)/test1.rpal
DEFAULT_FILE ?= test1.rpal

# Phony targets (targets that are not actual files)
.PHONY: all run test ast st default_run default_ast default_st clean help

# Default target: Print help
all: help

# Help target to explain usage
help:
    @echo "Makefile for RPAL Compiler"
    @echo "--------------------------"
    @echo "Usage: make [target] [VARIABLE=value]"
    @echo ""
    @echo "Targets:"
    @echo "  run FILE=<file> [OPTS=<opts>]  - Run the RPAL script on <file> with optional <opts>."
    @echo "                                   Example: make run FILE=$(TEST_DIR)/my_test.rpal OPTS=\"-ast\""
    @echo "  test FILE=<file>               - Run the RPAL script on <file> (no extra flags)."
    @echo "                                   Example: make test FILE=$(TEST_DIR)/my_test.rpal"
    @echo "  ast FILE=<file>                - Run with -ast flag on <file>."
    @echo "                                   Example: make ast FILE=$(TEST_DIR)/my_test.rpal"
    @echo "  st FILE=<file>                 - Run with -st flag on <file>."
    @echo "                                   Example: make st FILE=$(TEST_DIR)/my_test.rpal"
    @echo "  default_run                    - Run on the default test file ($(DEFAULT_FILE))."
    @echo "  default_ast                    - Run with -ast on the default test file ($(DEFAULT_FILE))."
    @echo "  default_st                     - Run with -st on the default test file ($(DEFAULT_FILE))."
    @echo "  clean                          - Remove __pycache__ directories and .pyc files."
    @echo "  help                           - Show this help message."
    @echo ""
    @echo "Variables:"
    @echo "  FILE=<path>                    - Path to the RPAL file to process."
    @echo "  OPTS=\"<options>\"             - Optional flags for the 'run' target (e.g., \"-ast -st\")."
    @echo "  PYTHON=<interpreter>           - Python interpreter (default: $(PYTHON))."
    @echo "  DEFAULT_FILE=<path>            - Default RPAL file (default: $(DEFAULT_FILE))."

# Generic run target
run:
    @if [ -z "$(FILE)" ]; then \
        echo "Error: FILE variable must be set for 'run' target."; \
        echo "Usage: make run FILE=<path_to_rpal_file> [OPTS=<options>]"; \
        exit 1; \
    fi
    $(PYTHON) $(RPAL_SCRIPT) $(OPTS) $(FILE)

# Test target (runs without special flags)
test:
    @if [ -z "$(FILE)" ]; then \
        echo "Error: FILE variable must be set for 'test' target."; \
        echo "Usage: make test FILE=<path_to_rpal_file>"; \
        exit 1; \
    fi
    $(PYTHON) $(RPAL_SCRIPT) $(FILE)

# AST target
ast:
    @if [ -z "$(FILE)" ]; then \
        echo "Error: FILE variable must be set for 'ast' target."; \
        echo "Usage: make ast FILE=<path_to_rpal_file>"; \
        exit 1; \
    fi
    $(PYTHON) $(RPAL_SCRIPT) -ast $(FILE)

# Standardized Tree target
st:
    @if [ -z "$(FILE)" ]; then \
        echo "Error: FILE variable must be set for 'st' target."; \
        echo "Usage: make st FILE=<path_to_rpal_file>"; \
        exit 1; \
    fi
    $(PYTHON) $(RPAL_SCRIPT) -st $(FILE)

# Targets for running with the default file
default_run:
    @echo "Running default file: $(DEFAULT_FILE)"
    $(PYTHON) $(RPAL_SCRIPT) $(DEFAULT_FILE)

default_ast:
    @echo "Running default file with -ast: $(DEFAULT_FILE)"
    $(PYTHON) $(RPAL_SCRIPT) -ast $(DEFAULT_FILE)

default_st:
    @echo "Running default file with -st: $(DEFAULT_FILE)"
    $(PYTHON) $(RPAL_SCRIPT) -st $(DEFAULT_FILE)

# Clean up Python cache files (works cross-platform)
clean:
    @echo "Cleaning up Python cache files..."
    $(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__') if p.is_dir()]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc') if p.is_file()]"
    @echo "Cleanup complete."
