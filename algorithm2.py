import numpy as np
import matplotlib.pyplot as plt
import pydicom
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime
from util.key_gen import generate_round_keys
from util.padding import insertar_datos_aleatorios, quitar_datos_aleatorios
from util.histo import mostrar_histogramas
from util.v2.cypher2 import encrypt_image, decrypt_image
from util.anonimize import save_dicom

def read_dicom(path):
    """
    Lee una imagen DICOM, verifica su tipo y realiza normalización a 8 bits si es necesario.
    """
    # Leer el archivo DICOM
    data = pydicom.dcmread(path)
    image = data.pixel_array  # Extraer la matriz de píxeles

    # Comprobación del tipo de imagen
    if hasattr(data, "PhotometricInterpretation"):
        print(f"Photometric Interpretation: {data.PhotometricInterpretation}")

    if hasattr(data, "BitsAllocated"):
        print(f"Bits Allocated: {data.BitsAllocated}")

    # Comprobación del valor máximo
    max_val = image.max()
    print(f"El valor máximo es: {max_val}")

    # Normalización si el rango de valores excede 8 bits
    if max_val > 255:
        print("Normalizando la imagen a 8 bits...")
        image = ((image - image.min()) / (max_val - image.min()) * 255).astype(np.uint8)
    
    # Retornar la imagen normalizada y el rango original
    return image, data, image.min(), image.max()

if __name__ == "__main__":
    # Ruta del archivo DICOM
    dicom_path = './images/I1000000.dcm'
    output_path = './images/I1000000_processed.dcm'

    # Leer la imagen y convertirla a escala de grises si es necesario
    image, original_dicom, original_min, original_max = read_dicom(dicom_path)

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

    # Re-escalar la imagen descifrada de vuelta a 16 bits
    decrypted_image_rescaled = ((decrypted_image_no_padding / 255) * (original_max - original_min) + original_min).astype(np.uint16)

    # Guardar la imagen descifrada como archivo DICOM
    save_dicom(decrypted_image_rescaled, original_dicom, output_path)

    # Mostrar las imágenes en un gráfico
    plt.figure(figsize=(15, 5))

    # Imagen original
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Imagen Original (8 bits)')
    plt.axis('off')

    # Imagen cifrada
    plt.subplot(1, 3, 2)
    plt.imshow(encrypted_image_2, cmap='gray')
    plt.title('Imagen Cifrada (2 rondas, 8 bits)')
    plt.axis('off')

    # Imagen descifrada re-escalada
    plt.subplot(1, 3, 3)
    plt.imshow(decrypted_image_rescaled / original_max, cmap='gray')  # Escalar para visualizar
    plt.title('Imagen Descifrada (Re-escalada a 16 bits)')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Mostrar histogramas de las imágenes
    mostrar_histogramas(image, encrypted_image_2, decrypted_image_rescaled)
