#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    int filas, cols, i, j, temp;
    scanf("%d", &cols);
    scanf("%d", &filas);
    size_t size = filas * cols * sizeof(float);
    float *  A;
    A = (float *)malloc(size);
    srand(time(NULL));
    for ( i = 0; i < filas; i++ )
    {
        for ( j = 0; j < cols; j++)
        {
            printf("Posicion [%d, %d]: ", i, j);
            temp = rand() % 100;
            A[i * cols + j] = temp;
            printf("%d\n", temp);
        }
    }
    for ( i = 0; i < filas; i++ )
    {
        for ( j = 0; j < cols; j++)
        {
            printf("Posicion [%d, %d] = %f\n", i, j, A[i * cols + j]);
        }
    }
    free(A);

}