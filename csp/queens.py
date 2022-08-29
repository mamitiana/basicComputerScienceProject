from tkinter.messagebox import NO
from typing import Dict, List, Optional
from csp import CSP , Constraint

class QueensConstraint(Constraint[int, int]):
    def __init__(self, columns : List[int]) -> None:
        super().__init__(columns)
        self.columns:List[int] = columns

    def satisfied(self, assignement: Dict[int, int]) -> bool:
        # q1c 1 columns , q1r queen 1 ron
        for q1c, q1r in assignement.items():
            #q2c queen 2 columns
            for q2c in range(q1c+1 , len(self.columns) +1 ):
                if q2c in assignement:
                    q2r:int = assignement[q2c] # queen 2 row
                    if q1r == q2r:
                        return False ##same row
                    if abs(q1r-q2r) == abs(q1c - q2c): # same diag
                        return False
        return True # no conflict
    pass
if __name__=="__main__":
    columns: List[int] = [i for i in range(1, 8)]
    rows : Dict[int, List[int]] = {}
    for col in columns:
        rows[col] = [ i for i in range(1, 8) ]
    csp: CSP[int ,int ]= CSP(columns , rows)
    csp.add_constraint(QueensConstraint(columns))
    solution: Optional[Dict[int, int]] = csp.backtracking_search()

    if solution in None:
        print("no solution")

    else: 
        print("solution")