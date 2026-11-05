from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self
from .model_node import Node
# REMOVE
import networkx as nx
import matplotlib.pyplot as plt


class Graph(BaseModel):
    """A Graph is a non-linear data structure that consists of points,
    called nodes, and connections between those points, called edges.

    For this project, our Graph will be unweighted and undirected.
    Other values will only affect the pathfinding and travelling processes.

    Variables:
        nb_drones:  the number of drones that will travel through the graph.
        nodes:      all the nodes in the graph stored as a dict, where the
                key is an increasing index, and the value is a Node object
                with the corresponding values.
        edges:      all the edges in the graph, stored as a list of tuples
                with the two nodes it connects and the capacity of each edge.
        start:      the index of the graph's starting node.
        end:        the index of the graph's ending node.
    """
    nb_drones: int = Field(ge=1)
    nodes: dict[int, Node]
    edges: dict[int, tuple[int, int, int]]
    start: int
    end: int
    visual: list[list[int]] = []  # REMOVE

    def display(self) -> None:
        print("N of drones: ", self.nb_drones)
        for ind, node in self.nodes.items():
            if ind == self.start:
                print("START ", end='')
            elif ind == self.end:
                print("END ", end='')
            print("Node ", ind)
            node.display()
        for row in self.edges:
            print(row)

    # ==========
    # REMOVE
    # ==========

    def addEdge(self, a: int, b: int) -> None:
        temp = [a, b]
        self.visual.append(temp)

    def visualize(self) -> None:
        for n1, n2, l in self.edges.values():
            self.addEdge(n1, n2)
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()


"""
    @field_validator('start', 'end', mode='before')
    @classmethod
    def check_start_end(cls, value: str, ctx: str) -> str:
        if value is None:
            raise ValueError(f"{ctx.field_name.capitalize()} node is missing")
        return value

    for e in self.edges:
        n1 = e[0]
        n2 = e[1]
        if n1 == n2:
            raise AttributeError("Found an edge between the same node")
        if n1 not in self.nodes or n2 not in self.nodes:
            raise IndexError("Found an edge to a non-existent node")
        if e[2] < 1:
            raise ValueError("Max link capacity must be bigger than 0")
    if not all_positions_unique():
        raise ValueError("Two nodes cannot be on the same coordinates")
    if not all_edges_unique():
        raise ValueError("Found two edges connecting the same nodes")

    def get_adjacency_matrix(self) -> list[list[int]]:
        nodes = set()
        for edge in self.edges:
            nodes.add(edge[0])
            nodes.add(edge[1])
        nodes_l = sorted(list(nodes))
        num_nodes = len(nodes)
        adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]
        for edge in self.edges:
            index_1 = nodes_l.index(edge[0])
            index_2 = nodes_l.index(edge[1])
            adjacency_matrix[index_1][index_2] = 1
            adjacency_matrix[index_2][index_1] = 1
        return adjacency_matrix

    def get_neighbors(self, u: str) -> list[str]:
        nb_l: list[str] = []
        for n1, n2, l in self.edges:
            if n1 == u:
                nb_l.append(n2)
            elif n2 == u:
                nb_l.append(n1)
        return nb_l

"""
