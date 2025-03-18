clientes = {}

def mostrar_menu_principal():
    print("\nMenu de opciones")
    print("1. Crear cuenta ⚪")
    print("2. Retirar dinero 🔴")
    print("3. Ingresar dinero 🟢")
    print("4. Revisar el estado de tu cuenta 🟡")
    print("5. Salir 💥")

# VALIDACION DE DNI Y TELEFONO
def validar_dni(dni):
    return dni.isdigit() and len(dni) == 8
def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 9
#

def mostrar_menu(tipo):
    global clientes
    print(f"\nOpcion: {tipo}")

    if tipo == "crear cuenta":
        while True:
            dni = input("\nIngrese DNI: ")
            print("-"*20)
            if validar_dni(dni):
                break
            else:
                print("❌ DNI inválido. Recuerde que son 8 digitos.")

                salir = input("\n¿Desea regresar al menu principal? 😿 (Si/No): ").lower()
            if salir == "no":
                print("\nContinuamos...😸")
                continue  # Regresa al menú principal"
            elif salir == "si":
                mostrar_menu_principal()
            else:
                print("\n❌ Opción no válida. El programa continuará.")
                
        
        while True:
            telefono = input("\nIngrese su numero de telefono: ")
            print("-"*20)
            if validar_telefono(telefono):
                break
            else:
                print("❌ ERROR - Número incorrecto. Debe tener 9 dígitos.")
                
        nombre = input("\nNombre del titular de la cuenta: ")
        print("-"*20)
        saldo_inicial = input("\nIngrese el saldo inicial: S/ ")
        print("-"*20)

        try:
            saldo_inicial = float(saldo_inicial)
        except ValueError:
            print("\n❌ El saldo inicial debe ser un número.")
            return

        clientes[dni] = {
            "nombre": nombre,
            "telefono": telefono,
            "saldo": saldo_inicial
        }
        print("\n🟢 Cuenta creada correctamente.")

    elif tipo == "retirar dinero":
        dni = input("\nIngrese DNI del titular: ")
        print("-"*20)
        if dni in clientes:
            cantidad = input("\nIngrese la cantidad a retirar: S/ ")
            print("-"*20)
            try:
                cantidad = float(cantidad)
                if cantidad <= clientes[dni]["saldo"]:
                    clientes[dni]["saldo"] -= cantidad
                    saldo_restante = clientes[dni]["saldo"]
                    # GENERA VAUCHER :D
                    print("\n🟢 Retiro exitoso.")
                    print("-" * 30)
                    print("🎟️ VOUCHER DE RETIRO")
                    print(f"Cliente: {clientes[dni]['nombre']}")
                    print(f"Cantidad retirada: S/ {cantidad}")
                    print(f"Saldo restante: S/ {saldo_restante}")
                    print("-" * 30)
                else:
                    print("\n❌ Saldo insuficiente.")
            except ValueError:
                print("\n❌ Cantidad inválida.")
        else:
            print("\n❌ Cliente no encontrado.")

    elif tipo == "ingresar dinero":
        dni = input("\nIngrese DNI del titular: ")
        print("-"*20)
        if dni in clientes:
            cantidad = input("\nIngrese la cantidad a ingresar: S/ ")
            print("-"*20)
            try:
                cantidad = float(cantidad)
                clientes[dni]["saldo"] += cantidad
                print(f"🟢 Ingreso exitoso. Saldo actual: S/ {clientes[dni]['saldo']}")
            except ValueError:
                print("\n❌ Cantidad inválida.")
        else:
            print("\n❌ Cliente no encontrado.")

    elif tipo == "revisar estado de cuenta":
        dni = input("\nIngrese DNI del titular: ")
        print("-"*20)
        if dni in clientes:
            cliente = clientes[dni]
            print(f"Cliente: {cliente['nombre']}")
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
        confirmacion = input("\n¿Seguro que desea salir? 😿 (Si/No): ").lower()
        if confirmacion == "no":
            print("\nRegresando al menú principal...😸")
            continue  # Regresa al menú principal"
        elif confirmacion == "si":
            print("\nSaliendo del programa....😧")
            break  # Sale del programa 
        else:
            print("\n❌ Opción no válida. El programa continuará.")
    else:
        print("\n❌ EROR - Opción inválida - ERROR")
