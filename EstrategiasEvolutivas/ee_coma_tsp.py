from random import choice, random, uniform, randint
import csv
import sys



def ee (n, d, m, l, mut, numgen):
    """
    Algoritmo basico EE para resolver el problema del viajante
    Parametros:
    n - numero de ciudades
    d - vector de costos
    mut - operador de mutacion
    m - mu
    l - lambda
    numgen - numero de generaciones sin mejora
    """

    # Se crea una poblcion de  individuos (permutaciones) aleatorios
    x, aptitud = poblacionInicial(n, d, m)

    # Se ordena el conjunto
    comb = list(zip(x, aptitud))
    comb = sorted(comb, key = lambda x: x[1], reverse = True)

    x = [elem[0] for elem in comb[:m]]
    aptitud = [elem[1] for elem in comb[:m]]

    mejorx = x[0]
    mejoraptitud = aptitud[0]
    
    generacion = 0
    generacionesSinMejora = 0
    generacionMejor = 0
    while (generacionesSinMejora < numgen):
        generacion = generacion + 1
    
        # Se mutan los individuos actuales x para obtener
        # los nuevos individuos x'
        # y se evalua x' en la funcion de aptitud
        xprima, aptitudprima = mutarPoblacion(x, d, mut, l)
    
        # Se selecciona el mejor individuo original
        mejor = aptitud.index(max(aptitud))
        
        # Se selecciona el peor individuo que resulta de la mutacion
        peor = aptitudprima.index(min(aptitudprima))
        
        # Se reemplaza la peor mutacion por el mejor original
        xprima[peor] = x[mejor]
        aptitudprima[peor] = aptitud[mejor]
        
        # Se reemplaza la poblacion original por el resultado de la mutacion
        x = xprima
        aptitud = aptitudprima

        # Si la solucion actual x' es mejor que x,
        # se actualiza x
        if aptitud[0] > mejoraptitud:
            mejorx = x[0]
            mejoraptitud = aptitud[0]
            generacionMejor = generacion
            generacionesSinMejora = 0
        else:
            generacionesSinMejora = generacionesSinMejora + 1
    
    return x[0], (-1 * aptitud[0]), generacionMejor, generacion



def mutarPoblacion(x, d, mut, l):
    xprima = []
    aptitudprima = []
    for i in range(l):
        xprima.append(mutacion (x[i], mut))
        aptitudprima.append(calcularAptitud(xprima[i], d))
        
    return xprima, aptitudprima




# Se elige el operador de mutacion que se aplicara
def mutacion (x, mut):
    if mut == 'int':
        xprima = intercambio(x)
    elif mut == 'ins':
        xprima = insercion(x)
    elif mut == 'inv':
        xprima = inversion(x)
    else:
        if random() <= 1.0/3:
            xprima = insercion (x)
        elif random() <= 0.5:
            xprima = intercambio (x)
        else:
            xprima = inversion (x)
    return xprima


# Mutacion por intercambio
def intercambio (x):
    n = len(x)
    xprima = x * 1
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    temp = xprima[i]
    xprima[i] = xprima[j]
    xprima[j] = temp
    return xprima


# Mutacion por insercion
def insercion (x):
    n = len(x)
    xprima = x * 1
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    if j < i:
        temp = i
        i = j
        j = temp
    xprima.pop(j)
    xprima.insert(i, x[j])
    return xprima


# Mutacion por inversion
def inversion (x):
    n = len(x)
    xprima = x * 1
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    for k in range(j - i + 1):
        xprima[i+k] = x[j-k]
    return xprima



# Se crea una poblacion inicial aleatoria
def poblacionInicial(n, d, m):
    # Se crea un conjunto de vectores aleatorios y se
    # evalua la funcion objetivo
    x = [1] * m
    aptitud = [1] * m
    for i in range(m):
        x[i] = permutacionAleatoria(n)
        aptitud[i] = calcularAptitud(x[i], d)
        
    return x, aptitud




# Crea una permutacion aleatoria de 1..n
def permutacionAleatoria(n):
    x = [1] * n
    ciudades = list(range(n))
    for i in range(n):
        c = choice(ciudades)
        x[i] = c
        ciudades.remove(c)
    return x



# Obtiene la distancia de la ciudad i a la ciudad j
def distancia(i, j, n, d):
    return d[(i * n) + j]


# Calcula el costo del recorrido en x
def calcularAptitud (x, d):
    n = len(x)
    costo = distancia(x[n-1], x[0], n, d)
    for i in range(n-1):
        costo = costo + distancia(x[i], x[i+1], n, d)
    return -1 * costo



# Lee datos del problema del archivo de texto
def preproceso (problema):
    # Se lee la informacion del caso de prueba
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


# Despliega los resultados
def resultado(x, costo, promcosto, generacionMejor, generaciones):
    print("\nMEJOR SOLUCION ENCONTRADA")
    print("Recorrido:", x)
    print("Costo:", costo)
    print("Generacion encontrada:", generacionMejor)
    print("Generaciones:", generaciones)
    print("Costo promedio:", promcosto, "\n")



def eetsp (problema, mu, l, mutacion, generacionesSinMejora, repeticiones):
    n, d = preproceso(problema)
    mejorcosto = 100**10
    promcosto = 0.0
    for i in range(repeticiones):
        x, costo, genMejor, gen = ee(n, d, mu, l, mutacion, generacionesSinMejora)
        promcosto = promcosto + costo
        if mejorcosto > costo:
            mejorx = x
            mejorcosto = costo
            generacionMejor = genMejor
            generaciones = gen
    resultado(mejorx, mejorcosto, promcosto/repeticiones, generacionMejor, generaciones)



if __name__ == "__main__":
    if(len(sys.argv) < 4):
        print("Sintaxis: eetsp.py <problema> <mu> <lambda> <mutacion> <numiter> <repeticiones>")
    else:
        eetsp(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6]))
