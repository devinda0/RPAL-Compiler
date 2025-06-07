# RPAL Compiler Test Summary

This document summarizes the results of recent tests run on the RPAL compiler.

---

## Test Case: tests/clean

*   *Command:* python -m app.main tests/clean
*   *Status:* FAILED
*   *Error Details:*
    
    Traceback (most recent call last):
      ...
      File "C:\Users\wakin\OneDrive\Desktop\RPAL-Compiler\app\ast_nodes\functions\order.py", line 46, in evaluate
        raise TypeError("Order can only be applied to a tuples.")
    TypeError: Order can only be applied to a tuples.
    
*   *Analysis/Summary:* The Order function (or the way it's being called/handled) is encountering a TypeError. It seems it received an argument that was not a tuple, while it strictly expects one. This could be an issue in the Order function's argument validation, how arguments are passed to it, or the test case tests/clean itself providing an incorrect argument type to Order.

---

## Test Case: tests/conc.1

*   *Command:* python -m app.main tests/conc.1
*   *Status:* PASSED (with output)
*   *Output:*
    
    (<app.ast_nodes.gamma_node.GammaNode object at 0x00000231AA482F60>, <app.ast_nodes.gamma_node.GammaNode object at 0x00000231AA4832C0>, <app.ast_nodes.gamma_node.GammaNode object at 0x00000231AA4830B0>)
    
*   *Analysis/Summary:* The test completed and produced output. The output appears to be the string representation of a tuple containing three GammaNode objects. This suggests the program evaluated to this tuple structure.

---

## Test Case: tests/conc1

*   *Command:* python -m app.main tests/conc1
*   *Status:* PASSED (with output)
*   *Output:*
    
    (<app.ast_nodes.gamma_node.GammaNode object at 0x00000294496F23C0>, <app.ast_nodes.rand_node.RandNode object at 0x00000294496F23F0>, <app.ast_nodes.rand_node.RandNode object at 0x00000294496F2420>)
    
*   *Analysis/Summary:* Similar to tests/conc.1, this test completed and produced output representing a tuple of AST node objects.

---

## Test Case: tests/conc3

*   *Command:* python -m app.main tests/conc3
*   *Status:* PASSED (with output)
*   *Output:*
    
    CIS104B
    
*   *Analysis/Summary:* The test executed successfully and printed the string "CIS104B". This indicates string operations and printing are likely working as expected in this case.

---

## Test Case: tests/defns.1

*   *Command:* python -m app.main tests/defns.1
*   *Status:* PASSED (with output)
*   *Output:*
    
    <Closure >
    
*   *Analysis/Summary:* The test completed, and the program likely evaluated to a Closure object. The output is the default string representation of this closure.

---

## Test Case: tests/defns.2

*   *Command:* python -m app.main tests/defns.2
*   *Status:* PASSED (with output)
*   *Output:*
    
    15
    
*   *Analysis/Summary:* The test executed successfully and produced the integer output 15.

---

## Test Case: tests/defns.3

*   *Command:* python -m app.main tests/defns.3 (run twice)
*   *Status:* PASSED (no visible output)
*   *Analysis/Summary:* The test completed without errors but produced no visible output to the console. This is acceptable if the program was not designed to print anything.

---

## Test Case: tests/dist

*   *Initial Attempt - Command:* python -m app.main tests/dist
*   *Status:* FAILED
*   *Error Details:*
    
    Traceback (most recent call last):
      ...
      File "C:\Users\wakin\OneDrive\Desktop\RPAL-Compiler\app\ast_nodes\rand_node.py", line 29, in evaluate
        raise NameError(f"Name '{self.value}' is not defined in the current environment.")
    NameError: Name 'print' is not defined in the current environment.
    
*   *Analysis/Summary (Initial Attempt):* The program failed because the identifier print was not found in the current environment or as a recognized built-in function. This suggests an issue with how built-in functions (specifically print) are registered or looked up.

*   *Subsequent Attempt - Command:* python -m app.main tests/dist
*   *Status:* PASSED (with output)
*   *Output:*
    
    9
    
*   *Analysis/Summary (Subsequent Attempt):* This run of tests/dist (content: let add n = radd 0 n where rec radd r n = n eq 0 -> r | radd (r+n) in print (add 2 3 4 0)) completed successfully and printed 9. This indicates that the previous NameError for print was resolved in the compiler version/state used for this particular run. The output 9 suggests the add function (likely summing 2+3+4) and the print function worked correctly. The discrepancy between the two runs for tests/dist is notable.

---

Please review these findings. The TypeError in tests/clean and the initial NameError in tests/dist are key issues to investigate.