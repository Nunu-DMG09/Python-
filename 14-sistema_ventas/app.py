from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.usuario import login, registrar_usuario
from models.cliente import listar_clientes, registrar_cliente, eliminar_cliente, obtener_cliente, actualizar_cliente
from models.producto import listar_productos, agregar_producto, eliminar_producto, obtener_producto, actualizar_producto
from models.venta import registrar_venta, listar_ventas, obtener_detalle_venta
from utils.db import get_connection

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
    
    if request.method == "POST":
        id_cliente = request.form["id_cliente"]
        # 💥 AÑADE ESTA LÍNEA:
        productos = [(1, 2, 10.0)]  # Producto 1, 2 unidades, S/.10 cada una
        registrar_venta(id_cliente, productos)  # o la lógica que uses
        flash("Venta registrada exitosamente", "success")
        return redirect(url_for("ventas"))

    ventas = listar_ventas()
    clientes = listar_clientes()  # ⚠️ Esto es CLAVE

    return render_template("ventas.html", ventas=ventas, clientes=clientes)

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

@app.route("/venta/detalle/<int:id>")
def detalle_venta(id):
    if "usuario" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login_usuario"))
    detalles = obtener_detalle_venta(id)
    return render_template("detalle_venta.html", detalles=detalles)



# INICIAR LA APP
if __name__ == "__main__":
    app.run(debug=True)


