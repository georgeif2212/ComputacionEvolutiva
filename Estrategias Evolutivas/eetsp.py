from random import choice, random, uniform, randint
import csv
import sys



def ee (n, d, num_generaciones, mutacion):
    """
    Algoritmo basico EE para resolver el problema del viajante
    Parametros:
    n - numero de ciudades
    d - vector de costos
    num_generaciones - numero de generaciones sin mejora
    mutacion - operador de mutacion
    """

    # Se crea un individuo (permutacion) aleatorio
    x = permutacion_aleatoria(n)
    aptitud = calcular_aptitud(x, d)
  
    generacion = 0
    generaciones_sin_mejora = 0
    while (generaciones_sin_mejora < num_generaciones):
        generacion = generacion + 1
    
        # Se muta el vector actual x para obtener x_prima
        # y se evalua x_prima en la función de aptitud
        x_prima = mutar (x, mutacion)
        aptitud_prima = calcular_aptitud(x_prima, d)
    
        # Si la mutación x_prima es mejor que x,
        # se actualiza x
        if aptitud_prima > aptitud:
            x = x_prima
            aptitud = aptitud_prima
            generacion_mejor = generacion
            generaciones_sin_mejora = 0
        else:
            generaciones_sin_mejora = generaciones_sin_mejora + 1
    
    return x, (-1 * aptitud), generacion_mejor


def mutar (x, mutacion):
    """Aplica el operador de mutación especificado a x."""
    if mutacion == 'intercambio':
        x_prima = intercambio(x)
    elif mutacion == 'insercion':
        x_prima = insercion(x)
    elif mutacion == 'inversion':
        x_prima = inversion(x)
    else:
        if random() <= 1.0/3:
            x_prima = insercion (x)
        elif random() <= 0.5:
            x_prima = intercambio (x)
        else:
            x_prima = inversion (x)
    return x_prima


def intercambio (x):
    """Operador de mutación por intercambio."""
    n = len(x)
    x_prima = x[:]
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    temp = x_prima[i]
    x_prima[i] = x_prima[j]
    x_prima[j] = temp
    return x_prima


def insercion (x):
    """Operador de mutación por inserción."""
    n = len(x)
    x_prima = x[:]
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    if j < i:
        temp = i
        i = j
        j = temp
    x_prima.pop(j)
    x_prima.insert(i, x[j])
    return x_prima


def inversion (x):
    """Operador de mutación por inversión."""
    n = len(x)
    x_prima = x[:]
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    if j < i:
        temp = i
        i = j
        j = temp
    for k in range(j - i + 1):
        x_prima[i+k] = x[j-k]
    return x_prima


def permutacion_aleatoria(n):
    """Crea una permutacion aleatoria de los números 1 a n."""
    x = [1] * n
    ciudades = list(range(n))
    for i in range(n):
        c = choice(ciudades)
        x[i] = c
        ciudades.remove(c)
    return x


def distancia(i, j, n, d):
    """Obtiene la distancia de la ciudad i a la ciudad j."""
    return d[(i * n) + j]


def calcular_aptitud (x, d):
    """Calcula el costo del recorrido en de x."""
    n = len(x)
    costo = distancia(x[n-1], x[0], n, d)
    for i in range(n-1):
        costo = costo + distancia(x[i], x[i+1], n, d)
    return -1 * costo



def preproceso (problema):
    """Lee del archivo de texto los datos del caso de pruba."""
    arch = open('tsp/' + problema + '.atsp')
    info = list(map(int, arch.read().split()))
    arch.close()
    n = info[0]
    info = info[1:]
    with open('tsp/best-known.atsp') as f:
        reader = csv.reader(f, delimiter=' ')
        data = [(col1, int(col2)) for col1, col2 in reader]
    
    i = 0
    while problema not in data[i][0]:
        i = i+1
    opt = int(data[i][1])
    
    print("DATOS DEL CASO DEL PROBLEMA")
    print("Nombre:", problema)
    print("Numero de ciudades:", n)
    print("Costo del recorrido de la solucion optima:", opt)
    
    return n, info


def resultado(x, costo, prom_costo, generacion_mejor):
    """Despliega los resultados."""
    print("\nMEJOR SOLUCION ENCONTRADA")
    print("Recorrido:", x)
    print("Costo:", costo)
    print("Generacion encontrada:", generacion_mejor)
    print("Costo promedio:", prom_costo, "\n")



def eetsp (problema, generaciones_sin_mejora, repeticiones = 1, mutacion = None):
    n, d = preproceso(problema)
    mejor_costo = 100 ** 10
    prom_costo = 0.0
    for i in range(repeticiones):
        x, costo, generacion = ee(n, d, generaciones_sin_mejora, mutacion)
        prom_costo = prom_costo + costo
        if mejor_costo > costo:
            mejor_x = x
            mejor_costo = costo
            generacion_mejor = generacion
    resultado(mejor_x, mejor_costo, prom_costo/repeticiones, generacion_mejor)



if __name__ == "__main__":
    print(len(sys.argv))
    if(len(sys.argv) < 3) or (len(sys.argv) > 5):
        print("Sintaxis: eetsp.py <problema> <núm_generaciones_sin_mejora> <repeticiones> <mutación>")
    elif len(sys.argv) == 3:
        eetsp(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) == 4:
        eetsp(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        eetsp(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
