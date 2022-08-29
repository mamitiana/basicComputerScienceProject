from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractclassmethod, abstractmethod
V = TypeVar("V") # Varibale

D = TypeVar('D') # domain
#base class for all domain
class Constraint(Generic[V, D] , ABC):
    
    def __init__(self , variable: List[V]) -> None:
        self.variables = variable
    
    @abstractmethod
    def satisfied(self, assignement: Dict[V, D] ) ->bool:
        ...
    
class CSP(Generic[V, D]):
    def __init__(self , variables : List[V], domains: Dict[V , List[D] ]) -> None:
        self.variables:List[V] = variables
        self.domains:Dict[V,  List[D]] = domains
        self.constrains:Dict[V, List[Constraint[V , D]]] = {}

        for variable in self.variables:
            self.constrains[variable] = []
            if variable not in self.domains:
                print(variable)
                raise LookupError("Every variables should have a domain assigned to it")
    
    def add_constraint(self, constraint: Constraint[V , D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError(" variables in constraint not in csp")
            else:
                self.constrains[variable].append(constraint)
        
    def consistent(self, variable: V , assigenment: Dict[V , D]) -> bool:
        for constraint in self.constrains[variable]:
            if not constraint.satisfied(assigenment):
                return False
        return True
        
    def backtracking_search(self, assignment: Dict[V , D]={}) -> Optional[Dict[V, D ]]:
        # assignement is complete if every variable is assigned 

        if len(assignment)== len(self.variables):
            return assignment
        #geet all variable in the csv bot not in the assignement
        unassigned : List[V] = [v for v in self.variables if v not in assignment]
        #get the every possible domain valie of the first unssignd variable
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first , local_assignment):
                result: Optional[Dict[V , D]] = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None
        pass