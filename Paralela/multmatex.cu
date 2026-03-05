#include "stdlib.h"
#include "stdio.h"
#include "math.h"
#include "time.h"

// Matrices are stored in row-major order:
// M(row, col) = *(M.elements + row * M.width + col)

typedef struct {
	int width;
	int height;
	double* elements;
} Matrix;

// thread block size
// #define BLOCK_SIZE 16
// #define BLOCK_SIZE 4

// Forward declaration of the matrix multiplication kernel
__global__ void MatMulKernel(const Matrix A, const Matrix B, Matrix C);

// Matrix multiplication - host code
// Matrix dimensions are assumed to be multiples of BLOCK_SIZE
void MatMul(const Matrix A, const Matrix B, Matrix C) {
	// load A and B to devic memory
	Matrix d_A;
	d_A.width = A.width;
	d_A.height = A.height;
	size_t size = A.width * A.height * sizeof(double);
	cudaMalloc(&d_A.elements, size);
	cudaMemcpy(d_A.elements, A.elements, size, cudaMemcpyHostToDevice);
	Matrix d_B;
	d_B.width = B.width;
	d_B.height = B.height;
	size = B.width * B.height * sizeof(double);
	cudaMalloc(&d_B.elements, size);
	cudaMemcpy(d_B.elements, B.elements, size, cudaMemcpyHostToDevice);
	// allocate C in device memory 
	Matrix d_C;
	d_C.width = C.width;
	d_C.height = C.height;
	printf("\n\n  dimensiones de C (antes del kernel): %d, %d\n",C.width,C.height);
	size = C.width * C.height * sizeof(double);
	cudaMalloc(&d_C.elements, size);
	int BLOCK_SIZE = 16;
	// invoke kernel
	dim3 dimBlock(BLOCK_SIZE, BLOCK_SIZE);
	dim3 dimGrid(B.width / dimBlock.x, A.height / dimBlock.y);
	MatMulKernel<<<dimGrid,dimBlock>>>(d_A,d_B,d_C);
	// Read C from device memory
	cudaMemcpy(C.elements, d_C.elements, size, cudaMemcpyDeviceToHost);
	// porqueria
	int i,j;
	printf("\n\n  dimensiones de C: %d, %d\n",C.height,C.width);
	/*for (i=0; i< C.width ; ++i) 
	for (j=0; j < C.height; ++j) {			
		//printf("\n\n%f", C.elements[i*C.width+j]); 
	}*/
	
	
	// free device memory
	cudaFree(d_A.elements);
	cudaFree(d_B.elements);
	cudaFree(d_C.elements);
}

// Matrix multiplication kernel called by MatMul()
__global__ void MatMulKernel(Matrix A, Matrix B, Matrix C) {
	// each thread compute one element of C
	// by acumulating results into Cvalue
	double Cvalue = 0;
	int row = blockIdx.y * blockDim.y + threadIdx.y;
	int col = blockIdx.x * blockDim.x + threadIdx.x;
	for (int e = 0; e < A.width; ++e) {
		Cvalue = Cvalue + A.elements[row *A.width + e] * B.elements[e * B.width + col];
	}
	C.elements[row * C.width + col] = Cvalue;
}

size_t index(int filas, int cols, int ancho)
{
	return (filas *  ancho + cols);
}

