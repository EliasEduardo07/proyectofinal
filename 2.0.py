# en esta version hemos creado las paginas y generado las graficas de IMC, esta version 2.0 aun no esta lista y se espera que la version 3.0 ya tenga implementado el algoritmo apriori. 
import streamlit as st
import csv
import matplotlib.pyplot as plt

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
                archivo = "datos_usuarios.csv"

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
