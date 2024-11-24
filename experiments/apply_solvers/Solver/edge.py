from typing import List, Union, Tuple


class Edge:
    """Class for a normal edge or hyperedge"""

    def __init__(self, n: List[int], weight: float, intermediate: Union[None, int] = None):
        self.nodes = tuple(sorted(n))
        self.weight = weight
        self.intermediate = intermediate

    def __hash__(self):
        return hash((self.nodes, self.weight, self.intermediate))

    def __eq__(self, other):
        return (
            self.nodes == other.nodes and 
            self.weight == other.weight and 
            self.intermediate == other.intermediate
        )

    def __repr__(self):
        if self.intermediate is not None:
            return f"({self.nodes}, weight: {self.weight}, intermediate: {self.intermediate})"
        return f"({self.nodes}, weight: {self.weight})"
    

    def split(self):
        """If there is an intermediate node, return two edges"""
        if self.intermediate is not None:
            edge1 = Edge([self.nodes[0], self.intermediate], self.weight)
            edge2 = Edge([self.intermediate, self.nodes[1]], self.weight)
            return [edge1, edge2]
        return [self]
