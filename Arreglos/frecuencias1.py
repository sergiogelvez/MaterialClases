import random as rnd

n = int(input("Número de elementos: "))
a = int(input("Límite inferior: "))
b = int(input("Límite superior: "))

lista = []
for i in range(n):
    lista.append(rnd.randint(a, b))

print(lista)

valores = []
for i in range(a, b + 1):
    valores.append(i)

print(valores)

#valores = [*range(a, b + 1)]
#print(valores)

conteos = []
for i in valores :
    conteo = 0
    for j in range(n):
        if lista[j] == i :
            conteo += 1
    conteos.append(conteo)

print(valores)
print(conteos)

suma = 0 
for i in range(len(conteos)) :
    suma += conteos[i]

if suma == n :
    print("Todo está súper")
else :
    print("Uh oh.")