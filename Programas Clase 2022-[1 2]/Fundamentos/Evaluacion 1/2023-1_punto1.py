'''
Construir un programa que lea un número entero positivo n y después lea, uno a uno, n valores. 
El resultado que entregara el programa es la media de los números impares de entre los leídos, 
es decir, la suma de todos los valores impares leídos dividida por la cantidad de estos.
Implementarlo ya sea usando listas o sin usarlas.
'''

n = int(input("Número de elementos, por favor: "))
suma_impares = 0.0
n_impares = 0
lista_completa = []
lista_impares = []
for i in range(n):
    valor_leido = int(input("Introduzca un valor: "))
    lista_completa.append(valor_leido)
    if (valor_leido % 2 != 0):
        suma_impares += valor_leido
        n_impares += 1
        lista_impares.append(valor_leido)
if n_impares > 0:
    promedio_impar = suma_impares / n_impares
    print(f'promedio de los impares: {promedio_impar}')
else:
    print(f'no hay impares')
    
print("-- Solución por listas --")
if len(lista_impares) > 0:
    print(f'promedio de los impares: {sum(lista_impares) / len(lista_impares)}, con {len(lista_impares)} elementos.')
    print(lista_impares)
else:
    print(f'no hay impares')

print(lista_completa)
