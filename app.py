import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pillow_avif
import streamlit as st
import tempfile
from util.padding import insertar_datos_aleatorios, quitar_datos_aleatorios
from util.histo import mostrar_histogramas
from util.cypher import encrypt_image, decrypt_image
from util.key_gen import generate_round_keys

# Streamlit Application
st.title("Cifrado y Descifrado de Imágenes Médicas con Scrambling y Difusión")

uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg", "avif"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        image = Image.open(temp_file.name).convert('L')  # Convertir a escala de grises
    image = np.array(image)

    # Mostrar imagen original
    st.image(image, caption='Imagen Original', use_column_width=True, clamp=True, channels='L')

    # Generar claves de cifrado
    (x1, r1), (x2, r2) = generate_round_keys()
    key1 = (x1, r1)
    key2 = (x2, r2)

    imagen_expandida = insertar_datos_aleatorios(image)

    # Cifrar imagen
    encrypted_image_1, encryption_data_1 = encrypt_image(imagen_expandida, key1)
    encrypted_image_2, encryption_data_2 = encrypt_image(encrypted_image_1, key2)

    # Descifrar imagen
    decrypted_image_1 = decrypt_image(encrypted_image_2, key2, encryption_data_2)
    decrypted_image_2 = decrypt_image(decrypted_image_1, key1, encryption_data_1)

    # Remover el padding
    decrypted_image_no_padding = quitar_datos_aleatorios(decrypted_image_2)

    # Mostrar la imagen cifrada y descifrada
    st.image(encrypted_image_2, caption='Imagen Cifrada (2 rondas)', use_container_width=True, clamp=True, channels='L')
    st.image(decrypted_image_no_padding, caption='Imagen Descifrada', use_container_width=True, clamp=True, channels='L')

    # Mostrar histogramas
    mostrar_histogramas(image, encrypted_image_2, decrypted_image_no_padding)
