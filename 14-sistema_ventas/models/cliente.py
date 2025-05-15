from utils.db import get_connection

def listar_clientes():
    conn = get_connection()
    clientes = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        cursor.close()
        conn.close()
    return clientes

def registrar_cliente(nombre, dni, direccion, telefono):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre_cliente, dni, direccion, telefono) VALUES (%s, %s, %s, %s)",
                       (nombre, dni, direccion, telefono))
        conn.commit()
        cursor.close()
        conn.close()

def eliminar_cliente(id_cliente):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id_cliente,))
        conn.commit()
        cursor.close()
        conn.close()

def obtener_cliente(id_cliente):
    conn = get_connection()
    cliente = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE id_cliente=%s", (id_cliente,))
        cliente = cursor.fetchone()
        cursor.close()
        conn.close()
    return cliente

def actualizar_cliente(id_cliente, nombre, dni, direccion, telefono):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE clientes SET nombre_cliente=%s, dni=%s, direccion=%s, telefono=%s 
                          WHERE id_cliente=%s""",
                       (nombre, dni, direccion, telefono, id_cliente))
        conn.commit()
        cursor.close()
        conn.close()
