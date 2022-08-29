from __future__ import annotations
from enum import Enum
from heapq import heappop, heappush
from os import stat
from re import T
from typing import Deque, Dict, Set, TypeVar, Generic, List, NamedTuple, Callable, Optional
import random
from math import sqrt
#from generic_search import dfs, bfs, node_to_path, astar, Node
T = TypeVar('T')

class Stacks(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) ->bool:
        return not self._container
    
    def push(self, item:T) ->None:
        self._container.append(item)
    
    def pop(self) ->T:
        return self._container.pop()
    def __repr__(self) -> str:
        return repr(self._container)

class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container:  Deque[T] = Deque()

    @property
    def empty(self) ->bool:
        return not self._container
    
    def push(self, item:T) ->None:
        self._container.append(item)
    
    def pop(self) ->T:
        return self._container.popleft()
    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(self , state:T , parent: Optional [Node], cost:float=0.0, heuristic:float=0.0 ) -> None:
        # linked liste
        self.state:T = state
        self.parent:Optional[Node] = parent
        self.cost:float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node)->bool:
        return (self.cost+self.heuristic) < (other.cost+ other.heuristic)

def dfs(initial:T , goal_test:Callable[[T], bool] , 
    successors:Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier is where we've yet to go

    frontier:Stacks[Node[T]] = Stacks()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored:Set[T] = {initial}
    
    # Keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state:T = current_node.state 
        #if we got the goal then end
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None
    pass

def bfs(initial:T , goal_test:Callable[[T] , bool] ,
     successors:Callable[[T] , List[T]] ) -> Optional[Node[T]]:
    
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial , None))
    #explored is where we've been
    explored:Set[T] = {initial}

    #keep going
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state:T = current_node.state
        #if we found the goal

        if goal_test(current_state):
            return current_node
        #check where we can go next and haven t explored
        for child in successors(current_state):
            if child in explored: #skip
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))

    return None
def node2path(node: Node[T]) -> List[T]:
    path: List[T]= [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path



class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) ->bool:
        return not self._container
    
    def push(self, item:T) ->None:
        heappush(self._container, item)
    
    def pop(self) ->T:
        return heappop(self._container)
    def __repr__(self) -> str:
        return repr(self._container)


def astar(initial:T , goal_test: Callable[[T] , bool] , successors: Callable[[T] , List[T]] , heuristic: Callable[[T], float ]) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier : PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))

    #explored is where we've been
    explored: Dict[T, float] = {initial: 0.0}

    #keep going while there is more to explore
    while not frontier.empty:
        current_node : Node[T] = frontier.pop()
        current_state:T = current_node.state
        #if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            new_cost: float = current_node.cost+1
            # 1 assumes a grid , need a cost function for more sphositicated apps
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None #went throught everything and never found goal
    