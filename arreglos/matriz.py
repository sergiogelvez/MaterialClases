from random import randint
import numpy as np

def print_2dlist(L):
    filas = len(L)
    if filas > 0 :
        cols = len(L[0])
        print("[", end = "")
        for i in range(filas):
            print("[ ", end = "")
            for j in range(cols):
                print(f" {L[i][j]} ", end = "")
            if i < (filas - 1) :
                print("]")
            else :
                print("]", end="")
        print("]")
    else :
        print("La matriz no se puede imprimir porque no tiene filas")

filas1 = 3
cols1 = 3

filas2 = 3
cols2 = 3

lista2d = [ [ 0 ]*cols1 for n in range(filas1) ]

for i in range(filas1):
    for j in range(cols1):
        lista2d[i][j] = randint(1, 10)

A = [ [ 0 ]*cols1 for n in range(filas1) ]
for i in range(filas1):
    for j in range(cols1):
        A[i][j] = randint(1, 10)

B = [ [ 0 ]*cols2 for n in range(filas2) ]
for i in range(filas2):
    for j in range(cols2):
        B[i][j] = randint(1, 10)

print_2dlist(A)
print_2dlist(B)


if cols1 == filas2 :
    C = [ [ 0 ]*cols2 for n in range(filas2) ]
    for i in range(filas1):
        for j in range(cols2):
            for k in range(cols1):
                C[i][j] += A[i][k] * B[k][j]
    print_2dlist(C)
    nA = np.array(A)
    nB = np.array(B)
    nC = nA @ nB
    print(nC)
else :
    print("No se puede hacer la multiplicación ya que las dimensiones no son adecuadas")
