from collections import deque
from typing import Deque
import random
from .models import Graph, Node, Edge


def shortest_distance(adj_list: list[list[int]], nodes: dict[int, Node], 
                      start: int, end: int, size: int) -> list[int]:
    """..."""
    path = set()
    current_node = start
    path.add(current_node)
    i = 0
    iters = 100
    while i < iters:
        print(f"current node is : {current_node}")
        possible = set()
        prioritized = set()
        next_node = -1
        print(f" - > {adj_list[current_node]}")
        if len(adj_list[current_node]) >= 1:
            for neighbor in adj_list[current_node]:
                if nodes[neighbor].zone.value == 'priority':
                    prioritized.add(neighbor)
                elif nodes[neighbor].zone.value != 'blocked':
                    possible.add(neighbor)
            prioritized = prioritized - path            
            possible = possible - path
            print(f"  possible {possible}")
            print(f"  priority {prioritized}")
            if prioritized:
                next_node = random.choice(list(prioritized))
            elif possible:
                next_node = random.choice(list(possible))    
        else:
            next_node = adj_list[current_node][0]
        if next_node != -1:
            print(f"    next is {next_node}")
            current_node = next_node
            path.add(next_node)
        else:
            current_node = list(path).pop()
        print(path)
        if current_node == end:
            break
        i += 1
    return list(path)


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


def find_paths_1(g: Graph) -> list[int]:
    """Return the shortest path between the start and end nodes."""
    size = len(g.nodes)
    adj_list = get_adjacency_list(g.edges, size)
    path = shortest_distance(adj_list, g.nodes, g.start, g.end, size)
    print(f"Path: {path}")
    return list(reversed(path))
