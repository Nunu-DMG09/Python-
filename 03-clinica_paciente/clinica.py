pacientes = {}

def mostrar_menu_principal():
    print("Menu de opciones")
    print("1. Insertar un paciente")
    print("2. Buscar paciente")
    print("3. Costo")
    print("4. Eliminar paciente")
    print("5. Salir")

def validar_dni(dni):
    return dni.isdigit() and len(dni) == 8

def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 9

def validar_edad(edad):
    return edad.isdigit() 

def mostrar_menu(tipo):
    global pacientes
    print(f" Opcion: {tipo}")

    if tipo == "insertar paciente":
        while True:
            dni = input("Ingrese DNI (8 dígitos numéricos): ")
            if validar_dni(dni):
                break
            else:
                print("DNI inválido")

        apellido_paterno = input("Apellido Paterno: ")
        apellido_materno = input("Apellido Materno: ")
        nombre = input("Nombre: ")
        while True:
            telefono = input("Ingrese su numero: ")
            if validar_telefono(telefono):
                break
            else:
                print("Telefono incorrecto. Solo son 9 digitos")
        while True:
            edad = input("Ingrese su edad: ")
            if validar_edad(edad):
                break
            else:
                print("Solo números")
            
    
        pacientes[dni] = {
            "apellido_paterno": apellido_paterno,
            "apellido_materno": apellido_materno,
            "nombre": nombre,
            "telefono": telefono,
            "edad": edad
        }
        print("Paciente registrado correctamente")

    elif tipo == "buscar paciente":
        while True:
            dni_buscar = input("Ingrese DNI del paciente registrado (8 dígitos): ")
            if validar_dni(dni_buscar):
                break
            else:
                print("DNI inválido. Asegúrese de que el DNI tenga 8 dígitos numéricos.")
        
        if dni_buscar in pacientes:
            paciente = pacientes[dni_buscar]
            print(f"Paciente encontrado: {paciente['nombre']} {paciente['apellido_paterno']} {paciente['apellido_materno']}")
        else:
            print("Paciente no encontrado")

    elif tipo == "costo":
        dni_costo = input("Ingrese DNI del paciente: ")
        print("El costo es de S/100")

    elif tipo == "eliminar paciente":
        dni_eliminar = input("Ingrese DNI del paciente: ")
        if dni_eliminar in pacientes:
            del pacientes[dni_eliminar]
            print("Paciente eliminado")
        else:
            print("Paciente no encontrado")

while True:
    mostrar_menu_principal()
    op = input("Seleccione la opcion por favor: ")

    if op == "1":
        mostrar_menu("insertar paciente")
    elif op == "2":
        mostrar_menu("buscar paciente")
    elif op == "3":
        mostrar_menu("costo")
    elif op == "4":
        mostrar_menu("eliminar paciente")
    elif op == "5":
        print("Saliendo del programa....")
        break
    else:
        print("Opcion inválida - ERROR")

