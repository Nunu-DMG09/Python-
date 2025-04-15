###
# SENTENCIAS CONDICIONALES (IF - ELSE - ELIF)
# Permiten ejecutar bloques de codigo si se cumplen ciertas condiciones 
###

import os # IMPORTAR MODULOS DEL SISTEMA OPERATIVO
os.system("clear")  


print("\n Sentencia simple condicional")
edad = 19
if edad >= 18:
    print("Eres mayor de edad")



print("\n Sentencia condicional con ELSE")
edad = 15
if edad >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")



print("\n Sentencia condicional con ELIF")
nota = 9
if nota >= 9:
    print("Sobresaliente")
elif nota >= 7:
    print("Bueno")
elif nota >= 5:
    print("Regular")
else:
    print("Reprobaste")



print("\n Condiciones multiples")
edad = 25
licencia_conducir = True
if edad >= 18 and licencia_conducir: # con operador logico -> AND 
    print("Puedes conducir")
else:
    print("No puedes conducir, estas detenido 👮‍♀️")


if edad >= 18 or licencia_conducir: # con operador logico -> OR 
    print("Puedes ingresar a Peru")
else:
    print("No puedes ingresar, al menos a que pagues al policia")



fin_semana = False
if not fin_semana:  # con operador logico -> NOT
    print("Estas trabajando")



print("\n Anidar condicionales")
edad = 20
tiene_dinero = True
if edad >= 18:
    if tiene_dinero:
        print("Puedes comprar un automovil")
    else:
        print("No tienes suficiente dinero")
else:
    print("No puedes comprar un automovil, estas detenido ��‍��️")

# FORMA MAS FACIL 

# if edad < 18: 
#    print("No puedes comprar un automovil, estas detenido ��‍��️")
# elif: tiene_dinero:
#    print("Puedes comprar un automovil")
# else:
#    print("No tienes suficiente dinero")

numero = 3 # Asignacion 
es_tres = numero == 3 # Comparacion

if es_tres:
    print("El número es 3 ")

print("\nLa condicion ternaria")
# es una forma concisa de un if-else en una linea de codigo
# [codigo si cumple la condicion] if [condicion] else [codigo si no cumple]

edad = 17
mensaje = "Es mayor de edad" if edad >= 18 else "Es menor de edad"
print(mensaje)

###
# EJERCICIOS
###

# Ejercicio 1: Determinar el mayor de dos números
# Pide al usuario que introduzca dos números y muestra un mensaje 
# Indicando cuál es mayor o si son iguales

# Ejercicio 2: Calculadora simple
# Pide al usuario dos números y una operación (+, -, *, /)
# Realiza la operacion y muestra el resultado (Maneja la división entre cero)

# Ejercicio 3: Año bisiesto
# Pide al usuario que introduzca un año y determina si es bisiesto
# Un año es bisiesto si es divisible por 4, excepto si es divisible por 100 pero no por 400

# Ejercicio 4: Categorizar edades
# Pide al usuario que introduzca una edad y la clasifique en:
# - Bebé (0-2 años)
# - Niño (3-12 años)
# - Adolescente (13-17 años)
# - Adulto (18-64 años)
# - Adulto mayor (65 años a más)





