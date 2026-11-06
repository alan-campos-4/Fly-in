from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self
from .model_node import Node
from .model_edge import Edge
from .parser_exception import get_message_by_key
# REMOVE
import networkx as nx
import matplotlib.pyplot as plt


class Graph(BaseModel):
    """A Graph is a non-linear data structure that consists of points,
    called nodes, and connections between those points, called edges.
    In this project, Graphs will be weighted and undirected.

    Variables:
        nb_drones:  the number of drones that will travel through this graph.
        nodes:      all the nodes in this graph, stored in a dict, where the
                key is an increasing index, and the value is a Node object
                with the corresponding values.
        edges:      all the edges in this graph, stored in a dict, where the
                key is an increasing index, and the value is an Edge object
                with the corresponding values.
        start:      the index of this graph's starting node.
        end:        the index of this graph's ending node.
    """
    nb_drones: int = Field(ge=1)
    nodes: dict[int, Node]
    edges: dict[int, Edge]
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    visual: list[list[int]] = []  # REMOVE

    @model_validator(mode='after')
    def check_model(self) -> Self:
        """Ensure that all the data inserted into the Graph is valid."""
        if not self.nodes:
            raise ValueError(get_message_by_key('NODES_MISS'))
        if not self.edges:
            raise ValueError(get_message_by_key('EDGES_MISS'))
        return self

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
            for edge in self.edges.values():
                self.addEdge(edge.node_a, edge.node_b)
            G = nx.Graph()
            G.add_edges_from(self.visual)
            nx.draw_networkx(G)
            plt.show()
