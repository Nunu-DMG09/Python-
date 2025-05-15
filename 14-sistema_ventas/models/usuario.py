from utils.db import get_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_usuario(nombre_usuario, contraseña):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        hashed = hash_password(contraseña)
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contraseña) VALUES (%s, %s)",
                       (nombre_usuario, hashed))
        conn.commit()
        cursor.close()
        conn.close()

def login(nombre_usuario, contraseña):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        hashed = hash_password(contraseña)
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario=%s AND contraseña=%s",
                       (nombre_usuario, hashed))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    return False
