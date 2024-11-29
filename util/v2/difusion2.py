from util.v2.scrambling2 import logistic_sine_map
import numpy as np

def modulo(val, mod):
    return ((val % mod) + mod) % mod

def generate_diffusion_matrix(height, width, x0, r):
    """
    Genera la matriz Q_{i,j} utilizando LSS con los parámetros proporcionados.
    """
    # Generar secuencia de números basada en el mapa seno-logístico
    lss_sequence = logistic_sine_map(x0, r, height * width)
    print("Secuencia generada por logistic_sine_map:", lss_sequence)  # Debug

    # Escalar los valores a enteros en el rango [0, 255]
    diffusion_matrix = (lss_sequence * 256).astype(np.uint8).reshape(height, width)
    return diffusion_matrix


def pixel_adaptive_diffusion(image, Q):
    """
    Aplica difusión adaptativa de píxeles utilizando la matriz Q_{i,j}.
    """
    F = 256  # Para imágenes de 8 bits
    rows, cols = image.shape

    # Convertir a int32 para evitar overflow
    image = image.astype(np.int32)
    Q = Q.astype(np.int32)
    diffused = np.zeros_like(image, dtype=np.int32)

    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:  # Caso i=1, j=1
                diffused[i, j] = modulo(image[i, j] + image[rows - 1, cols - 1] + Q[i, j], F)
            elif i == 0:  # Caso i=1, j!=1
                diffused[i, j] = modulo(image[i, j] + diffused[i, j - 1] + Q[i, j], F)
            else:  # Caso i!=1
                diffused[i, j] = modulo(image[i, j] + diffused[i - 1, j] + Q[i, j], F)

    # Convertir de vuelta a uint8
    return diffused.astype(np.uint8)


def inverse_pixel_adaptive_diffusion(diffused, Q):
    """
    Reversa la difusión adaptativa de píxeles utilizando la matriz Q_{i,j}.
    """
    F = 256  # Para imágenes de 8 bits
    rows, cols = diffused.shape

    # Convertir a int32 para evitar overflow
    diffused = diffused.astype(np.int32)
    Q = Q.astype(np.int32)
    original = np.zeros_like(diffused, dtype=np.int32)

    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:  # Caso i=1, j=1
                original[i, j] = modulo(diffused[i, j] - diffused[rows - 1, cols - 1] - Q[i, j], F)
            elif i == 0:  # Caso i=1, j!=1
                original[i, j] = modulo(diffused[i, j] - original[i, j - 1] - Q[i, j], F)
            else:  # Caso i!=1
                original[i, j] = modulo(diffused[i, j] - original[i - 1, j] - Q[i, j], F)

    # Convertir de vuelta a uint8
    return original.astype(np.uint8)


def modulo(val, mod):
    """
    Aplica un módulo seguro que maneja valores negativos.
    """
    return ((val % mod) + mod) % mod

