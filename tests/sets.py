
set1 = set([1, 9, 4, 5, 2])
set2 = set([1, 4, 5])

should_have = set([1, 2, 4, 5, 6, 8, 9])

found = set1.union(set2)
print(found)
found.add(40)
print(found)
missing = should_have.difference(found)
print(missing)


print()
print()
print()


set_of_tuples = set()
set_of_tuples.add(tuple([0, 9, 8, 2, 1, 9]))
set_of_tuples.add(tuple([0, 3, 4, 2, 1, 9]))
print(set_of_tuples)
