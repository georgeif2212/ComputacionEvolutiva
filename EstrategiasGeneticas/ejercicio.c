#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct
{
  int *permutacion;
  double fitness;
} individuo;

void generaSolucionInicial(individuo *solucion, int tam);
void swap(int *A, int *B);
void calculaFitness(int **matrizCostos, int **matrizDistancias, individuo *solucion, int tam);

int main(int argc, char *argv[])
{
  srand(time(NULL));
  int tamInstancia = atoi(argv[1]);
  FILE *archivoCostos, *archivoDistancias;
  archivoCostos = fopen(argv[2], "r");
  archivoDistancias = fopen(argv[3], "r");
  int tamPoblacion = atoi(argv[4]);
  int numGeneraciones = atoi(argv[5]);
  float probCruza = atof(argv[6]);
  float probMutacion = atof(argv[7]);
  // int tamCromosoma = atoi(argv[7]);

  // * Se define la memoria para el problema
  int **matrizCostos = (int **)malloc(sizeof(int *) * tamInstancia);
  int **matrizDistancias = (int **)malloc(sizeof(int *) * tamInstancia);
  individuo * poblacion=(individuo*)malloc(sizeof(individuo)*tamPoblacion);
  individuo *solucionInicial = (individuo *)malloc(sizeof(individuo));

  for (int i = 0; i < tamInstancia; i++)
  {
    matrizCostos[i] = (int *)malloc(sizeof(int) * tamInstancia);
    matrizDistancias[i] = (int *)malloc(sizeof(int) * tamInstancia);
  }

  // * Se lee la información desde los archivos y la guardamos en las matrices
  for (int i = 0; i < tamInstancia; i++)
  {
    for (int j = 0; j < tamInstancia; j++)
    {
      fscanf(archivoCostos, "%d", &matrizCostos[i][j]);
      fscanf(archivoDistancias, "%d", &matrizDistancias[i][j]);
    }
  }

  generaSolucionInicial(solucionInicial, tamInstancia);
  calculaFitness(matrizCostos, matrizDistancias, solucionInicial, tamInstancia);
}

void generaSolucionInicial(individuo *solucion, int tam)
{
  solucion->permutacion = (int *)malloc(tam * sizeof(int));
  for (int i = 0; i < tam; i++)
  {
    solucion->permutacion[i] = i;
  }
  for (int i = 0; i < tam; i++)
  {
    printf("%d ", solucion->permutacion[i]);
  }
  for (int i = 0; i < tam - 1; i++)
  {
    int posAleatoria = rand() % (i + 1);
    swap(&solucion->permutacion[i], &solucion->permutacion[posAleatoria]);
  }
  printf("\n");
  for (int i = 0; i < tam; i++)
    printf("%d ", solucion->permutacion[i]);
}

void swap(int *A, int *B)
{
  int temporal;
  temporal = *A;
  *A = *B;
  *B = temporal;
}

void calculaFitness(int **matrizCostos, int **matrizDistancias, individuo *solucion, int tam)
{
  double costoTotal = 0.0;
  for (int i = 0; i < tam; i++)
  {
    for (int j = 0; j < tam; j++)
    {
      costoTotal += matrizDistancias[i][j] * matrizCostos[solucion->permutacion[i]][i];
    }
  }
}