from random import choice, random, sample
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
    aux=list()
    aptitudes=list()
    # * Generar población de mu soluciones
    for i in range(mu):
        x = permutacion_aleatoria(n)
        aux.append(x)
        aptitudes.append(calcular_aptitud(aux[i], d))

    # * Hacer una lista de pares, [(permutación),(aptitudes)]
    aux= list(zip(aux, aptitudes))
    # * Ordena la lista de manera descendente en función de la aptitud
    aux = sorted(aux, key = lambda x: x[1], reverse = True)
    # print("AUX:",aux)
    # * Lista P y de aptitudes ordenada de manera descendente
    P = [elem[0] for elem in aux[:mu]]
    aptitudes= [elem[1] for elem in aux[:mu]]
    
    mejoraptitud = aptitudes[0]
    
    generacion = 0
    generaciones_sin_mejora = 0
    generacion_mejor=0
    while (generaciones_sin_mejora < num_generaciones):
        aptitudesPrima=list()
        # print("Mejor Aptitud: ",mejoraptitud)
        generacion = generacion + 1
        
        # * Q = lista con lambda mutaciones de P
        Q= mutar(mutacion, P, lamb)
        
        # * Se evaluan las funciones de Q
        # * y las aptitudes originales con las mutadas
        for i in range(len(Q)):
            aptitudesPrima.append(calcular_aptitud(Q[i], d))
        
        Q.extend(P)
        # print("Q con P:",Q)
        aptitudesPrima.extend(aptitudes)
        # print("Aptitudes de Q y P:",aptitudesPrima)
        # * Se añade a Q las mutaciones de P 
        
        # * Hacer una lista de pares, [(permutación),(aptitudes)]
        comb= list(zip(Q, aptitudesPrima))
        # print("Q con aptitudes:",Q)
        # * Ordena la lista de manera descendente en función de la aptitud
        comb = sorted(comb, key = lambda x: x[1], reverse = True)

        P = [elem[0] for elem in comb[:mu]]
        aptitudes = [elem[1] for elem in comb[:mu]]
        # print("Mejores aptitudes P:",aptitudes)
        

        if aptitudes[0] > mejoraptitud:
            # print("hola")
            mejoraptitud = aptitudes[0]
            generacion_mejor = generacion
            generaciones_sin_mejora = 0
        else:
            generaciones_sin_mejora = generaciones_sin_mejora + 1

    return x, (-1 * aptitudes[0]), generacion_mejor


def mutar (mutacion,P,lamb):
    
    """Aplica el operador de mutación especificado a x."""
    if mutacion == 'inversionConjunto':
        Q = inversionConjunto(P,lamb)
    return Q

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

def inversionConjunto(P, lamb):
    Q = []
    
    # Selecciona lambda números aleatorios de 0 hasta el tamaño de P
    numerosAleatorios = sample(range(len(P)), lamb)
    # print("P:",P)
    for i in range(lamb):
        elemento_seleccionado = P[numerosAleatorios[i]]
        elemento_mutado = inversion(elemento_seleccionado)
        Q.append(elemento_mutado)
    # print("Q solito:",Q)
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
