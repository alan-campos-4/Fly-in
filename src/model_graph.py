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
        nodes:  all the nodes in the graph stored as a dict, where the
            key is an increasing index, and the value is a Node object
            with the corresponding values.
        edges:  all the edges in the graph, stored as a list of tuples
            with the two nodes it connects and the capacity of each edge.
        start:  the index of the graph's starting node.
        end:    the index of the graph's ending node.
        drones: the number of drones that will travel through the graph.
    """
    nodes: dict[int, Node]
    edges: list[tuple[int, int, int]]
    start: int
    end: int
    drones: int = Field(ge=1)
    visual: list[list[int]] = []  # REMOVE

    @model_validator(mode='after')
    def check_model(self) -> Self:
        """Ensure that all the data inserted into the Graph is valid."""

        def all_positions_unique() -> bool:
            """Check that there are no repeated positions in the nodes."""
            positions: set[tuple[int, ...]] = set()
            for node in self.nodes.values():
                t = tuple((node.x, node.y))
                if t in positions:
                    return False
                else:
                    positions.add(t)
            return True

        def all_edges_unique() -> bool:
            """Check that there are no repeated edges (two edges connecting
            the same two nodes).
            """
            edge_data: set[tuple[int, int]] = set()
            for n1, n2, l in self.edges:
                if (n1, n2) in edge_data:
                    return False
                elif (n2, n1) in edge_data:
                    return False
                else:
                    edge_data.add((n1, n2))
            return True

        def start_end_connected() -> tuple[bool, bool]:
            """Return two variables, each representing whether its nodes,
            start and end, are reachable in the graph.
            """
            found_s: bool = False
            found_e: bool = False
            for n1, n2, l in self.edges:
                if found_s and found_e:
                    break
                if found_s is False and n1 == self.start or n2 == self.start:
                    found_s = True
                if found_e is False and n1 == self.end or n2 == self.end:
                    found_e = True
            return found_s, found_e

        if not all_positions_unique():
            raise ValueError(
                "Found two nodes with the same coordinate values"
            )
        if not all_edges_unique():
            raise ValueError(
                "Found two different edges connecting the same two nodes"
            )
        found_start, found_end = start_end_connected()
        f: str = ""
        match found_start, found_end:
            case True, False:
                f = "end node is"
            case False, True:
                f = "start node is"
            case False, False:
                f = "start and end nodes are"
            case _:
                pass
        if f != "":
            raise ValueError(f"The {f} not connected to the graph")
        return self

    def display(self) -> None:
        print("N of drones: ", self.drones)
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
        for e in self.edges:
            self.addEdge(e[0], e[1])
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
