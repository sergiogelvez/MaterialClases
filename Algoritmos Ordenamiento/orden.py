from random import random, randrange
from time import perf_counter, perf_counter_ns
import matplotlib.pyplot as plt
import numpy as np

def partition(array, low, high):

    '''
    # choose the rightmost element as pivot
    pivot = array[high]
    '''

    '''    
    # choose a random element
    r = randrange(low, high)
    array[r], array[high] = array[high], array[r]
    pivot = array[high]
    '''
    
    
    # choose median of 3
    m = int((low + high) / 2)
    if array[m] < array[low]: 
        array[low], array[m] = array[m], array[low]
    if array[high] < array[low]:
        array[low], array[high] = array[high], array[low]
    if array[m] < array[high]:
        array[m], array[high] = array[high], array[m] 
    pivot = array[high]
    
    
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            array[i], array[j] = array[j], array[i]
 
    # Swap the pivot element with the greater element specified by i
    array[i + 1], array[high] = array[high], array[i + 1]
 
    # Return the position from where partition is done
    return i + 1

def quickSort(array, low, high):
    if low < high:
 
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)

        #print(f"Lista de la izquierda: {data[:pi]}")
        # Recursive call on the left of pivot
        quickSort(array, low, pi - 1)
        #print(f"Lista de la derecha: {data[pi:]}")
        # Recursive call on the right of pivot
        quickSort(array, pi + 1, high)
 
 
#data = [1, 7, 4, 1, 10, 9, -2]

N = [ 10, 50, 100, 200, 500, 1000, 2000, 5000, 10000 ]

T_quick = []

for n in N:
    data = [ int(n*random())  for i in range(n) ]

    print("Unsorted Array")
    print(data)
    
    size = len(data)

    t_quick_ini = perf_counter_ns()    
    quickSort(data, 0, size - 1)
    t_quick_fin = perf_counter_ns()

    T_quick.append(t_quick_fin - t_quick_ini)

    print('Sorted Array in Ascending Order:')
    print(data)

print(N)
print(T_quick)

x_values = np.array(N)
y_values = np.array(T_quick)



plt.plot(N, T_quick, "-r")
plt.show()