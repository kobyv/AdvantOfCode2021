* The assembly instructions were saved to `assembly.txt`.
* Run `python assembly2d.py | pbcopy` (or the equivalent `xsel` in Linux), and paste into Excel.
* You'll see 13 iterations, 18 instructions each.
  All iterations are the same except for 3 lines (divide by 26 or not, modulo offset, output offset). These parameters are copied into `solve.py`, `rounds` table.
* Run `solve.py` to get all possible solutions from lowest to highest.