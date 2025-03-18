
# PROGRAMADOR: DAVID MESTA 

import pandas as pd
import random
import re
from datetime import datetime


# Datos iniciales
usuarios = {"72357275": "1234"}
transacciones = []

# Base de datos de libros
libros_data = [
    ["El gran drama", "Juan Pérez", "Drama", "2005", "disponible", 50],
    ["Hamlet", "William Shakespeare", "Drama", "1603", "disponible", 80],
    ["Edipo rey", "Sófocles", "Drama", "1872", "disponible", 90],
    ["Dracula", "Bram Stoker", "Terror", "1897", "disponible", 55],
    ["Noche de terror", "María Gómez", "Terror", "2010", "disponible", 60],
    ["Guerra mundial Z", "Max Brooks", "Terror", "2006", "disponible", 90],
    ["Accion sin limites", "Carlos Ruiz", "Accion", "2018", "disponible", 45],
    ["Dulces sueños", "Robert Bloch", "Accion", "2021", "disponible", 83],
    ["Esperando al diluvio", "Dolores Rodondo", "Accion", "2024", "disponible", 75]
]
columnas = ["titulo", "autor", "categoria", "fecha_edicion", "estado", "precio"]
libros = pd.DataFrame(libros_data, columns=columnas)

def consulta():
    disponibles = libros[libros["estado"] == "disponible"]
    if disponibles.empty:
        print("📚 No hay libros disponibles.")
    else:
        print(disponibles[["titulo", "autor", "categoria", "fecha_edicion", "estado"]])

def prestar():
    consulta()
    try:
        opcion = int(input("Seleccione el número del libro a prestar (por índice): ").strip())
        if 0 <= opcion < len(libros) and libros.at[opcion, "estado"] == "disponible":
            libros.at[opcion, "estado"] = "prestado"
            nombre_prestatario = input("Ingrese el nombre del prestatario: ").strip()
            fecha_devolucion = input("Ingrese la fecha de devolución (DD/MM/AAAA): ").strip()
            transacciones.append({"titulo": libros.at[opcion, "titulo"], "prestatario": nombre_prestatario, "fecha_devolucion": fecha_devolucion, "devuelto": False})
            print(f"📖 Libro '{libros.at[opcion, 'titulo']}' prestado a {nombre_prestatario} hasta {fecha_devolucion}.")
        else:
            print("❌ Opción inválida o el libro ya está prestado.")
    except ValueError:
        print("❌ Entrada no válida. Ingrese un número de índice válido.")

def devolver():
    titulo = input("Ingrese el título del libro a devolver: ").strip()
    for i in range(len(libros)):
        if libros.at[i, "titulo"].lower() == titulo.lower() and libros.at[i, "estado"] == "prestado":
            libros.at[i, "estado"] = "disponible"
            for transaccion in transacciones:
                if transaccion["titulo"].lower() == titulo.lower() and not transaccion["devuelto"]:
                    transaccion["devuelto"] = True
                    break
            print(f"✅ El libro '{titulo}' ha sido devuelto con éxito.")
            return
    print("❌ Libro no encontrado o no está prestado.")

def comprar():
    consulta()
    try:
        opcion = int(input("Seleccione el número del libro a comprar (por índice): ").strip())
        if 0 <= opcion < len(libros) and libros.at[opcion, "estado"] == "disponible":
            libros.at[opcion, "estado"] = "vendido"
            fecha_venta = datetime.now().strftime('%d/%m/%Y')
            transacciones.append({"titulo": libros.at[opcion, "titulo"], "tipo": "venta", "precio": libros.at[opcion, "precio"], "fecha": fecha_venta})
            print(f"💰 Libro '{libros.at[opcion, 'titulo']}' vendido por {libros.at[opcion, 'precio']} soles el {fecha_venta}.")
        else:
            print("❌ Opción inválida o el libro ya está vendido.")
    except ValueError:
        print("❌ Entrada no válida. Ingrese un número de índice válido.")

def consultar_libro(titulo):
    resultado = libros[libros["titulo"].str.lower() == titulo.lower()]
    if not resultado.empty:
        print(resultado)
    else:
        print("❌ Libro no encontrado.")

def verificar_prestamos():
    prestamos = [t for t in transacciones if "prestatario" in t]
    if not prestamos:
        print("📚 No hay préstamos registrados.")
        return
    
    print("\n📋 Estado de Préstamos:")
    for t in prestamos:
        estado = "✅ Devuelto" if t["devuelto"] else "❌ No devuelto"
        print(f"📖 {t['titulo']} | 🧑 {t['prestatario']} | 📅 Devolución: {t['fecha_devolucion']} | {estado}")


