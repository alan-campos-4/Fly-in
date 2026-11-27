from .models import Graph, Node, Edge, Drone
import math


def display_drones(drones: list[Drone], nodes: dict[int, Node]) -> None:
    """Print the drones and the name their current node."""
    for d in drones:
        if d.curr_node != -1:
            print(f"{d}-{nodes[d.curr_node].name} ", end='')
        else:
            print(f"{d}-{nodes[d.prev_node].name}-{nodes[d.next_node].name} ", end='')
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
    """"Make a drone attempt to move to the next node in its path.

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
    moved = False
    next_node_av = is_node_available(nodes, d.next_node)
    # If the drone is set to arrive to a restricted node this turn,
    # change the current node, occupy it and free the edge traversed.
    if d.in_transit:
        if next_node_av:
            d.move_to_next_node()
            nodes[d.prev_node].curr_drones -= 1
            nodes[d.curr_node].curr_drones += 1
            d.in_transit = False
            moved = True
    else:
        edge_to_travel = find_edge_to_travel(edges, d.curr_node, d.next_node)
        edge_to_travel_av = is_edge_traversable(edges, edge_to_travel)
        if next_node_av and edge_to_travel_av:
            # If there is a previous edge or node, leave it.
            if d.prev_edge != -1:
                edges[d.prev_edge].occupancy -= 1
            # Enter the new edge, and set it as the previous edge.
            edges[edge_to_travel].occupancy += 1
            d.prev_edge = edge_to_travel
            if nodes[d.next_node].zone.value == 'restricted':
                # If the next node is a resctricted one,
                # set current node to -1 and the drone to in transit.
                d.prev_node = d.curr_node
                d.curr_node = -1
                d.in_transit = True
            else:
                # If the next node is not resctricted,
                # move to it, and occupy it.
                d.move_to_next_node()
                nodes[d.prev_node].curr_drones -= 1
                nodes[d.curr_node].curr_drones += 1
            moved = True
    # If the drone has sucessfully moved, return True
    if moved:
        # If the drone has reached the end,
        # leave the previous edge and mark it as delivered.
        if d.delivered:
            edges[d.prev_edge].occupancy -= 1
        return True
    return False


def get_drone_paths(g: Graph, paths: list[tuple[int, ...]],
                    n_paths: int, n_drones: int) -> list[int]:
    """Obtain a list of paths that will be assigned to the drones.
    The method will depend on the number of drones that need to travel
    the number of paths available.

    Args:
        g:          the Graph.
        paths:      the list of paths.
        n_paths:    the number of paths.
        n_drones:   the number of drones.

    Returns:
        a list of with the indexes of paths for every drone.
    """

    def path_fill(drones: list[tuple[int, ...]],
                  paths: list[tuple[int, ...]],
                  g: Graph,
                  n_drones: int, n_paths: int) -> None:
        """Iterate through every drone and assign to it a path.
        The path to assign will change if it has its capacity filled,
        or if too many drones have been given it.

        An inital limit is established to ensure that drones do not
        clutter a small number of paths.

        Args:
            drones:     the paths that will be assigned to the drones.
        """
        assigned = [0] * n_paths
        spaces = g.spaces
        total_space = sum(spaces)
        limit = [int(n_drones * s / total_space) for s in spaces] # rule of threes

        p_i = 0
        for d_i in range(n_drones):
            if assigned[p_i] >= limit[p_i]:
                p_i += 1
            if p_i < n_paths:
                drones[d_i] = p_i
                assigned[p_i] += 1
            else:
                p_i = 0
        # If after the first assignment loop there are drones without paths,
        # repeat the loop without a limit.
        for d_i in [i for i in range(n_drones) if drones[i] == -1]:
            if p_i < n_paths:
                drones[d_i] = p_i
                assigned[p_i] += 1
            else:
                p_i = 0

    drone_paths = [-1] * n_drones
    if n_paths == 1:
        for i in range(n_drones):
            drone_paths[i] = 0
    elif n_paths >= n_drones:
        for i in range(n_drones):
            drone_paths[i] = i
    else:
        path_fill(drone_paths, paths, g, n_drones, n_paths)
    return drone_paths


def travel(g: Graph, log: bool, multipath: bool) -> None:
    """Create a list of drones that will travel through the Graph from
    the start to the end following the paths given.

    The movement follows turn scheduling. In every turn, each drone tries
    to move to its next node in its path. The drones that successfully move
    are displayed in the output.

    Args:
        g:          the Graph object.
        log:        if True, display more information.
        multipath:  if True, assign different paths for drones.
    """
    nodes = g.nodes
    edges = g.edges
    paths = g.paths
    n_drones = g.nb_drones
    # Set the drones' path depending on the flag.
    if multipath:
        paths_d = get_drone_paths(g, paths, g.n_paths, n_drones)
        if log:
            print("Assigned")
            for i in range(n_drones):
                print(f"Drone {i} will take path {paths_d[i]}")
            print()
        drones = [Drone(ind=i, path=paths[paths_d[i]]) for i in range(n_drones)]
    else:
        drones = [Drone(ind=i, path=paths[0]) for i in range(n_drones)]
    # Set the start node with all drones in it.
    nodes[g.start].curr_drones = n_drones

    t: int = 1
    not_moved_count: int = 0
    while 1:
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
        if all_finished(drones):
            break
        t += 1
    print(f"{t} turns")


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
