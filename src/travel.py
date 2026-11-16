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


def is_next_node_av(nodes: dict[int, Node], node: int) -> bool:
    return nodes[node].max_drones - nodes[node].drones >= 1


def is_edge_traversable(edges: dict[int, Edge], edge_to_travel: int) -> bool:
    return (edges[edge_to_travel].max_link_capacity
            - edges[edge_to_travel].occupancy >= 1)


def try_to_move(d: Drone,
                nodes: dict[int, Node],
                edges: dict[int, Edge], end: int) -> bool:
    """"
    select from path, with drone_val, the current node and the next one
    find the values for the corresponding node
    if max capacity and max drones allow it, move
    if not, wait
    """
    next_node: int = d.get_next_node()
    edge_to_travel = find_edge_to_travel(edges, d.current_node, next_node)
    if next_node == end:
        next_node_av = True
    else:
        next_node_av = is_next_node_av(nodes, next_node)
    edge_to_travel_av = is_edge_traversable(edges, edge_to_travel)
    # print(f"  tries to move from {d.current_node} to {next_node}")
    # print(f"      capacity of node {next_node}: {next_node_av}")
    # print(f"      capacity of edge {edge_to_travel}: {edge_to_travel_av}")
    if (next_node_av and edge_to_travel_av):
        if d.previous_edge != -1:
            edges[d.previous_edge].occupancy -= 1
        # if d.previous_node != -1:
        #    nodes[d.previous_node].drones -= 1
        edges[edge_to_travel].occupancy += 1
        d.previous_edge = edge_to_travel
        d.previous_node = d.current_node
        d.current_node = next_node
        nodes[d.current_node].drones += 1
        nodes[d.previous_node].drones -= 1
        if d.current_node == end:
            d.delivered = True
            edges[d.previous_edge].occupancy -= 1
            d.previous_edge = -1
        return True
    else:
        return False


def all_finished(drones: list[Drone]) -> bool:
    return all(d.delivered for d in drones)


def display_moved_drones(drones: list[Drone], nodes: dict[int, Node]) -> None:
    print(' '.join(f"{d}-{nodes[d.current_node].name}" for d in drones))


def travel(g: Graph, path: list[int]) -> None:
    """
    The drones will be stored in a dict of length nb_drones, in which
    the key will be a number (0, nb_drones - 1), and the value will an
    object containg the data for a Drone.

    The simulation start after setting all the drones at the start.

    Args:
        g:      the Graph object.
        path:   a list with the indexes of all the nodes will go through.
    """
    print(f"Path:  {path}")
    end = path[-1]

    drones = [Drone(ind=i, path=path) for i in range(g.nb_drones)]
    g.nodes[g.start].drones = g.nb_drones

    t = 1
    while 1:
        print(f"\nTurn {t}")
        """for p in path:
            n = g.nodes[p]
            print(f"Node {p}: {n.max_drones} max, {n.drones} curr")
        for d in drones:
            if d.delivered:
                print(f"{d} is finished")
            else:
                print(f"{d} is in node {d.current_node}")
        """
        moved = []
        for d in drones:
            if not d.delivered:
                # print(f"  {d}", end='')
                move = try_to_move(d, g.nodes, g.edges, end)
                if move:
                    # print("  has moved")
                    moved.append(d)
        display_moved_drones(moved, g.nodes)
        if t >= 20:
            break
        if all_finished(drones):
            print("All finished")
            break
        t += 1
