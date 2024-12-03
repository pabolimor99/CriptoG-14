import numpy as np
from util.v1.scrambling import logistic_sine_map

def pixel_adaptive_diffusion(image, random_data, modulus=256):
    """
    Aplica difusión adaptativa de píxeles para cifrar la imagen.
    """
    height, width = image.shape
    diffused = np.copy(image).astype(np.int32)
    for i in range(height):
        for j in range(width):
            if i == 0 and j == 0:
                diffused[i, j] = (image[i, j] + random_data[i, j]) % modulus
            elif i == 0:
                diffused[i, j] = (diffused[i, j - 1] + image[i, j] + random_data[i, j]) % modulus
            else:
                diffused[i, j] = (diffused[i - 1, j] + image[i, j] + random_data[i, j]) % modulus
    return diffused.astype(np.uint8)  # Convertir a uint8 para mantener los valores en rango

def inverse_pixel_adaptive_diffusion(encrypted_image, random_data, modulus=256):

    height, width = encrypted_image.shape
    diffused = np.copy(encrypted_image).astype(np.int32)

    for i in range(height - 1, -1, -1):
        for j in range(width - 1, -1, -1):
            if i == 0 and j == 0:
                diffused[i, j] = (encrypted_image[i, j] - random_data[i, j]) % modulus
            elif i == 0:
                diffused[i, j] = (encrypted_image[i, j] - diffused[i, j - 1] - random_data[i, j]) % modulus
            else:
                diffused[i, j] = (encrypted_image[i, j] - diffused[i - 1, j] - random_data[i, j]) % modulus

    return diffused.astype(np.uint8)


