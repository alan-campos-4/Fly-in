from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self
from .node import Node
from .edge import Edge
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

        paths:      all the valid paths found between the start and end.
        costs:      the minimum cost, in turns, of each path.
        spaces:     the average space, in number of drones, of each path.
    """
    nb_drones: int = Field(ge=1)
    nodes: dict[int, Node]
    edges: dict[int, Edge]
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    n_paths: int = Field(default=0)
    paths: list[tuple[int, ...]] = []
    costs: list[int] = []
    spaces: list[int] = []
    visual: list[list[int]] = []  # REMOVE

    @model_validator(mode='after')
    def check_model(self) -> Self:
        """Change the capacity of the special drones."""
        self.nodes[self.start].max_drones = self.nb_drones
        self.nodes[self.end].max_drones = self.nb_drones
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

    def add_path(self, path: tuple[int, ...]) -> None:
        """Adds the given path to the Graph's list, and assigns
        its costs and space."""
        cost = 0
        space_total = 0
        for p in path:
            zone = self.nodes[p].zone.value
            space_total += self.nodes[p].max_drones
            if zone == 'restricted':
                cost += 2
            else:
                cost += 1
        self.costs.append(cost)
        self.spaces.append(int(space_total / len(path)))
        self.paths.append(path)
        self.n_paths += 1

    def sort_paths(self) -> None:
        """Sort the Graph's paths by its costs and spaces."""
        sorted_lists = sorted(zip(self.costs, self.spaces, self.paths))
        self.paths = [s[2] for s in sorted_lists]
        self.costs = [s[0] for s in sorted_lists]
        self.spaces = [s[1] for s in sorted_lists]

    def print_paths(self):
        for i in range(self.n_paths):
            print(f"{self.paths[i]}  [{self.costs[i]} | {self.spaces[i]}]")

    # ====================
    # REMOVE
    # ====================

    def addEdge(self, a: int, b: int) -> None:
        temp = [a, b]
        self.visual.append(temp)

    def visualize(self) -> None:
        for edge in self.edges.values():
            self.addEdge(edge.node_a, edge.node_b)
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()
