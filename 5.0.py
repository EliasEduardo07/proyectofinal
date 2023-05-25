# Esta version incluye hasta metricas de distanciabien! en la 5.1 probare con otro tipo de distancia de manhattan
import streamlit as st
import csv
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import googlemaps
import folium
from streamlit_folium import folium_static
# Definir la función para obtener los datos del usuario
def obtener_datos_usuario():
    st.header("Ingrese sus datos")

    nombre = st.text_input("Nombre", max_chars=40)
    apellido = st.text_input("Apellido Paterno", max_chars=15)
    edad = st.text_input("Edad")
    altura = st.text_input("Altura (cm)")
    peso = st.text_input("Peso (kg)")

    return nombre, apellido, edad, altura, peso

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
    # Aquí deberías implementar y mostrar los resultados de las métricas de distancia

    clave_api = 'AIzaSyCRoRdEBeMZUfx_kSjmB-Dgezk2jYWh7bQ'

cliente_maps = googlemaps.Client(key=clave_api)

def obtener_ubicacion_actual():
    ubicacion = cliente_maps.geolocate()
    return ubicacion['location']['lat'], ubicacion['location']['lng']

@st.cache_data  # Almacena en caché los resultados de la función
def buscar_tiendas(latitud, longitud, radio):
    resultados = cliente_maps.places_nearby(
        location=(latitud, longitud),
        radius=radio,
        type='department_store'
    )
    return resultados['results']

def calcular_distancia_manhattan(coordenadas1, coordenadas2):
    lat1, lon1 = coordenadas1
    lat2, lon2 = coordenadas2
    return abs(lat1 - lat2) + abs(lon1 - lon2)

def calcular_distancia_euclidiana(coordenadas1, coordenadas2):
    return cliente_maps.distance_matrix(coordenadas1, coordenadas2)['rows'][0]['elements'][0]['distance']['text']

def app():
    st.title("Tiendas departamentales cercanas")

    # Obtener la ubicación actual
    latitud_actual, longitud_actual = obtener_ubicacion_actual()
    st.write("Tu ubicación actual: {}, {}".format(latitud_actual, longitud_actual))

    # Solicitar el radio de búsqueda al usuario en metros
    radio_busqueda = st.number_input("Ingrese el radio de búsqueda en metros:", min_value=100)

    # Buscar tiendas departamentales cercanas
    tiendas_departamentales_cercanas = buscar_tiendas(latitud_actual, longitud_actual, radio_busqueda)

    # Crear una lista de tiendas y sus distancias
    tiendas_y_distancias = []

    # Calcular las distancias y almacenar los nombres de las tiendas
    for tienda in tiendas_departamentales_cercanas:
        nombre = tienda['name']
        direccion = tienda['vicinity']
        coordenadas_tienda = tienda['geometry']['location']
        latitud_tienda = coordenadas_tienda['lat']
        longitud_tienda = coordenadas_tienda['lng']

        distancia_manhattan = calcular_distancia_manhattan((latitud_actual, longitud_actual), (latitud_tienda, longitud_tienda))
        distancia_euclidiana = calcular_distancia_euclidiana((latitud_actual, longitud_actual), (latitud_tienda, longitud_tienda))

        tiendas_y_distancias.append((nombre, distancia_manhattan, distancia_euclidiana, latitud_tienda, longitud_tienda))

    # Ordenar las tiendas por distancia euclidiana en orden ascendente
    tiendas_y_distancias.sort(key=lambda x: x[2])

    # Mostrar las distancias en la página principal
    st.subheader("Distancias de tiendas departamentales:")
    opciones_tiendas = [nombre for nombre, _, _, _, _ in tiendas_y_distancias]
    tienda_seleccionada = st.selectbox("Seleccione una tienda:", opciones_tiendas)

    # Encontrar los datos de la tienda seleccionada
    for nombre, distancia_manhattan, distancia_euclidiana, latitud_tienda, longitud_tienda in tiendas_y_distancias:
        if nombre == tienda_seleccionada:
            st.write("Nombre: ", nombre)
            st.write("Dirección: ", direccion)
            st.write("Distancia Manhattan: ", distancia_manhattan)
            st.write("Distancia Euclidiana: ", distancia_euclidiana)
            break

    # Mostrar el mapa en la página principal
    mapa = folium.Map(location=[latitud_actual, longitud_actual], zoom_start=13)
    mapa.add_child(folium.Marker([latitud_actual, longitud_actual], popup='Ubicación actual', icon=folium.Icon(color='blue')))
    for _, _, _, latitud_tienda, longitud_tienda in tiendas_y_distancias:
        mapa.add_child(folium.Marker([latitud_tienda, longitud_tienda], popup='Tienda', icon=folium.Icon(color='red')))
    folium_static(mapa)

if __name__ == "__main__":
    app()
