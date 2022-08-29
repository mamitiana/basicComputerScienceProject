from typing import TypeVar, Generic, List, Optional
from edge import Edge
import sys

sys.path.append("..")
sys.path.append(".")
from search.genericsearch import bfs, Node, node2path
V = TypeVar("V")

class Graph(Generic[V]):
    def __init__(self , vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices
        self._edges: List[List[Edge]]= [[] for _ in vertices]

    @property
    def vertex_count(self) -> int:
        return len(self._vertices) #number of verticies
    @property
    def edge_count(self)-> int:
        return sum(map(len, self._edges))
    # add  new vertex to the graph and return its index
    def add_vertex(self, vertex:V) ->int:
        self._vertices.append(vertex)
        self._edges.append([])
        return self.vertex_count -1
    
    #this is an undirected graph, so we add edge in both direction
    def add_edge(self, edge:Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())
    # add new edge by the indices of the vertex
    def add_edge_by_indices(self, u:int , v:int) -> None:
        edge:Edge = Edge(u , v)
        self.add_edge(edge)
    # add new edge by creating vertices at the same time
    def add_edge_by_vertices(self, first:V , second:V ) ->None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v)
    # return the vertices at the index
    def vertex_at(self, index:int) -> V :
        return self._vertices[index]        
    
    # index of the vertices
    def index_of(self, vertex:V ) ->V:
        return self._vertices.index(vertex)
    #retur the vertices's neighbors
    def neighbors_for_index(self, index:int )-> List[V]:
        
        return list( map( self.vertex_at , [e.v for e in self._edges[index]] ) )

    # look at the indice of the vertex and finds it's neigbors
    def neighbors_for_vertex(self, vertex:V) -> List[V]:
        return self.neighbors_for_index( self.index_of(vertex)  )
    
    # return all edge associated with the vertex indice
    def edges_for_index(self, index:int) -> List[Edge]:
        return self._edges[index] 
    # look up index of a vertex and return its edges
    def edge_for_vertex(self, vertex: V):
        return self.edges_for_index(  self.index_of(vertex) )

    # make it easy to pretty- print a Graph
    def __str__(self) -> str:
        desc: str=""
        for i in range(self.vertex_count):
            desc+= f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc

if __name__=="__main__":
    #test
    city_graph:Graph[str] = Graph(["Seattle", "San Francisco", "Los Angeles", "Riverside", "Phoenix", "Chicago", "Boston", "New York", "Atlanta", "Miami", "Dallas", "Houston", "Detroit", "Philadelphia", "Washington"])
    print(city_graph)
    print("-"*30)
    city_graph.add_edge_by_vertices("Seattle", "Chicago")
    city_graph.add_edge_by_vertices("Seattle", "San Francisco")
    city_graph.add_edge_by_vertices("San Francisco", "Riverside")
    city_graph.add_edge_by_vertices("San Francisco", "Los Angeles")
    city_graph.add_edge_by_vertices("Los Angeles", "Riverside")
    city_graph.add_edge_by_vertices("Los Angeles", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Chicago")
    city_graph.add_edge_by_vertices("Phoenix", "Dallas")
    city_graph.add_edge_by_vertices("Phoenix", "Houston")
    city_graph.add_edge_by_vertices("Dallas", "Chicago")
    city_graph.add_edge_by_vertices("Dallas", "Atlanta")
    city_graph.add_edge_by_vertices("Dallas", "Houston")
    city_graph.add_edge_by_vertices("Houston", "Atlanta")
    city_graph.add_edge_by_vertices("Houston", "Miami")
    city_graph.add_edge_by_vertices("Atlanta", "Chicago")
    city_graph.add_edge_by_vertices("Atlanta", "Washington")
    city_graph.add_edge_by_vertices("Atlanta", "Miami")
    city_graph.add_edge_by_vertices("Miami", "Washington")
    city_graph.add_edge_by_vertices("Chicago", "Detroit")
    city_graph.add_edge_by_vertices("Detroit", "Boston")
    city_graph.add_edge_by_vertices("Detroit", "Washington")
    city_graph.add_edge_by_vertices("Detroit", "New York")
    city_graph.add_edge_by_vertices("Boston", "New York")
    city_graph.add_edge_by_vertices("New York", "Philadelphia")
    city_graph.add_edge_by_vertices("Philadelphia", "Washington")
    

    print(city_graph)

    bfs_result: Optional[Node[V]] = bfs("Boston", lambda x: x == "Miami", city_graph.neighbors_for_vertex)
    if bfs_result is None:
        print("No solution found using breadth-first search!")
    else:
        path: List[V] = node2path(bfs_result)
        print("Path from Boston to Miami:")
        print(path)