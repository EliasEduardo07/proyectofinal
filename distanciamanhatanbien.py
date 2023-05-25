import csv
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import googlemaps
import folium
from streamlit_folium import folium_static
import polyline
import streamlit as st


# Definir la función para obtener los datos del usuario, creo que este etsa bien con manhattan
def obtener_datos_usuario():
    st.header("Ingrese sus datos")

    nombre = st.text_input("Nombre", max_chars=40)
    apellido = st.text_input("Apellido Paterno", max_chars=15)
    edad = st.text_input("Edad")
    altura = st.text_input("Altura (cm)")
    peso = st.text_input("Peso (kg)")

    return nombre, apellido, edad, altura, peso


# Definir la función para obtener la ubicación actual
def obtener_ubicacion_actual():
    # Esta función debería implementar la obtención de la ubicación actual del usuario
    # utilizando servicios como Google Maps API. Por simplicidad, vamos a retornar valores
    # de ubicación fijos en este ejemplo.
    return 37.7749, -122.4194  # Latitud y longitud de San Francisco


# Definir la función para buscar supermercados cercanos
def buscar_supermercados(latitud, longitud, radio):
    # Esta función debería utilizar servicios como Google Maps Places API para buscar
    # supermercados cercanos a la ubicación proporcionada. Por simplicidad, vamos a
    # retornar una lista fija de supermercados en este ejemplo.
    supermercados = [
        {"name": "Supermercado A", "vicinity": "Dirección A", "geometry": {"location": {"lat": 37.7749, "lng": -122.4194}}},
        {"name": "Supermercado B", "vicinity": "Dirección B", "geometry": {"location": {"lat": 37.7831, "lng": -122.4039}}},
        {"name": "Supermercado C", "vicinity": "Dirección C", "geometry": {"location": {"lat": 37.7917, "lng": -122.4105}}},
    ]
    return supermercados


# Definir la función para calcular la distancia Manhattan
def calcular_distancia_manhattan(coordenadas1, coordenadas2):
    latitud1, longitud1 = coordenadas1
    latitud2, longitud2 = coordenadas2
    return abs(latitud1 - latitud2) + abs(longitud1 - longitud2)


# Definir la función para calcular la distancia euclidiana
def calcular_distancia_euclidiana(coordenadas1, coordenadas2):
    latitud1, longitud1 = coordenadas1
    latitud2, longitud2 = coordenadas2
    return ((latitud1 - latitud2) ** 2 + (longitud1 - longitud2) ** 2) ** 0.5