int main( int argc, char** argv) {
	// crear dos matrices guardadas en row major order, y una más para el resultado
	int filas = 2048;
	int cols;
	cols = filas;

	// double A_elem, B_elem, C_elem;
	Matrix A, B, C;

	double* A_elem = new double[filas * cols];
	double* B_elem = new double[filas * cols];
	double* C_elem = new double[filas * cols];
	double* C_elem_GPU = new double[filas * cols];
	
	// vamos al ejemplo de la matriz cuadrada, 8x8
	A.width = cols;
	B.width = cols;
	C.width = cols;
	A.height = filas;
	B.height = filas;
	C.height = filas;

	int count = 0;
	int i, j, k;
	printf("\n\n\n\n\n");
	printf("\n************************************\n");
	printf("Prueba de multiplicacion de matrices");
	printf("\n************************************\n");
	// llenado de la matriz A.
	for (i=0; i< A.width ; ++i)
	{
		for (j=0; j < A.height; ++j)
		{
			A_elem[index(i, j, cols)] = rand()%10*1.0;
			
		}
	}
	// llenado de la matriz B.
	for (i=0; i< B.width ; ++i) {
		for (j=0; j < B.height; ++j) {
			B_elem[index(i, j, cols)] = rand()%10*1.0;
		}
	}
	// Ahora la impresión inicial de las dos matrices

	// La A
	count = 0;
	printf("\n\n -- Matriz A --\n");
	for (i=0; i< A.width ; ++i) {
		// printf("\n");
		for (j=0; j < A.height; ++j) {
			// printf(" %3.2f ", A_elem[index(i, j, A.width)]);
			count++;
		}
		//printf("\n");
	}
	printf("\nContador = %d", count);

	// ahora la B
	count = 0;
	printf("\n\n -- Matriz B --\n");
	for (i=0; i< B.width ; ++i) {
		// printf("\n");
		for (j=0; j < B.height; ++j) {
			// printf(" %3.2f ", B_elem[index(i, j, B.width)]);
			count++;
		}
		//printf("\n");
	}
	printf("\nContador = %d", count);

	// Creación de las matrices en memoria de la GPU
	// Cálculo del tamaño de la matriz en memoria, matriz A
	size_t size = A.width*A.height*sizeof(double);
	A.elements = (double*)malloc(size);
	// Asignación elementos uno a uno
	for (i=0; i< A.width ; ++i) {
		for (j=0; j < A.height; ++j) {
			A.elements[i*A.width+j] = A_elem[index(i, j, A.width)];
		}
	}
	// Cálculo del tamaño de la matriz en memoria, matriz B
	size = B.width*B.height*sizeof(double);
	B.elements = (double*)malloc(size);
	for (i=0; i< B.width ; ++i) {
		for (j=0; j < B.height; ++j) {
			B.elements[i*B.width+j] = B_elem[index(i, j, B.width)];
		}
	}
	// pasar la mat a la funcion MulMat
	C.elements = (double*)malloc(size);
	// aca hay que incluir el codigo que lleva control del tiempo
	clock_t tinicio, t_GPU;
	float tg,tc;
	tinicio=clock();
	//
	MatMul(A,B,C);
	//
	t_GPU=clock();
	tg = ((float)t_GPU-(float)tinicio)/CLOCKS_PER_SEC;
	printf("\n\ntiempo de procesamiento (GPU): %6.3f s\n\n",tg);
	// aca se calculó el tiempo de la GPU, ahora la prueba y la CPU




	tinicio=clock();
	//
	MatMul(A,B,C);
	//
	t_GPU=clock();
	tg = ((float)t_GPU-(float)tinicio)/CLOCKS_PER_SEC;
	printf("\n\ntiempo de procesamiento (GPU), segunda vuelta: %6.3f s\n\n",tg);


	for (i=0; i< C.width ; ++i) {
		for (j=0; j < C.height; ++j) {
			C_elem_GPU[index(i, j, C.width)] = C.elements[i * C.width + j];
		}
	}
	printf("\n -- Matrix resultante (GPU) --\n");
	for (i=0; i< C.width ; ++i) {
		//printf("\n");
		for (j=0; j < C.height; ++j) {
			// printf(" %3.2f ", C_elem_GPU[index(i, j, C.width)]);
		}
		//printf("\n");
	}


	// aca vamos a realizar la multiplicacion de matrices mediante la cpu.
	// se analizaran los resultados.
	tinicio=clock();
	//
	for (i=0; i < A.height ; ++i) {
		for (j=0; j < B.width; ++j) {
			C_elem[index(i, j, C.width)] = 0;
			for(k=0 ; k < A.width; k++) {
				//C_elem[index(i, j, C.width)] = C_elem[index(i, j, C.width)] + A_elem[index(i, k, A.width)] * B_elem[index(k, j, B.width)];
			}
		}
	}
	//
	t_GPU=clock();
	tc = ((float)t_GPU-(float)tinicio)/CLOCKS_PER_SEC;
	printf("\n\ntiempo de procesamiento (CPU): %6.3f s\n\n",tc);
	printf("\n -- Matrix resultante (CPU) - (GPU) --\n");
	for (i=0; i< C.width ; ++i) {
		// printf("\n");
		for (j=0; j < C.height; ++j) {
			//printf(" %3.2f -> %3.2f ", C_elem[index(i, j, C.width)], C.elements[index(i, j, C.width)]);
		}
		//printf("\n");
	}
}
