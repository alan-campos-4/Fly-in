
set1 = set([1, 9, 4, 5, 2])
set2 = set([1, 4, 5])

should_have = set([1, 2, 4, 5, 6, 8, 9])

found = set1.union(set2)
print(found)
found.add(40)
print(found)
missing = should_have.difference(found)
print(missing)