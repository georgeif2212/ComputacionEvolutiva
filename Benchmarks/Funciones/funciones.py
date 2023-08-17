"""
Contiene funciones de optimización de prueba.
"""


def seleccionar_funcion(f_obj):
    """
    Devuelve las cotas inferior y superior para la
    función de prueba especificada f_obj.
    """

    if f_obj == 'himmelblau':
        minimo = -10
        maximo = 10
        f = himmelblau
    elif f_obj == 'esfera':
        minimo = -100
        maximo = 100
        f = esfera
    elif f_obj == 'ackley':
        minimo = -32.768
        maximo = 32.768
        f = ackley
    elif f_obj == 'griewank':
        minimo = -600
        maximo = 600
        f = griewank
    elif f_obj == 'rastrigin':
        minimo = -5.12
        maximo = 5.12
        f = rastrigin
    elif f_obj == 'rosenbrock':
        minimo = -2.048
        maximo = 2.048
        f = rosenbrock
    elif f_obj == 'schwefel':
        minimo = -500
        maximo = 500
        f = schwefel
    else:
        minimo = 0
        maximo = 0
        f = None

    return minimo, maximo, f


def himmelblau(x):
    """
    Rango de prueba: xi en [-10, 10]
    Mínimos en:
        x = (3, 2)
        x = (-2.805118, 3.283186)
        x = (-3.779310, -3.283186)
        x = (3.584458, -1.848126)
    Evaluación: 0
    """

    f = (x[0] ** 2 + x[1] - 11) ** 2 + (x[0] + x[1] ** 2 - 7) ** 2
    return f


def ackley(x):
    """
    Rango de prueba: xi en [-32.768, 32.768]
    Mínimo en: xi = 0
    Evaluación: 0
    """
    from math import cos, exp, sqrt, pi

    dimension = len(x)
    suma_1 = 0
    suma_2 = 0
    for i in range(dimension):
        xi = x[i]
        suma_1 = suma_1 + xi ** 2
        suma_2 = suma_2 + (cos(2 * pi * xi))
    term_1 = -20 * exp(-0.2 * sqrt(suma_1 / dimension))
    term_2 = -exp(suma_2 / dimension)
    return term_1 + term_2 + 20 + exp(1)


def esfera(x):
    """
    Rango de prueba: xi en [-100, 100]
    Mínimo en: xi = 0
    Evaluación: 0
    """

    dimension = len(x)
    suma = 0
    for i in range(dimension):
        x_i = x[i]
        suma = suma + x_i ** 2
    return suma


def griewank(x):
    """
    Rango de prueba: xi en [-600, 600]
    Mínimo en: xi = 0
    Evaluación: 0
    """
    from math import cos, sqrt

    dimension = len(x)
    suma = 0
    producto = 1
    for i in range(dimension):
        x_i = x[i]
        suma = suma + x_i ** 2 / 4000
        producto = producto * cos(x_i / sqrt(i + 1))
    return suma - producto + 1


def rastrigin(x):
    """
    Rango de prueba: xi en [-5.12, 5.12]
    Mínimo en: xi = 0
    Evaluación: 0
    """
    from math import cos, pi

    dimension = len(x)
    suma = 0
    for i in range(dimension):
        x_i = x[i]
        suma = suma + (x_i ** 2 - 10 * cos(2 * pi * x_i))
    return 10 * dimension + suma


def rosenbrock(x):
    """
    Rango de prueba: xi en [-2.048, 2.048]
    Mínimo en: xi = 1
    Evaluación: 0
    """

    dimension = len(x)
    suma = 0
    for i in range(dimension - 1):
        x_i = x[i]
        x_j = x[i + 1]
        suma = suma + (100 * (x_j - x_i ** 2) ** 2 + (1 - x_i) ** 2)
    return suma


def schwefel(x):
    """
    Rango de prueba: xi en [-500, 500]
    Mínimo en: xi = 420.9687
    Evaluación: 0
    """
    from math import sin, sqrt

    dimension = len(x)
    suma = 0
    for i in range(dimension):
        x_i = x[i]
        suma = suma + (x_i * sin(sqrt(abs(x_i))))
    return 418.9829 * dimension - suma
