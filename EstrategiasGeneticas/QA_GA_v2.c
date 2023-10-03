#include <stdio.h>
#include <time.h>
#include <stdlib.h>

typedef struct
{
	int *permutacion; // esto es el cromosoma
	double fitness;
} individuo;

double calculaFitness(int **matrizCostos, int **matrizDistancias, individuo *solucion, int tamanio)
{
	// el calculo de la funcion objetivo (fitness) para este problema, necesita calcular la suma de la distancia * el costo de asignacion de la fabrica a la localizacion
	double costoTotal = 0.0;
	// recorremos a la matriz de distancias
	// recorremos a nuestro arreglo de solucion
	for (int i = 0; i < tamanio; ++i)
		for (int j = 0; j < tamanio; ++j)
			costoTotal += matrizDistancias[i][j] * matrizCostos[solucion->permutacion[i]][i];
	return costoTotal;
}

void intercambia(int *A, int *B)
{
	int temporal;
	temporal = *A;
	*A = *B;
	*B = temporal;
}

void generaPoblacionInicial(individuo *solucion, int tamanio, int tamanioPoblacion)
{
	// reservamos la memoria para el arreglo de la permutacion
	for (int i = 0; i < tamanioPoblacion; ++i)
	{
		solucion[i].permutacion = (int *)malloc(tamanio * sizeof(int));
		for (int j = 0; j < tamanio; ++j)
			solucion[i].permutacion[j] = j;
		// hasta aqui hemos llenado el arreglo de la permutacion con valores de 0 a tamanio-1 --> 0,1,2,3,4,....,tamanio-1
		/*for(int j=0;j<tamanio;j++)
			printf("%d ",solucion[i].permutacion[j]);
	*/

		for (int i = tamanio - 1; i > 0; i--)
		{
			int posAleatoria = rand() % (i + 1);
			intercambia(&solucion->permutacion[i], &solucion->permutacion[posAleatoria]);
		}
		printf("\nSolución barajeada:\n"); // esta es la solucion barajeada
		for (int i = 0; i < tamanio; i++)
			printf("%d ", solucion->permutacion[i]);
	}
}

int seleccionRuleta(individuo *poblacion, int tamanioPoblacion, int sumaInversa, int tamanioInstancia)
{
	int ruleta = rand() % sumaInversa;
	int acumulado = 0;
	int posicion = 0;
	for (int i = 0; i < tamanioPoblacion; i++)
	{
		acumulado += 1 / poblacion[i].fitness;
		if (acumulado <= ruleta)
		{
			posicion = i;
		}
	}
	return posicion;
}

cruza(poblacion,tamanioPoblacion,nuevaPoblacion,tamanioInstancia,probCruza){
}

int main(int argc, char *argv[])
{ // tamanioInstancia nombreMatrizCosto nombreMatrizDistancia tamanioPoblacion generaciones probCruza
	srand(time(NULL));
	int tamanioInstancia = atoi(argv[1]); // leemos el primer parametro
	FILE *archivoCostos, *archivoDistancias;
	archivoCostos = fopen(argv[2], "r");		 // abrimos el primer archivo
	archivoDistancias = fopen(argv[3], "r"); // abrimos el segundo archivo
	// definimos la memoria para nuestro problema
	int tamanioPoblacion = atoi(argv[4]);
	int numGeneraciones = atoi(argv[5]);
	float probCruza = atof(argv[6]);
	float probMutacion = atof(argv[7]);
	int **matrizCostos = (int **)malloc(sizeof(int *) * tamanioInstancia);
	int **matrizDistancias = (int **)malloc(sizeof(int *) * tamanioInstancia);
	individuo *poblacion = (individuo *)malloc(sizeof(individuo) * tamanioPoblacion); // generamos  
	for (int i = 0; i < tamanioInstancia; ++i)
	{
		matrizCostos[i] = (int *)malloc(sizeof(int) * tamanioInstancia);
		matrizDistancias[i] = (int *)malloc(sizeof(int) * tamanioInstancia);
	}
	// leemos la informacion desde los archivos y la guardamos en las matrices
	for (int i = 0; i < tamanioInstancia; ++i)
	{
		for (int j = 0; j < tamanioInstancia; j++)
		{
			fscanf(archivoCostos, "%d ", &matrizCostos[i][j]);
			fscanf(archivoDistancias, "%d ", &matrizDistancias[i][j]);
		}
	}
	// es necesario realizar la codificación (representación de la solución)
	generaPoblacionInicial(poblacion, tamanioInstancia, tamanioPoblacion); // recuerden que siempre es aleatorio
	// calculaFitness(matrizDistancias,matrizCostos,solucionInicial,tamanioInstancia);

	for (int i = 0; i < tamanioPoblacion; i++)
	{
		calculaFitness(matrizDistancias, matrizCostos, &poblacion[i], tamanioInstancia);
	}

	individuo mejorSolucion = poblacion[0];
	for (int generaciones = 0; generaciones < numGeneraciones; generaciones++)
	{
		for (int i = 0; i < tamanioPoblacion; i++)
		{
			if (mejorSolucion.fitness > poblacion[i].fitness)
				// * Se copia el individuo completo con fitness y mutacion
				mejorSolucion.fitness = poblacion[i].fitness;
		}
	}
	individuo *nuevaPoblacion = (individuo *)malloc(sizeof(individuo) * tamanioPoblacion);
	nuevaPoblacion[0] = mejorSolucion;
	float sumaInversa = 0.0;
	for (int i = 0; i < tamanioPoblacion; i++)
	{
		sumaInversa = 1.0 / poblacion[i].fitness;
	}
	// * Ya paso por elitismo por lo que se debe completar la nueva población
	for (int i = 1; i < tamanioPoblacion; i++)
	{
		int posicionSeleccionada = seleccionRuleta(poblacion, tamanioPoblacion, sumaInversa, tamanioInstancia);
		nuevaPoblacion[i] = poblacion[posicionSeleccionada];
	}

	cruza(poblacion,tamanioPoblacion,nuevaPoblacion,tamanioInstancia,probCruza);
}
