from enum import Enum
from os import stat
from re import T
from tkinter.messagebox import NO
from turtle import distance
from typing import Set, TypeVar, Generic, List, NamedTuple, Callable, Optional
import random
from math import sqrt
from unittest.mock import patch

from genericsearch import Node, astar, bfs, dfs, node2path
#from generic_search import dfs, bfs, node_to_path, astar, Node

class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"

class MazeLocation(NamedTuple):
    row: int
    column: int

class Maze:
    
    def __init__(self, rows: int = 10, columns: int = 10, sparseness: float = 0.2, start: MazeLocation = MazeLocation(0, 0), goal: MazeLocation =  MazeLocation(9, 9)) -> None:
        # initialize basic instance variables
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # fill the grid with empty cells
        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        # populate the grid with blocked cells
        self._randomly_fill(rows, columns, sparseness)
        # fill the start and goal locations in
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL
    
    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED
    
    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    def goal_test(self, ml:MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml:MazeLocation) -> List[MazeLocation]:
        locations:List[MazeLocation] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL
    
    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL   


    pass      

def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation] , float]:
    def distance(ml:MazeLocation) -> float:
        xdist: int =  ml.column - goal.column
        ydist:int = ml.row - goal.row
        return sqrt((xdist*xdist) + (ydist*ydist))
    return distance

def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return (xdist + ydist)
    return distance
    
if __name__=="__main__":
    maze:Maze = Maze()
    print(maze)
    print("-"*20)
    print("sol 1")
    '''solution1:Optional[Node[MazeLocation]] = dfs(
        maze.start, maze.goal_test, maze.successors
    )

    if solution1 is None:
        print("no sol")
    else:
        pathdfs: List[MazeLocation] = node2path(solution1)
        maze.mark(pathdfs)
        print(maze)
        maze.clear(pathdfs)
    print("maze after clear")'''
    print(maze)
    solution2:Optional[Node[MazeLocation]] = bfs(
        maze.start, maze.goal_test, maze.successors
    )
    print("-"*20)
    print("sol 2")
    if solution2 is None:
        print("no sol")
    else:
        pathdfs: List[MazeLocation] = node2path(solution2)
        maze.mark(pathdfs)
        print(maze)
        maze.clear(pathdfs)

    # test A*
    distance: Callable[[MazeLocation] , float] = manhattan_distance(maze.goal)
    solution3: Optional[Node[MazeLocation]] = astar(maze.start , maze.goal_test, maze.successors, distance)

    print('-'*30)
    if solution3 is None:
        print("no solution found")
    else:
        path3: List[MazeLocation] = node2path(solution3)
        maze.mark(path3)
        print(maze)


    