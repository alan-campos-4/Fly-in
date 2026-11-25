from collections import deque
from typing import Deque
import random
from .models import Graph, Node, Edge


def print_adj_list(adj_list: list[set[int]], size: int) -> None:
    for i in range(size):
        print(f"{i}: ", end='')
        for a in adj_list[i]:
            print(f"{a}, ", end='')
        print()


class PathFindingError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def bfs(adj_list: list[set[int]], nodes: dict[int, Node],
        start: int, size: int) -> tuple[list[int], list[float]]:
    """Iterate through the graph to find the distance between the nodes
    and the parent of each node applying the Breadth First Search algorithm.

    Args:
        adj_list:   the adjacency list of the graph.
        start:      the index of start node.
        size:       the number of nodes in the graph.

    Returns:
        parent: a list containing the parent of each node.
        dist:   a list containing the distance of each node to the start.
    """
    parent = [-1] * size
    dist = [1e9] * size
    dist[start] = 0
    q: Deque = deque()
    q.append(start)
    # Iterate till the queue is not empty
    while q:
        # Pop the node at the front of the queue
        node = q.popleft()
        # Explore all the neighbors of the current node
        for neighbor in adj_list[node]:
            # Check if the neighboring node is not visited
            if (dist[neighbor] == 1e9):
                # Mark the current node as the parent of
                # the neighboring node
                parent[neighbor] = node
                # Mark the distance of the neighboring
                # node as distance of the current node + 1
                dist[neighbor] = dist[node] + 1
                # Insert the neighboring node to the queue
                q.append(neighbor)
            # If it has been visited,
            # check if the neighboring node is a priority node,
            # and is not already the parent of this node.
            elif (nodes[neighbor].zone.value == 'priority'
                    and parent[neighbor] != node):
                # Set the neihboring node as the parent of the current node
                parent[node] = neighbor
    return parent, dist


def shortest_distance(adj_list: list[set[int]], nodes: dict[int, Node],
                      start: int, end: int, size: int) -> tuple[int, ...]:
    """Create a list of nodes indexes describing the shortest distance
    from start to the end nodes given.

    Args:
        adj_list:   the adjancency list of the graph.
        start:      the index of the start node.
        end:        the index of the destination node.
        size:       the number of nodes in the graph.

    Returns:
        a list with the indexes of the nodes comprising the shortest
            path, from start to end.

    Raises:
        PathFindingError: if end node could not be reached.
    """
    parent, dist = bfs(adj_list, nodes, start, size)
    """
    print(f"        ", end='')
    print('  '.join([f"{a:02}" for a in nodes.keys()]))
    print(f"Parent: ", end='')
    print(', '.join([f"{a:02}" for a in parent]))
    print(f"dist:   ", end='')
    print(', '.join([f"{a:02}" for a in dist]))
    """
    if dist[end] == 1e9:
        raise PathFindingError(
            "The start and end nodes could not be connected to each other"
        )
    path = []
    currentNode = end
    path.append(end)
    i = 0
    while parent[currentNode] != -1 and i < size:
        path.append(parent[currentNode])
        currentNode = parent[currentNode]
        i += 1
    path.reverse()
    return tuple(path)


def get_adjacency_list(nodes: dict[int, Node], edges: dict[int, Edge],
                       size: int) -> list[set[int]]:
    """Return the adjacency list based on the nodes and edges of the graph.

    Args:
        nodes:  the graphs' nodes.
        edges:  the graph's edges.
        size:   the number of node in the graph

    Return:
        the adjacency list of the graph, a list of sets where
            each element of the primary list represents a node,
            and each set is the neighbors of that node.
    """
    adl: list[set[int]] = [set() for _ in range(size)]
    for edge in edges.values():
        zone_a = nodes[edge.node_a].zone.value
        zone_b = nodes[edge.node_b].zone.value
        if zone_a != 'blocked' and zone_b != 'blocked':
            adl[edge.node_a].add(edge.node_b)
            adl[edge.node_b].add(edge.node_a)
    return adl


