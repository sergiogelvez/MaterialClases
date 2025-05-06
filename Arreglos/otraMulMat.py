import numpy as np

A = np.array([[4,6,8],[4,5,1],[2,5,8]])
B = np.array([[1,1,1],[1,2,3],[4,5,6]])

filas1, columnas1 = A.shape
filas2, columnas2 = B.shape

print(filas1, columnas1)
print(filas2, columnas2)

if columnas1 == filas2 :
    C = np.zeros((filas1, columnas2))
    for i in range(filas1):
        for j in range(columnas2):
            for k in range(filas2):
                C[i, j] += A[i, k] * B[k, j]
    print(C)

    D = np.zeros((filas1, columnas2))
    for i in range(filas1):
        for j in range(columnas2):
            D[i,j] = sum(A[i, :] * B[:, j])
    print(D)

    E = A @ B
    print(E)


            


