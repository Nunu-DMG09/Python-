from zk import ZK  # Controla dispositivos biométricos
import cv2 # Manejo de cámara y procesamiento de imágenes
import face_recognition # Detecta y reconoce rostros
from chatterbot import ChatBot # Motor de chatbot
from chatterbot.trainers import ChatterBotCorpusTrainer

# =========================
# Configuración del dispositivo ZKTeco - Define la IP y el puerto del lector biométrico
# =========================
ZKTECO_IP = "192.168.1.201"
ZKTECO_PORT = 4370

# =========================
# Inicializar ChatBot 
# =========================
chatbot = ChatBot('MiBot') # Crea un chatbot llamado 'MiBot'
# Se entrena con corpus de conversación en español. 
trainer = ChatterBotCorpusTrainer(chatbot) 
trainer.train('chatterbot.corpus.spanish') 

# =========================
# Registrar nuevo usuario en ZKTeco - Conecta al ZKTeco, registra un usuario por nombre e ID, pero sin huella, 
# solo con datos. Luego, la huella se debe registrar directamente en el dispositivo físico.
# =========================
def registrar_usuario(nombre, user_id="1234", role=0):
    zk = ZK(ZKTECO_IP, port=ZKTECO_PORT, timeout=5)
    try:
        conn = zk.connect()
        conn.disable_device()

        # Registrar usuario (sin huella)
        conn.set_user(uid=int(user_id), name=nombre, privilege=role, password='', group_id='', user_id=user_id)
        print(f"Usuario {nombre} (ID: {user_id}) registrado exitosamente. Ahora registra la huella directamente en el dispositivo.")
        conn.enable_device()
        conn.disconnect()
    except Exception as e:
        print(f"Error registrando usuario: {e}")

# =========================
# Registrar rostro con la cámara
# =========================
def registrar_rostro(nombre_archivo="persona_conocida.jpg"):
    cam = cv2.VideoCapture(0)
    print("Coloca tu rostro frente a la cámara y presiona 's' para capturar.")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Registrar Rostro", frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(nombre_archivo, frame)
            print(f"Rostro capturado y guardado como '{nombre_archivo}'")
            break

        elif cv2.waitKey(1) & 0xFF == ord('q'):
            print("Registro cancelado.")
            break

    cam.release()
    cv2.destroyAllWindows()

# =========================
# Verificación con ZKTeco MB360 (huella registrada)
# =========================
def verificar_huella_con_zkteco():
    zk = ZK(ZKTECO_IP, port=ZKTECO_PORT, timeout=5)
    try:
        print("Conectando al dispositivo ZKTeco...")
        conn = zk.connect()
        conn.disable_device()

        users = conn.get_users()
        if users:
            print("Usuarios encontrados en el dispositivo:")
            for user in users:
                print(f" - ID: {user.user_id}, Nombre: {user.name}")
            conn.enable_device()
            conn.disconnect()
            return True
        else:
            print("No hay usuarios registrados en el dispositivo.")
            conn.disconnect()
            return False

    except Exception as e:
        print(f"Error conectando al dispositivo: {e}")
        return False

# =========================
# Verificación Facial
# =========================
def verificar_rostro():
    video_capture = cv2.VideoCapture(0)
    known_image = face_recognition.load_image_file("persona_conocida.jpg")
    known_encoding = face_recognition.face_encodings(known_image)[0]
    known_faces = [known_encoding]

    print("🧠 Escaneando rostro... Presiona 'q' para cancelar.")

    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            if True in matches:
                print("Rostro reconocido.")
                video_capture.release()
                cv2.destroyAllWindows()
                return True

        cv2.imshow('Reconocimiento Facial', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return False

# =========================
# Iniciar ChatBot
# =========================
def iniciar_chatbot():
    print("\n ChatBot activado. Escribe 'salir' para terminar.")
    while True:
        entrada = input("Tú: ")
        if entrada.lower() == 'salir':
            print("Bot: ¡Hasta luego!")
            break
        respuesta = chatbot.get_response(entrada)
        print("Bot:", respuesta)

# =========================
# Menú principal
# =========================
def mostrar_menu():
    print("\n=== MENÚ ===")
    print("1. Registrar nuevo usuario (huella)")
    print("2. Registrar nuevo rostro")
    print("3. Iniciar sistema biométrico")
    print("4. Salir")
    
    opcion = input("Selecciona una opción (1-4): ")

    if opcion == '1':
        nombre = input("Introduce el nombre del nuevo usuario: ")
        user_id = input("Introduce el ID del nuevo usuario: ")
        registrar_usuario(nombre, user_id)
    elif opcion == '2':
        registrar_rostro()
    elif opcion == '3':
        autenticado = False
        if verificar_huella_con_zkteco():
            if verificar_rostro():
                autenticado = True
        if autenticado:
            iniciar_chatbot()
        else:
            print("Acceso denegado.")
    elif opcion == '4':
        print("¡Hasta luego!")
        exit()
    else:
        print("Opción no válida. Intenta de nuevo.")

# =========================
# Programa Principal
# =========================
if __name__ == "__main__":
    while True:
        mostrar_menu()
