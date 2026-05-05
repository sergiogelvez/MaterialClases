#include <iostream>
#include <cstdlib>

void imprimirArray(int *A, int n)
{
    int i;
    for (i = 0; i < n; i++)
    {
        std::cout << A[i];
        if (i != (n - 1))
        {
            std::cout << " " ;
        }
    }
}

int partition(int *A, int low, int high)
{
    // código para generar la partición
    // lo primero es generar el pivote, y hay varias maneras
    // 19/09/2023 : implementar la forma trivial, o sea, pivote al final
    int pivot = A[high];
    int i = low - 1;
    int j;
    for (j = low; j < high; ++j)
    {
        if (A[j] <= pivot)
        {
            // si se encuentra un elemento menor que el valor del pivote
            // intercambiarlo con el elemento mayor apuntado por i.
            i = i + 1;
            // cambiando el elemnto en i por el elemento en j.
            std::swap(A[i], A[j]);
        }
    }
    std::swap(A[i + 1], A[high]);
    return (i + 1);


}

void quick_sort(int *A, int low, int high)
{
    int pi;
    if (low < high)
    {
        pi = partition(A, low, high);
        quick_sort(A, low, pi - 1);
        quick_sort(A, pi + 1, high);
    }
}

int main()
{
    int i, n = 10;
    int data[n];
    srand(time(NULL));
    for (i = 0; i < n; i++)
    {
        data[i] = random() % 1000;
    }
    imprimirArray(data, n);
    quick_sort(data, 0, n - 1);
    std::cout << std::endl;
    imprimirArray(data, n);
}


