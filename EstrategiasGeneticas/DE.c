// * funcion fitness f(x1,x2)=100*(x1^2-x2)^2+(1-x1)^2
// * los valores de x1 y x2 van de -10 a 10
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// * Estructura
typedef struct
{
  float fitness;
  float *array
} vector_DE;

void inicializa(vector_DE *poblacion, int NP, int n, float limiteInferior, float limiteSuperior);
void calculaFitness(vector_DE * poblacion, int NP);

int main(int argc, char *argv[])
{
  srand(time(NULL));
  int NP = atoi(argv[1]);
  float F = atof(argv[2]);
  float GR = atof(argv[3]);
  int G = atoi(argv[4]);
  int n = atoi(argv[5]); // Para ejemplo básico n es 2
  float limiteInferior[n];
  float limiteSuperior[n];
  printf("\nDame los limites inferior y superior para cada ", "una de tus variables (separados por una coma)");
  for (int i = 0; i < n; i++)
  {
    printf("\nParametros de la variable");
    scanf("%f, %f", &limiteInferior[i], &limiteSuperior[i]);
  }
  vector_DE *objetivo = (vector_DE *)malloc(NP * sizeof(vector_DE));
  vector_DE *ruidosos = (vector_DE *)malloc(NP * sizeof(vector_DE));
  vector_DE *prueba = (vector_DE *)malloc(NP * sizeof(vector_DE));
  inicializa(objetivo,NP,limiteInferior,limiteSuperior);
  calculaFitness(objetivo,NP);
}

void inicializa(vector_DE *poblacion, int NP, int n, float limiteInferior, float limiteSuperior)
{
  // * Reservar memoria para los arreglos de variables para cada uno de nuestros vectores
  for (int i = 0; i < NP; i++)
  {
    poblacion[i].array = (float *)malloc(n * sizeof(float));
    for (int j = 0; j < n; j++)
    {
      float aleatorio =  rand()/RAND_MAX;
      poblacion[i].array[j]=limiteInferior[j]+aleatorio*(limiteSuperior[j]-limiteInferior[j]);
    }
    
  }
}
void calculaFitness(vector_DE * poblacion, int NP){
  for (int i = 0; i < NP; i++)
  {
    float x1=poblacion->array[0];
    float x2=poblacion->array[0];
  }
  
  poblacion->fitness=100*pow(())
}