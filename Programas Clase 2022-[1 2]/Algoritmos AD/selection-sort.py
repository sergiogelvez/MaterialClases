import random as rnd

n = 10
L = []
for i in range(n):
    L.append(int(30*rnd.random()))
print(L)
for i in range(len(L) - 1):
    min = i
    for j in range(i + 1, len(L)):
        if (L[min] > L[j]):
            min = j
    if min != i:
        L[min], L[i] = L[i], L[min]
    print(f"paso {i + 1}: {L}") 