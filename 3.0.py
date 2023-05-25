 # este ya esta funcionando, falta quitarle la impresion de las conexiones del grafico en apriori, pero esta bien 
import streamlit as st
import googlemaps
import matplotlib.pyplot as plt
from gmplot import gmplot

def obtener_ubicacion_actual():
    ubicacion = cliente_maps.geolocate()
    return ubicacion['location']['lat'], ubicacion['location']['lng']

def buscar_tiendas_departamentales_cercanas(latitud, longitud, radio):
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
    return cliente_maps.distance_matrix(coordenadas1, coordenadas2)['rows'][0]['elements'][0]['distance']['value']

def main():
    clave_api = 'TU_CLAVE_DE_API'

    cliente_maps = googlemaps.Client(key=clave_api)

    # Obtener la ubicación actual
    latitud_actual, longitud_actual = obtener_ubicacion_actual()
    st.write("Tu ubicación actual: {}, {}".format(latitud_actual, longitud_actual))

    # Solicitar el radio de búsqueda al usuario en metros
    radio_busqueda = st.number_input("Ingrese el radio de búsqueda en metros:", value=1000)

    # Buscar tiendas departamentales cercanas
    tiendas_departamentales_cercanas = buscar_tiendas_departamentales_cercanas(latitud_actual, longitud_actual, radio_busqueda)

    # Almacenar las distancias y nombres de las tiendas
    distancias_manhattan = []
    distancias_euclideanas = []
    nombres_tiendas = []
    latitudes_tiendas = []
    longitudes_tiendas = []

    # Calcular las distancias y almacenar los nombres de las tiendas
    for tienda in tiendas_departamentales_cercanas:
        nombre = tienda['name']
        direccion = tienda['vicinity']
        coordenadas_tienda = tienda['geometry']['location']
        latitud_tienda = coordenadas_tienda['lat']
        longitud_tienda = coordenadas_tienda['lng']

        distancia_manhattan = calcular_distancia_manhattan((latitud_actual, longitud_actual), (latitud_tienda, longitud_tienda))
        distancia_euclidiana = calcular_distancia_euclidiana((latitud_actual, longitud_actual), (latitud_tienda, longitud_tienda))

        distancias_manhattan.append(distancia_manhattan)
        distancias_euclideanas.append(distancia_euclidiana)
        nombres_tiendas.append(nombre)
        latitudes_tiendas.append(latitud_tienda)
        longitudes_tiendas.append(longitud_tienda)

    # Crear el gráfico de dispersión
    plt.figure(figsize=(10, 6))
    plt.scatter(distancias_manhattan, distancias_euclideanas, c='blue', alpha=0.7)

    # Agregar etiquetas a los puntos
    for i, nombre in enumerate(nombres_tiendas):
        plt.annotate(nombre, (distancias_manhattan[i], distancias_euclideanas[i]), fontsize=8)

    # Configurar los ejes y el título del gráfico
    plt.xlabel('Distancia Manhattan')
    plt.ylabel('Distancia Euclidiana')
    plt.title('Distancias de Tiendas Departamentales')

    # Mostrar el gráfico
    st.pyplot(plt)

    # Crear el mapa con gmplot
    gmap = gmplot.GoogleMapPlotter(latitud_actual, longitud_actual, 13)

    # Agregar marcador para la ubicación actual
    gmap.marker(latitud_actual, longitud_actual, color='blue')

    # Agregar marcadores para las tiendas departamentales cercanas
    for lat, lon, nombre in zip(latitudes_tiendas, longitudes_tiendas, nombres_tiendas):
        gmap.marker(lat, lon, color='red', title=nombre)

    # Dibujar el mapa en un archivo HTML y abrirlo en el navegador
    gmap.draw('mapa_tiendas_departamentales.html')
    st.write("Mapa de tiendas departamentales generado.")

if __name__ == "__main__":
    main()
