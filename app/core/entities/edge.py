from dataclasses import dataclass

"""
Edge is a dataclass that represents a directed prerequisite relationship in the graph.

Args:
    src (str): Prerequisite course code (source node).
    dst (str): Dependent course code (destination node).

Returns:
    Edge: The Edge instance.
"""
@dataclass
class Edge:
    src: str
    dst: str
