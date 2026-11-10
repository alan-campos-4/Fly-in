from .model_graph import Graph
from .model_node import Node
from .model_edge import Edge
from .model_drone import Drone


def find_edge_to_travel(edges: dict[int, Edge],
                        curr_node: int, next_node: int) -> int:
    for edge_ind, edge in edges.items():
        if curr_node == edge.node_a and next_node == edge.node_b:
            return edge_ind
        elif curr_node == edge.node_b and next_node == edge.node_a:
            return edge_ind
    return -1


def is_next_node_available(nodes: dict[int, Node],
                            next_node: int, end: int) -> bool:
    if next_node == end:
        return True
    return nodes[next_node].max_drones - nodes[next_node].drones >= 1


def is_travel_edge_available(edges: dict[int, Edge],
                             edge_to_travel: int) -> bool:
    return (edges[edge_to_travel].max_link_capacity 
            - edges[edge_to_travel].occupancy >= 1)


def try_to_move(d: Drone,
                nodes: dict[int, Node],
                edges: dict[int, Edge]) -> int:
    """"
    select from path, with drone_val, the current node and the next one
    find the values for the corresponding node
    if max capacity and max drones allow it, move
    if not, wait
    """
    print(d, end='')
    if d.delivered:
        return 2
    next_node: int = d.get_next_node()
    edge_to_travel = find_edge_to_travel(edges, d.current_node, next_node)

    print(f"  tries to move from {d.current_node} to {next_node}")
    print(f"      node capacity of {next_node}: {next_node_space}")
    print(f"      edge capacity of {edge_to_travel}: {edge_to_travel_capacity}")
    if d.previous_node != -1:
        print(f"      node capacity of {next_node} (previous): {next_node_space}")
    if d.previous_edge != -1:
        print(f"      edge capacity of {d.previous_edge} (previous): "
              f"{edges[d.previous_edge].max_link_capacity - edges[d.previous_edge].occupancy}")
    if (is_next_node_available(nodes, next_node, d.path[-1])
            and is_travel_edge_available(edges, edge_to_travel)):
        if d.previous_edge != -1:
            edges[d.previous_edge].occupancy -= 1
        if d.previous_node != -1:
            nodes[d.previous_node].drones -= 1
        edges[edge_to_travel].occupancy += 1
        d.previous_node = d.current_node
        d.current_node = next_node
        d.previous_edge = edge_to_travel
        nodes[next_node].drones += 1
        if d.current_node == d.path[-1]:
            d.delivered = True
            edges[d.previous_edge].occupancy -= 1
            d.previous_edge = -1
        return 1                
    else:
        return 0


def all_finished(drones: list[Drone]) -> bool:
    return all(d.delivered for d in drones)


def travel(g: Graph, path: list[int]) -> None:
    """
    The drones will be stored in a dict of length nb_drones, in which
    the key will be a number (0, nb_drones - 1), and the value will be
    the index of the node it is currently located at.

    Args:
        g:      the Graph object.
        path:   a list with the indexes of all the nodes gone through.
    """
    print(f"Path:  {path}")
    # edges_in_path = find_edges_in_path(g.edges, path)
    # print(f"Edges in path:   {edges_in_path}")
    # print(f"Edges' capacity: {[g.edges[edge][2] for edge in edges_in_path]}")

    drones = [Drone(ind=i, path=path) for i in range(g.nb_drones)]

    t = 1
    while 1:
        print(f"\nTurn {t}")
        if all_finished(drones):
            print("    All finished")
            break
        for d in drones:
            move = try_to_move(d, g.nodes, g.edges)
            if move == 2:
                print("     finished")
            elif move == 1:
                print("  will move")
            else:
                print("  will wait")
        if t >= 20:
            break
        t += 1
