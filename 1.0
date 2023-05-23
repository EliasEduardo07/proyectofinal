## Este archivo en streamlit genera lo siguiente: Pide datos del usuario y genera el archivo csv
import streamlit as st
import csv

# Definir la función para obtener los datos del usuario
def obtener_datos_usuario():
    st.header("Ingrese sus datos")

    nombre = st.text_input("Nombre", max_chars=40)
    apellido = st.text_input("Apellido Paterno", max_chars=15)
    edad = st.text_input("Edad")
    altura = st.text_input("Altura (cm)")
    peso = st.text_input("Peso (kg)")

    return nombre, apellido, edad, altura, peso

# Mostrar formulario y obtener los datos del usuario
nombre, apellido, edad, altura, peso = obtener_datos_usuario()

# Verificar si se han ingresado datos
if nombre and apellido and edad and altura and peso:
    # Validar que nombre y apellido contengan solo letras y espacios
    if not nombre.replace(" ", "").isalpha() or not apellido.replace(" ", "").isalpha():
        st.error("Ingrese un valor válido para el nombre y el apellido (solo letras y espacios).")
    # Validar que edad, altura y peso contengan solo números
    elif not edad.isdigit() or not altura.isdigit() or not peso.isdigit():
        st.error("Ingrese un valor válido para la edad, altura y peso (solo números).")
    else:
        # Crear una lista para almacenar el registro del usuario
        registro_usuario = [nombre, apellido, edad, altura, peso]

        # Navegar a una siguiente página o sección
        if st.button("Guardar"):
            # Nombre del archivo para almacenar los registros en formato CSV
            archivo = "datos_usuarios.csv"

            # Escribir los datos en el archivo CSV
            with open(archivo, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(registro_usuario)

            # Mostrar mensaje de éxito
            st.success("Los datos se han guardado correctamente en el archivo CSV.")
else:
    st.info("Por favor, complete todos los campos antes de guardar.")
