#include <iostream>
#include <cstdlib>
#include <cmath>

using namespace std;

void imprimirVec(int vec[], int n)
{
    int i; 
    for (i = 0; i < n; i++)
    {
        cout << vec[i] << " ";
    }
}

int main()
{
    int i, j, t, n;
    cout << "Introduzca el número de elementos del vector: ";
    cin >> n;
    int A[n];
    srand(time(0));
    for (i = 0; i < n; i++)
    {
        A[i] = rand() % 100;
    }
    cout << "Vector original: \n"; 
    imprimirVec(A, n);
    cout << endl;
    // algoritmo de ordenamiento por inserción, versión con intercambios
    i = 1;
    while (i < n)
    {
        j = i;
        while (j > 0 && (A[j - 1] > A[j]) )
        {
            cout << "(" << A[i] << ") : ";
            swap(A[j], A[j - 1]);
            j = j - 1;
            imprimirVec(A, n);
            cout << endl;
        }
        cout << "(" << A[i] << ") : ";
        imprimirVec(A, n);
        cout << endl;
        i = i + 1;
    }
    cout << "Vector ordenado: \n";
    imprimirVec(A, n);
}

/* i ← 1
while i < length(A)
    j ← i
    while j > 0 and A[j-1] > A[j]
        swap A[j] and A[j-1]
        j ← j - 1
    end while
    i ← i + 1
end while */