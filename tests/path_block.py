import sys
import os
from collections import deque
import random

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src.models import Graph, Node, Edge
from src import get_data_from_file, bfs


def print_adj_list(adj_list, size) -> None:
    for i in range(size):
        print(f"{i}: ", end='')
        print(', '.join(str(a) for a in adj_list[i]))


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


def get_adjacency_list(nodes: dict[int, Node], edges: dict[int, Edge],
                       size: int) -> list[list[int]]:
    adl: list[list[int]] = [[] for _ in range(size)]
    for edge in edges.values():
        zone_a = nodes[edge.node_a].zone.value
        zone_b = nodes[edge.node_b].zone.value
        if zone_a != 'blocked' and zone_b != 'blocked':
            adl[edge.node_a].append(edge.node_b)
            adl[edge.node_b].append(edge.node_a)
    return adl


if __name__ == "__main__":
    g = get_data_from_file(os.getcwd() + '/tests/path.txt')
    size = len(g.nodes)
    adj_list = get_adjacency_list(g.nodes, g.edges, size)
    print_adj_list(adj_list, size)
    path = shortest_distance(adj_list, g.start, g.end, size)
    print(path)
