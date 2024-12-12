import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import tempfile
import pydicom
from util.padding import insertar_datos_aleatorios, quitar_datos_aleatorios
from util.v2.cypher2 import encrypt_image, decrypt_image
from util.key_gen import generate_round_keys
from util.anonimize import save_dicom

# Streamlit Application
st.title("Cifrado y Descifrado de Imágenes Médicas con Scrambling y Difusión")

# Cachear cifrado
@st.cache_data
def cifrar_imagen(image, clave_cifrado, _dicom_data):
    (x1, r1), (x2, r2) = generate_round_keys(clave_cifrado)
    key1 = (x1, r1)
    key2 = (x2, r2)

    # Agregar padding y cifrar
    imagen_expandida = insertar_datos_aleatorios(image)
    encrypted_image_1, _, _ = encrypt_image(imagen_expandida, key1)
    encrypted_image_2, _, _ = encrypt_image(encrypted_image_1, key2)

    # Guardar imagen cifrada como archivo DICOM
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".dcm").name
    save_dicom(encrypted_image_2, _dicom_data, output_path)

    return encrypted_image_2, output_path


# Cachear descifrado
@st.cache_data
def descifrar_imagen(encrypted_image, clave_descifrado):
    (x1_d, r1_d), (x2_d, r2_d) = generate_round_keys(clave_descifrado)
    key1_d = (x1_d, r1_d)
    key2_d = (x2_d, r2_d)

    # Descifrar en dos rondas
    decrypted_image_1 = decrypt_image(encrypted_image, key2_d)
    decrypted_image_2 = decrypt_image(decrypted_image_1, key1_d)

    # Remover padding
    return quitar_datos_aleatorios(decrypted_image_2)

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

    # Normalizar si es necesario
    max_val = image.max()
    if max_val > 255:
        image = ((image - image.min()) / (max_val - image.min()) * 255).astype(np.uint8)

    # Mostrar la imagen original y su histograma
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

    # Cifrar la imagen
    encrypted_image_2, output_path = cifrar_imagen(image, clave_cifrado, data)

    # Mostrar imagen cifrada y permitir descarga
    col3, col4 = st.columns(2)
    with col3:
        st.image(encrypted_image_2, caption="Imagen Cifrada", width=300, clamp=True, channels="L")
    with col4:
        fig, ax = plt.subplots()
        ax.hist(encrypted_image_2.ravel(), bins=256, range=[0, 256], color='red', alpha=0.5)
        ax.set_title('Histograma de la Imagen Cifrada')
        ax.set_xlabel('Intensidad de píxeles')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

    # Botón para descargar el archivo DICOM
    with open(output_path, "rb") as file:
        st.download_button(
            label="Descargar imagen cifrada en formato DICOM",
            data=file,
            file_name="imagen_cifrada.dcm",
            mime="application/dicom",
        )

# Sección para descifrar la imagen
st.header("Descifrar Imagen")
uploaded_encrypted_file = st.file_uploader("Sube una imagen DICOM cifrada", type=["dcm"])
clave_descifrado = st.text_input("Introduzca la clave para descifrar:", type="password")

if uploaded_encrypted_file is not None and clave_descifrado:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_encrypted_file.read())
        encrypted_dicom_path = temp_file.name

    # Leer la imagen cifrada
    encrypted_data = pydicom.dcmread(encrypted_dicom_path)
    encrypted_image = encrypted_data.pixel_array

    # Descifrar la imagen
    decrypted_image_no_padding = descifrar_imagen(encrypted_image, clave_descifrado)

    # Mostrar la imagen descifrada
    col5, col6 = st.columns(2)
    with col5:
        st.image(decrypted_image_no_padding, caption="Imagen Descifrada", width=300, clamp=True, channels="L")
    with col6:
        fig, ax = plt.subplots()
        ax.hist(decrypted_image_no_padding.ravel(), bins=256, range=[0, 256], color='green', alpha=0.5)
        ax.set_title('Histograma de la Imagen Descifrada')
        ax.set_xlabel('Intensidad de píxeles')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)
 
    decrypted_dicom_path = encrypted_dicom_path.replace("_encrypted.dcm", "_decrypted.dcm")
    save_dicom(decrypted_image_no_padding, encrypted_data, decrypted_dicom_path)

    # Proporcionar un enlace para descargar la imagen descifrada
    with open(decrypted_dicom_path, "rb") as file:
        btn = st.download_button(
            label="Descargar Imagen Descifrada",
            data=file,
            file_name="imagen_descifrada.dcm",
            mime="application/dicom"
        )

