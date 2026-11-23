
print()
print()
print()


set_of_tuples = set()
set_of_tuples.add(tuple([0, 9, 8, 2, 1, 9]))
set_of_tuples.add(tuple([0, 3, 4, 1, 9]))
set_of_tuples.add(tuple([0, 6, 5, 3, 4, 1, 9]))
if len(set_of_tuples) > 2:
    li = list(set_of_tuples)
    li.sort(key=len)
    print(li)
