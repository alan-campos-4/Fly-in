
def print_adj_list(adj_list, size) -> None:
    for i in range(size):
        print(f"{i}: ", end='')
        print(', '.join(str(a) for a in adj_list[i]))
    print()


if __name__ == "__main__":
    adj_list = [
        [1],
        [0, 2, 3],
        [1, 4],
        [1, 4],
        [2, 3]
    ]
    adj_setlist = [set(a for a in item) for item in adj_list]
    size = len(adj_list)

    node_a = 1
    node_b = 2
    adj_setlist[node_a].remove(node_b)
    adj_setlist[node_b].remove(node_a)
    print_adj_list(adj_setlist, size)
    adj_setlist[node_a].add(node_b)
    adj_setlist[node_b].add(node_a)
    print_adj_list(adj_setlist, size)

    node_a = 2
    node_b = 4
    adj_setlist[node_a].remove(node_b)
    adj_setlist[node_b].remove(node_a)
    print_adj_list(adj_setlist, size)
    adj_setlist[node_a].add(node_b)
    adj_setlist[node_b].add(node_a)
    print_adj_list(adj_setlist, size)

    print_adj_list(adj_list, size)