# Definir la función para calcular la ruta entre dos ubicaciones
def calcular_ruta(latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    # Esta función debería utilizar servicios como Google Maps Directions API para calcular
    # la ruta entre dos ubicaciones. Por simplicidad, vamos a retornar una ruta fija en este
    # ejemplo utilizando la codificación polyline.
    puntos_ruta = [
        (latitud_origen, longitud_origen),
        (37.7845, -122.4308),
        (37.7829, -122.4216),
        (latitud_destino, longitud_destino),
    ]
    ruta_codificada = polyline.encode(puntos_ruta)
    return ruta_codificada


# Configuración de página
st.set_page_config(page_title="NutriAI", page_icon="🥦", layout="centered")

# Título de la aplicación
st.title("NutriAI - Análisis de Nutrición y Dietas")

# Barra lateral para seleccionar la página
page = st.sidebar.selectbox(
    "Elige una página",
    ["Inicio", "Algoritmo Apriori", "Métricas de Distancia", "Clustering Jerárquico Ascendente"]
)

# Página de inicio
if page == "Inicio":
    import datetime
    today = datetime.date.today()
    st.write(f"Bienvenido a NutriAI. Hoy es {today}")

    # Obtener los datos del usuario y guardarlos en un archivo CSV
    nombre, apellido, edad, altura, peso = obtener_datos_usuario()

    if nombre and apellido and edad and altura and peso:
        if not nombre.replace(" ", "").isalpha() or not apellido.replace(" ", "").isalpha():
            st.error("Ingrese un valor válido para el nombre y el apellido (solo letras y espacios).")
        elif not edad.isdigit() or not altura.isdigit() or not peso.isdigit():
            st.error("Ingrese un valor válido para la edad, altura y peso (solo números).")
        else:
            registro_usuario = [nombre, apellido, edad, altura, peso]

            # Calcular el IMC
            altura_metros = float(altura) / 100  # Convertir la altura de cm a metros
            imc = float(peso) / (altura_metros ** 2)
            registro_usuario.append(imc)  # Agregar el IMC al registro del usuario

            if st.button("Guardar"):
                archivo = "ingredientes.csv"

                with open(archivo, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(registro_usuario)

                st.success("Los datos se han guardado correctamente en el archivo CSV.")

            # Calcular el IMC ideal
            imc_ideal = 22.5  # Puedes ajustar el valor del IMC ideal según tus criterios

            # Mostrar el IMC y el IMC ideal
            st.write(f"**Tu IMC:** {imc:.2f}")
            st.write(f"**IMC Ideal:** {imc_ideal}")

            # Comparar el IMC con el IMC ideal
            if imc < imc_ideal - 2:
                st.write("Tu IMC indica que estás por debajo del peso ideal.")
            elif imc > imc_ideal + 2:
                st.write("Tu IMC indica que estás por encima del peso ideal.")
            else:
                st.write("Tu IMC indica que tienes un peso saludable.")

            # Visualización gráfica del IMC
            labels = ["Tu IMC", "IMC Ideal"]
            imc_data = [imc, imc_ideal]
            colors = ["blue", "green"]

            fig, ax = plt.subplots()
            ax.bar(labels, imc_data, color=colors)
            ax.set_ylabel("IMC")
            ax.set_title("Comparación del IMC con el IMC Ideal")
            st.pyplot(fig)

    else:
        st.info("Por favor, complete todos los campos antes de guardar.")

# Página del algoritmo Apriori
elif page == "Algoritmo Apriori":
    st.header("Algoritmo Apriori")

    # Obtener los parámetros del usuario
    min_support = st.number_input("Soporte mínimo", min_value=0.0, max_value=1.0, value=0.3)
    min_confidence = st.number_input("Confianza mínima", min_value=0.0, max_value=1.0, value=0.7)
    min_lift = st.number_input("Elevación mínima", min_value=0.0, value=1.2)

    if st.button("Generar reglas de asociación"):
        # Leer el archivo CSV
        transactions = []
        try:
            with open("ingredientes.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    # Eliminar elementos con espacios en blanco
                    transaction = [item for item in row if item.strip() != '']
                    transactions.append(transaction)

            # Aplicar el algoritmo Apriori
            rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift)

            # Mostrar las reglas de asociación
            st.subheader("Reglas de asociación")
            for rule in rules:
                st.write(f"{list(rule.items)} => {list(rule.ordered_statistics[0].items_add)}")
                st.write(f"Support: {rule.support}, Confidence: {rule.ordered_statistics[0].confidence}, Lift: {rule.ordered_statistics[0].lift}")
                st.write("---")

            # Obtener la frecuencia de los elementos
            item_counts = {}
            for transaction in transactions:
                for item in transaction:
                    if item in item_counts:
                        item_counts[item] += 1
                    else:
                        item_counts[item] = 1

            # Descartar elementos con frecuencia igual o menor a 1
            item_counts = {item: count for item, count in item_counts.items() if count > 1}

            # Mostrar el gráfico de barras
            items = list(item_counts.keys())
            counts = list(item_counts.values())

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(items, counts)
            ax.set_xlabel('Elemento')
            ax.set_ylabel('Cantidad')
            ax.set_title('Cantidad de cada elemento en el archivo')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        except FileNotFoundError:
            st.error("El archivo 'store_data.csv' no se encontró en el directorio actual.")
elif page == "Métricas de Distancia":
    st.header("Métricas de Distancia")

    API_KEY = "YOUR_API_KEY"
    gmaps = googlemaps.Client(key=API_KEY)

    def app():
        st.title("Metricas de distancia")

        # Obtener la ubicación actual
        latitud_actual, longitud_actual = obtener_ubicacion_actual()
        st.write("Tu ubicación actual: {}, {}".format(latitud_actual, longitud_actual))

        # Solicitar el radio de búsqueda al usuario en metros
        radio_busqueda = st.number_input("Ingrese el radio de búsqueda en metros:", min_value=100)

        # Buscar supermercados cercanos
        supermercados_cercanos = buscar_supermercados(latitud_actual, longitud_actual, radio_busqueda)

        # Crear una lista de supermercados y sus distancias
        supermercados_y_distancias = []

        # Calcular las distancias y almacenar los nombres de los supermercados
        for supermercado in supermercados_cercanos:
            nombre = supermercado['name']
            direccion = supermercado['vicinity']
            coordenadas_supermercado = supermercado['geometry']['location']
            latitud_supermercado = coordenadas_supermercado['lat']
            longitud_supermercado = coordenadas_supermercado['lng']

            distancia_manhattan = calcular_distancia_manhattan((latitud_actual, longitud_actual), (latitud_supermercado, longitud_supermercado))
            distancia_euclidiana = calcular_distancia_euclidiana((latitud_actual, longitud_actual), (latitud_supermercado, longitud_supermercado))

            supermercados_y_distancias.append((nombre, distancia_manhattan, distancia_euclidiana, latitud_supermercado, longitud_supermercado))

        # Ordenar los supermercados por distancia euclidiana en orden ascendente
        supermercados_y_distancias.sort(key=lambda x: x[2])

        # Mostrar las distancias en la página principal
        st.subheader("Distancias de supermercados cercanos:")
        opciones_supermercados = [nombre for nombre, _, _, _, _ in supermercados_y_distancias]
        supermercado_seleccionado = st.selectbox("Seleccione un supermercado:", opciones_supermercados)

        # Encontrar los datos del supermercado seleccionado
        for nombre, distancia_manhattan, distancia_euclidiana, latitud_supermercado, longitud_supermercado in supermercados_y_distancias:
            if nombre == supermercado_seleccionado:
                st.write("Nombre: ", nombre)
                st.write("Dirección: ", direccion)
                st.write("Distancia Manhattan: ", distancia_manhattan)
                st.write("Distancia Euclidiana: ", distancia_euclidiana)
                break

        # Mostrar el mapa en la página principal
        mapa = folium.Map(location=[latitud_actual, longitud_actual], zoom_start=13)
        mapa.add_child(folium.Marker([latitud_actual, longitud_actual], popup='Ubicación actual', icon=folium.Icon(color='blue')))
        for _, _, _, latitud_supermercado, longitud_supermercado in supermercados_y_distancias:
            mapa.add_child(folium.Marker([latitud_supermercado, longitud_supermercado], popup='Supermercado', icon=folium.Icon(color='red')))
        folium_static(mapa)
        
        # Calcular y mostrar la ruta en el mapa
        if st.button("Calcular ruta"):
            for nombre, _, _, latitud_supermercado, longitud_supermercado in supermercados_y_distancias:
                if nombre == supermercado_seleccionado:
                    ruta = calcular_ruta(latitud_actual, longitud_actual, latitud_supermercado, longitud_supermercado)
                    break
            if ruta:
                puntos_ruta = polyline.decode(ruta)

                ruta_mapa = folium.Map(location=[latitud_actual, longitud_actual], zoom_start=13)
                ruta_mapa.add_child(folium.Marker([latitud_actual, longitud_actual], popup='Ubicación actual', icon=folium.Icon(color='blue')))
                ruta_mapa.add_child(folium.Marker([latitud_supermercado, longitud_supermercado], popup='Supermercado', icon=folium.Icon(color='red')))
                ruta_mapa.add_child(folium.PolyLine(puntos_ruta, color='green'))
                folium_static(ruta_mapa)
            else:
                st.write("No se pudo calcular la ruta.")
    
    if __name__ == "__main__":
        app()
