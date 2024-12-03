import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from util.key_gen import generate_round_keys
from util.padding import insertar_datos_aleatorios, quitar_datos_aleatorios
from util.v2.scrambling2 import gen_matrix, scramble_image, descramble_image

def debug_scrambling():
    # Caso controlado: matriz pequeña
    P = np.array([[11, 12, 13, 14],
                  [21, 22, 23, 24],
                  [31, 32, 33, 34],
                  [41, 42, 43, 44]])
    
    # Generar claves para generar la matriz S
    x0, r = 0.5, 3.9  # Ejemplo de claves para depuración
    S = gen_matrix(*P.shape, x0, r)

    print("Matriz original (P):")
    print(P)

    print("\nMatriz de scrambling (S):")
    print(S)

    # Aplicar scrambling
    scrambled = scramble_image(P, S)
    print("\nMatriz después del scrambling:")
    print(scrambled)

    # Aplicar descrambling
    descrambled = descramble_image(scrambled, S)
    print("\nMatriz después del descrambling:")
    print(descrambled)

    # Verificar si la matriz descrambled coincide con la original
    if np.array_equal(P, descrambled):
        print("\nEl scrambling y descrambling funcionan correctamente.")
    else:
        print("\nError: La matriz descrambled no coincide con la original.")

if __name__ == "__main__":
    # Depuración con matriz pequeña
    print("=== Depuración con Matriz Pequeña ===")
    debug_scrambling()

    # Ahora procesamos la imagen real
    print("\n=== Procesamiento de Imagen Real ===")
    
    # Cargar la imagen y convertirla a escala de grises
    image = Image.open('./images/fali.jpg').convert('L')
    image = np.array(image)

    # Generar clave para una ronda
    x0, r = 0.5, 3.9  # Ejemplo de clave
    key = (x0, r)

    # Agregar padding a la imagen original
    imagen_expandida = insertar_datos_aleatorios(image)

    # Generar matriz de scrambling
    S = gen_matrix(*imagen_expandida.shape, *key)

    # Aplicar scrambling
    scrambled_image = scramble_image(imagen_expandida, S)

    # Aplicar descrambling
    descrambled_image = descramble_image(scrambled_image, S)

    # Quitar padding de la imagen descifrada
    descrambled_image_no_padding = quitar_datos_aleatorios(descrambled_image)

    # Mostrar las imágenes en un gráfico
    plt.figure(figsize=(15, 5))

    # Imagen original
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Imagen Original')
    plt.axis('off')

    # Imagen cifrada
    plt.subplot(1, 3, 2)
    plt.imshow(scrambled_image, cmap='gray')
    plt.title('Imagen Cifrada (Scrambling, 1 ronda)')
    plt.axis('off')

    # Imagen descifrada
    plt.subplot(1, 3, 3)
    plt.imshow(descrambled_image_no_padding, cmap='gray')
    plt.title('Imagen Descifrada')
    plt.axis('off')

    plt.tight_layout()
    plt.show()
