import pandas as pd
from datetime import datetime

clientes = {}
transacciones = []

# Función para guardar clientes en Excel
def guardar_clientes():
    df = pd.DataFrame.from_dict(clientes, orient="index")
    df.to_excel("clientes.xlsx", index_label="DNI", engine="openpyxl")

# Función para guardar transacciones en Excel
def guardar_transacciones():
    df = pd.DataFrame(transacciones)
    df.to_excel("transacciones.xlsx", index=False, engine="openpyxl")

def mostrar_menu_principal():
    print("\nMenu de opciones")
    print("1. Crear cuenta ⚪")
    print("2. Retirar dinero 🔴")
    print("3. Ingresar dinero 🟢")
    print("4. Revisar el estado de tu cuenta 🟡")
    print("5. Salir 💥")

# VALIDACIONES
def validar_dni(dni):
    return dni.isdigit() and len(dni) == 8

def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 9

def validar_edad(edad):
    return edad.isdigit() and int(edad) >= 18  

def validar_contraseña(contraseña):
    """La contraseña debe ser de 6 dígitos numéricos"""
    return contraseña.isdigit() and len(contraseña) == 6

def verificar_contraseña(dni):
    """Permite verificar la contraseña antes de retirar o ingresar dinero"""
    intentos = 3
    while intentos > 0:
        contraseña = input("\nIngrese su contraseña (6 dígitos): ")
        if clientes[dni]["contraseña"] == contraseña:
            return True
        else:
            intentos -= 1
            print(f"\n❌ Contraseña incorrecta. Intentos restantes: {intentos}")

    print("\n🚫 Acceso bloqueado por intentos fallidos.")
    return False

def mostrar_menu(tipo):
    global clientes, transacciones
    print(f"\nOpción: {tipo}")

    if tipo == "crear cuenta":
        while True:
            dni = input("\nIngrese DNI: ")
            print("-" * 20)
            if validar_dni(dni):
                break
            else:
                print("❌ DNI inválido. Recuerde que son 8 dígitos.")

        while True:
            telefono = input("\nIngrese su número de teléfono: ")
            print("-" * 20)
            if validar_telefono(telefono):
                break
            else:
                print("❌ ERROR - Número incorrecto. Debe tener 9 dígitos.")

        nombre = input("\nIngrese su nombre: ")
        apellido = input("\nIngrese su apellido: ")

        while True:
            edad = input("\nIngrese su edad: ")
            print("-" * 20)
            if validar_edad(edad):
                edad = int(edad)
                break
            else:
                print("❌ ERROR - Debe ser mayor de 18 años.")

        while True:
            contraseña = input("\nCree una contraseña (6 dígitos): ")
            print("-" * 20)
            if validar_contraseña(contraseña):
                break
            else:
                print("❌ ERROR - La contraseña debe tener exactamente 6 dígitos numéricos.")

        saldo_inicial = input("\nIngrese el saldo inicial: S/ ")
        print("-" * 20)

        try:
            saldo_inicial = float(saldo_inicial)
        except ValueError:
            print("\n❌ El saldo inicial debe ser un número.")
            return

        clientes[dni] = {
            "nombre": nombre,
            "apellido": apellido,
            "edad": edad,
            "telefono": telefono,
            "contraseña": contraseña,  # Solo 6 dígitos numéricos
            "saldo": saldo_inicial
        }
        guardar_clientes()  # Guardar clientes en Excel
        print("\n🟢 Cuenta creada correctamente.")

    elif tipo == "retirar dinero":
        dni = input("\nIngrese DNI del titular: ")
        print("-" * 20)
        if dni in clientes:
            if verificar_contraseña(dni):
                cantidad = input("\nIngrese la cantidad a retirar: S/ ")
                print("-" * 20)
                try:
                    cantidad = float(cantidad)
                    if cantidad <= clientes[dni]["saldo"]:
                        clientes[dni]["saldo"] -= cantidad
                        guardar_clientes()  # Guardar cambios en clientes.xlsx
                        transacciones.append({
                            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "DNI": dni,
                            "Tipo": "Retiro",
                            "Monto": cantidad
                        })
                        guardar_transacciones()  # Guardar transacción en Excel
                        
                        print("\n🟢 Retiro exitoso.")
                        print(f"Saldo restante: S/ {clientes[dni]['saldo']}")
                    else:
                        print("\n❌ Saldo insuficiente.")
                except ValueError:
                    print("\n❌ Cantidad inválida.")
        else:
            print("\n❌ Cliente no encontrado.")

    elif tipo == "ingresar dinero":
        dni = input("\nIngrese DNI del titular: ")
        print("-" * 20)
        if dni in clientes:
            if verificar_contraseña(dni):
                cantidad = input("\nIngrese la cantidad a ingresar: S/ ")
                print("-" * 20)
                try:
                    cantidad = float(cantidad)
                    clientes[dni]["saldo"] += cantidad
                    guardar_clientes()  # Guardar cambios en clientes.xlsx
                    transacciones.append({
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "DNI": dni,
                        "Tipo": "Depósito",
                        "Monto": cantidad
                    })
                    guardar_transacciones()  # Guardar transacción en Excel
                    
                    print(f"🟢 Ingreso exitoso. Saldo actual: S/ {clientes[dni]['saldo']}")
                except ValueError:
                    print("\n❌ Cantidad inválida.")
        else:
            print("\n❌ Cliente no encontrado.")

    elif tipo == "revisar estado de cuenta":
        dni = input("\nIngrese DNI del titular: ")
        print("-" * 20)
        if dni in clientes:
            cliente = clientes[dni]
            print(f"Cliente: {cliente['nombre']} {cliente['apellido']}")
            print(f"Edad: {cliente['edad']} años")
            print(f"Saldo actual: S/ {cliente['saldo']}")
        else:
            print("\n❌ Cliente no encontrado.")

while True:
    mostrar_menu_principal()
    print("-" * 25)
    op = input("\nSeleccione la opción por favor: ")

    if op == "1":
        mostrar_menu("crear cuenta")
    elif op == "2":
        mostrar_menu("retirar dinero")
    elif op == "3":
        mostrar_menu("ingresar dinero")
    elif op == "4":
        mostrar_menu("revisar estado de cuenta")
    elif op == "5":
        print("\nSaliendo del programa....😧")
        break  
    else:
        print("\n❌ ERROR - Opción inválida - ERROR")
