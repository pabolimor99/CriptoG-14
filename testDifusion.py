import numpy as np
from util.v2.difusion2 import generate_diffusion_matrix, pixel_adaptive_diffusion, inverse_pixel_adaptive_diffusion
from matplotlib import pyplot as plt
from PIL import Image
from util.key_gen import generate_round_keys

def debug_diffusion():
    # Caso controlado: matriz pequeña
    P = np.array([[11, 12, 13, 14],
                  [21, 22, 23, 24],
                  [31, 32, 33, 34],
                  [41, 42, 43, 44]])

    # Generar clave para difusión
    (x0, r), _ = generate_round_keys()
    Q = generate_diffusion_matrix(*P.shape, x0, r)

    print("Matriz original (P):")
    print(P)

    print("\nMatriz de difusión (Q):")
    print(Q)

    # Aplicar difusión adaptativa
    diffused = pixel_adaptive_diffusion(P, Q)
    print("\nMatriz después de la difusión:")
    print(diffused)

    # Revertir la difusión adaptativa
    restored = inverse_pixel_adaptive_diffusion(diffused, Q)
    print("\nMatriz después de revertir la difusión:")
    print(restored)

    # Verificar si la matriz restaurada coincide con la original
    if np.array_equal(P, restored):
        print("\nLa difusión y su inversa funcionan correctamente.")
    else:
        print("\nError: La matriz restaurada no coincide con la original.")

if __name__ == "__main__":
    # Prueba de difusión
    print("=== Depuración con Difusión ===")
    debug_diffusion()

    # Ahora procesamos la imagen real
    print("\n=== Procesamiento de Imagen Real ===")

    # Cargar la imagen y convertirla a escala de grises
    image = Image.open('./images/fali.jpg').convert('L')
    image = np.array(image)

    # Generar clave para difusión
    (x0, r), _ = generate_round_keys()

    # Generar matriz de difusión
    Q = generate_diffusion_matrix(*image.shape, x0, r)

    # Aplicar difusión adaptativa
    diffused_image = pixel_adaptive_diffusion(image, Q)

    # Revertir la difusión adaptativa
    restored_image = inverse_pixel_adaptive_diffusion(diffused_image, Q)

    # Mostrar las imágenes en un gráfico
    plt.figure(figsize=(15, 5))

    # Imagen original
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Imagen Original')
    plt.axis('off')

    # Imagen después de la difusión
    plt.subplot(1, 3, 2)
    plt.imshow(diffused_image, cmap='gray')
    plt.title('Imagen con Difusión (1 ronda)')
    plt.axis('off')

    # Imagen restaurada
    plt.subplot(1, 3, 3)
    plt.imshow(restored_image, cmap='gray')
    plt.title('Imagen Restaurada')
    plt.axis('off')

    plt.tight_layout()
    plt.show()