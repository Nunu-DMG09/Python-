import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import numpy as np
from sklearn.preprocessing import StandardScaler


def load_data(productos_file, ventas_file):
    # Cargar productos y eliminar duplicados
    productos = pd.read_csv(productos_file).drop_duplicates(subset=['id_producto'], keep='first')

    # Cargar ventas, asegurando que los nombres de columnas sean correctos
    ventas = pd.read_csv(ventas_file, skipinitialspace=True)  # Elimina espacios ocultos en los nombres de las columnas

    # Verificar si 'precio_unitario' existe
    if 'precio_unitario' not in ventas.columns:
        print("⚠️ ERROR: La columna 'precio_unitario' no se encuentra en ventas.csv")
        print("Columnas encontradas en ventas.csv:", ventas.columns)
        return productos, ventas  # Devuelve los datos para depuración

    # Convertir precio_unitario a número
    ventas['precio_unitario'] = pd.to_numeric(ventas['precio_unitario'], errors='coerce')

    # Convertir cantidad a número
    ventas['cantidad'] = pd.to_numeric(ventas['cantidad'], errors='coerce')

    # Calcular el total
    ventas['total'] = ventas['cantidad'] * ventas['precio_unitario']

    # Reemplazar valores NaN con 0
    ventas = ventas.fillna(0)

    return productos, ventas

def recomendar_productos(ventas, productos, n=10):
    # Calcular el total de ventas por producto
    ventas_por_producto = ventas.groupby('id_producto')['total'].sum().reset_index()
    ventas_por_producto.columns = ['id_producto', 'total_ventas']

    # Unir con productos
    productos = productos.merge(ventas_por_producto, on='id_producto', how='left').fillna(0)

    # Ordenar por total_ventas y puntuación
    productos = productos.sort_values(by=['total_ventas', 'puntuacion'], ascending=[False, False])

    return productos[['id_producto', 'nombre', 'total_ventas', 'puntuacion']].head(n)


def segmentar_productos_con_kmeans(productos):

    ventas_agrupadas = ventas.groupby('id_producto')['cantidad'].sum().reset_index()
    ventas_agrupadas.rename(columns={'cantidad': 'total_ventas'}, inplace=True)

    # Unir la información de ventas con los productos
    productos = productos.merge(ventas_agrupadas, on='id_producto', how='left')

    # Si un producto no tiene ventas, asignamos 0
    productos['total_ventas'].fillna(0, inplace=True)

    # Aplicar transformación logarítmica para evitar valores extremos
    productos['total_ventas'] = np.log1p(productos['total_ventas'])  # log(1 + x) para evitar log(0)

    # Normalizar los datos
    scaler = MinMaxScaler()
    productos[['precio']] = scaler.fit_transform(productos[['precio']])


    # Aplicar K-Means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    productos['cluster'] = kmeans.fit_predict(productos[['precio', 'total_ventas']])

    # Nombres de los clusters
    cluster_names = {
        0: "Bajo precio, bajas ventas",
        1: "Precio medio, ventas moderadas",
        2: "Productos caros y populares"
    }

    productos['cluster_name'] = productos['cluster'].map(cluster_names)

    # Graficar resultados
    colores = ['green', 'blue', 'red']
    for cluster in range(kmeans.n_clusters):
        cluster_data = productos[productos['cluster'] == cluster]
        plt.scatter(cluster_data['precio'], cluster_data['total_ventas'], 
                    color=colores[cluster], label=f'{cluster_names[cluster]}')

    # Configuración del gráfico
    plt.xlabel('Precio')
    plt.ylabel('Cantidad Vendida')
    plt.title('Segmentación de Productos con K-Means')
    plt.legend()
    plt.show()


def segmentar_categorias_con_kmeans(productos, ventas):
    # Unir productos con ventas para obtener la categoría de cada venta
    ventas = ventas.merge(productos[['id_producto', 'categoria']], on='id_producto', how='left')

    # Agrupar por categoría y calcular el total de ventas por categoría
    ventas_por_categoria = ventas.groupby('categoria')['total'].sum().reset_index()

    # Normalizar los datos
    scaler = MinMaxScaler()
    ventas_por_categoria[['total']] = scaler.fit_transform(ventas_por_categoria[['total']])

    # Aplicar K-Means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    ventas_por_categoria['cluster'] = kmeans.fit_predict(ventas_por_categoria[['total']])

    # Nombres de los clusters
    cluster_names = {
        0: "Categorías con bajas ventas",
        1: "Categorías más populares",
        2: "Categorías con ventas moderadas"
    }

    # Graficar los clusters
    colores = ['green', 'blue', 'red']
    for cluster in range(kmeans.n_clusters):
        cluster_data = ventas_por_categoria[ventas_por_categoria['cluster'] == cluster]
        plt.scatter(cluster_data['categoria'], cluster_data['total'], 
                    color=colores[cluster], label=f'{cluster_names[cluster]}', s=200)

    # Configuración del gráfico
    plt.xlabel('Categorías')
    plt.ylabel('Total de Ventas')
    plt.title('Segmentación de Categorías por Popularidad con K-Means')
    plt.xticks(rotation=45, ha='right')  
    plt.legend()
    plt.show()


if __name__ == "__main__":
    productos, ventas = load_data('productos.csv', 'ventas.csv')
    print("Productos recomendados:")
    print(recomendar_productos(ventas, productos))
    segmentar_productos_con_kmeans(productos)
    segmentar_categorias_con_kmeans(productos, ventas)
