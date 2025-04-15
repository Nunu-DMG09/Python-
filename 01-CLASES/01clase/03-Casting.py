# --------------
# CASTING DE DATOS
# --------------

# Transformar un tipo a otro valor

print("CONVERSION DE TIPOS :D")

# CONVERSION A ENTERO
print(2 + int("100"))

# CONVERSION A STRING
print("100" + str(2))

# CONVERSION A FLOAT
print(type(float(3.1416)))

# CONVERSION A ENTERO
print(int(3.1416))

# CONVERSION A BOOLEANOS
print(bool(3))
print(bool(0)) # unico numero entero donde sera FALSE, lo demas TRUE
print(bool(-1))

print(bool("")) # Unico string que sera FALSE, lo demas TRUE
print(bool(" "))
print(bool("FALSE"))

# Conversion de ENTEROS a CADENA DE TEXTO
print(int("Hola mundo")) # Todo tiene su limite, te dará ERROR

#TIP CON LA FUNCION ROUND()
# ROUND solamente va redondear al par cercano justo en el medio, es decir: 

print(round(3.5)) # 4
print(round(2.5)) # 2
print(round(2.51)) # 3
