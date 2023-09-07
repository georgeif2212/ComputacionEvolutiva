from random import choice, random, uniform, randint, sample
import csv
import sys


# * P, Q conjuntos de elementos // mu = número de soluciones iniciales
# * lambda = numero de elementos a mutar
def ee (n, d, num_generaciones, mutacion,mu,lamb):
    """
    Algoritmo basico EE para resolver el problema del viajante
    Parametros:
    n - numero de ciudades
    d - vector de costos
    num_generaciones - numero de generaciones sin mejora
    mutacion - operador de mutacion
    """

    # Se crea un individuo (permutacion) aleatorio
    P=list()
    aptitudes=list()
    aptitudesPrima=list()
    # * Generar mu soluciones aleatorias dentro de P
    for _ in range(mu):
        x = permutacion_aleatoria(n)
        P.append(x)
    # * Calcular aptitudes de P
    for i in range(len(P)):
        aptitudes.append(calcular_aptitud(P[i], d)) 

    # * Seleccionar las mejores mu aptitudes de P
    aptitudes.sort(reverse=True)
    aptitudes = aptitudes[:mu]

    generacion = 0
    generaciones_sin_mejora = 0
    while (generaciones_sin_mejora < num_generaciones):
        generacion = generacion + 1
    
        # * Q es igual a Q + P con mutación
        Q = mutar(x,mutacion,P,lamb)
        # * Se evaluan las aptitudes de Q
        for i in range(len(Q)):
            aptitudesPrima.append(calcular_aptitud(Q[i], d)) 
        # * Seleccionar las mejores mu aptitudes de Q
        aptitudesPrima.sort(reverse=True)
        aptitudesPrima = aptitudesPrima[:mu]

        # * Identificar las mejores aptitudes de cada lista
        mejorAptitud = max(aptitudes)
        mejorAptitudPrima = max(aptitudesPrima)
        
        # * Si la aptitud mutada es mejor que la original se cambia
        if mejorAptitudPrima > mejorAptitud:
            P=Q[:mu]
            aptitudes = aptitudesPrima[:]
            generacion_mejor = generacion
            generaciones_sin_mejora = 0
        else:
            generaciones_sin_mejora = generaciones_sin_mejora + 1
    
    aptitud = max(aptitudes)
    
    return x, (-1 * aptitud), generacion_mejor


def mutar (x, mutacion,P,lamb):
    """Aplica el operador de mutación especificado a x."""
    if mutacion == 'intercambio':
        x_prima = intercambio(x)
    elif mutacion == 'insercion':
        x_prima = insercion(x)
    elif mutacion == 'inversion':
        x_prima = inversion(x)
    elif mutacion == 'inversionConjunto':
        x_prima = inversionConjunto(P,lamb)
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

def inversion(x):
    """Operador de mutación por inversión para 2-opt."""
    n = len(x)  # Número de nodos en la ruta (ciudades a visitar)
    x_prima = x[:]  # Creamos una copia de la ruta original
    
    # Elegir aleatoriamente dos índices distintos i y j
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))

    # Asegurarse de que j > i para definir correctamente la subsecuencia a invertir
    if j < i:
        temp = i
        i = j
        j = temp

    # Invertir la subsecuencia entre los índices i y j en la copia de la ruta
    for k in range(j - i + 1):
        x_prima[i + k] = x[j - k]

    return x_prima  # Devolver la ruta con la mutación por inversión

def inversionConjunto(P,la):
    Q=P[:]
    "Operador de mutación por inversión para 2-opt."
    # * Selecciono lambda numeros aleatorios de 0 hasta el tamaño de P
    numerosAleatorios = sample(range(0, len(P)), la)
    
    for i in range(len(numerosAleatorios)):
        Q[numerosAleatorios[i]]=inversion(P[numerosAleatorios[i]])

    Q = Q + P
    return Q


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
    arch = open('../Benchmarks/tsp/' + problema + '.atsp')
    info = list(map(int, arch.read().split()))
    arch.close()
    n = info[0]
    info = info[1:]
    with open('../Benchmarks/tsp/best-known.atsp') as f:
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


def eetsp(problema, generaciones_sin_mejora, repeticiones=1, mutacion=None, mu=10, lamb=5):
    n, d = preproceso(problema)
    mejor_costo = float('inf')  # Usamos infinito positivo como valor inicial
    prom_costo = 0.0
    for i in range(repeticiones):
        x, costo, generacion = ee(n, d, generaciones_sin_mejora, mutacion, mu, lamb)
        prom_costo += costo
        if mejor_costo > costo:
            mejor_x = x
            mejor_costo = costo
            generacion_mejor = generacion
    resultado(mejor_x, mejor_costo, prom_costo / repeticiones, generacion_mejor)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 7:
        print("Sintaxis: eetsp.py <problema> <núm_generaciones_sin_mejora> [<repeticiones> [<mutación> <mu> <lamb>]]")
    else:
        problema = sys.argv[1]
        generaciones_sin_mejora = int(sys.argv[2])
        repeticiones = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        mutacion = sys.argv[4] if len(sys.argv) > 4 else None
        mu = int(sys.argv[5]) if len(sys.argv) > 5 else 10  # Valor predeterminado de mu
        lamb = int(sys.argv[6]) if len(sys.argv) > 6 else 5  # Valor predeterminado de lamb

        eetsp(problema, generaciones_sin_mejora, repeticiones, mutacion, mu, lamb)
