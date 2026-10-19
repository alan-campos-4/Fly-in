from collections import deque
from .model_graph import Graph
from .field_exception import FieldException


def bfs(adj_list: list[list[int]],
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
    parent = [-1] * size
    dist = [1e9] * size
    dist[start] = 0
    q = deque()
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
    """Create a list containing the path with the shortest_distance
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

    parent, dist = bfs(adj_list, start, size)
    if dist[end] == 1e9:
        raise FieldException(
            "path finding", "The start and end nodes could not be connected "
            "to each other"
        )

    path = []
    currentNode = end
    path.append(end)
    while parent[currentNode] != -1:
        path.append(parent[currentNode])
        currentNode = parent[currentNode]

    return path


def get_adjacency_list(edges: list[tuple[int, int, int]],
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
    for edge in edges:
        adl[edge[0]].append(edge[1])
        adl[edge[1]].append(edge[0])
    return adl


def find_paths(g: Graph) -> list[int]:
    """Return the shortest path between the start and end nodes.
    """
    size = len(g.nodes)
    start = g.start
    end = g.end
    adj_list = get_adjacency_list(g.edges, size)
    path = shortest_distance(adj_list, start, end, size)
    return path


"""
print("Edge list")
print('\n'.join(f"({n1}, {n2})" for n1,n2,l in g.edges))
print()
print("Adjacency list")
print('\n'.join(f"{i}: {g}" for i, g in enumerate(adj_list)))
print()
print("Path")
print(','.join(f"{p}" for p in path))
"""


"""
    # ====================
    # WIKIPEDIA HEAP
    # ====================

    source: str = g.start
    dist: dict[str, float] = {}
    prev: dict[str, str] = {}
    Q = FibonacciHeap()

    dist[source] = 0
    Q.insert(source, 0)

    for v in g.nodes.keys():
        if v != source:
            prev[v] = ""
            dist[v] = float('inf')
            Q.insert(v, float('inf'))

    while not Q.is_empty():
        u = Q.extract_min()
        l = g.get_neighbors(u)
        print("For ",u," -> ",l)

        for v in l:
            alt = dist[u] # + Graph.Distance(u,v)
            if alt < dist[v]:
                prev[v] = u
                dist[v] = alt
                Q.decrease_key(v, alt)

    return dist
"""


"""
    # ====================
    # WIKIPEDIA BASIC
    # ====================

    dist: dict[str, float] = {}
    prev: dict[str, str] = {}
    heap: list[str] = []
    S: list[str] = []

    for name, node in g.nodes.items():
        dist[name] = float('inf')
        prev[name] = ""
        heappush(heap, name)
    dist[g.start] = 0

    while len(heap):
        u = heappop(heap)
        for e1, e2, l in g.edges:
            alt = dist[e1] + 1
            if alt < dist[e2]:
                dist[e2] = alt
                prev[e2] = e1

    un: str = g.end
    if prev[un] or un == g.start:
        while un:
            S.append(un)
            un = prev[un]
"""

"""
    # ====================
    # ADJ MATRIX
    # ====================

class Path:
    def __init__(self, g: Graph):
        self.names = g.nodes.keys()
        self.vertices = len(g.nodes)
        self.start = g.start
        self.matrix = {}
        for name in g.nodes.keys():
            inner = {}
            for name1 in g.nodes.keys():
                inner.update({name1: 0})
            self.matrix.update({name: inner})
        for n1, n2, l in g.edges:
            self.add_edge(n1, n2, l)

    def add_edge(self, source: str, destination: str, weight: int):
        self.matrix[source][destination] = weight
        self.matrix[destination][source] = weight

    def get_minimum_vertex(self, spt, distance):
        min_key = float('inf')
        vertex = -1
        for i in self.names:
            if not spt[i] and min_key > distance[i]:
                min_key = distance[i]
                vertex = i
        return vertex

    def dijkstra_get_min_distances(self):
        source_vertex = self.start
        spt = {name: False for name in self.names} # [False] * self.vertices
        distance = {name: float('inf') for name in self.names}

        # Start from the source vertex
        distance[source_vertex] = 0

        # Create SPT
        for _ in self.names:
            vertex_u = self.get_minimum_vertex(spt, distance)
            spt[vertex_u] = True

            for vertex_v in self.names:
                if self.matrix[vertex_u][vertex_v] > 0:
                    if (not spt[vertex_v] and
                            self.matrix[vertex_u][vertex_v] != float('inf')):
                        new_key = (self.matrix[vertex_u][vertex_v]
                                   + distance[vertex_u])
                        if new_key < distance[vertex_v]:
                            distance[vertex_v] = new_key
        # Print shortest path tree
        self.print_dijkstra(source_vertex, distance)

    def print_dijkstra(self, source_vertex, key):
        print("Dijkstra Algorithm: (Adjacency Matrix)")
        for i in self.names:
            print(f"Source Vertex: {source_vertex} to vertex {i}"
                  f" distance: {key[i]}")
"""

"""
    # ====================
    # ADJ_MARTRIX 2
    # ====================

void dijkstra(int graph[V][V], int start) {
    int dist[V];
    bool sptSet[V];
    for (int i = 0; i < V; i++) {
        dist[i] = INT_MAX;
        sptSet[i] = false;
    }
    dist[start] = 0;
    for (int count = 0; count < V - 1; count++) {
        int u = minDistance(dist, sptSet);
        sptSet[u] = true;
        for (int v = 0; v < V; v++) {
            if (!sptSet[v] && graph[u][v] && dist[u] != INT_MAX &&
                   dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
            }
        }
    }
}
"""
