from random import randint

filas = 3
cols = 3

lista2d = [ [ 0 ]*cols for n in range(filas) ]

for i in range(filas):
    for j in range(cols):
        lista2d[i][j] = randint(1, 10)

print(lista2d)