def get_response(input_user):
    words = input_user.lower().split()
    if not words:
        return unknown()
    command = words[0]
    commands = {
        'consultar': consulta,
        'prestar': prestar,
        'devolver': devolver,
        'comprar': comprar,
        'info': consultar_libro,
        'verificar': verificar_prestamos
    }
    if command in commands:
        if command == 'info':
            if len(words) > 1:
                titulo = ' '.join(words[1:]).upper()
                consultar_libro(titulo)
            else:
                return 'Por favor, escribe "info" seguido del título del libro.\nEjemplo: info IT'
        else:
            commands[command]()
        return f'Comando {command} ejecutado correctamente'

    splited = re.split(r'\s|[,:;.?!-_@]\s*', input_user.lower())
    response = check_all_messages(splited)
    return response

def msg_probability(user_msg, recognized_words, single_response=False, required_words=[]):
    msg_certainty = 0
    has_required_words = True
    for word in user_msg:
        if word in recognized_words:
            msg_certainty += 1
    pergentage = float(msg_certainty) / float(len(user_msg))
    for word in required_words:
        if word not in user_msg:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(pergentage * 100)
    else:
        return 0

def check_all_messages(msg):
    highest_prob = {}

    def response(bot_responses, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob
        responses = bot_responses if isinstance(bot_responses, list) else [bot_responses]
        highest_prob[tuple(responses)] = msg_probability(msg, list_of_words, single_response, required_words)
    response('''
        🤖 Comandos disponibles:
        📚 consultar - Ver todos los libros
        📖 prestar - Prestar un libro
        ↩️ devolver - Devolver un libro
        💰 comprar - Comprar un libro
        ℹ️   info (título) - Ver información de un libro
        ✅ verificar - Verificar prestamo 
    ''', ['ayuda', 'comandos', 'opciones', 'help', 'ayudame'], single_response=True)
    response([
        '👋 ¡Hola! ¿Cómo puedo ayudarte?',
        '¡Hola! ¿En qué puedo servirte hoy? 😊',
        '¡Saludos! ¿Qué necesitas? 🌟',
        '¡Bienvenido! ¿En qué te puedo ayudar? 🤝',
    ], ['hola', 'saludos', 'buenas'], single_response=True)
    response('📍 Estamos ubicados en Senati Chiclayo', ['donde', 'ubicados', 'direccion', 'ubicacion'], single_response=True)
    response([
        '😊 ¡Siempre a tus órdenes!',
        '¡No hay de qué! 🌟',
        '¡Es un placer ayudarte! 💫',
        '¡Para eso estamos! 🤝'
    ], ['gracias', 'agradezco', 'thanks', 'adios', 'hasta pronto'], single_response=True)
    response('Para ver los libros disponibles, escribe "consultar"', ['libros', 'consulta', 'ver', 'disponibles'], required_words=['consultar'])
    response('Para prestar un libro, escribe "prestar"', ['prestar', 'tomar', 'libro', 'prestado'], required_words=['prestar'])
    response('Para devolver un libro, escribe "devolver"', ['devolver', 'regresar', 'libro'], required_words=['devolver'])
    response('Para comprar un libro, escribe "comprar"', ['comprar', 'adquirir', 'libro'], required_words=['comprar'])
    response('Para ver la información de un libro, escribe "info (nombre del libro deseado)"', ['info', 'informacion', 'detalles', 'libro'], required_words=['info'])
    response('Para ver si se ha devuelto el libro escribe "verificar"', ['verificar', 'comprobar', 'examinar', 'confirmar'], required_words=['verificar'])
    response([
        'Estoy bien, gracias'
        '¡Estoy genial! 😊',
        '¡Todo bien! ¿Y tú? 🌟',
        'Todo bacán, mano 🤝',
        'Chévere, mi king 👑'
    ], ['como', 'estas', 'vas', 'tal', 'que', 'onda', 'encuentras'], single_response=True)

    response('🤖 Soy un bot creado por DavidPro, soy genial!!!', ['quien', 'eres', 'creador', 'bot'], single_response=True)

    best_match = max(highest_prob, key=highest_prob.get)
    if highest_prob[best_match] < 1:
        return unknown()
    return random.choice(list(best_match))

def unknown():
    responses = [
        '❓ ¿Puedes decirlo de nuevo?',
        '😕 No estoy seguro de lo que quieres decir',
        '🤔 No entiendo lo que dices',
        '🤨 ¿Podrías reformular tu pregunta?',
        '😅 No logro entender, ¿podrías ser más específico?'
    ]
    return random.choice(responses)