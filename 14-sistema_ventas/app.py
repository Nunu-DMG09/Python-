from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.usuario import login, registrar_usuario
from models.cliente import listar_clientes, registrar_cliente, eliminar_cliente, obtener_cliente, actualizar_cliente
from models.producto import listar_productos, agregar_producto, eliminar_producto, obtener_producto, actualizar_producto
from models.venta import registrar_venta, listar_ventas, obtener_detalle_venta, obtener_venta_por_id, listar_productos_con_stock, obtener_producto_por_id, obtener_venta, obtener_detalles_venta
from utils.db import get_connection
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import make_response

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# RUTAS DE USUARIO
@app.route("/")
def index():
    return redirect(url_for("login_usuario"))

@app.route("/login", methods=["GET", "POST"])
def login_usuario():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]

        if login(usuario, clave):
            session["usuario"] = usuario
            flash("Bienvenido al sistema POS 💼", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciales incorrectas ❌", "danger")
    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        registrar_usuario(usuario, clave)
        flash("Usuario registrado correctamente ✅", "success")
        return redirect(url_for("login_usuario"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada 📴", "info")
    return redirect(url_for("login_usuario"))

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    return render_template("dashboard.html", usuario=session["usuario"])

# CRUD CLIENTES
@app.route("/clientes",  methods=["GET", "POST"])
def clientes():
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    clientes = listar_clientes()
    return render_template("clientes.html", clientes=clientes)

@app.route("/clientes/agregar", methods=["GET", "POST"])
def agregar_cliente():
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    if request.method == "POST":
        nombre = request.form["nombre"]
        dni = request.form["dni"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        registrar_cliente(nombre, dni, direccion, telefono)
        flash("Cliente agregado ✅", "success")
        return redirect(url_for("clientes"))
    return render_template("agregar_cliente.html")

@app.route("/clientes/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar_cliente(id_cliente):
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    cliente = obtener_cliente(id_cliente)
    if request.method == "POST":
        nombre = request.form["nombre"]
        dni = request.form["dni"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        actualizar_cliente(id_cliente, nombre, dni, direccion, telefono)
        flash("Cliente actualizado ✅", "success")
        return redirect(url_for("clientes"))
    return render_template("editar_cliente.html", cliente=cliente)

@app.route("/clientes/eliminar/<int:id_cliente>")
def eliminar_cliente_route(id_cliente):
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    eliminar_cliente(id_cliente)
    flash("Cliente eliminado ✅", "success")
    return redirect(url_for("clientes"))

# CRUD PRODUCTOS
@app.route("/productos",  methods=["GET", "POST"])
def productos():
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    productos = listar_productos()
    return render_template("productos.html", productos=productos)

@app.route("/productos/agregar", methods=["GET", "POST"])
def agregar_producto_route():
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        agregar_producto(nombre, precio, stock)
        flash("Producto agregado ✅", "success")
        return redirect(url_for("productos"))
    return render_template("agregar_producto.html")

@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
def editar_producto(id_producto):
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    producto = obtener_producto(id_producto)
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        actualizar_producto(id_producto, nombre, precio, stock)
        flash("Producto actualizado ✅", "success")
        return redirect(url_for("productos"))
    return render_template("editar_producto.html", producto=producto)

@app.route("/productos/eliminar/<int:id_producto>")
def eliminar_producto_route(id_producto):
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    eliminar_producto(id_producto)
    flash("Producto eliminado ✅", "success")
    return redirect(url_for("productos"))

# VENTAS
@app.route("/ventas", methods=["GET", "POST"])
def ventas():
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))

    productos = listar_productos()
    clientes = listar_clientes()
    ventas = listar_ventas()

    if request.method == "POST":
        id_cliente = request.form["id_cliente"]
        productos_seleccionados = []

        for p in productos:
            cantidad_str = request.form.get(f"producto_{p['id_producto']}", "")
            if cantidad_str.isdigit() and int(cantidad_str) > 0:
                cantidad = int(cantidad_str)
                subtotal = cantidad * float(p['precio'])  # Asegúrate que p['precio'] sea float
                productos_seleccionados.append((p['id_producto'], cantidad, subtotal))

        if not productos_seleccionados:
            flash("Selecciona al menos un producto válido", "warning")
            return redirect(url_for("ventas"))

        registrar_venta(id_cliente, productos_seleccionados)
        flash("Venta registrada exitosamente ✅", "success")
        return redirect(url_for("ventas"))

    return render_template("ventas.html", ventas=ventas, clientes=clientes, productos=productos)



@app.route("/venta/eliminar/<int:id>")
def eliminar_venta(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Primero elimina los detalles asociados a la venta
            cursor.execute("DELETE FROM detalle_ventas WHERE id_venta = %s", (id,))
            # Luego elimina la venta
            cursor.execute("DELETE FROM ventas WHERE id_venta = %s", (id,))
            conn.commit()
            flash("Venta eliminada correctamente", "success")
        except Exception as e:
            conn.rollback()
            print("Error eliminando venta:", e)
            flash("Error al eliminar la venta", "danger")
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for("ventas"))

@app.route('/detalle_venta/<int:id>', methods=['GET', 'POST'])
def detalle_venta(id):
    if request.method == 'POST':
        id_producto = request.form.get('id_producto')
        cantidad = int(request.form.get('cantidad'))

        producto = obtener_producto_por_id(id_producto)

        if not producto:
            flash("Producto no encontrado", "danger")
            return redirect(url_for('detalle_venta', id=id))

        if cantidad > producto['stock']:
            flash("No hay suficiente stock disponible", "danger")
            return redirect(url_for('detalle_venta', id=id))

        # Insertar detalle en la tabla detalle_venta (ajústalo a tu modelo real)
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id, id_producto, cantidad, producto['precio']))
            
            # Actualizar el stock del producto
            cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (cantidad, id_producto))
            
            # 🔥 ACTUALIZAR TOTAL DE LA VENTA
            cursor.execute("""
                SELECT SUM(cantidad * precio_unitario)
                FROM detalle_ventas
                WHERE id_venta = %s
            """, (id,))
            nuevo_total = cursor.fetchone()[0] or 0

            cursor.execute("UPDATE ventas SET total = %s WHERE id_venta = %s", (nuevo_total, id))

            conn.commit()
            cursor.close()
            conn.close()

        flash("Producto agregado correctamente", "success")
        return redirect(url_for('detalle_venta', id=id))

    # Modo GET: Mostrar la venta con su detalle
    venta = obtener_venta(id)
    productos = listar_productos_con_stock()
    detalles = obtener_detalles_venta(id)
    total = sum([d['cantidad'] * d['precio_unitario'] for d in detalles])

    return render_template('detalle_venta.html', venta=venta, productos=productos, detalles=detalles, total=total)


@app.route('/detalle_venta/<int:id>/pdf')
def generar_pdf_venta(id):
    venta = obtener_venta(id)
    detalles = obtener_detalles_venta(id)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Detalle de Venta N° {venta['id_venta']}")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Cliente: {venta['nombre_cliente']}")
    y -= 20
    c.drawString(50, y, f"Total: S/. {venta['total']:.2f}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Producto")
    c.drawString(250, y, "Cantidad")
    c.drawString(350, y, "Precio Unitario")
    c.drawString(480, y, "Subtotal")
    y -= 20

    c.setFont("Helvetica", 12)
    for detalle in detalles:
        if y < 60:
            c.showPage()
            y = height - 50
        c.drawString(50, y, detalle['nombre_producto'])
        c.drawString(250, y, str(detalle['cantidad']))
        c.drawString(350, y, f"S/. {detalle['precio_unitario']:.2f}")
        subtotal = detalle['cantidad'] * detalle['precio_unitario']
        c.drawString(480, y, f"S/. {subtotal:.2f}")
        y -= 20

    c.showPage()
    c.save()
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=venta_{id}.pdf'
    return response




# INICIAR LA APP
if __name__ == "__main__":
    app.run(debug=True)


