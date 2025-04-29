n = int(input("Por favor introduzca el número de filas: "))
m = int(input("Por favor introduzca el número de columnas: "))

A = []
# ciclo que genera las filas a partir del n leído
for i in range(n) :
    fila = []
    # ciclo que genera las celdas por fila, es decir, el mismo número de columnas m
    for j in range(m) :
        # se lee el valor correspondiente a la celda, y se introduce en la fila, que luego se unirá a la matriz 
        fila.append(float(input(f"Introduzca el valor correspondiente a la fila {n} y la columna {m}: ")))
    # Se agrega la fila a la matriz
    A.append(fila.copy())
    
print(A)

