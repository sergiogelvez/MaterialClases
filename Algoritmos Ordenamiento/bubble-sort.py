import random as rnd

n = 10
L = []
for i in range(n):
    L.append(int(30*rnd.random()))
print(L)

'''
operaciones = 0
intercambios = 0
'''

n = len(L)
for i in range(n - 1):
    for j in range(n - i - 1):
        #operaciones += 1
        if L[j] > L[j + 1]:
            L[j], L[j + 1] = L[j + 1], L[j]
            #intercambios += 1
    print(f"paso {i + 1}: {L}")

print(L)
#print(f"Número de operaciones realizadas: {operaciones}.  Número de intercambios: {intercambios}")
