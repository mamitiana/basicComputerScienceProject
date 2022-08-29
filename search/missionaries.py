from __future__ import annotations
from typing import List, Optional
from genericsearch import bfs, Node, node2path

MAX_NUM:int = 3
class MCState:
    def __init__(self, missionaries:int, canibals:int, boat:bool) -> None:
        self.wm:int = missionaries #west bank missionaries
        self.wc:int = canibals # west bank cannibals
        self.em:int = MAX_NUM-self.wm
        self.ec:int = MAX_NUM - self.wc 
        self.boat:bool = boat
        pass

    def __str__(self) -> str:
        return("on the west bank there are {} miss and {} canibals \non the east bank there are {} missionaries and {} cannibales \n the boat is on the {} bank.".format(self.wm, self.wc, self.em, self.ec, ("west" if self.boat  else "east")) )

    def goal_test(self) -> bool:
        return self.is_legal and self.em ==MAX_NUM and self.ec == MAX_NUM

    @property
    def is_legal(self) -> bool:
        if self.wm < self.wc and self.wm >0:
            return False
        if self.em < self.ec and self.em > 0:
            return False
        
        return True

    def successors(self) -> List[MCState]:
        sucs: List[MCState] = []
        if self.boat: # boat on west bank
            if self.wm > 1:
                sucs.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:
                sucs.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:
                sucs.append(MCState(self.wm, self.wc - 1, not self.boat))
            if (self.wc > 0) and (self.wm > 0):
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else: # boat on east bank
            if self.em > 1:
                sucs.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em > 0:
                sucs.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec > 1:
                sucs.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec > 0:
                sucs.append(MCState(self.wm, self.wc + 1, not self.boat))
            if (self.ec > 0) and (self.em > 0):
                sucs.append(MCState(self.wm + 1, self.wc + 1, not self.boat))
        return [x for x in sucs if x.is_legal]


def display_solution(path: List[MCState]):
    if len(path) ==0: 
        return
    old_state: MCState = path[0]
    print(old_state)
    for current_state in path[1:] :
        if current_state.boat:
            print('{} missio and {} canib moved from east to west bank \n'.format(old_state.em - current_state.em, old_state.ec- current_state.ec))
        else:
            print(" {} miss and {} cann moved from the west to east".format( old_state.wm - current_state.wm , old_state.wc - current_state.wc ))
        print(current_state)
        old_state = current_state

if __name__ == "__main__" : 
    start : MCState = MCState(MAX_NUM , MAX_NUM, True)
    solution: Optional[Node[MCState]] = bfs(start, MCState.goal_test , MCState.successors)

    if solution is None:
        print("no solution found")
    else:
        path: List[MCState] = node2path(solution)
        display_solution(path)