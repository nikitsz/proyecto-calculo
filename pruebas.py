import sympy as sp
from sympy import symbols
from sympy import expand, factor
from sympy import *

#---------- EJERCICIOS SYMPY -----------

#Esto hace que las operaciones se vean mas "bonitas" en el print
init_printing(use_unicode=True)

#ejercicios
t, o = symbols('t o')
func= 5*t + 3**o
print("Funcion: ", func)

x, y = symbols('x y') #Symbols: define los simbolos que se ocuparan (por lo que leí, deben ser siempre los mismos simbolos) 
expr = x*(x + 2*y) #ejemplo
print("Ejercicio: ", expr)


#Para resolver ecuaciones "Eq"
#En este ejemplo tenemos la ecuación x + 1 = 4"
print("\nhola: ", Eq(x + 1, 4))

#expand, factor
expresion_expandida = expand(expr) #expande la expresion (la resuelve)
expresion_factorizada = factor(expr) #factoriza la expresion
print("\nFuncion expandida: ", expresion_expandida)
print("\nFuncion factorizada: ", expresion_factorizada)

#.sqrt = Raiz cuadrada
ocho = sp.sqrt(8) #Lo que hace esto especial, es que nos deja la raiz de 8 representada simbolicamente, que sería 2(raiz de 2)
print("\nRaiz cuadrada de 8: ", ocho)

nueve = sp.sqrt(9)
print("\nRaiz cuadrada de 9: ", nueve)

#Limites (para esto se necesita el "from sympy import *")
escribir_limite = int(input("Ingrese a qué número tiende x: "))
limite = limit(sin(x)/x, x, escribir_limite)
print("\nLimite es: ", limite)

#Solve, encuentra los valores de x, para que la ecuacion x al cuadrado - 2 sea igual a 0, no creo que la ocupemos pero igual esta buena
print("\n valores de x para que se cumpla la operacion: ", solve(x**2 - 2, x))

#.equals: para saber si dos terminos son iguales
a = cos(x)**2 - sin(x)**2
b = cos(2*x)
print("\n Es a igual a b?: ", a.equals(b))

#cancel(): Toma una expresion y la muestra en su forma canonica

#División de dos enteros da racional usando Integer
print("\n División de enteros con sympy usando integer: ", Integer(1)/Integer(3))
print("División de enteros en python: ", 1/3)
#También se puede usar el rational
print("\nUsando rational: ", Rational(1, 3))

#Simplify
a = (x + 1)**2
b = x**2 + 2*x + 1
c = x**2 - 2*x + 1
print("\n A menos B: ", simplify(a - b))
print("\n A menos C: ", simplify(a - c))

print("\n\nTrigonometria")

#--Trigonometria--
#Arcocoseno
acos(x)
#Arcoseno
asin(x)

#Simplificar trigonometria (trigsimp)
print("\n Sen al cuadrado + Cos al cuadrado: ", trigsimp(sin(x)**2 + cos(x)**2))
#expand_trig: cumple lo mismo de expand

#---Potencias---
#Aplicar propiedades de potencias 
#powsimp()
g, h = symbols('g h')
print("\nLOL: ", powsimp(x**g*x**h))



x = symbols('x')
funcion = sp.sin()
valor_x = int(input("Ingrese valor de x: "))
funcion_nueva = 0 