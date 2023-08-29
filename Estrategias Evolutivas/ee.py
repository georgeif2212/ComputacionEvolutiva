from random import choice, random, uniform
import funciones 
import sys


def ee(f_obj, dimension, num_iter, mut='unif'):
    """
    Algoritmo basico EE-(1+1)
    Parámetros:
    f_obj - función objetivo (función a minimizar)
    dimension - número de dimensiones (variables)
    num_iter - número de iteraciones
    mut - función de mutación (default uniforme)
    """

    # Se obtienen los límites inferior y superior
    # de cada dimension de la función a optimizar
    minimo, maximo, f = funciones.seleccionar_funcion(f_obj)

    # Se crea un vector aleatorio y se evalúa la función objetivo
    x = vector_aleatorio(dimension, minimo, maximo)
    aptitud = -1 * f(x)
    print("*** Inicio:\n f(x) =", -1 * aptitud, "\n x = ", x, "\n")

    generacion = 0
    while generacion < num_iter:
        # Se muta el vector actual x para obtener x'
        # y se evalúa x' con la función objetivo
        generacion = generacion + 1
        if mut == 'unif':
            x_prima = mutacion_uniforme(x, minimo, maximo)
        elif mut == 'no_unif':
            x_prima = mutacion_no_uniforme(x, generacion, num_iter, minimo, maximo, 3)
        elif mut == 'muhl':
            x_prima = mutacion_muhlenbein(x, minimo, maximo)
        else:
            x_prima = x
        aptitud_prima = -1 * f(x_prima)

        # Si la solución actual x' es mejor que x,
        # se actualiza x
        if aptitud_prima > aptitud:
            x = x_prima
            aptitud = aptitud_prima
            print("*** Generación ", generacion, ":\n f(x) =", -1 * aptitud, "\n x = ", x, "\n")


# Uniform mutation (Michalewicz, 1992)
def mutacion_uniforme(x, minimo, maximo):
    dimension = len(x)
    x_prima = x[:]
    i = choice(range(dimension))
    x_prima[i] = uniform(minimo, maximo)
    return x_prima


# Non-uniform mutation (Michalewicz, 1992)
def mutacion_no_uniforme(x, t, g_max, minimo, maximo, b):
    dimension = len(x)
    x_prima = []
    for i in range(dimension):
        tau = choice([0, 1])
        if tau == 0:
            y = maximo - x[i]
        else:
            y = x[i] - minimo
        delta = (1 - t / g_max) ** b
        delta = random() ** delta
        delta = y * (1 - delta)
        if tau == 0:
            x_prima.append(x[i] + delta)
        else:
            x_prima.append(x[i] - delta)

        # Si el valor está fuera de rango,
        # fuerza a ubicarse dentro de los límites
        if (x_prima[i] < minimo) or (x_prima[i] > maximo):
            x_prima[i] = x_prima[i] % (maximo - minimo) + minimo
    return x_prima


# Muhlenbein's mutation (Muhlenbein et al., 1993)
def mutacion_muhlenbein(x, minimo, maximo):
    dimension = len(x)
    x_prima = x * 1
    rang_i = 0.1 * (maximo - minimo)
    gamma = 0
    for k in range(15):
        if random() <= (1 / 16):
            alpha_k = 1
        else:
            alpha_k = 0
        gamma = gamma + (alpha_k * 2 ** (-k))

    for i in range(dimension):
        if random() <= 0.5:
            x_prima[i] = x_prima[i] + rang_i * gamma
        else:
            x_prima[i] = x_prima[i] - rang_i * gamma
    return x_prima


# Crea y devuelve un vector de dim dimensiones.
# El valor en cada dimensión está dentro el rango [min, max].
def vector_aleatorio(dimension, minimo, maximo):
    vector = []
    for i in range(dimension):
        vector.append(uniform(minimo, maximo))
    return vector


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Sintaxis: ee.py <función_objetivo> <dimension> <número_iteraciones> [<mutación>]")
    elif len(sys.argv) == 4:
        ee(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        ee(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
