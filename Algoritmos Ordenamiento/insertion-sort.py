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

i = 1
while i < len(L):
    j = i
    while j > 0 and L[j - 1] > L[j]:
        #operaciones += 1
        L[j], L[j - 1] = L[j - 1], L[j]
        #intercambios += 1
        j -= 1
    i += 1
    print(f"paso {i + 1}: {L}")

print(L)
#print(f"Número de operaciones realizadas: {operaciones}.  Número de intercambios: {intercambios}")