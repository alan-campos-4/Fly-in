from collections import deque
from typing import Deque
import random
from .models import Graph, Node, Edge


def print_adj_list(adj_list, size) -> None:
    for i in range(size):
        print(f"{i}: ", end='')
        print(', '.join(str(a) for a in adj_list[i]))


class PathFindingError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def bfs(adj_list: list[list[int]], nodes: dict[int, Node],
        start: int, size: int) -> tuple[list[int], list[float]]:
    """Iterate through the graph grid to find the distance between the nodes
    and the parent of each node applying the Breadth First Search algorithm.

    Args:
        adj_list:   the adjacency list of the graph.
        start:      the index of start node.
        size:       the number of nodes in the graph.

    Returns:
        parent: a list containing the parent of each node.
        dist:   a list containing the distance of each node to the start.
    """
    parent = [-2] * size
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
            # Check if the neighboring node is a priority node
            # which has been visited
            elif (nodes[neighbor].zone.value == 'priority'):
                # Set the neihboring node as the parent of the current node 
                parent[node] = neighbor
                # print(f"{neighbor} is the parent of {node}")
    return parent, dist


def shortest_distance(adj_list: list[list[int]], nodes: dict[int, Node],
                      start: int, end: int, size: int) -> list[int]:
    """Create a list of nodes indexes describing the shortest distance
    from end to the start nodes given.

    Args:
        adj_list:   the adjancency list of the graph.
        start:      the index of the start node.
        end:        the index of the destination node.
        size:       the number of nodes in the graph.

    Returns:
        a list with the indexes of the nodes comprising the shortest
        path, from end to start.

    Raises:

    """
    # print_adj_list(adj_list, size)
    parent, dist = bfs(adj_list, nodes, start, size)
    """print(f"        ", end='')
    print('  '.join([f"{a:02}" for a in nodes.keys()]))
    print(f"Parent: ", end='')
    print(', '.join([f"{a:02}" for a in parent]))
    print(f"dist:   ", end='')
    print(', '.join([f"{a:02}" for a in dist]))"""
    if dist[end] == 1e9:
        raise PathFindingError(
            "The start and end nodes could not be connected to each other"
        )
    path = []
    currentNode = end
    path.append(end)
    while parent[currentNode] != -2:
        path.append(parent[currentNode])
        currentNode = parent[currentNode]
    return path


def get_adjacency_list(nodes: dict[int, Node], edges: dict[int, Edge],
                       size: int) -> list[list[int]]:
    """Return the adjacency list based on the nodes and edges of the graph.

    Args:
        nodes:  the graphs' nodes.
        edges:  the graph's edges.
        size:   the number of node in the graph

    Return:
        the adjacency list of the graph, a list of lists where
            each element of the primary list represents a node,
            and each subsequent list is the neighbors of that node.
    """
    adl: list[list[int]] = [[] for _ in range(size)]
    for edge in edges.values():
        zone_a = nodes[edge.node_a].zone.value
        zone_b = nodes[edge.node_b].zone.value
        if zone_a != 'blocked' and zone_b != 'blocked':
            adl[edge.node_a].append(edge.node_b)
            adl[edge.node_b].append(edge.node_a)
    return adl


def remove_edge(adj_list: list[list[int]], path: list[int]) -> None:
    """Select two random nodes of the given path and delete their
    connected positions in the adjacency list, effectively removing an edge.

    Args:
        adj_list:   the adjacency list of a Graph.
        path:       the path from which the random node is selected.

    Returns:
        a new adjancency list with and 'edge' removed.
    """
    new_a = adj_list.copy()
    index = random.randint(0, len(path) - 2)
    node_a = path[index]
    node_b = path[index + 1]
    print(node_a, node_b)
    new_a[node_a].remove(node_b)
    new_a[node_b].remove(node_a)
    return new_a


def check_edge_remove(adj_list: list[list[int]]) -> dict[int, list[int]]:
    """Check if the adjancency list contains nodes whose edges can be
    removed without making a path impossible.

    Args:
        adj_list:   the adjacency list of a Graph.

    Returns:
        a dict containing the indexes of nodes with 3 or more edges,
            as well as said edges.
    """
    removable = {}
    for i in range(len(adj_list)):
        if len(adj_list[i]) >= 3:
            removable.update({i: adj_list[i]})
    return removable


def find_paths(g: Graph) -> list[list[int]]:
    """
    Find the shortest path between the start and end nodes.
    Once found, modify the adjacency list to attempt to find an alternate
    path of similar length.

    Returns:
        a set containing a series of paths between the start and end nodes.
    """
    valid_paths = []
    size = len(g.nodes)
    adj_list = get_adjacency_list(g.nodes, g.edges, size)
    path = shortest_distance(adj_list, g.nodes, g.start, g.end, size)
    path.reverse()
    print(path)
    valid_paths.append(path)
    removable_nodes = check_edge_remove(adj_list)
    while removable_nodes:
        node_a = random.choice(list(removable_nodes.keys()))
        node_b = random.choice(removable_nodes[node_a])
        adj_list[node_a].remove(node_b)
        adj_list[node_b].remove(node_a)
        try:
            new_path = shortest_distance(adj_list, g.nodes,
                                         g.start, g.end, size)
            new_path.reverse()
            valid_paths.append(path)
        except PathFindingError:
            adj_list[node_a].append(node_b)
            adj_list[node_b].append(node_a)
    return valid_paths
