"""
Assignment Q3: Create a function with a logical bug and use pdb to identify the issue.
"""


def calculate_twenty_percent_discount_buggy(price) -> float:
    """
    Calculate the final price after a 20% discount.

    BUG: Multiplying by 0.20 calculates only the discount amount ($20),
    but we accidentally return it as the final price!
    """
    final_price = price * 0.20
    return final_price


def calculate_twenty_percent_discount_fixed(price) -> float:
    """Correctly calculates the final price after a 20% discount."""
    discount_amount = price * 0.20
    final_price = price - discount_amount
    return final_price


if __name__ == "__main__":
    test_price = 100.0

    buggy_result = calculate_twenty_percent_discount_buggy(test_price)
    print(f"Buggy final price: ${buggy_result} (Expected: $80.0)")

    correct_result = calculate_twenty_percent_discount_fixed(test_price)
    print(f"Correct final price: ${correct_result}")
    
    
# ==============================================================================
# PDB DEBUGGING TERMINAL SESSION LOG
# ==============================================================================
# PS C:\Users\Gourav yadav\git-assignment\Gourav_python_training> python -m pdb python_advance\testing_debugging\buggy_percent_function.py
# > c:\users\gourav yadav\git-assignment\gourav_python_training\python_advance\testing_debugging\buggy_percent_function.py(1)<module>()
# -> """
# (Pdb) b 14
# Breakpoint 1 at c:\users\gourav yadav\git-assignment\gourav_python_training\python_advance\testing_debugging\buggy_percent_function.py:14
# (Pdb) c
# > c:\users\gourav yadav\git-assignment\gourav_python_training\python_advance\testing_debugging\buggy_percent_function.py(14)calculate_twenty_percent_discount_buggy()
# -> return final_price
# (Pdb) p price
# 100.0
# (Pdb) p final_price
# 20.0
# (Pdb) q
# PS C:\Users\Gourav yadav\git-assignment\Gourav_python_training> 