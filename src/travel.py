from .models import Graph, Node, Edge, Drone


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
        na = edge.node_a
        nb = edge.node_b
        if curr_node == na and next_node == nb:
            return edge_ind
        elif curr_node == nb and next_node == na:
            return edge_ind
    return -1


def is_node_available(nodes: dict[int, Node], node: int) -> bool:
    """Return True is the node given has enough space to let another
    drone travel to it."""
    return nodes[node].max_drones - nodes[node].curr_drones > 0


def is_edge_traversable(edges: dict[int, Edge], edge: int) -> bool:
    """Return True if the edge given has enough capacity to let another
    drone travel through it."""
    return edges[edge].max_link_capacity - edges[edge].occupancy > 0


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
        nodes[d.current_node].curr_drones += 1
        nodes[d.previous_node].curr_drones -= 1
        if d.current_node == end:
            d.delivered = True
            edges[d.previous_edge].occupancy -= 1
            # d.previous_edge = -1
        return True
    else:
        return False


def travel(g: Graph, paths: list[tuple[int, ...]]) -> None:
    """
    Create a list of drones of length nb_drones that will travel through
    the Graph from the start to the end following the paths given.

    The movement follows turn scheduling. In every turn, each drone tries
    to move to its next node in its path. The drones that successfully move
    are displayed in the output.

    Args:
        g:      the Graph object.
        paths:   a list with valid paths between the start and end nodes.
    """
    if not paths:
        return
    path = paths[0]
    end = path[-1]
    nodes = g.nodes
    edges = g.edges
    drones = [Drone(ind=i, path=path) for i in range(g.nb_drones)]
    nodes[g.start].curr_drones = g.nb_drones

    t = 1
    while 1:
        print(f"Turn {t}")
        moved = []
        for d in drones:
            if not d.delivered and try_to_move(d, nodes, edges, end):
                moved.append(d)
        display_drones(moved, nodes)
        if t >= 25:
            break
        if all_finished(drones):
            break
        t += 1
