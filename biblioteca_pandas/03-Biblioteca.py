
from datetime import datetime

usuarios = {"72357275": "1234"}
transacciones = []
libros = [
    {"titulo": "El gran drama", "autor": "Juan Pérez", "categoria": "Drama", "fecha_edicion": "2005", "estado": "disponible", "precio": 50},
    {"titulo": "Hamlet", "autor": "William Shakespeare", "categoria": "Drama", "fecha_edicion": "1603", "estado": "disponible", "precio": 80},
    {"titulo": "Edipo rey", "autor": "Sófocles", "categoria": "Drama", "fecha_edicion": "1872", "estado": "disponible", "precio": 90},
    {"titulo": "Dracula", "autor": "Bram Stoker", "categoria": "Terror", "fecha_edicion": "1897", "estado": "disponible", "precio": 55},
    {"titulo": "Noche de terror", "autor": "María Gómez", "categoria": "Terror", "fecha_edicion": "2010", "estado": "disponible", "precio": 60},
    {"titulo": "Guerra mundial Z", "autor": "Max Brooks", "categoria": "Terror", "fecha_edicion": "2006", "estado": "disponible", "precio": 90},
    {"titulo": "Accion sin limites", "autor": "Carlos Ruiz", "categoria": "Accion", "fecha_edicion": "2018", "estado": "disponible", "precio": 45},
    {"titulo": "Dulces sueños", "autor": "Robert Bloch", "categoria": "Accion", "fecha_edicion": "2021", "estado": "disponible", "precio": 83},
    {"titulo": "Esperando al diluvio", "autor": "Dolores Rodondo", "categoria": "Accion", "fecha_edicion": "2024", "estado": "disponible", "precio": 75},
]



def login():
    print("\n--- Bienvenido ---")
    usuario = input("Ingrese su número de usuario: ")
    contrasena = input("Ingrese su contraseña: ")
    
    if usuario in usuarios and usuarios[usuario] == contrasena:
        print(f"Acceso concedido.\n")
        return True
    else:
        print("Usuario o contraseña incorrectos.\n")
        return False
       

def mostrar_libros():
    print("\n--- Libros Disponibles ---")
    for i, libro in enumerate(libros, 1):
        print(f"{i}. {libro['titulo']} - {libro['autor']} ({libro['categoria']}) - {libro['fecha_edicion']} - Estado: {libro['estado']}")

def vender_libro():
    mostrar_libros()
    opcion = int(input("Seleccione el número del libro a vender: ")) - 1
    
    if 0 <= opcion < len(libros) and libros[opcion]["estado"] == "disponible":
        libros[opcion]["estado"] = "vendido"
        fecha_venta = datetime.now().strftime('%d/%m/%Y')
        transacciones.append({
            "titulo": libros[opcion]["titulo"],
            "tipo": "venta",
            "precio": libros[opcion]["precio"],
            "fecha": fecha_venta
        })
        print(f"Libro '{libros[opcion]['titulo']}' vendido por {libros[opcion]['precio']} soles el {fecha_venta}.\n")
    else:
        print("Selección inválida o libro no disponible.\n")

def prestar_libro():
    mostrar_libros()
    opcion = int(input("Seleccione el número del libro a prestar: ")) - 1
    
    if 0 <= opcion < len(libros) and libros[opcion]["estado"] == "disponible":
        libros[opcion]["estado"] = "prestado"
        nombre_prestatario = input("Ingrese el nombre del prestatario: ")
        fecha_devolucion = input("Ingrese la fecha de devolución (DD/MM/AAAA): ")
        transacciones.append({
            "titulo": libros[opcion]["titulo"],
            "tipo": "prestamo",
            "prestatario": nombre_prestatario,
            "fecha_devolucion": fecha_devolucion
        })
        print(f"Libro '{libros[opcion]['titulo']}' prestado a {nombre_prestatario} hasta {fecha_devolucion}.\n")
    else:
        print("Selección inválida o libro no disponible.\n")

def buscar_libro():
    titulo = input("Ingrese el título del libro a buscar: ").lower()
    encontrado = False
    for libro in libros:
        if libro["titulo"].lower() == titulo.lower():
            print(f"Libro: {libro['titulo']} - Autor: {libro['autor']} ({libro['categoria']}) - {libro['fecha_edicion']}")
            if libro["estado"] == "vendido":
                for transaccion in transacciones:
                    if transaccion["titulo"] == libro["titulo"] and transaccion["tipo"] == "venta":
                        print(f"Estado: Vendido - Precio: {transaccion['precio']} soles - Fecha de venta: {transaccion['fecha']}")
            elif libro["estado"] == "prestado":
                for transaccion in transacciones:
                    if transaccion["titulo"] == libro["titulo"] and transaccion["tipo"] == "prestamo":
                        print(f"Estado: Prestado a {transaccion['prestatario']} hasta {transaccion['fecha_devolucion']}")
            else:
                print("Estado: Disponible")
            encontrado = True
            break
    
    if not encontrado:
        print("Libro no encontrado.\n")

def menu():
    while True:
        print("\n--- Biblioteca ElGranSaber ---")
        print("1. Mostrar libros disponibles")
        print("2. Vender libro")
        print("3. Prestar libro")
        print("4. Buscar libro")
        print("5. Salir")
        op = input("Seleccione una opción: ")
        
        if op == "1":
            mostrar_libros()
        elif op == "2":
            vender_libro()
        elif op == "3":
            prestar_libro()
        elif op == "4":
            buscar_libro()
        elif op == "5":
            confirmacion = input("\n¿Seguro que desea salir? 😿 (Si/No): ").lower()
            if confirmacion == "no":
                print("\nRegresando al menú principal...😸")
                continue  # Regresa al menú principal"
            elif confirmacion == "si":
                print("\nSaliendo del programa....hasta pronto!!")
                break  # Sale del programa 
            else:
                print("\n❌ Opción no válida. El programa continuará.")
        else:
            print("Opción inválida. Intente de nuevo.\n")

if login():
    menu()
