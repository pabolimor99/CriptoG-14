import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pillow_avif
import pydicom as dcmread
from util.key_gen import generate_round_keys
from util.padding import insertar_datos_aleatorios, quitar_datos_aleatorios
from util.histo import mostrar_histogramas
from util.v1.cypher import encrypt_image, decrypt_image

#TODO: cambiar flujo: introducir texto, generar clave, cifrar, guardar imagen cifrada y luego introducir clave para descifrar

def read_dicom(path):

    data = dcmread.dcmread(path)
    image = data.pixel_array

    if image.max() > 255:
        print(f"El valor máximo es: {image.max()}")
        image = (image / image.max() * 255).astype(np.uint8)
    return image

if __name__ == "__main__":

    image = Image.open('./images/fali.jpg').convert('L')

    image = np.array(image)

    image = read_dicom('./images/I1000000')

    (x1, r1), (x2, r2) = generate_round_keys()
    key1 = (x1, r1)
    key2 = (x2, r2)

    imagen_expandida = insertar_datos_aleatorios(image)

    encrypted_image_1, encryption_data_1 = encrypt_image(imagen_expandida, key1)

    encrypted_image_2, encryption_data_2 = encrypt_image(encrypted_image_1, key2)

    decrypted_image_1 = decrypt_image(encrypted_image_2, key2, encryption_data_2)

    decrypted_image_2 = decrypt_image(decrypted_image_1, key1, encryption_data_1)

    decrypted_image_no_padding = quitar_datos_aleatorios(decrypted_image_2)

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Imagen Original')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(encrypted_image_2, cmap='gray')
    plt.title('Imagen Cifrada (2 rondas)')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(decrypted_image_no_padding, cmap='gray')
    plt.title('Imagen Descifrada')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    mostrar_histogramas(image, encrypted_image_2, decrypted_image_no_padding)

