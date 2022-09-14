from __future__ import annotations
from typing import TypeVar , Tuple, Type
from abc import ABC, abstractclassmethod, abstractmethod

# interface , all method will be override

class Chromosome(ABC):
    @abstractmethod
    def fitness(self) ->float:
        ...
    
    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) ->T:
        ...

    @abstractmethod
    def crossover(self:T , other:T ) -> Tuple[T,T]:
        ...
    @abstractmethod
    def mutate(self) -> None:
        ...
    