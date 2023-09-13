#include <stdio.h>
#include <time.h>
#include <stdlib.h>

typedef struct
{
    int *cromosoma;
    int fitness;
} individuo;

void generaPoblacionInicial(individuo *poblacion, int tamPoblacion, int tamCromosoma);
void funcionFitness(individuo *poblacion, int tamPoblacion, int tamCromosoma);
void cruza(individuo *poblacion, int tamPoblacion, int tamCromosoma);
void mutar(individuo *poblacion, int tamPoblacion, int tamCromosoma, float probMutacion);

int main(int argc, char *argv[])
{ // * Para trabajar con los parametros de main
    // *Los parametros son tamPoblación, numGeneraciones, probMutacion, tamCromosoma
    int tamPoblacion = atoi(argv[1]);
    int numGeneraciones = atoi(argv[2]);
    float probMutacion = atof(argv[3]);
    int tamCromosoma = atoi(argv[4]);

    // ? Reservar memoria para la poblacion
    individuo *poblacion = (individuo *)malloc(sizeof(individuo) * tamPoblacion);
    generaPoblacionInicial(poblacion, tamPoblacion, tamCromosoma);
    funcionFitness(poblacion, tamPoblacion, tamCromosoma);

    int iteracion = 0;
    while (iteracion < numGeneraciones)
    {

        // * Seleccion de padres

        // * Cruza
        cruza(poblacion, tamPoblacion, tamCromosoma);
        
        // * Mutacion
        mutar(poblacion, tamPoblacion, tamCromosoma, probMutacion);
        
        // * Seleccion elitista
        
        iteracion++;
    }

    for (int i = 0; i < tamPoblacion; i++)
    {
        printf("\nIndividuo %d con fitness %d y con cromosomas:",i,poblacion[i].fitness);
        for (int j = 0; j < tamCromosoma; j++)
        {
            printf("%i",poblacion[i].cromosoma[j]);
        }
    }
}

void generaPoblacionInicial(individuo *poblacion, int tamPoblacion, int tamCromosoma)
{
    srand(time(NULL)); // * Con srand se define la semilla para generar numeros pseudoaleatorios
    for (int i = 0; i < tamPoblacion; ++i)
    {
        //* Se reserva memoria para los cromosomas
        poblacion[i].cromosoma = (int *)malloc(sizeof(int) * tamCromosoma);

        for (int j = 0; j < tamCromosoma; ++j)
        {
            // * Se generan numeros aleatorios que son solo 1 y 0
            poblacion[i].cromosoma[j] = rand() % 2;
        }
    }
}

void funcionFitness(individuo *poblacion, int tamPoblacion, int tamCromosoma)
{
    for (int i = 0; i < tamPoblacion; ++i)
    {
        int decimal = 0;
        // * Base es la variable que ayuda a calcular la posicion del gen en el
        //* cromosoma y así poder dar el valor en base 10
        int base = 1;

        for (int j = tamCromosoma; j >= 0; j--)
        {
            decimal += poblacion[i].cromosoma[j] * base;
            base *= 2;
        }
        poblacion[i].fitness = decimal;
    }
}

void cruza(individuo *poblacion, int tamPoblacion, int tamCromosoma)
{
    // * Padres: indices de los elementos de la población
    int padre1, padre2;

    int puntoCruza;
    srand(time(NULL));
    padre1 = rand() % tamPoblacion;
    padre2 = rand() % tamPoblacion;
    puntoCruza = rand() % tamPoblacion;

    int *hijo1 = (int *)malloc(tamCromosoma * sizeof(int));
    int *hijo2 = (int *)malloc(tamCromosoma * sizeof(int));
    for (int j = 0; j < tamCromosoma; j++)
    {
        // * hacer una copia
        hijo1[j] = poblacion[padre1].cromosoma[j];
        hijo2[j] = poblacion[padre2].cromosoma[j];
    }

    for (int j = puntoCruza; j < tamCromosoma; j++)
    {
        // * copiar lo del padre 1 desde el punto de cruza al padre 2
        hijo1[j] = poblacion[padre2].cromosoma[j];
        hijo2[j] = poblacion[padre1].cromosoma[j];
    }

    for (int j = 0; j < puntoCruza; j++)
    {
        // * copiar lo del padre 2 hasta el punto de cruza al padre 1
        poblacion[padre1].cromosoma[j] = hijo1[j];
        poblacion[padre2].cromosoma[j] = hijo2[j];
    }
    funcionFitness(poblacion,tamPoblacion,tamCromosoma);
}

void mutar(individuo *poblacion, int tamPoblacion, int tamCromosoma, float probMutacion)
{
    for (int i = 0; i < tamPoblacion; i++)
    {
        for (int j = 0; j < tamCromosoma; j++)
        {
            float probabilidad = (float)rand() / RAND_MAX;
            if (probabilidad < probMutacion)
            {
                poblacion[i].cromosoma[j] = (poblacion[i].cromosoma[j] + 1) % 2;
            }
        }
    }
}