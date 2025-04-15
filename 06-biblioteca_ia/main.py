
# PROGRAMADOR: DAVID MESTA

import chatbot as bot
from chatbot import consulta, prestar, devolver, comprar, consultar_libro, verificar_prestamos

def login():
    att = 3
    print('\n=== 🔐 Inicio de Sesión 🔐 ===')
    while att > 0:
        usuario = input('👤 Usuario: ').strip()
        contrasena = input('🔑 Contraseña: ').strip()
        if usuario == 'david' and contrasena == '123':
            print('✅ Inicio de sesión exitoso.')
            return True
        else:
            att -= 1
            print(f'❌ Usuario o contraseña incorrectos. Intentos restantes: {att}')
    return False

def inicio():
    while True:
        print('\n=== 📚 Bienvenido a la Biblioteca Virtual 📚 ===')
        print('1. 🔐 Iniciar sesión')
        print('2. 🤖 Chatbot')
        print('3. 🚪 Salir')

        opc = input('\n➜ Opción: ').strip()
        if opc == '1':
            if login():
                menu()
            else:
                print('❌ Acceso denegado.')
        elif opc == '2':
            print("💬 Chatbot iniciado (escribe 'salir' para terminar)")
            while True:
                user_input = input('Tu: ').strip()
                if user_input.lower() == 'salir':
                    print('👋 Chatbot finalizado')
                    break
                print('Bot:', bot.get_response(user_input))
        elif opc == '3':
            print("👋 Nos vemos, cuidate!")
            break
        else:
            print('❌ Opción incorrecta.')

def menu():
    while True:
        print('\n=== 📋 Menú Principal 📋 ===')
        print('1. 📚 Consultar libros')
        print('2. 📖 Prestar libro')
        print('3. ↩️  Devolver libro')
        print('4. 💰 Comprar libro')
        print('5. ℹ️  Ver info de un libro')
        print('6. 🔍 Verificar préstamos')
        print('7. 🚪 Salir')

        opc = input('\n➜ Opción: ').strip()
        if opc == '1':
            consulta()
        elif opc == '2':
            prestar()
        elif opc == '3':
            devolver()
        elif opc == '4':
            comprar()
        elif opc == '5':
            titulo = input('Ingrese el título del libro: ').strip()
            consultar_libro(titulo)
        elif opc == '6':
            verificar_prestamos()
        elif opc == '7':
            print("👋 Cerrando sesión...")
            break
        else:
            print('❌ Opción incorrecta.')

if __name__ == '__main__':
    inicio()

