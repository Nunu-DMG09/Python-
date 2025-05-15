from utils.db import get_connection

def listar_productos():
    conn = get_connection()
    productos = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
    return productos

def agregar_producto(nombre, precio, stock):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre_producto, precio, stock) VALUES (%s, %s, %s)",
                       (nombre, precio, stock))
        conn.commit()
        cursor.close()
        conn.close()

def eliminar_producto(id_producto):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
        conn.commit()
        cursor.close()
        conn.close()

def obtener_producto(id_producto):
    conn = get_connection()
    producto = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (id_producto,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()
    return producto

def actualizar_producto(id_producto, nombre, precio, stock):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE productos SET nombre_producto=%s, precio=%s, stock=%s 
                          WHERE id_producto=%s""",
                       (nombre, precio, stock, id_producto))
        conn.commit()
        cursor.close()
        conn.close()

def actualizar_stock(id_producto, cantidad_vendida):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        # Reducimos stock tras la venta
        cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto=%s",
                       (cantidad_vendida, id_producto))
        conn.commit()
        cursor.close()
        conn.close()
