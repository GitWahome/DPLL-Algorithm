import itertools
n=3
table = list(itertools.product(["false", "true", "free"] , repeat = n))
print(table)