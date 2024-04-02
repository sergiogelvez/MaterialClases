import numpy as np
import random as rnd

n = 1000

A = [0] * n

min = 1
max = 6

print(A)

for i in range(n):
    A[i] = rnd.randint(min, max)

print(A)

B = np.linspace(0, 1, 100)

C = np.arange(0, 100, 1)

print(B)
print(type(B))
print(B.shape)
print(C)
print(type(C))
print(C.shape)