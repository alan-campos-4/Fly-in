from .models import Graph, Node, Edge, Drone


def display_drones(drones: list[Drone], nodes: dict[int, Node]) -> None:
    """Print the drones and the name their current node."""
    # print(' '.join(f"{d}-{nodes[d.curr_node].name}" for d in drones))
    for d in drones:
        if d.curr_node != -1:
            print(f"{d}-{nodes[d.curr_node].name} ", end='')
        else:
            print(f"{d}__it ", end='')
    print()


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


def try_to_move(d: Drone, nodes: dict[int, Node],
                edges: dict[int, Edge]) -> bool:
    """"
    Make a drone attempt to move to the next node in its path.

    Check if the next node has enough space, and if the edge that it will
    travel through has enough capacity for it. If so, then change the node's
    current position, and use previous_node and previous_edge to make the
    corresponding changes to the graph.

    The current and next nodes' occupancy changes within the turn.
    The edges are occupied by a drone for the duration of its turn, then freed
    when they move through a different one.

    Args:
        d:      the drone that will try to travel.
        nodes:  the graph's nodes.
        edges:  the graph's edges.

    Returns:
        True, if the drone has successfuly moved to the next node.
    """
    next_node_av = is_node_available(nodes, d.next_node)
    # If the drone is set to arrive to a restricted node this turn,
    # change the current node, occupy it and free the edge traversed.
    if d.in_transit:
        if next_node_av:
            # ### d.curr_node = d.next_node
            # ### d.pos += 1
            d.move_to_next_node()
            # ### edges[d.prev_edge].occupancy -= 1
            nodes[d.curr_node].curr_drones += 1
            d.in_transit = False
            d.update_next_node()
            if d.delivered:
                edges[d.prev_edge].occupancy -= 1
                nodes[d.prev_node].curr_drones -= 1
            return True
        return False
    edge_to_travel = find_edge_to_travel(edges, d.curr_node, d.next_node)
    edge_to_travel_av = is_edge_traversable(edges, edge_to_travel)
    if next_node_av and edge_to_travel_av:
        # If there is a previous edge or node, leave it.
        if d.prev_edge != -1:
            edges[d.prev_edge].occupancy -= 1
        if d.prev_node != -1:
            nodes[d.prev_node].curr_drones -= 1
        # If the next node is a resctricted one,
        if not d.in_transit and nodes[d.next_node].zone.value == 'restricted':
            # Set current node to -1 and occupy the edge to travel.
            # ### nodes[d.prev_node].curr_drones -= 1
            d.prev_node = d.curr_node
            d.curr_node = -1
            edges[edge_to_travel].occupancy += 1
            d.prev_edge = edge_to_travel
            d.in_transit = True
            return True
        # Enter the new edge, and set it as the previous edge.
        edges[edge_to_travel].occupancy += 1
        d.prev_edge = edge_to_travel
        # Leave the previous node and enter the next one.
        d.move_to_next_node()
        nodes[d.curr_node].curr_drones += 1
        d.update_next_node()
        # If the drone has reached the end,
        # leave the previous edge and mark it as delivered.
        if d.delivered:
            edges[d.prev_edge].occupancy -= 1
            nodes[d.prev_node].curr_drones -= 1
        return True
    return False


def get_best_path_ind(paths: list[tuple[int, ...]],
                      nodes: dict[int, Node], log: bool) -> tuple[int, ...]:
    """Iterate through the paths found and return which one has the
    lowest cost in terms of turns.

    Args:
        paths:  the list of valid paths through the node.
        nodes:  the graph's nodes.

    Returns:
        the index corresponding to the path witht the lowest cost.
    """
    costs = [0 for _ in range(len(paths))]
    for i in range(len(paths)):
        for p in paths[i]:
            zone = nodes[p].zone.value
            if zone == 'restricted':
                costs[i] += 2
            else:
                costs[i] += 1
    cost_ind = 0
    for i in range(len(costs)):
        if costs[i] < costs[cost_ind]:
            cost_ind = i
    if log:
        print("Costs:")
        print(costs)
        print(cost_ind)
    return cost_ind


def travel(g: Graph, paths: list[tuple[int, ...]], log: bool) -> None:
    """Create a list of drones that will travel through the Graph from
    the start to the end following the paths given.

    The movement follows turn scheduling. In every turn, each drone tries
    to move to its next node in its path. The drones that successfully move
    are displayed in the output.

    Args:
        g:      the Graph object.
        paths:   a list with valid paths between the start and end nodes.
    """
    if not paths:
        return
    nodes = g.nodes
    edges = g.edges
    ind = get_best_path_ind(paths, nodes, log)
    drones = [Drone(ind=i, path=paths[ind]) for i in range(g.nb_drones)]
    # Set the start node with all drones in it.
    nodes[g.start].curr_drones = g.nb_drones

    t: int = 1
    not_moved_count: int = 0
    print()
    while 1:
        print(f"Turn {t}")
        moved = []
        for d in drones:
            if not d.delivered and try_to_move(d, nodes, edges):
                moved.append(d)
                not_moved_count = 0
        if moved:
            display_drones(moved, nodes)
        else:
            not_moved_count += 1
        if not_moved_count > 3:
            print("Drones are stuck")
            break
        """if t > 105:
            print("Limit surpassed")
            break"""
        if all_finished(drones):
            break
        t += 1

"""
  0           1           2           3
( 3 ) ----> ( 8 ) ----> ( 9 ) ----> ( 7 )
  n           n           r           n

before
    prev node = 3
    curr node = 8
    next node = 9
    pos       = 1
    prev edge = 3-8
    next edge = 8-9

next node zone == 'priority'

1st turn
    prev node = 8
    curr node = -1
    next node = 9
    pos       = 1
    prev edge = 3-8
    next edge = 8-9

2nd turn
    prev node = 8
    curr node = 9
    next node = 7
    pos       = 2
    prev edge = 8-9
    next edge = 9-3
"""
