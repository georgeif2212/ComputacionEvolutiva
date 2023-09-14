from random import choice, random, uniform, randint, randrange
import sys



def ee (n, w_max, v, w, num_iter):
    """
    Algoritmo basico EE para resolver el problema de la mochila
    Parametros:
    n - numero de articulos
    w_max - capacidad de la mochila
    v - vector de los valores de cada articulo
    w - vector de los pesos de cada articulo
    num_iter - numero de iteraciones
    """
    # Se crea una solución inicial factible, eligiendio un articulo
    # de forma aleatoria y se evalua la funcion objetivo (valor y peso)
    # TODO
    x = [0] * n
    aux = randint(0, n)
    x[aux]=1
    valor, peso = valor_peso(x,v,w)

    generacion = 0
    while (generacion < num_iter):
        # Se incrementa la generacion
        # TODO
        generacion= generacion+1
        
        # Se muta el vector actual x para obtener x_prima
        # TODO
        x_prima = bitflip(x)
        
        # Se evalua x_prima en la funcion objetivo
        # TODO
        valor_primo, peso_primo = valor_peso(x_prima,v,w)
        # Si la mutación x_prima es factible y es mejor que x,
        # se reemplazan x, el valor y el peso
        # TODO
        if(valor_primo>valor and peso_primo<=w_max):
            x = x_prima.copy()
            valor = valor_primo
            peso=peso_primo
            
    
    # Al finalizar el ciclo, se regresan x, el valor y el peso
    # TODO
    return x,valor, peso



# Mutacion bit-flip
def bitflip (x):
    """Aplica el operador de mutación bitflip sobre x y devuelve x_prima."""
    
    # TODO:
    # Completar operador de mutación
    # Debe devolver x_prima
    x_prima = x.copy()
    L= len(x)
    pm = 1 / L
    
    if (pm > uniform(0,1)):
      aux = randint(0, L-1)
      if(x[aux]==1):
        x_prima[aux]=0
      else:
        x_prima[aux]=1
    return x_prima



def valor_peso (x, v, w):
    """Calcula el valor (v) y el peso (w) de los articulos seleccionados en x."""

    n = len(x)
    valor = 0
    peso = 0
    for i in range(n):
      if x[i] == 1:
        valor = valor + v[i]
        peso = peso + w[i]
    return valor, peso



def preproceso (problema):
    """Lee datos del problema del archivo de texto."""
    
    # Se lee la informacion del caso de prueba
    arch = open('mochila/' + problema)
    info = list(map(int, arch.readline().split()))
    n = info[0]
    w_max = info[1]
    v = []
    w = []
    i = 0
    while i < n:
      info = list(map(int, arch.readline().split()))
      v.append(info[0])
      w.append(info[1])
      i = i+1
    arch.close()
    
    # Se lee el valor de la mochila de la solucion optima
    arch = open('mochila/' + problema + '_opt')
    opt = int(arch.read())
    arch.close()
    
    print("DATOS DEL CASO DEL PROBLEMA")
    print("Nombre:", problema)
    print("Numero de articulos:", n)
    print("Capacidad de la mochila:", w_max)
    print("Valor de la mochila de la solucion optima:", opt)
    
    return n, w_max, v, w



def articulos (x):
  """Devuelve los articulos seleccionados en x."""
  
  arts = []
  for i in range(len(x)):
    if x[i] == 1:
      arts.append(i+1)
  return arts



def resultado(x, valor, peso):
    """Despliega los resultados."""
    
    print("\nMEJOR SOLUCION ENCONTRADA")
    print("Articulos:", articulos(x))
    print("Valor:", valor)
    print("Peso:", peso, "\n")



if __name__ == "__main__":
    if(len(sys.argv) < 3):
      print("Sintaxis: eem.py <problema> <número_iteraciones>")
    else:
      n, w_max, v, w = preproceso(sys.argv[1])
      x, valor, peso = ee(n, w_max, v, w, int(sys.argv[2]))
      resultado(x, valor, peso)
