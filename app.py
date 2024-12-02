import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pillow_avif
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
clave = st.text_input("Introduzca la clave para cifrar/descifrar:", type="password")

uploaded_file = st.file_uploader("Sube una imagen DICOM", type=["dcm"])

if uploaded_file is not None and clave:
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

    # Mostrar imagen original
    st.image(image, caption='Imagen Original', width=300, clamp=True, channels='L')

    # Generar claves de cifrado
    (x1, r1), (x2, r2) = generate_round_keys(clave)
    key1 = (x1, r1)
    key2 = (x2, r2)

    # Agregar padding a la imagen original
    imagen_expandida = insertar_datos_aleatorios(image)

    # Primera ronda de cifrado
    encrypted_image_1, S1, Q1 = encrypt_image(imagen_expandida, key1)
    
    # Segunda ronda de cifrado
    encrypted_image_2, S2, Q2 = encrypt_image(encrypted_image_1, key2)

    # Segunda ronda de descifrado
    decrypted_image_1 = decrypt_image(encrypted_image_2, key2, S2, Q2)

    # Primera ronda de descifrado
    decrypted_image_2 = decrypt_image(decrypted_image_1, key1, S1, Q1)

    # Quitar padding de la imagen descifrada
    decrypted_image_no_padding = quitar_datos_aleatorios(decrypted_image_2)

    # Mostrar la imagen cifrada y descifrada
    st.image(encrypted_image_2, caption='Imagen Cifrada (2 rondas)', width=300, clamp=True, channels='L')
    st.image(decrypted_image_no_padding, caption='Imagen Descifrada', width=300, clamp=True, channels='L')

    # Mostrar histogramas
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].hist(image.ravel(), bins=256, range=[0, 256], color='blue', alpha=0.5)
    ax[0].set_title('Histograma de la Imagen Original')
    ax[0].set_xlabel('Intensidad de píxeles')
    ax[0].set_ylabel('Frecuencia')

    ax[1].hist(encrypted_image_2.ravel(), bins=256, range=[0, 256], color='red', alpha=0.5)
    ax[1].set_title('Histograma de la Imagen Cifrada')
    ax[1].set_xlabel('Intensidad de píxeles')
    ax[1].set_ylabel('Frecuencia')

    ax[2].hist(decrypted_image_no_padding.ravel(), bins=256, range=[0, 256], color='green', alpha=0.5)
    ax[2].set_title('Histograma de la Imagen Descifrada')
    ax[2].set_xlabel('Intensidad de píxeles')
    ax[2].set_ylabel('Frecuencia')

    plt.subplots_adjust(wspace=0.3)
    st.pyplot(fig)