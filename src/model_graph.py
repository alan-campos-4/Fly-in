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
        edges:      all the edges in the graph, stored as a dict, where the
                key is an increasing index, and the value is a tuples with
                the two nodes it connects and the capacity of each edge.
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

    # ====================
    # REMOVE
    # ====================

    def addEdge(self, a: int, b: int) -> None:
        temp = [a, b]
        self.visual.append(temp)

    def visualize(self) -> None:
        opt = input("Visualize? (y/n): ")
        if opt == 'y':
            for n1, n2, l in self.edges.values():
                self.addEdge(n1, n2)
            G = nx.Graph()
            G.add_edges_from(self.visual)
            nx.draw_networkx(G)
            plt.show()
