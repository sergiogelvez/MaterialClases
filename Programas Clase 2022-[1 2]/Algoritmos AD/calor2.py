#include <iostream>
#include <cmath>

import numpy as np
import math
import matplotlib.pyplot as plt


def uInicial(x) :
    #return math.sqrt(math.sin(x)**2)
    return 300

dt = 0.1
m = 100
nsteps = 100
largo = 1000
dx = largo / m
tmax = nsteps * dt
cesp = 460 # en J / (Kg*K)

alpha2 = 18.8 / 1e6

print(f"El dx es {dx}, el dt es {dt} y el tiempo máximo es {tmax}")
    
if (dt <= (dx * dx) / 2) :
    U = np.zeros([m, nsteps])

    for i in range(m):
        U[i, 0] = uInicial(i * dx)
    
    # condiciones de frontera

    for j in range(0,nsteps):
        U[0, j] = 273
        U[m - 1, j] = 10000

    # bucle principal
    for j in range (nsteps-1):
        for i in range(1,m-1):
            U[i, j + 1] = U[i, j] + alpha2 * (dt / (dx * dx)) * (U[i + 1, j] - 2 * U[i, j] + U[i - 1, j])
    print(U)
    plt.imshow(U.T, cmap='hot')
    plt.colorbar()
    plt.show()
    

else:
    
    print("Los parámetros de dx y dt no permiten la convergencia.  Fin del programa")
    