from __future__ import print_function, absolute_import

from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np
from numba import prange, set_num_threads, njit
import random

@njit(parallel=True)
def estimate_pi_par(num_samples: int) -> float:
    set_num_threads(4)    
    inside_circle = 0
    for _ in prange(num_samples):
        # Genera coordenadas aleatorias (x, y) entre -1 y 1
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        # Comprueba si el punto (x, y) está dentro del círculo
        if x**2 + y**2 <= 1:
            inside_circle += 1

    # La proporción de puntos dentro del círculo sobre el total de puntos es ~ π/4
    pi_estimate = (inside_circle / num_samples) * 4
    return pi_estimate



def estimate_pi(num_samples: int) -> float:
    inside_circle = 0

    for _ in range(num_samples):
        # Genera coordenadas aleatorias (x, y) entre -1 y 1
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        # Comprueba si el punto (x, y) está dentro del círculo
        if x**2 + y**2 <= 1:
            inside_circle += 1

    # La proporción de puntos dentro del círculo sobre el total de puntos es ~ π/4
    pi_estimate = (inside_circle / num_samples) * 4
    return pi_estimate


@cuda.jit
def compute_pi(rng_states, iterations, out):
    """Find the maximum value in values and store in result[0]"""
    thread_id = cuda.grid(1)

    # Compute pi by drawing random (x, y) points and finding what
    # fraction lie inside a unit circle
    inside = 0
    for i in range(iterations):
        x = xoroshiro128p_uniform_float32(rng_states, thread_id)
        y = xoroshiro128p_uniform_float32(rng_states, thread_id)
        if x**2 + y**2 <= 1.0:
            inside += 1

    out[thread_id] = 4.0 * inside / iterations

threads_per_block = 512
blocks = 512
iter = 100

rng_states = create_xoroshiro128p_states(threads_per_block * blocks, seed=1)
out = np.zeros(threads_per_block * blocks, dtype=np.float32)

compute_pi[blocks, threads_per_block](rng_states, iter, out)
print('pi:', out.mean())

num_samples = iter * threads_per_block * blocks  # Puedes ajustar el número de muestras para mejorar la precisión
pi_approx = estimate_pi(num_samples)
print(f"Estimación de π con {num_samples} muestras: {pi_approx}")

pi_approx = estimate_pi_par(num_samples)
print(f"Estimación de π con {num_samples} muestras: {pi_approx}")



""" 

# Ejemplo de uso

 """