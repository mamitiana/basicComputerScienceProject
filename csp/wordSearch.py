from optparse import Option
from turtle import width
from typing import NamedTuple, List, Dict, Optional
from random import choice
from string import ascii_uppercase
from csp import CSP, Constraint

Grid= List[List[str]] #type alias for grids

class GridLocation(NamedTuple):
    row:int
    column: int

def generate_grid(rows:int, columns:int) -> Grid:
    return [[choice(ascii_uppercase) for c in range(columns)] for r in range(rows)  ]

def display_grid(grid: Grid)-> None:
    for row in grid:
        print("".join(row))

def generate_domain(word:str , grid:Grid) -> List[List[GridLocation]]:
    domain:List[List[GridLocation]] = []
    height:int = len(grid)
    width:int= len(grid[0])
    length:int= len(word)    
    
    for row in range(height):
        for col in range(width):
            columns:range = range(col, col+length+1)
            rows:range= range(row , row+length+1)
            if col+ length<=width:
                #left to right
                domain.append( [GridLocation(row , c) for c in columns ] )
                #diagonal
                if row+length <=height:
                    domain.append( [GridLocation(r, col + (r-row)) for r in rows] )
            if row + length <= height:
                #top to bottom
                domain.append([GridLocation(r , col) for r in rows])
                if col - length> 0:
                    domain.append([GridLocation(r , col - (r-row) ) for r in rows])
    return domain

class WordSearchConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words:List[str] = words

    def satisfied(self, assignement: Dict[str, List[GridLocation]]) -> bool:
        #if there is any duplicates, then there is an overlap
        all_locations= [locs for values in assignement.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)

if __name__=="__main__":
    grid:Grid= generate_grid(9,9)
    display_grid(grid)
    print("-"*30)
    words: List[str] = ["MATTHEW", "JOE", "MARY", "SARAH", "SALLY"]
    locations: Dict[str, List[List[GridLocation]]] = {}
    for word in words:
        locations[word] = generate_domain(word, grid)
    #print(locations)
    csp: CSP[str, List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()

    if solution is None:
        print("no sol")
    else:
        for word, grid_location in solution.items():
            if choice([True, False]):
                grid_location.reverse()
            for index , letter in enumerate(word):
                (row, col) = (grid_location[index].row , grid_location[index].column)
                grid[row][col] = letter
        display_grid(grid)