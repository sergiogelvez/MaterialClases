import csv

path = "/home/sgelvez/linuxProjekte/MaterialClases/arreglos/datos.csv"
archivo = open(path)

lineas = archivo.readlines()
print(lineas)

Tabla = []
for i,linea in enumerate(lineas):
    if i > 0:
        fila = linea.strip().split(";")
        Tabla.append(fila)

print(Tabla)
print(type(Tabla))
print(len(Tabla))


with open(path, "r") as csvfile:
    reader_variable = csv.reader(csvfile, delimiter=";")
    for row in reader_variable:
        print(row)