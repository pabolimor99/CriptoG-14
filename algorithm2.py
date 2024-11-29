import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pillow_avif
from util.key_gen import generate_round_keys
from util.padding import insertar_datos_aleatorios, quitar_datos_aleatorios
from util.histo import mostrar_histogramas
from util.v2.cypher2 import encrypt_image, decrypt_image

if __name__ == "__main__":
    # Cargar la imagen y convertirla a escala de grises
    image = Image.open('./images/fali.jpg').convert('L')
    image = np.array(image)

    # Generar claves para dos rondas
    (x1, r1), (x2, r2) = generate_round_keys()
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

    # Mostrar las imágenes en un gráfico
    plt.figure(figsize=(15, 5))

    # Imagen original
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Imagen Original')
    plt.axis('off')

    # Imagen cifrada
    plt.subplot(1, 3, 2)
    plt.imshow(encrypted_image_2, cmap='gray')
    plt.title('Imagen Cifrada (2 rondas)')
    plt.axis('off')

    # Imagen descifrada
    plt.subplot(1, 3, 3)
    plt.imshow(decrypted_image_no_padding, cmap='gray')
    plt.title('Imagen Descifrada')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Mostrar histogramas de las imágenes
    mostrar_histogramas(image, encrypted_image_2, decrypted_image_no_padding)
