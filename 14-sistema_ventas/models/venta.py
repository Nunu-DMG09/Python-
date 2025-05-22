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

def obtener_venta_por_id(id_venta):
    conn = get_connection()
    venta = None
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id_venta, v.fecha, v.total, v.id_cliente, c.nombre_cliente
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            WHERE v.id_venta = %s
        """, (id_venta,))
        venta = cursor.fetchone()
        cursor.close()
        conn.close()
    return venta

def agregar_detalle_venta(id_venta, id_producto, cantidad, precio_unitario):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Insertar el detalle de venta
            cursor.execute("""
                INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """, (id_venta, id_producto, cantidad, precio_unitario))

            # Actualizar stock del producto
            cursor.execute("""
                UPDATE productos SET stock = stock - %s WHERE id_producto = %s
            """, (cantidad, id_producto))

            conn.commit()
        except Exception as e:
            conn.rollback()
            print("Error al agregar detalle de venta:", e)
        finally:
            cursor.close()
            conn.close()

def obtener_precio_producto(id_producto):
    conn = get_connection()
    precio = 0
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT precio FROM productos WHERE id_producto = %s", (id_producto,))
            resultado = cursor.fetchone()
            if resultado:
                precio = resultado[0]
        except Exception as e:
            print("Error al obtener precio del producto:", e)
        finally:
            cursor.close()
            conn.close()
    return precio

def obtener_venta(id_venta):
    conn = get_connection()
    venta = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT v.id_venta, v.fecha, v.total, v.id_cliente, c.nombre_cliente
                FROM ventas v
                JOIN clientes c ON v.id_cliente = c.id_cliente
                WHERE v.id_venta = %s
            """, (id_venta,))
            venta = cursor.fetchone()
        except Exception as e:
            print("Error al obtener la venta:", e)
        finally:
            cursor.close()
            conn.close()
    return venta

def listar_productos_con_stock():
    conn = get_connection()
    productos = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id_producto, nombre_producto, stock, precio
                FROM productos
                WHERE stock > 0
                ORDER BY nombre_producto
            """)
            productos = cursor.fetchall()
        except Exception as e:
            print("Error al listar productos con stock:", e)
        finally:
            cursor.close()
            conn.close()
    return productos

def obtener_producto_por_id(id_producto):
    conn = get_connection()
    producto = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_producto, nombre_producto, precio, stock FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()
    return producto

def obtener_detalles_venta(id_venta):
    conn = get_connection()
    detalles = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT dv.id_producto, p.nombre_producto, dv.cantidad, dv.precio_unitario
            FROM detalle_ventas dv
            JOIN productos p ON dv.id_producto = p.id_producto
            WHERE dv.id_venta = %s
        """
        cursor.execute(sql, (id_venta,))
        detalles = cursor.fetchall()
        cursor.close()
        conn.close()
    return detalles
