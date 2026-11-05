from .model_graph import Graph
from .model_node import Node


def find_edges_in_path(edges: dict[int, tuple[int, int, int]],
                       path: list[int]) -> list[int]:
    """Create a list of the indexes of all the edges that a
    given path passes through. Its length will always be len(path) - 1.

    Args:
        edges:  the dict containing all the data for the Graph's edges.
        path:   a list with the indexes of all the nodes gone through.

    Returns:
        a list with the indexes of all the edges the path goes through.
    """
    i = 0
    edges_in_path = []
    while i < len(path) - 1:
        start_node = path[i]
        next_node = path[i + 1]
        for edge_ind, (n1, n2, l) in edges.items():
            if start_node == n1 and next_node == n2:
                edges_in_path.append(edge_ind)
            elif start_node == n2 and next_node == n1:
                edges_in_path.append(edge_ind)
        i += 1
    return edges_in_path


def display_drones(drones: dict[int, int], nodes: dict[int, Node]) -> None:
    for dk, dv in drones.items():
        " ".join(f"D{dk + 1}-{nodes[dv].name}")
    print()



def find_next_node(path: list[int], curr_node: int) -> int:
    i = 0
    for pos in path:
        if pos == curr_node:
            return path[i + 1]
        i += 1
    return -1


def find_edge_to_travel(edges: dict[int, tuple[int, int, int]],
                        curr_node: int, next_node: int) -> int:
    for edge_ind, (n1, n2, l) in edges.items():
        if curr_node == n1 and next_node == n2:
            return edge_ind
        elif curr_node == n2 and next_node == n1:
            return edge_ind
    return -1


def try_to_move(drones: dict[int, int], drone_i: int,
                path: list[int], edges: dict[int, tuple[int, int, int]],
                nodes: dict[int, Node]) -> None:
    """
    select from path, with drone_val, the current node and the next one
    find the values for the corresponding node
    if max capacity and max drones allow it, move
    if not, wait
    """
    print(f"D{drone_i + 1}")
    curr_node: int = drones[drone_i]
    next_node: int = find_next_node(path, curr_node)
    print(f"  tries to move from {curr_node} to {next_node}")
    edge_to_travel = find_edge_to_travel(edges, curr_node, next_node)
    next_node_space = nodes[next_node].max_drones - nodes[next_node].drones
    if next_node_space >= 1:
        print("  will move")
    else:
        print("  will wait")


def travel(g: Graph, path: list[int]) -> None:
    """
    The drones will be stored in a dict of length nb_drones, in which
    the key will be a number (0, nb_drones - 1), and the value will be
    the index of the node it is currently located at.

    Args:
        g:      the Graph object.
        path:   a list with the indexes of all the nodes gone through.
    """
    print(f"Path:            {path}")
    edges_in_path = find_edges_in_path(g.edges, path)
    print(f"Edges in path:   {edges_in_path}")
    print(f"Edges' capacity: {[g.edges[edge][2] for edge in edges_in_path]}")
    drone_dict = {i: g.start for i in range(g.nb_drones)}
    print(type(g.nodes))
    display_drones(drone_dict, g.nodes)

    print("\nTurn 1")
    try_to_move(drone_dict, 0, path, g.edges, g.nodes)
    try_to_move(drone_dict, 1, path, g.edges, g.nodes)
    try_to_move(drone_dict, 2, path, g.edges, g.nodes)
    print("\nTurn 2")
    try_to_move(drone_dict, 0, path, g.edges, g.nodes)

"""
    pos_in_path = 0
    edge_index = 0
    drone_i = 0
    while pos_in_path < len(path) - 1:
        print(f"current pos in path: {path[pos_in_path]}")
        edge_to_travel = g.edges[edges_in_path[edge_index]]
        curr_node_id, next_node_id, max_capacity = edge_to_travel
        if max_capacity >= 1:
            pos_in_path += 1
            g.edges[edges_in_path[edge_index]] = (
                curr_node_id, next_node_id, max_capacity - 1
            )
            edge_index += 1
            print(f"new pos in path: {path[pos_in_path]}")
            print(f"            {[g.edges[edge][2] for edge in edges_in_path]}")
            g.edges[edges_in_path[edge_index - 1]] = (
                curr_node_id, next_node_id, max_capacity
            )
            print(f"            {[g.edges[edge][2] for edge in edges_in_path]}")
        else:
            print("must wait")
"""

