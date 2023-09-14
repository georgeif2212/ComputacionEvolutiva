#include <stdio.h>
#include <time.h>
#include <stdlib.h>

typedef struct
{
    // * Individuos formados por genes "reales"
    double *cromosoma;
    double fitness;
} individuo;

void generaPoblacionInicial(individuo *poblacion, int tamPoblacion, int tamCromosoma, double min, double max);
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
    double min = atof(argv[5]);
    double max = atof(argv[6]);

    // ? Reservar memoria para la poblacion
    individuo *poblacion = (individuo *)malloc(sizeof(individuo) * tamPoblacion);
    generaPoblacionInicial(poblacion, tamPoblacion, tamCromosoma, min, max);
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
        printf("\nIndividuo %d con fitness %lf y con cromosomas:", i, poblacion[i].fitness);
        for (int j = 0; j < tamCromosoma; j++)
        {
            printf("%lf", poblacion[i].cromosoma[j]);
        }
    }
}

void generaPoblacionInicial(individuo *poblacion, int tamPoblacion, int tamCromosoma, double min, double max)
{
    srand(time(NULL)); // * Con srand se define la semilla para generar numeros pseudoaleatorios
    for (int i = 0; i < tamPoblacion; ++i)
    {
        //* Se reserva memoria para los cromosomas
        poblacion[i].cromosoma = (double *)malloc(sizeof(double) * tamCromosoma);

        for (int j = 0; j < tamCromosoma; ++j)
        {
            // * Se generan numeros aleatorios que estan entre el mínimo y el máximo
            poblacion[i].cromosoma[j] = (double)min + rand() / RAND_MAX * (max - min);
        }
    }
}

void funcionFitness(individuo *poblacion, int tamPoblacion, int tamCromosoma)
{
    double total = 0;
    for (int i = 0; i < tamPoblacion; ++i)
    {
        int decimal = 0;
        // * Base es la variable que ayuda a calcular la posicion del gen en el
        //* cromosoma y así poder dar el valor en base 10
        int base = 1;

        for (int j = 0; j < tamCromosoma; j++)
        {
            total += poblacion[i].cromosoma[j];
        }

        poblacion[i].fitness = total;
    }
}

void cruza(individuo *poblacion, int tamPoblacion, int tamCromosoma)
{
    individuo *hijo1 = (individuo *)malloc(sizeof(individuo));
    hijo1->cromosoma = (double *)malloc(tamCromosoma * sizeof(double));

    // * Recorrer a los padres
    srand(time(NULL));
    int padre1 = rand() % tamPoblacion;
    int padre2 = rand() % tamPoblacion;
    for (int i = 0; i < tamCromosoma; i++)
    {
        hijo1->cromosoma[i] = (poblacion[padre1].cromosoma[i] + poblacion[padre2].cromosoma[i]) / 2;
    }
    // * Evaluar a los padres y a los hijos
    funcionFitness(poblacion, tamPoblacion, tamCromosoma);
    funcionFitness(hijo1, 1, tamCromosoma);

    if (poblacion[padre1].fitness < poblacion[padre2].fitness)
    {
        poblacion[padre2].fitness = hijo1->fitness;
        for (int j = 0; j < tamCromosoma; j++)
        {
            poblacion[padre2].cromosoma[j] = hijo1->cromosoma[j];
        }
    }
    else if (poblacion[padre1].fitness > poblacion[padre2].fitness)
    {
        poblacion[padre1].fitness = hijo1->fitness;
        for (int j = 0; j < tamCromosoma; j++)
        {
            poblacion[padre1].cromosoma[j] = hijo1->cromosoma[j];
        }
    }
    else
    {
        poblacion[padre1].fitness = hijo1->fitness;
        for (int j = 0; j < tamCromosoma; j++)
        {
            poblacion[padre1].cromosoma[j] = hijo1->cromosoma[j];
        }
    }
}

void mutar(individuo *poblacion, int tamPoblacion, int tamCromosoma, float probMutacion)
{
    // * Esta mutación no está tan chida pero se cambiará el individuo 0.1 hacia arriba o abajo
    for (int i = 0; i < tamPoblacion; i++)
    {
        for (int j = 0; j < tamCromosoma; j++)
        {
            float probabilidad = (float)rand() / RAND_MAX;
            if (probabilidad < probMutacion)
            {
                // * Calcular un valor que sea 0.1 o -0.1
                float valor;
                valor = (rand() / RAND_MAX * 0.2) - 0.2;
                poblacion[i].cromosoma[j] += valor;
            }
        }
    }
}