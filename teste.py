import numpy as np
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j']

r = [(i,j) for (i,j) in zip(a,x) if i >= 4]

o = [item[0] for item in r]
print(o)

# lower = [i for i in j if i >= 1]
# print(lower)