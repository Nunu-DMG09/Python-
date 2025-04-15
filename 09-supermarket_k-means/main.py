
# Programador: David Mesta 

import customtkinter as ctk
from BOT.handlers import MessageHandler
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

class LoginWindow(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.title("Login")
        self.geometry("400x300")
        self.configure(fg_color="#2C2F33")

        self.label_email = ctk.CTkLabel(self, text="Correo:", text_color="#FFFFFF", font=("Helvetica", 14))
        self.label_email.pack(pady=10)
        self.entry_email = ctk.CTkEntry(self, width=300, fg_color="#23272A", text_color="#FFFFFF", font=("Helvetica", 14))
        self.entry_email.pack(pady=10)

        self.label_password = ctk.CTkLabel(self, text="Contraseña:", text_color="#FFFFFF", font=("Helvetica", 14))
        self.label_password.pack(pady=10)
        self.entry_password = ctk.CTkEntry(self, width=300, show="*", fg_color="#23272A", text_color="#FFFFFF", font=("Helvetica", 14))
        self.entry_password.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Iniciar Sesión", command=self.login, fg_color="#7289DA", text_color="white", font=("Helvetica", 14))
        self.login_button.pack(pady=20)

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        handler = MessageHandler()
        response = handler.login(f"{email},{password}")

        if handler.user_logged_in:
            self.withdraw()  # Oculta la ventana de login
            menu_window = MenuWindow(handler)
            menu_window.mainloop()
        else:
            ctk.CTkLabel(self, text=response, text_color="#FF0000", font=("Helvetica", 12)).pack(pady=5)

class MenuWindow(ctk.CTk):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.title("Menú Principal")
        self.geometry("400x300")
        self.configure(fg_color="#2C2F33")

        self.label = ctk.CTkLabel(self, text="Seleccione una opción", text_color="white", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.chatbot_button = ctk.CTkButton(self, text="Iniciar ChatBot", command=self.open_chatbot, fg_color="#7289DA", text_color="white", font=("Helvetica", 14))
        self.chatbot_button.pack(pady=10)

        self.graph_button = ctk.CTkButton(self, text="Ver Gráfico de Productos", command=self.show_graph, fg_color="#7289DA", text_color="white", font=("Helvetica", 14))
        self.graph_button.pack(pady=10)

    def open_chatbot(self):
        self.withdraw()
        app = ChatBotApp(self.handler)
        app.mainloop()

    def show_graph(self):
        self.withdraw()
        kmeans_por_usuario()
        grafico_productos_mas_vendidos()
        grafico_ventas_por_categoria()

class ChatBotApp(ctk.CTk):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.title("ChatBot")
        self.geometry("600x500")
        self.configure(fg_color="#2C2F33")

        self.chat_frame = ctk.CTkFrame(self, fg_color="#2C2F33")
        self.chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.chat_log = ctk.CTkTextbox(self.chat_frame, state='disabled', width=50, height=20, fg_color="#23272A", text_color="#FFFFFF", font=("Helvetica", 14), wrap="word")
        self.chat_log.pack(padx=10, pady=10, fill="both", expand=True)

        self.entry_box = ctk.CTkEntry(self, width=400, fg_color="#23272A", text_color="#FFFFFF", font=("Helvetica", 14))
        self.entry_box.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.entry_box.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self, text="Enviar", command=self.send_message, fg_color="#7289DA", text_color="white", font=("Helvetica", 14))
        self.send_button.pack(side="right", padx=10, pady=10)

        # Botón para volver al menú
        self.back_button = ctk.CTkButton(self, text="Volver al Menú", command=self.return_to_menu, fg_color="#FF4500", text_color="white", font=("Helvetica", 14))
        self.back_button.pack(pady=15)

    def send_message(self, event=None):
        user_input = self.entry_box.get()
        if user_input.lower() in ["salir", "adiós"]:
            self.quit()
            return

        self.chat_log.configure(state='normal')
        self.chat_log.insert("end", "Tú: " + user_input + "\n", "user")
        self.entry_box.delete(0, "end")

        response = self.handler.handle_message(user_input)
        self.chat_log.insert("end", "Bot: " + response + "\n", "bot")
        self.chat_log.configure(state='disabled')
        self.chat_log.yview("end")

    def return_to_menu(self):
        self.destroy()
        self.menu_window.deiconify()  # Mostrar de nuevo el menú principal


def kmeans_por_usuario():
    # Cargar datos
    ventas = pd.read_csv("DATA/ventas.csv")  
    productos = pd.read_csv("DATA/productos.csv")  

    # Renombrar para hacer coincidir columnas
    productos = productos.rename(columns={"id": "id_producto"})

    # Contar cuántas veces cada usuario ha comprado cada producto
    compras_usuario = ventas.groupby(["id_user", "id_producto"]).size().reset_index(name="cantidad_comprada")

    # Unir con información de productos
    compras_usuario = compras_usuario.merge(productos, on="id_producto", how="left")

    # Normalizar datos (Precio y Cantidad Comprada)
    escalador = MinMaxScaler()
    compras_usuario[["precio", "cantidad_comprada"]] = escalador.fit_transform(compras_usuario[["precio", "cantidad_comprada"]])

    # Aplicar K-Means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    compras_usuario["cluster"] = kmeans.fit_predict(compras_usuario[["precio", "cantidad_comprada"]])

    # Definir nombres de los clusters
    cluster_nombres = {
        0: "productos premium",
        1: "productos populares y accesibles",
        2: "productos de nicho"
    }

    # Graficar resultados
    plt.figure(figsize=(8,6))
    colores = ["red", "blue", "green"]

    for cluster in range(kmeans.n_clusters):
        plt.scatter(compras_usuario[compras_usuario["cluster"] == cluster]["precio"],
                    compras_usuario[compras_usuario["cluster"] == cluster]["cantidad_comprada"],
                    s=180, color=colores[cluster], alpha=0.6, label=cluster_nombres[cluster])
        
        plt.scatter(kmeans.cluster_centers_[cluster][0], kmeans.cluster_centers_[cluster][1],
                    marker="P", s=280, color=colores[cluster], edgecolors="black")

    plt.title("Segmentación productos Comprados", fontsize=14)
    plt.xlabel("Precio del Producto", fontsize=12)
    plt.ylabel("Cantidad Comprada", fontsize=12)
    plt.legend()
    plt.show()




def grafico_productos_mas_vendidos():
    ventas = pd.read_csv("DATA/ventas.csv")  
    productos = pd.read_csv("DATA/productos.csv")  

    productos = productos.rename(columns={"id": "id_producto"})

    ventas_por_producto = ventas["id_producto"].value_counts().reset_index()
    ventas_por_producto.columns = ["id_producto", "cantidad_vendida"]

    productos_info = productos.merge(ventas_por_producto, on="id_producto", how="left").fillna(0)

    # Ordenar de mayor a menor cantidad vendida
    productos_info = productos_info.sort_values(by="cantidad_vendida", ascending=False)

    plt.figure(figsize=(12, 6))
    plt.bar(productos_info["id_producto"].astype(str), productos_info["cantidad_vendida"], color="skyblue")
    
    plt.xlabel("ID del Producto", fontsize=12)
    plt.ylabel("Cantidad Vendida", fontsize=12)
    plt.title("Top Productos Más Vendidos", fontsize=15)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.show()


def grafico_ventas_por_categoria():
    ventas = pd.read_csv("DATA/ventas.csv")  
    productos = pd.read_csv("DATA/productos.csv")  

    productos = productos.rename(columns={"id": "id_producto"})

    ventas_por_producto = ventas["id_producto"].value_counts().reset_index()
    ventas_por_producto.columns = ["id_producto", "cantidad_vendida"]

    productos_info = productos.merge(ventas_por_producto, on="id_producto", how="left").fillna(0)

    # Agrupar por categoría
    ventas_por_categoria = productos_info.groupby("categoria")["cantidad_vendida"].sum()

    plt.figure(figsize=(8, 8))
    plt.pie(ventas_por_categoria, labels=ventas_por_categoria.index, autopct="%1.1f%%", colors=["red", "blue", "green", "orange", "purple", "brown", "yellow"])
    
    plt.title("Distribución de Ventas por Categoría", fontsize=15)
    plt.show()

if __name__ == "__main__":
    login_window = LoginWindow(lambda handler: MenuWindow(handler))  # Se pasa correctamente el handler
    login_window.mainloop()