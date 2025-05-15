from utils.db import get_connection

def registrar_venta(id_cliente, productos):
    """
    productos: lista de tuplas (id_producto, cantidad, precio_unitario)
    """
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            total = sum(cant * precio for _, cant, precio in productos)
            cursor.execute("INSERT INTO ventas (id_cliente, total) VALUES (%s, %s)", (id_cliente, total))
            id_venta = cursor.lastrowid

            for id_prod, cant, precio in productos:
                cursor.execute(
                    "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                    (id_venta, id_prod, cant, precio))
                # Actualizar stock
                cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (cant, id_prod))

            conn.commit()
        except Exception as e:
            conn.rollback()
            print("Error registrando venta:", e)
        finally:
            cursor.close()
            conn.close()

def listar_ventas():
    conn = get_connection()
    ventas = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.id_venta, v.fecha, v.total, c.nombre_cliente 
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            ORDER BY v.fecha DESC
        """)
        ventas = cursor.fetchall()
        cursor.close()
        conn.close()
    return ventas

def obtener_detalle_venta(id_venta):
    conn = get_connection()
    detalles = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.nombre_producto, dv.cantidad, dv.precio_unitario 
            FROM detalle_ventas dv
            JOIN productos p ON dv.id_producto = p.id_producto
            WHERE dv.id_venta = %s
        """, (id_venta,))
        detalles = cursor.fetchall()
        cursor.close()
        conn.close()
    return detalles
