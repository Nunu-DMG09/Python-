# --------------
# VARIABLES
# --------------

# Las variables sirven para guardar datos en memoria.
# Python es un lenguaje de tipado dinamico y fuerte. 

# Asignar una variable

nombre = "david"
print(nombre)

age = 19
print(age)

# TIPADO DINAMICO: el tipo de dato se determina en tiempo de ejecucion 
# que no tienes que declararlo explicitamente

nombre = "david" 
print(type(nombre))

nombre = 32
print(type(nombre))

# TIPADO FUERTE: Python no realiza conversione de tipo automatico 
print(10 + "2") # TE SALDRA ERROR 

# FORMART STRING 
print(f"hola {nombre}, tengo {age + 5} años")

# NO RECOMENDADA FORMA DE ASIGNAR VARIABLES 
name, age, city = "david", 19, "peru"

# CONVENCIONES DE NOMBRES DE VARIABLES
mi_nombre_de_variable = "ok" # SNAKE_CASE
name = "ok"
mi_nombre_de_variable_123 = "ok"

MI_CONSTANTE = 3.14 #UPPER_CASE -> constante

# NOMBRES DE VARIABLES NO PERMITIDOS

# 123123_variable = "ok"
# mi-variable = "ok"
# mi variable = "ok"
