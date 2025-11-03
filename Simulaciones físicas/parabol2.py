import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

n = 1000 # numero de pasos de tiempo
t0 = 0
tfinal = 100


a = -9.8 # m/s2
nbodies = 10 # numero de trayectorias a generar

theta = np.radians(np.random.randint(20, 85, nbodies))  # angulos aleatorios para cada una de las trayectorias
v0 = np.random.random(nbodies) * 100 # velocidades aleatorias entre 0 y 100 para cada una de las trayectorias

# para este ejemplo no usamos diferentes puntos de partida, pero se puede arreglar luego.
y0 = 50 # m
x0 = 0 # m, en el inicio de la gráfica

dt = (tfinal - t0) / n

vy0 = v0 * np.sin(theta)
vx0 = v0 * np.cos(theta)



print(f"La velocidad inicial en x es {vx0} m/s")
print(f"La velocidad inicial en y es {vy0} m/s")


t = t0
x = x0


x = np.zeros(nbodies)
y = np.zeros(nbodies)
vx = np.zeros(nbodies)
vy = np.zeros(nbodies)

#y = y0, solo que para todas las trayectorias
y = np.copy(y0)
vx = vx0
vy = vy0

T = np.zeros(n)
X = np.zeros((n, nbodies))
Y = np.zeros((n, nbodies))

T[0] = t
X[0, :] = x
Y[0, :] = y

# para numpy array que tiene un tamaño fijo, se usa un contador extra para guardar cuantos registros efectivamente se toman
i = 1

print(f"paso de tiempo: {dt}")
print(f"Para t = {t} | x = {x} | y = {y}")

while t < tfinal and y.all() > 0 and i < n : 
    vy = vy + a*dt
    y = y + vy * dt
    x = x + vx * dt
    t = t + dt
    print(f"Para t = {t} | x = {x} | y = {y}")
    for j,tray_y in enumerate(y) :
        if tray_y < 0 :
            X[i, j] = X[i - 1, j]
            Y[i, j] = 0
        else :
            X[i, j] = x[j]
            Y[i, j] = y[j]
    T[i] = t
    i += 1

""" X = np.resize(X, i)
Y = np.resize(Y, i)
T = np.resize(T, i) """

tray_final_temp = []
for i in range(n):
    tray_final_temp.append(np.array(list(zip(X[i, :], Y[i, :]))))

tray_final = np.array(tray_final_temp)
print(tray_final)
print(tray_final.shape)

tray_final_t = tray_final.T
print(tray_final_t)
print(tray_final_t.shape)


for i in range(nbodies):
    # generar cada gráfica por aparte, con lineas diferentes
    plt.plot(X[:, i], Y[:, i])

plt.show()



