import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter_ns

def bubble_sort(A):
    return 0

num_elements = np.arange(1000, 100001, 1000)
size = num_elements.size
print(size)
#print(num_elements)
t_bubble = np.zeros(size)
t_selection = np.zeros(size)
t_insertion = np.zeros(size)
t_quick_sort = np.zeros(size)

for i, n in enumerate(num_elements) :
    vector_ord = np.random.randint(0, 100, n, dtype=np.int16)
    t_inicio = perf_counter_ns()
    bubble_sort(vector_ord)
    t_final = perf_counter_ns()
    t_bubble[i] = t_final - t_inicio

plt.plot(num_elements, t_bubble, "g-")
plt.show()