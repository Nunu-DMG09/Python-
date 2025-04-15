###
# Entra de usuario (input()) - 
# La funcion input() permite obtener datos del usuario a traves de la consola.
# Cuando introuces informacion al usuario SIEMPRE pero SIEMPRE se guardará como cadena de texto
###

nombre = input("Hola, ¿Como te llamas?\n")
print(f"Hola {nombre}, encantado de conocerte")

age = input("Cuantos años tienes\n")
age = int(age)
print(f"Tienes {age} años ")

print("OBTENER MULTIPLES VALORES A LA VEZ")
print("----------------------------------")
county, city = input("En que pais y ciudad vives?\n").split()
print(f"Vives en {county}, {city}")