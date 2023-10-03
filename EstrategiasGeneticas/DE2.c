// funcion fitness f(x1,x2)=100*(x1^2-x2)^2+(1-x1)^2
// los valores de x1 y x2 van de -10 a 10
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
typedef struct
{
	float fitness;
	float *arreglo;
} vector_DE;

void mutacion(vector_DE *objetivo, vector_DE *ruidoso, int NP, float F, int n, float limiteInferior[], float limiteSuperior[])
{
	for (int i = 0; i < NP; i++)
	{
		ruidoso[i].arreglo = (float *)malloc(n * sizeof(float));
	}

	// vamos a elegir a 3 vectores aleatoriamente y deben ser distintos entre si
	int aleatorioa = 0, aleatoriob = 0, aleatorioc = 0;
	for (int i = 0; i < NP; ++i)
	{
		while (aleatorioa == aleatoriob || aleatorioa == aleatorioc || aleatoriob == aleatorioc)
		{
			aleatorioa = rand() % NP;
			aleatoriob = rand() % NP;
			aleatorioc = rand() % NP;
		}
		for (int j = 0; j < n; j++)
		{
			ruidoso[i].arreglo[j] = objetivo[aleatorioc].arreglo[j] + F * (objetivo[i].arreglo[aleatorioa] - objetivo[i].arreglo[aleatoriob]); // xc+F*(xa-xb)
			if (ruidoso[i].arreglo[j] < limiteInferior[j])
				ruidoso[i].arreglo[j] = limiteInferior[j];

			if (ruidoso[i].arreglo[j] > limiteSuperior[j])
				ruidoso[i].arreglo[j] = limiteSuperior[j];
		}
	}
}
void calculaFitness(vector_DE *poblacion, int NP)
{
	// vamos a evaluar a f(x1,x2)=100*(x1^2-x2)^2+(1-x1)^2
	for (int i = 0; i < NP; ++i)
	{
		float x1 = poblacion[i].arreglo[0]; // porque esta funcion no es dinamica en su dimension, lo hacemos de esta forma
		float x2 = poblacion[i].arreglo[1];
		poblacion[i].fitness = 100 * (pow((x1 * x1 - x2), 2) + pow((1 - x1), 2));
	}
}
void inicializa(vector_DE *poblacion, int NP, int n, float limiteInferior[], float limiteSuperior[])
{
	// tenemos que reservar la memoria para los arreglos de variables
	// para cada uno de nuestros vectores
	for (int i = 0; i < NP; ++i)
	{
		poblacion[i].arreglo = (float *)malloc(n * sizeof(float));
		// ahora si, los llenamos
		for (int j = 0; j < n; ++j)
		{
			double aleatorio = (double)rand() / RAND_MAX; // generamos un aleatorio entre 0 y 1
			poblacion[i].arreglo[j] = limiteInferior[j] + aleatorio * (limiteSuperior[j] - limiteInferior[j]);
		}
	}
}
int main(int argc, char *argv[])
{
	srand(time(NULL));
	int NP = atoi(argv[1]);	  // tamanio de la poblacion
	float F = atof(argv[2]);  // tasa de mutacion (0.5)-->esta puede variar entre 0 y 2
	float GR = atof(argv[3]); // tasa de cruza (0.5)--> esta puede variar entre 0 y 1
	int G = atoi(argv[4]);	  // numero de generaciones
	int n = atoi(argv[5]);	  // dimension de la funcion
	float limiteInferior[n];
	float limiteSuperior[n];
	printf("\nDame los limites inferior y superior para cada una de tus variables (separados por una coma):\n");
	for (int i = 0; i < n; ++i)
	{
		printf("\nParametros de la variable %d:", i + 1);
		scanf("%f,%f", &limiteInferior[i], &limiteSuperior[i]);
	}
	// para nuestro ejemplo basico n=2
	// definimos la memoria dinamica para los arreglos de vectores
	vector_DE *objetivo = (vector_DE *)malloc(NP * sizeof(vector_DE));
	vector_DE *ruidosos = (vector_DE *)malloc(NP * sizeof(vector_DE));
	vector_DE *prueba = (vector_DE *)malloc(NP * sizeof(vector_DE));
	// inicializamos a los vectores objetivo (poblacion inicial)
	inicializa(objetivo, NP, n, limiteInferior, limiteSuperior);
	calculaFitness(objetivo, NP); // mandamos a evaluar a todos porque nos conviene hacerlo de un jalón
	// vamos a imprimir a nuestro vector objetivo con su calculo del fitness
	printf("\nVectores objetivo");
	for (int i = 0; i < NP; ++i)
	{
		printf("\nYo soy el vector objetivo %d", i + 1);
		for (int j = 0; j < n; ++j)
		{
			printf("\n%f ", objetivo[i].arreglo[j]);
		}
		printf("\nY mi fitness es: %f", objetivo[i].fitness);
	}
	// vamos a mutar
	for (int i = 0; i < G; ++i)
	{ // este ciclo nos sirve para controlar las iteraciones
		mutacion(objetivo, ruidosos, NP, F, n, limiteInferior, limiteSuperior);
		// cruza
		// seleccion
	}
}
