###
# BOOLEANOS
# Valores logicos: True --> VERDADERO y False --> FALSO
# Fundamental para el control de flujo y logica en programacion 
###

print("\nValores booleanos basicos")
print(True)
print(False)

# Operadores de comparacion
print("\nOperadores de comparacion:")
print("5 > 3", 5 > 3)     # True
print("5 < 3", 5 < 3)     # False
print("5 == 5", 5 == 5)   # True (Igualdad)
print("5 != 3", 5 != 3)   # True (Desigualdad)
print("5 >= 5", 5 >= 5)   # True (Mayor o igual que)
print("5 <= 3", 5 <= 3)   # False (Menor o igual que)

print("\nComparacion de cadenas")
print("'manzana' < 'pera:'", "manzana" < "pera") # True
print("'Hola' == 'hola: '", "Hola" == "hola") # False

# Operadores logicos: and, or, not 
print("\n Operadores logicos")
print("True and True", True and True)    # True
print("True and False", True and False)  # False
print("True or False", True or False)    # True
print("False or False", False or False)  # False
print("not True", not True)              # False
print("not False", not False)            # True


# Tablas de verdad (referencia):
print("\nTablas Verdad")
print("\nAND:")
print("A     B     A and B")
print("True  True "  ,  True and True)
print("True  False " ,  True and False)
print("False True "  ,  False and True)
print("False False"  ,  False and False)


print("\nOR:")
print("A     B    A or B")
print("True  True " , True or True)
print("True  False ", True or False)
print("False True " , False or True)
print("False False" , False or False)

print("\nNOT:")
print("A   not A")
print("True ", not True)
print("False ", not False)