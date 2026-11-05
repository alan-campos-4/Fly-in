from .model_graph import Graph


def find_edge_capacity(edge_list, start_node, next_node) -> int:
    for n1, n2, l in edge_list:
        if start_node == n1 and next_node == n2:
            return l
        elif start_node == n2 and next_node == n1:
            return l
    return -1


def move(drones, drone_i: int, curr_node: int, next_node: int) -> None:
    drones[drone_i] = next_node


def travel(g: Graph, path: list[int]) -> None:
    drone_dict = {i: g.start for i in range(g.nb_drones)}

    drone_i = 0
    curr_pos_ind = 0
    next_pos_ind = 1
    print(drone_dict)
    while next_pos_ind != (len(path)):
        max_capacity = find_edge_capacity(g.edge_list, path[curr_pos_ind], path[next_pos_ind])
        if max_capacity != -1:
            move(drone_dict, drone_i, path[curr_pos_ind], path[next_pos_ind])
            g.edge_list
            curr_pos_ind = next_pos_ind
            next_pos_ind += 1
        print(drone_dict)
