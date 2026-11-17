from collections import deque
from typing import Deque
from .models import Graph, Node, Edge


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
            if dist[neighbor] == 1e9:
                # Mark the current node as the parent of
                # the neighboring node
                if nodes[neighbor].zone.value != 'blocked':
                    parent[neighbor] = node
                else:
                    parent[neighbor] = -1
                # Mark the distance of the neighboring
                # node as distance of the current node + 1
                dist[neighbor] = dist[node] + 1
                # Insert the neighboring node to the queue
                q.append(neighbor)
    return parent, dist


def shortest_distance(adj_list: list[list[int]], nodes: dict[int, Node],
                      start: int, end: int, size: int) -> list[int]:
    """Create a list containing the path with the shortest distance
    between the start and end nodes given.

    Args:
        adj_list:   the adjancency list of the graph.
        start:      the index of the start node.
        end:        the index of the destination node.
        size:       the number of nodes in the graph.

    Returns:
        a list with the indexes of the nodes comprising the shortest
        path, from end to start.
    """
    parent, dist = bfs(adj_list, nodes, start, size)
    print(f"        ", end='')
    print('  '.join([f"{a:02}" for a in nodes.keys()]))
    print(f"Parent: ", end='')
    print(', '.join([f"{a:02}" for a in parent]))
    print(f"dist:   ", end='')
    print(', '.join([f"{a:02}" for a in dist]))
    if dist[end] == 1e9:
        raise PathFindingError(
            "The start and end nodes could not be connected to each other"
        )
    path = []
    currentNode = start
    path.append(start)
    neighbors = []
    for i in range(size):
        if currentNode == parent[i]:
            neighbors.append(i)
    print(neighbors)
    # for n in neighbors:
    #     if nodes[n].zone.value == 'priority':
    return path


def get_adjacency_list(edges: dict[int, Edge],
                       size: int) -> list[list[int]]:
    """Return the adjacency list based on the edges of the graph.

    Args:
        edges:  the edge list from the graph
        size:   the number of node in the graph

    Return:
        the adjacency list of the graph, a list of lists where
            each element of the primary list represents a node,
            and each subsequent list is the neighbors of that node.
    """
    adl: list[list[int]] = [[] for _ in range(size)]
    for edge in edges.values():
        adl[edge.node_a].append(edge.node_b)
        adl[edge.node_b].append(edge.node_a)
    return adl


def find_paths_2(g: Graph) -> list[int]:
    """Return the shortest path between the start and end nodes."""
    size = len(g.nodes)
    adj_list = get_adjacency_list(g.edges, size)
    path = shortest_distance(adj_list, g.nodes, g.start, g.end, size)
    return list(reversed(path))
