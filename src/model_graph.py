from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self
from .model_node import Node
from .model_edge import Edge
from .parser_exception import ParserMessage
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
    start: int | None = None
    end: int | None = None
    visual: list[list[int]] = []  # REMOVE

    """
    def check_soe_connected(self, edges: dict[int, Edge],
                        start: int, end: int) -> str | None:
        #Iterate through the edge list and check if the start and end nodes
        #are found within it.

        Args:
            edges:  a dict containin all of the graph's edges.
            start:  the index of the start node.
            end:    the index of the end node.

        Returns:
            None if the start and end nodes are present, or a string clarifying
                which are missing.
        ##
        found_start: bool = False
        found_end: bool = False
        for edge in edges.values():
            if edge.node_a == start or edge.node_b == start:
                found_start = True
            if edge.node_a == end or edge.node_b == end:
                found_end = True
            if found_start is True and found_end is True:
                return None
        f: str = ""
        match found_start, found_end:
            case False, True:
                f = "start node is"
            case False, False:
                f = "start and end nodes are"
            case _:
                f = "end node is"
        return f
    """

    @model_validator(mode='after')
    def check_model(self) -> Self:
        """Ensure that all the data inserted into the Graph is valid."""
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
            for n1, n2, l in self.edges.values():
                self.addEdge(n1, n2)
            G = nx.Graph()
            G.add_edges_from(self.visual)
            nx.draw_networkx(G)
            plt.show()
