# Q4 - Use pdb breakpoints inside a loop and inspect variable values.
# Q4 - Use pdb breakpoints inside a loop and inspect variable values.

SAMPLE_NUMBERS = [4, 8, 15, 16, 23, 42]


def inspect_loop_with_pdb(numbers) -> int:
    """Calculate cumulative sum to demonstrate interactive loop debugging."""
    total: int = 0
    for index, number in enumerate(numbers):
        total += number
    return total


if __name__ == "__main__":
    print("Uncomment the breakpoint() line inside inspect_loop_with_pdb() to try it.")
    total: int = inspect_loop_with_pdb(SAMPLE_NUMBERS)
    print(f"Total calculated: {total}")
# ==============================================================================
# PDB DEBUGGING TERMINAL SESSION LOG
# ==============================================================================

# PS C:\Users\Gourav yadav\git-assignment\Gourav_python_training> python -m pdb python_advance\testing_debugging\pdb_loop_inspection.py
# > c:\users\gourav yadav\git-assignment\gourav_python_training\python_advance\testing_debugging\pdb_loop_inspection.py(3)<module>()
# -> SAMPLE_NUMBERS = [4, 8, 15, 16, 23, 42]
# (Pdb) b 10
# Breakpoint 1 at c:\users\gourav yadav\git-assignment\gourav_python_training\python_advance\testing_debugging\pdb_loop_inspection.py:10
# (Pdb) c
# Uncomment the breakpoint() line inside inspect_loop_with_pdb() to try it.
# > c:\users\gourav yadav\git-assignment\gourav_python_training\python_advance\testing_debugging\pdb_loop_inspection.py(10)inspect_loop_with_pdb()
# -> total += number
# (Pdb) p index
# 0
# (Pdb) p number
# 4
# (Pdb) p total
# 0
# (Pdb) c
# > c:\users\gourav yadav\git-assignment\gourav_python_training\python_advance\testing_debugging\pdb_loop_inspection.py(10)inspect_loop_with_pdb()
# -> total += number
# (Pdb) p index 
# 1
# (Pdb) p number
# 8
# (Pdb) p total 
# 4
# (Pdb) c
# > c:\users\gourav yadav\git-assignment\gourav_python_training\python_advance\testing_debugging\pdb_loop_inspection.py(10)inspect_loop_with_pdb()
# -> total += number
# (Pdb) p index 
# 2
# (Pdb) p number
# 15
# (Pdb) p total
# 12
# (Pdb) c
# > c:\users\gourav yadav\git-assignment\gourav_python_training\python_advance\testing_debugging\pdb_loop_inspection.py(10)inspect_loop_with_pdb()
# -> total += number
# (Pdb) q
# PS C:\Users\Gourav yadav\git-assignment\Gourav_python_training> 