

a = [
    (0, 1, 2, 6, 12, 14, 16),
    (0, 1, 2, 4, 6, 12, 14, 16),
    (0, 1, 2, 6, 12, 15, 16),
    (0, 1, 3, 4, 6, 12, 14, 16),
]
order = [7, 8, 6, 5]


Z = [x for _,x in sorted(zip(order,a))]
for p in Z:
    print(p)



(0, 1, 2, 6, 12, 14, 16)
(0, 1, 2, 6, 12, 15, 16)
(0, 1, 2, 4, 6, 12, 14, 16)
(0, 1, 3, 4, 6, 12, 14, 16)

"""
if not moved for two turns, change path
    look for curr node is same position, highest in the list
"""

(0, 1, 6, 7, 20, 23, 38, 39, 40, 47, 48, 49, 50, 51, 52, 53)
(0, 1, 6, 7, 20, 26, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53)
(0, 1, 2, 10, 11, 20, 23, 38, 39, 40, 47, 48, 49, 50, 51, 52, 53)
(0, 1, 6, 7, 20, 21, 22, 29, 30, 31, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53)

"""
if path_ind = 0 and curr_node = 2, can change to path_ind 1 or 2
if path_ind = 3 and curr_node = 4, can change to path_ind 2
"""