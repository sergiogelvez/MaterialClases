import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

n = 10000 # numero de pasos de tiempo
t0 = 0
tfinal = 100
a = -9.8 # m/s2
dt = (tfinal - t0) / n
nbodies = 10 # numero de trayectorias a generar


theta = np.radians(np.random.randint(20, 85, nbodies))  # angulos aleatorios para cada una de las trayectorias
v_mag0 = np.random.randint(80, 110, nbodies) # velocidades aleatorias entre 80 y 110 para cada una de las trayectorias

# para este ejemplo no usamos diferentes puntos de partida, pero se puede arreglar luego.
r0 = np.array([0, 50])
# m, en el inicio de la gráfica

v0 = np.zeros((nbodies, 2))

for i in range(nbodies):
    v0[i, 0], v0[i, 1] = (v_mag0[i] * np.cos(theta[i])), (v_mag0[i] * np.sin(theta[i]))

print(f"La velocidad inicial en x es {v0[:, 0]} m/s")
print(f"La velocidad inicial en y es {v0[:, 1]} m/s")

# acá se inicializa con el valor de v0 la matriz que guarda las trayectorias (nbodies trayectorias)

T = np.zeros(n)
R = np.zeros((n, nbodies, 2))

T[0] = t0
# importante, el orden de los indices es pasos de tiempo, luego numero de trayectoria, finalmente coordenada

# todos arrancan en r0
for i in range(nbodies):
    R[0, i, :] = r0

# la velocidad arranca en la velocidad inicial en x
v = v0
# para numpy array que tiene un tamaño fijo, se usa un contador extra para guardar cuantos registros efectivamente se toman

print(f"paso de tiempo: {dt}")
print(f"Para t = {T[0]} | x = {R[0, :, 0]} | y = {R[0, :, 1]}")

cutoff = 0

# acá tenemos mucha flexibilidad porque el calculo de cada trayectoria se asume independiente de los demás
for i in range(1, n) : # el ciclo que recorre todos los pasos de tiempo
    for j in range(nbodies) :  # acá el ciclo que recorre cada una de las trayectorias
        # cinematica en y
        v[:, 1] = v[:, 1] + a * dt
        R[i, j, 1] = R[i - 1, j, 1] + v[j, 1] * dt
        # cinematica en x
        R[i, j, 0] = R[i -1, j, 0] + v[j, 0] * dt
        # avance del tiempo
        T[i] = T[i - 1] + dt
        # descartamos las posiciones con y negativo
        if R[i, j, 1] < 0 :
            R[i, j, 1] = 0
    # para evitar generar muchos puntos de más
    if (R[i, :, 1] <= 0).all():
        cutoff = i
        break


print(R)
print(T)
print(cutoff)

for i in range(nbodies):
    # generar cada gráfica por aparte, con lineas diferentes
    plt.plot(R[:cutoff, i, 0], R[:cutoff, i, 1])

print(R[:cutoff, i, 0])
print(R[:cutoff, i, 1])

plt.show()



