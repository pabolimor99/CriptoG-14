import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
import tempfile
import pydicom
from util.padding import insertar_datos_aleatorios, quitar_datos_aleatorios
from util.histo import mostrar_histogramas
from util.v2.cypher2 import encrypt_image, decrypt_image
from util.key_gen import generate_round_keys
from util.anonimize import save_dicom

# Streamlit Application
st.title("Cifrado y Descifrado de Imágenes Médicas con Scrambling y Difusión")

# Solicitar clave de cifrado
clave_cifrado = st.text_input("Introduzca la clave para cifrar:", type="password")

uploaded_file = st.file_uploader("Sube una imagen DICOM", type=["dcm"])

if uploaded_file is not None and clave_cifrado:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        dicom_path = temp_file.name

    # Leer la imagen DICOM
    data = pydicom.dcmread(dicom_path)
    image = data.pixel_array

    # Comprobación del valor máximo
    max_val = image.max()
    if max_val > 255:
        image = ((image - image.min()) / (max_val - image.min()) * 255).astype(np.uint8)

    # Mostrar imagen original y su histograma
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption='Imagen Original', width=300, clamp=True, channels='L')
    with col2:
        fig, ax = plt.subplots()
        ax.hist(image.ravel(), bins=256, range=[0, 256], color='blue', alpha=0.5)
        ax.set_title('Histograma de la Imagen Original')
        ax.set_xlabel('Intensidad de píxeles')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

    # Generar claves de cifrado
    (x1, r1), (x2, r2) = generate_round_keys(clave_cifrado)
    key1 = (x1, r1)
    key2 = (x2, r2)

    # Agregar padding a la imagen original
    imagen_expandida = insertar_datos_aleatorios(image)

    # Primera ronda de cifrado
    encrypted_image_1, S1, Q1 = encrypt_image(imagen_expandida, key1)
    
    # Segunda ronda de cifrado
    encrypted_image_2, S2, Q2 = encrypt_image(encrypted_image_1, key2)

    # Guardar la imagen cifrada como archivo DICOM
    output_path = dicom_path.replace(".dcm", "_encrypted.dcm")
    save_dicom(encrypted_image_2, data, output_path)

    # Mostrar la imagen cifrada y su histograma
    col3, col4 = st.columns(2)
    with col3:
        st.image(encrypted_image_2, caption='Imagen Cifrada (2 rondas)', width=300, clamp=True, channels='L')
    with col4:
        fig, ax = plt.subplots()
        ax.hist(encrypted_image_2.ravel(), bins=256, range=[0, 256], color='red', alpha=0.5)
        ax.set_title('Histograma de la Imagen Cifrada')
        ax.set_xlabel('Intensidad de píxeles')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

    # Enlace para descargar la imagen cifrada en formato DICOM
    with open(output_path, "rb") as file:
        btn = st.download_button(
            label="Descargar imagen cifrada en formato DICOM",
            data=file,
            file_name="imagen_cifrada.dcm",
            mime="application/dicom"
        )

# Sección para descifrar la imagen
st.header("Descifrar Imagen")

uploaded_encrypted_file = st.file_uploader("Sube una imagen DICOM cifrada", type=["dcm"])
clave_descifrado = st.text_input("Introduzca la clave para descifrar:", type="password")

if uploaded_encrypted_file is not None and clave_descifrado:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_encrypted_file.read())
        encrypted_dicom_path = temp_file.name

    # Leer la imagen DICOM cifrada
    encrypted_data = pydicom.dcmread(encrypted_dicom_path)
    encrypted_image = encrypted_data.pixel_array

    # Generar claves de descifrado
    (x1_d, r1_d), (x2_d, r2_d) = generate_round_keys(clave_descifrado)
    key1_d = (x1_d, r1_d)
    key2_d = (x2_d, r2_d)

    # Segunda ronda de descifrado
    decrypted_image_1 = decrypt_image(encrypted_image, key2_d)

    # Primera ronda de descifrado
    decrypted_image_2 = decrypt_image(decrypted_image_1, key1_d)

    # Remover el padding
    decrypted_image_no_padding = quitar_datos_aleatorios(decrypted_image_2)

    # Mostrar la imagen descifrada y su histograma
    col5, col6 = st.columns(2)
    with col5:
        st.image(decrypted_image_no_padding, caption='Imagen Descifrada', width=300, clamp=True, channels='L')
    with col6:
        fig, ax = plt.subplots()
        ax.hist(decrypted_image_no_padding.ravel(), bins=256, range=[0, 256], color='green', alpha=0.5)
        ax.set_title('Histograma de la Imagen Descifrada')
        ax.set_xlabel('Intensidad de píxeles')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)