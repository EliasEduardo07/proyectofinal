import streamlit as st
import googlemaps
import folium
from streamlit_folium import folium_static

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


