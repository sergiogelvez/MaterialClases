'''
Construir un programa que lea un número entero positivo y si este es primo calcule el factorial de dicho número.
'''
import math as m

n = int(input("Introduzca el número a evaluar: "))
numero_divisiones = 0
divisiones = False
if n < 2:
    print("Ni 1 ni 0 pueden ser considerados primos")
else:
    for i in range(2, n): 
        if n % i == 0:
            divisiones = True
            numero_divisiones += 1
    if divisiones > 0:
        print(f"{n} no es primo")
    else:
        factorial = 1
        for j in range(2, n):
            factorial *= j
        factorial *= n
        print(f"El factorial de {n} es {factorial}")
    print("-- Por el método de los booleanos --")
    if not divisiones:
        factorial = m.factorial(n)
        print(f"El factorial de {n} es {factorial}")
    else:
        print(f"{n} no es primo")