def check_edge_remove(adj_list: list[set[int]], nodes: dict[int, Node],
                      start: int, end: int,
                      size: int) -> dict[int, set[int]]:
    """Find any node in the adjancency list with removable edges.

    In order for a path to be made between any two nodes, there must be
    a minimum amount of edges (1 for the start and end, and 2 for the rest).
    All other edges are considered to be removable.

    Args:
        adj_list:   the adjacency list of the Graph.
        start:      the Graph's start node.
        end:        the Graph's end node.
        size:       the number of nodes in the Graph.

    Returns:
        a dict containing the of the nodes whose edges can be
            removed, and their neighboring nodes.
    """
    removable = {}
    for i in range(size):
        neighbors = adj_list[i]
        if len(neighbors) > 1 and (i == start or i == end):
            removable.update({i: set(neighbors)})
        elif len(neighbors) > 2:
            removable.update({i: set(neighbors)})
    return removable


def sort_path_by_costs(paths: list[tuple[int, ...]],
                       nodes: dict[int, Node]) -> list[tuple[int, ...]]:
    """Sort the paths in accordance to their cost. The length of each path
    as well as any restricted nodes within it will increase its cost.

    Args:
        paths:  the list of paths.
        nodes:  the Graph's nodes.

    Returns:
        the list of paths sorted.
    """
    n_paths = len(paths)
    costs = [0 for _ in range(n_paths)]
    for i in range(n_paths):
        for p in paths[i]:
            zone = nodes[p].zone.value
            if zone == 'restricted':
                costs[i] += 2
            else:
                costs[i] += 1
    sorted_paths = [x for _, x in sorted(zip(costs, paths))]
    return sorted_paths


def find_paths(g: Graph) -> list[tuple[int, ...]]:
    """
    Find the shortest path between the start and end nodes.
    Once found, it will try to find alternate paths.

    If a graph is found to have removable edges, then it will enter a loop.
    This loops temporarily removes an edge from the adjancency list,
    and tries to find a new path with the altered list. Then it starts
    again with a different edge.
    Once all possible removable edges have been tried, the loop ends.

    Returns:
        a list containing one or more paths between the start and end nodes,
            ordererd by cost.

    Raises:
        PathFindingError:   if the Graph is not solvable.
    """
    valid_paths: list[tuple[int, ...]] = []
    nodes: dict[int, Node] = g.nodes
    start: int = g.start
    end: int = g.end
    size: int = len(g.nodes)
    adj_list = get_adjacency_list(nodes, g.edges, size)
    # print_adj_list(adj_list, size)
    path = shortest_distance(adj_list, nodes, start, end, size)
    valid_paths.append(path)

    removable_edges = check_edge_remove(adj_list, nodes, start, end, size)
    if removable_edges:
        # Before the loop, randomly select a node.
        node_a = random.choice(list(removable_edges.keys()))
        while 1:
            # At the start of the loop, randomly select one of the
            # node's neighbors, and remove them both from the adj_list.
            node_b = random.choice(list(removable_edges[node_a]))
            adj_list[node_a].remove(node_b)
            adj_list[node_b].remove(node_a)
            # Try to find a new path with the reduced adj_list.
            # If the path is solvable and not redundant,
            # add it to the valid paths.
            try:
                new_path = shortest_distance(adj_list, nodes,
                                             start, end, size)
                if new_path not in valid_paths and len(new_path) <= size:
                    valid_paths.append(new_path)
            except PathFindingError:
                pass
            # After checking if the new path is possible,
            # restore the adj_list to its previous state.
            adj_list[node_a].add(node_b)
            adj_list[node_b].add(node_a)
            # First, remove the neighbor used.
            # If this leaves the node with no neighbors, remove the node.
            #  If there are still other nodes in the dict, choose another.
            #  If there are no more nodes, end the loop.
            removable_edges[node_a].remove(node_b)
            if not removable_edges[node_a]:
                removable_edges.pop(node_a)
                if removable_edges:
                    node_a = random.choice(list(removable_edges.keys()))
                else:
                    break
    return sort_path_by_costs(valid_paths, nodes)
