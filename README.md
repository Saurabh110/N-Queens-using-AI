# N-Queens-using-AI
Solved the N-Queens problem using Backtracking search with forward checking and Maintaining Arc Consistency approach

## Description

The N Queen is the problem of placing N chess queens on an N×N chessboard so that no two queens attack each other. For example, following is a solution for 4 Queen problem.  
![4x4 N-Queens](https://miro.medium.com/max/468/1*eJQ8xMUJ9WDX_2-7ZMWw3g.png)

## Executaion  

```bash
NQueens.py ALG N CFile RFile
```
where _ALG_ is one of **FOR** or **MAC** representing **Backtracking Search with Forward Checking** or **Maintaining Arc Consistency** respectively. _N_ represents the number of rows and columns in the chessboard as well as the **number of queens** to be assigned. _CFile_ is an output filename for your constraint problem. And _RFile_ is an output file for your results.


## Implementation

* This code attempts the N-queens problem row by row, the domain values of the queen represents the column numbers where that queen can be placed. Since, the domains(variable name in the code is → all_dom) are stored as 2-D list, the domains for the Queen1 are stored in the 0
th index in the domains list, for Queen2 on 1st index of domains, and so on.  
* Code begins by calling backtracking function on Queen1 for the 1st value in its domain. Then domains for next remaining queens is reduced using FOR (forward checking) and AC3 (if MAC is specified). These reduced domains are checked, if found empty, function returns false
otherwise it calls the backtracking function on the next queen passing the reduced domains.  
* The outputs are printed in the files passed while calling the program.
