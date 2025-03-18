import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from pathlib import Path

# Definir rutas de los archivos
ruta_clientes = Path(__file__).parent / "clientes.xlsx"
ruta_transacciones = Path(__file__).parent / "transacciones.xlsx"

# Inicializar estructuras
clientes = {}
transacciones = []

# Verificar y cargar datos de clientes
if ruta_clientes.exists():
    try:
        df_clientes = pd.read_excel(ruta_clientes, engine="openpyxl")
        clientes = df_clientes.set_index("DNI").to_dict(orient="index")
    except Exception as e:
        print(f"⚠️ Error al cargar clientes.xlsx: {e}")

# Verificar y cargar datos de transacciones
if ruta_transacciones.exists():
    try:
        df_transacciones = pd.read_excel(ruta_transacciones, engine="openpyxl")
        transacciones = df_transacciones.to_dict(orient="records")
    except Exception as e:
        print(f"⚠️ Error al cargar transacciones.xlsx: {e}")

# Función para guardar clientes
def guardar_clientes():
    df_clientes = pd.DataFrame.from_dict(clientes, orient="index")
    df_clientes.to_excel(ruta_clientes, sheet_name="Clientes", index_label="DNI", engine="openpyxl")

# Función para guardar transacciones
def guardar_transacciones():
    df_transacciones = pd.DataFrame(transacciones)
    df_transacciones.to_excel(ruta_transacciones, sheet_name="Transacciones", index=False, engine="openpyxl")

# Menú principal
def mostrar_menu_principal():
    print("\nMenu de opciones")
    print("1. Crear cuenta ⚪")
    print("2. Retirar dinero 🔴")
    print("3. Ingresar dinero 🟢")
    print("4. Revisar estado de cuenta 🟡")
    print("5. Ver gráfico 📊")
    print("6. Salir 💥")

# VALIDACIONES
def validar_dni(dni):
    return dni.isdigit() and len(dni) == 8

def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 9

def validar_edad(edad):
    return edad.isdigit() and int(edad) >= 18  

def validar_contraseña(contraseña):
    return contraseña.isdigit() and len(contraseña) == 6

def verificar_contraseña(dni):
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

def ver_grafico():
    if not transacciones:
        print("\n❌ No hay transacciones registradas para generar gráficos.")
        return
    
    df_transacciones = pd.DataFrame(transacciones)
    
    # Gráfico de pastel: Cliente con más transacciones
    transacciones_por_cliente = df_transacciones["DNI"].value_counts()
    
    plt.figure(figsize=(8, 6))
    plt.pie(transacciones_por_cliente, labels=transacciones_por_cliente.index, autopct="%1.1f%%", startangle=140)
    plt.title("Distribución de transacciones por cliente")
    plt.axis("equal")
    plt.show()
    
# Función principal del menú
def mostrar_menu(tipo):
    global clientes, transacciones
    print(f"\nOpción: {tipo}")

    if tipo == "crear cuenta":
        while True:
            dni = input("\nIngrese DNI: ")
            if validar_dni(dni):
                break
            print("❌ DNI inválido. Debe tener 8 dígitos.")

        while True:
            telefono = input("\nIngrese su número de teléfono: ")
            if validar_telefono(telefono):
                break
            print("❌ Número inválido. Debe tener 9 dígitos.")

        nombre = input("\nIngrese su nombre: ")
        apellido = input("\nIngrese su apellido: ")

        while True:
            edad = input("\nIngrese su edad: ")
            if validar_edad(edad):
                edad = int(edad)
                break
            print("❌ Debe ser mayor de 18 años.")

        while True:
            contraseña = input("\nCree una contraseña (6 dígitos): ")
            if validar_contraseña(contraseña):
                break
            print("❌ La contraseña debe tener exactamente 6 dígitos.")

        saldo_inicial = input("\nIngrese el saldo inicial: S/ ")
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
            "contraseña": contraseña,
            "saldo": saldo_inicial
        }
        guardar_clientes()  # Guardar en Excel
        print("\n🟢 Cuenta creada correctamente.")

    elif tipo == "retirar dinero":
        dni = input("\nIngrese DNI del titular: ")
        if dni in clientes:
            if verificar_contraseña(dni):
                cantidad = input("\nIngrese la cantidad a retirar: S/ ")
                try:
                    cantidad = float(cantidad)
                    if cantidad <= clientes[dni]["saldo"]:
                        clientes[dni]["saldo"] -= cantidad
                        guardar_clientes()
                        transacciones.append({
                            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "DNI": dni,
                            "Tipo": "Retiro",
                            "Monto": cantidad
                        })
                        guardar_transacciones()
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
        if dni in clientes:
            if verificar_contraseña(dni):
                cantidad = input("\nIngrese la cantidad a ingresar: S/ ")
                try:
                    cantidad = float(cantidad)
                    clientes[dni]["saldo"] += cantidad
                    transacciones.append({
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "DNI": dni,
                        "Tipo": "Depósito",
                        "Monto": cantidad
                    })
                    guardar_transacciones()
                    print(f"🟢 Ingreso exitoso. Saldo actual: S/ {clientes[dni]['saldo']}")
                except ValueError:
                    print("\n❌ Cantidad inválida.")
        else:
            print("\n❌ Cliente no encontrado.")

    elif tipo == "revisar estado de cuenta":
        dni = input("\nIngrese DNI del titular: ")
        if dni in clientes:
            cliente = clientes[dni]
            print(f"Cliente: {cliente['nombre']} {cliente['apellido']}")
            print(f"Edad: {cliente['edad']} años")
            print(f"Saldo actual: S/ {cliente['saldo']}")
        else:
            print("\n❌ Cliente no encontrado.")

# Bucle principal
while True:
    mostrar_menu_principal()
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
        ver_grafico()
    elif op == "6":
        print("\nSaliendo del programa....😧")
        break  
    else:
        print("\n❌ ERROR - Opción inválida - ERROR")


