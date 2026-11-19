import sys
import os
import random
from collections import deque
from typing import Deque

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src.models import Graph
from src import get_data_from_file, get_adjacency_list


def remove_edge(adj_list: list[list[int]], path: list[int]) -> None:
    index = random.randint(0, len(path) - 2)
    node_a = path[index]
    node_b = path[index + 1]
    print(node_a, node_b)
    adj_list[node_a].remove(node_b)
    adj_list[node_b].remove(node_a)


def bfs(adj_list: list[list[int]],
        start: int, size: int) -> tuple[list[int], list[float]]:
    parent = [-1] * size
    dist = [1e9] * size
    dist[start] = 0
    q: Deque = deque()
    q.append(start)
    # Iterate till the queue is not empty
    while q:
        # Pop the node at the front of the queue
        node = q.popleft()
        # Explore all the neighbours of the current node
        for neighbour in adj_list[node]:
            # Check if the neighbouring node is not visited
            if dist[neighbour] == 1e9:
                # Mark the current node as the parent of
                # the neighbouring node
                parent[neighbour] = node
                # Mark the distance of the neighbouring
                # node as distance of the current node + 1
                dist[neighbour] = dist[node] + 1
                # Insert the neighbouring node to the queue
                q.append(neighbour)
    return parent, dist


def shortest_distance(adj_list: list[list[int]],
                      start: int, end: int, size: int) -> list[int]:
    parent, dist = bfs(adj_list, start, size)
    if dist[end] == 1e9:
        raise PathFindingError(
            "The start and end nodes could not be connected to each other"
        )
    path = []
    currentNode = end
    path.append(end)
    while parent[currentNode] != -1:
        path.append(parent[currentNode])
        currentNode = parent[currentNode]
    return path


if __name__ == "__main__":
    g = get_data_from_file(os.getcwd() + '/tests/path.txt')
    size = len(g.nodes)
    adj_list = get_adjacency_list(g.edges, size)
    path = shortest_distance(adj_list, g.start, g.end, size)
    for i in range(size):
        print(f"{i}: ", end='')
        print(', '.join(str(a) for a in adj_list[i]))
    print(f"Path: {path}")
    print()

    remove_edge(adj_list, path)
    for i in range(size):
        print(f"{i}: ", end='')
        print(', '.join(str(a) for a in adj_list[i]))
    new_path = shortest_distance(adj_list, g.start, g.end, size)
    print(f"New: {new_path}")

    """valid_paths = find_all_paths(adj_list, g)
    if valid_paths:
        print(f"Paths found: ")
        for path in valid_paths:
            print(", ".join([str(p) for p in path]))
        shortest = min(valid_paths, key=len)
        print(f"Shortest path: {shortest}")"""
