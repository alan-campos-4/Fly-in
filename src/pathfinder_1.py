from collections import deque
from typing import Deque
import random
from .models import Graph, Node, Edge


def list_difference(l: list[int], l_remove: list[int]) -> None:
    """
    Similar to set.difference
    """
    for e in l:
        if e in l_remove:
            l.remove(e)


def find_one_path(adj_list: list[list[int]], g: Graph) -> list[int]:
    """..."""
    path = []
    v_nodes = set()
    current_node = g.start
    path.append(current_node)
    v_nodes.add(current_node)
    i = 0
    iters = 100
    while i < iters:
        print(f"current node is : {current_node}")
        possible = []
        prioritized = []
        next_node = -1
        print(f" - > {adj_list[current_node]}")
        if len(adj_list[current_node]) >= 1:
            for neighbor in adj_list[current_node]:
                if neighbor not in path and neighbor not in v_nodes:
                    if g.nodes[neighbor].zone.value == 'priority':
                        prioritized.append(neighbor)
                    elif g.nodes[neighbor].zone.value != 'blocked':
                        possible.append(neighbor)
            print(f"  possible {possible}")
            print(f"  priority {prioritized}")
            if prioritized:
                next_node = random.choice(prioritized)
            elif possible:
                if v_nodes:
                    list_difference(possible, list(v_nodes))
                next_node = random.choice(possible)
        else:
            next_node = adj_list[current_node][0]
        if next_node != -1:
            print(f"    next is {next_node}")
            current_node = next_node
            path.append(next_node)
            v_nodes.add(next_node)
        else:
            if len(path) > 1:
                path.pop()
                current_node = path.pop()
                print(f"    went back to {current_node}")
            else:
                current_node = g.start
        print(path)
        if current_node == g.end:
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
    visited_nodes = set()
    visited_edges = set()
    possible_paths = []
    for _ in range(3):
        p = find_one_path(adj_list, g)
        visited_nodes = visited_nodes.union(p)
        possible_paths.append(p)
        print(f"Path:     {p}")
        print(f"v nodes: {visited_nodes}")
    return possible_paths
