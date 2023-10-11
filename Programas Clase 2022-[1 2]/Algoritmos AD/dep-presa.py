import matplotlib.pyplot as plt
import numpy as np
import curses as cl

def dir_a_coord(dir):
    # direcciones:
    # | 0 | 1 | 2 |
    # | 7 | x | 3 |
    # | 6 | 5 | 4 |
    match dir:
        case 0:
            return -1, -1
        case 1:
            return 0, -1
        case 2:
            return 1, -1
        case 3:
            return 1, 0
        case 4:
            return 1, 1
        case 5:
            return 0, 1
        case 6:
            return -1, 1
        case 7:
            return -1, 0
        
def revisar_posicion(i, j):
    global campo, campo_prox
    if campo[i, j] != 0:
        return False
    else:
        return True



n = 100
cols = n
filas = n
max_depredadores = 20
max_presas = 50
t_nat_presas = 0.2
t_nat_depredador = 0.1
t_caza = 0.4
t_competencia = 0.1


DEP = []
PRE = []

t = 0
T_MAX = 1000

# creación del espacio de simulación
# 0 - espacio vacio
# 1 - depredador
# 2 - presa
campo = np.zeros((filas, cols))
campo_prox = np.zeros((filas, cols))
i = 0
while  i < max_depredadores :
    x = np.random.randint(0, cols)
    y = np.random.randint(0, filas)
    if campo[y, x] != 0:
        i = i - 1
    else :
        campo[y, x] = 1
    i += 1

i = 0 
while  i < max_presas :
    x = np.random.randint(0, cols)
    y = np.random.randint(0, filas)
    if campo[y, x] != 0:
        i = i - 1
    else :
        campo[y, x] = 2
    i += 1

#ciclo principal
while t < T_MAX:
    for i in range(filas):
        for j in range(cols):
            # movimiento de cada actor en cada celda:
            # reglas de prelación:
            # izquierda > derecha, arriba > abajo, presas se mueven antes que el depredador.  Muertes ocurren antes que nacimientos.
            # direcciones:
            # | 0 | 1 | 2 |
            # | 7 | x | 3 |
            # | 6 | 5 | 4 |
            if campo[i, j] == 2:
                # reglas para las presas.
                direccion = np.random.randint(0, 8)
                print(f'tiempo {t}, direccion {direccion}')
                match direccion:
                    case 0:
                        # revisar bordes y existencia de otro actor
                        if (i - 1 >=0 and j - 1 >=0) :
                            if campo[i-1, j-1] == 0 :
                                # esto representa que se movió a una casilla válida que estaba vacía
                                campo_prox[i - 1, j - 1] == 2
                                campo_prox[i, j] == 0
                            elif campo[i-1, j-1] == 1 :
                                # posibilidad de caer en cacería
                                p = np.random.random()
                                if p < 1 - t_caza :
                                    # casa exitosa
                                    campo_prox[i, j] == 0
                                    campo[i, j] == 0
                            elif campo[i-1, j-1] == 2 :
                                # posibilidad de reproducirse
                                p = np.random.random()
                                if p < t_nat_presas :
                                    # reproducción
                                    # poner otra presa en una casilla adyacente al azar
                                    temp_dir = np.random.randint(0, 8)
                                    temp_offset = dir_a_coord(temp_dir)
                                    print(i + temp_offset[0], j + temp_offset[1] )
                                    if revisar_posicion(i + temp_offset[0], j + temp_offset[1] ) :
                                        campo[i + temp_offset[0], j + temp_offset[1] ] = 2



    # campo_prox se vuelve el actual
    campo = campo_prox

# porción de código para contar depredadores y presas en un tiempo t
presas_t = np.where(campo == 2)
depredadores_t = np.where(campo == 1)
PRE.append(len(presas_t[0]))
DEP.append(len(depredadores_t[0]))
print(DEP)
print(PRE)
#print(sum(sum(campo)))