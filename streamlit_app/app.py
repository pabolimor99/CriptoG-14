import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pillow_avif
import streamlit as st
import tempfile

def insertar_datos_aleatorios(imagen):
    alto, ancho = imagen.shape
    R = np.random.randint(0, 256, (2, ancho), dtype=np.uint32)
    O = np.random.randint(0, 256, (alto + 2, 2), dtype=np.uint32)
    
    imagen_exp = np.vstack([R[0], imagen, R[1]])
    imagen_exp = np.hstack([O[:, 0].reshape(-1, 1), imagen_exp, O[:, 1].reshape(-1, 1)])
    
    return imagen_exp

def quitar_datos_aleatorios(imagen):
    return imagen[1:-1, 1:-1]

def logistic_sine_map(x0, r, iterations):
    seq = []
    x = x0
    for _ in range(iterations):
        x = (r * x * (1 - x) + (4 - r) * np.sin(np.pi * x) / 4) % 1
        seq.append(x)
    return np.array(seq)

def generate_scrambling_matrix(height, width, x0, r):
    seq_x = logistic_sine_map(x0, r, height)
    seq_y = logistic_sine_map(x0, r, width)
    indices_x = np.argsort(seq_x)
    indices_y = np.argsort(seq_y)
    return indices_x, indices_y

def scramble_image(image, indices_x, indices_y):
    scrambled = image[indices_x, :]
    scrambled = scrambled[:, indices_y]
    return scrambled

def invert_permutation(indices):
    inverse = np.zeros_like(indices)
    for i, idx in enumerate(indices):
        inverse[idx] = i
    return inverse

def pixel_adaptive_diffusion(image, random_data, modulus=255):
    height, width = image.shape
    diffused = np.copy(image)
    for i in range(height):
        for j in range(width):
            if i == 0 and j == 0:
                diffused[i, j] = (image[i, j] + random_data[i, j]) % modulus
            elif i == 0:
                diffused[i, j] = (diffused[i, j - 1] + image[i, j] + random_data[i, j]) % modulus
            else:
                diffused[i, j] = (diffused[i - 1, j] + image[i, j] + random_data[i, j]) % modulus
    return diffused

def inverse_pixel_adaptive_diffusion(encrypted_image, random_data, modulus=255):
    height, width = encrypted_image.shape
    diffused = np.copy(encrypted_image)

    for i in range(height - 1, -1, -1):
        for j in range(width - 1, -1, -1):
            if i == 0 and j == 0:
                diffused[i, j] = (encrypted_image[i, j] - random_data[i, j]) % modulus
            elif i == 0:
                diffused[i, j] = (encrypted_image[i, j] - diffused[i, j - 1] - random_data[i, j]) % modulus
            else:
                diffused[i, j] = (encrypted_image[i, j] - diffused[i - 1, j] - random_data[i, j]) % modulus

    return diffused

def encrypt_image(image, key):
    height, width = image.shape
    x0, r = key
    random_data = np.random.randint(0, 256, size=(height, width), dtype=np.uint32)

    indices_x, indices_y = generate_scrambling_matrix(height, width, x0, r)
    scrambled_image = scramble_image(image, indices_x, indices_y)

    encrypted_image = pixel_adaptive_diffusion(scrambled_image, random_data)

    return encrypted_image, (indices_x, indices_y, random_data)

def decrypt_image(encrypted_image, key, encryption_data):
    indices_x, indices_y, random_data = encryption_data

    diffused_image = inverse_pixel_adaptive_diffusion(encrypted_image, random_data)

    # Invertir las permutaciones de scrambling
    inv_indices_x = invert_permutation(indices_x)
    inv_indices_y = invert_permutation(indices_y)

    unscrambled = diffused_image[inv_indices_x, :]
    unscrambled = unscrambled[:, inv_indices_y]

    return unscrambled

def mostrar_histogramas(imagen_original, imagen_cifrada, imagen_descifrada):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].hist(imagen_original.ravel(), bins=256, range=[0, 256], color='blue', alpha=0.5)
    axs[0].set_title('Histograma de la Imagen Original')
    axs[0].set_xlabel('Intensidad de píxeles')
    axs[0].set_ylabel('Frecuencia')

    axs[1].hist(imagen_cifrada.ravel(), bins=256, range=[0, 256], color='red', alpha=0.5)
    axs[1].set_title('Histograma de la Imagen Cifrada')
    axs[1].set_xlabel('Intensidad de píxeles')
    axs[1].set_ylabel('Frecuencia')

    axs[2].hist(imagen_descifrada.ravel(), bins=256, range=[0, 256], color='green', alpha=0.5)
    axs[2].set_title('Histograma de la Imagen Descifrada')
    axs[2].set_xlabel('Intensidad de píxeles')
    axs[2].set_ylabel('Frecuencia')

    plt.tight_layout()
    st.pyplot(fig)

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

    # Clave de cifrado
    key = (0.5, 3.99)  # x0, r

    imagen_expandida = insertar_datos_aleatorios(image)

    # Cifrar imagen
    encrypted_image, encryption_data = encrypt_image(imagen_expandida, key)

    # Descifrar imagen
    decrypted_image = decrypt_image(encrypted_image, key, encryption_data)

    # Remover el padding
    decrypted_image_no_padding = quitar_datos_aleatorios(decrypted_image)

    # Mostrar la imagen cifrada y descifrada
    st.image(encrypted_image, caption='Imagen Cifrada', use_container_width=True, clamp=True, channels='L')
    st.image(decrypted_image_no_padding, caption='Imagen Descifrada', use_container_width=True, clamp=True, channels='L')

    # Mostrar histogramas
    mostrar_histogramas(image, encrypted_image, decrypted_image_no_padding)
