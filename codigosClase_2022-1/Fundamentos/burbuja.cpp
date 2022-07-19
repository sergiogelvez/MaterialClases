#include <cstdlib>
#include <iostream>
using namespace std;

int main()
{
    // semilla de los números aleatorios
    // pongo esto para no tener que introducirlos desde el teclado.

    srand(time(0));
    int n;
    int operaciones, intercambios;
    cout << "Introduzca el número de elementos del vector\n"  ;
    cin >>  n;
    // creamos un vector con números enteros aleatorios
    int lista[n], lista2[n];
    for(int i = 0; i < n; i++)
    {
        lista[i] = rand() % 100;
        lista2[i] = lista[i];
        cout << lista[i] << " ";
    }
    cout << endl;
    // Acá empezamos el ordenamiento
    int temp;
    operaciones = 0;
    intercambios = 0;
    for (int i=0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            // acá viene el posible intercambio
            operaciones++;
            if (lista[j] > lista[j+1])
            {
                // temp = lista[j];
                // lista[j] = lista[j + 1];
                // lista[j + 1] = temp;
                swap(lista[j], lista[j + 1]);
                intercambios++;
            }
        }
        // el paso interno
    }
    cout << "primera versión de ordenamiento" << endl;
    cout << "Numero de comparaciones realizadas: " << operaciones << " Intercambios: " << intercambios << endl;
    // imprimir el vector ordenado
    for(int i = 0; i < n; i++)
    {
        cout << lista[i] << " ";
    }
    cout << endl;
    operaciones = 0;
    intercambios = 0;
    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            operaciones++;
            if (lista2[i] > lista2[j])
            {
                temp = lista2[j];
                lista2[j] = lista2[i];
                lista2[i] = temp;
                intercambios++;
            }
        }
    }
    cout << "Segunda versión del ordenamiento" << endl;
    cout << "Numero de comparaciones realizadas: " << operaciones << " Intercambios: " << intercambios << endl;
    // imprimir el vector ordenado
    for(int i = 0; i < n; i++)
    {
        cout << lista2[i] << " ";
    }
    cout << endl;
    return 0;
}