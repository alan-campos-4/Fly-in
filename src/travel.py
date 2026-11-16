from .model_graph import Graph
from .model_node import Node
from .model_edge import Edge
from .model_drone import Drone


def display_drones(drones: list[Drone], nodes: dict[int, Node]) -> None:
    """Print the drones and the name their current node."""
    print(' '.join(f"{d}-{nodes[d.current_node].name}" for d in drones))


def all_finished(drones: list[Drone]) -> bool:
    """Return True if all the drones are delivered."""
    return all(d.delivered for d in drones)


def find_edge_to_travel(edges: dict[int, Edge],
                        curr_node: int, next_node: int) -> int:
    """Return the index of the edge that connects the two nodes given."""
    for edge_ind, edge in edges.items():
        if curr_node == edge.node_a and next_node == edge.node_b:
            return edge_ind
        elif curr_node == edge.node_b and next_node == edge.node_a:
            return edge_ind
    return -1


def is_node_available(nodes: dict[int, Node], node: int) -> bool:
    """Return True is the node given has enough space to let another
    drone travel to it."""
    return nodes[node].max_drones - nodes[node].drones >= 1


def is_edge_traversable(edges: dict[int, Edge], edge: int) -> bool:
    """Return True if the edge given has enough capacity to let another
    drone travel through it."""
    return edges[edge].max_link_capacity - edges[edge].occupancy >= 1


def try_to_move(d: Drone, nodes: dict[int, Node], edges: dict[int, Edge],
                end: int) -> bool:
    """"
    Make a drone attempt to move to the next node in its path.

    Check if the next node has enough space, and if the edge that it will
    travel through has enough capacity for it. If so, then change the node's
    current position, and use previous_node and previous_edge to make the
    corresponding changes to the graph.

    The current and next nodes' occupancy changes within the turn.
    The edges are occupied by a drone for teh duration of its turn, then freed
    when they move through a different one.

    Args:
        d:      the drone that will try to travel.
        nodes:  the graph's nodes.
        edges:  the graph's edges.
        end:    the graph's end node.

    Returns:
        True, if the drone has successfuly moved to the next node. 
    """
    next_node = d.get_next_node()
    next_node_av = is_node_available(nodes, next_node)
    edge_to_travel = find_edge_to_travel(edges, d.current_node, next_node)
    edge_to_travel_av = is_edge_traversable(edges, edge_to_travel)
    if (next_node_av and edge_to_travel_av):
        if d.previous_edge != -1:
            edges[d.previous_edge].occupancy -= 1
        edges[edge_to_travel].occupancy += 1
        d.previous_edge = edge_to_travel
        d.previous_node = d.current_node
        d.current_node = next_node
        nodes[d.current_node].drones += 1
        nodes[d.previous_node].drones -= 1
        if d.current_node == end:
            d.delivered = True
            edges[d.previous_edge].occupancy -= 1
            # d.previous_edge = -1
        return True
    else:
        return False


def travel(g: Graph, path: list[int]) -> None:
    """
    The drones will be stored in a dict of length nb_drones, in which
    the key will be a number (0, nb_drones - 1), and the value will an
    object containg the data for a Drone.

    The simulation starts after setting all the drones at the start.

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
        moved = []
        for d in drones:
            if not d.delivered and try_to_move(d, g.nodes, g.edges, end):
                moved.append(d)
        display_drones(moved, g.nodes)
        if t >= 20:
            break
        if all_finished(drones):
            print("All finished")
            break
        t += 1
