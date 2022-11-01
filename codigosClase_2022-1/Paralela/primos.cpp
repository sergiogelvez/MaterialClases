#include <iostream>

using namespace std;

int main()
{
    int n = 10000;
    int i, cont = 0;
    for (i = 3; i < n; i++)
    {
        cout << "Número a evaluar: " << i ;
        // hallar si es primo o no
        cont = 0;
        for (int j = 1; j < i; j++)
        {
            if (i%j==0)
            {
                cont++;
            }
        }
        if (cont >= 2)
        {
            cout << " no es primo " << endl;
        }
        else
        {
            cout << " es primo " << endl;
        }
    }
}