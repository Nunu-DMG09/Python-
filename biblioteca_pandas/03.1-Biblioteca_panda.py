
import pandas as pd
from datetime import datetime

# Datos iniciales
usuarios = {"72357275": "1234"}
transacciones = []

# Creando DataFrame para libros
libros_data = [
    ["El gran drama", "Juan Pérez", "Drama", "2005", "disponible", 50],
    ["Hamlet", "William Shakespeare", "Drama", "1603", "disponible", 80],
    ["Edipo rey", "Sófocles", "Drama", "1872", "disponible", 90],
    ["Dracula", "Bram Stoker", "Terror", "1897", "disponible", 55],
    ["Noche de terror", "María Gómez", "Terror", "2010", "disponible", 60],
    ["Guerra mundial Z", "Max Brooks", "Terror", "2006", "disponible", 90],
    ["Accion sin limites", "Carlos Ruiz", "Accion", "2018", "disponible", 45],
    ["Dulces sueños", "Robert Bloch", "Accion", "2021", "disponible", 83],
    ["Esperando al diluvio", "Dolores Rodondo", "Accion", "2024", "disponible", 75],
]
columnas = ["titulo", "autor", "categoria", "fecha_edicion", "estado", "precio"]
libros = pd.DataFrame(libros_data, columns=columnas)

def login():
    print("\n--- Bienvenido ---")
    usuario = input("Ingrese su número de usuario: ")
    contrasena = input("Ingrese su contraseña: ")
    if usuario in usuarios and usuarios[usuario] == contrasena:
        print("Acceso concedido.\n")
        return True
    else:
        print("Usuario o contraseña incorrectos.\n")
        return False

def mostrar_libros():
    print("\n--- Libros Disponibles ---")
    print(libros[libros["estado"] == "disponible"][["titulo", "autor", "categoria", "fecha_edicion", "estado"]])

def vender_libro():
    mostrar_libros()
    opcion = int(input("Seleccione el número del libro a vender (por índice): "))
    if 0 <= opcion < len(libros) and libros.at[opcion, "estado"] == "disponible":
        libros.at[opcion, "estado"] = "vendido"
        fecha_venta = datetime.now().strftime('%d/%m/%Y')
        transacciones.append({"titulo": libros.at[opcion, "titulo"], "tipo": "venta", "precio": libros.at[opcion, "precio"], "fecha": fecha_venta})
        print(f"Libro '{libros.at[opcion, 'titulo']}' vendido por {libros.at[opcion, 'precio']} soles el {fecha_venta}.\n")
    else:
        print("Selección inválida o libro no disponible.\n")

def prestar_libro():
    mostrar_libros()
    opcion = int(input("Seleccione el número del libro a prestar (por índice): "))
    if 0 <= opcion < len(libros) and libros.at[opcion, "estado"] == "disponible":
        libros.at[opcion, "estado"] = "prestado"
        nombre_prestatario = input("Ingrese el nombre del prestatario: ")
        fecha_devolucion = input("Ingrese la fecha de devolución (DD/MM/AAAA): ")
        transacciones.append({"titulo": libros.at[opcion, "titulo"], "tipo": "prestamo", "prestatario": nombre_prestatario, "fecha_devolucion": fecha_devolucion})
        print(f"Libro '{libros.at[opcion, 'titulo']}' prestado a {nombre_prestatario} hasta {fecha_devolucion}.\n")
    else:
        print("Selección inválida o libro no disponible.\n")

def buscar_libro():
    titulo = input("Ingrese el título del libro a buscar: ").lower()
    resultado = libros[libros["titulo"].str.lower() == titulo]
    if not resultado.empty:
        print(resultado)
    else:
        print("Libro no encontrado.\n")


def verificar_prestamos():
    hoy = datetime.now().strftime('%d/%m/%Y')
    print("\n--- Libros Prestados ---")
    prestamos_pendientes = [t for t in transacciones if t["tipo"] == "prestamo"]
    
    if not prestamos_pendientes:
        print("No hay libros prestados actualmente.\n")
        return
    
    for prestamo in prestamos_pendientes:
        titulo = prestamo["titulo"]
        prestatario = prestamo["prestatario"]
        fecha_devolucion = prestamo["fecha_devolucion"]
        
        if datetime.strptime(hoy, "%d/%m/%Y") > datetime.strptime(fecha_devolucion, "%d/%m/%Y"):
            print(f"❌ El libro '{titulo}' NO ha sido devuelto a tiempo. Debía ser devuelto el {fecha_devolucion}.")
        else:
            print(f"✅ El libro '{titulo}' está prestado a {prestatario} y debe ser devuelto el {fecha_devolucion}.")



def menu():
    while True:
        print("\n--- Biblioteca ElGranSaber ---")
        print("1. Mostrar libros disponibles")
        print("2. Vender libro")
        print("3. Prestar libro")
        print("4. Buscar libro")
        print("5. Verificar préstamos no devueltos")
        print("6. Salir")
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
            verificar_prestamos()
        elif op == "6":
            confirmacion = input("\n¿Seguro que desea salir? 😿 (Si/No): ").lower()
            if confirmacion == "no":
                print("\nRegresando al menú principal...😸")
            elif confirmacion == "si":
                print("\nSaliendo del programa....hasta pronto!!")
                break
            else:
                print("\n❌ Opción no válida. El programa continuará.")
        else:
            print("Opción inválida. Intente de nuevo.\n")

if login():
    menu()