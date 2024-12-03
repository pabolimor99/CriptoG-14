from util.v2.scrambling2 import logistic_sine_map
import numpy as np

def modulo(val, mod):
    return ((val % mod) + mod) % mod

def generate_diffusion_matrix(height, width, x0, r):

    lss_sequence = logistic_sine_map(x0, r, height * width)
    print("Secuencia generada por logistic_sine_map:", lss_sequence)

    diffusion_matrix = (lss_sequence * 256).astype(np.uint8).reshape(height, width)
    return diffusion_matrix


def pixel_adaptive_diffusion(image, Q):
    F = 256
    rows, cols = image.shape
    image = image.astype(np.int32)
    Q = Q.astype(np.int32)
    diffused = np.zeros_like(image, dtype=np.int32)

    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                # c[0,0] = (T[0,0] + Q[0,0]) mod F
                diffused[i, j] = modulo(image[i, j] + Q[i, j], F)
            elif i == 0:
                # c[0,j] = (T[0,j] + c[0,j-1] + Q[0,j]) mod F
                diffused[i, j] = modulo(image[i, j] + diffused[i, j - 1] + Q[i, j], F)
            else:
                # c[i,j] = (T[i,j] + c[i-1,j] + Q[i,j]) mod F
                diffused[i, j] = modulo(image[i, j] + diffused[i - 1, j] + Q[i, j], F)
    return diffused.astype(np.uint16)

def inverse_pixel_adaptive_diffusion(diffused, Q):
    F = 256
    rows, cols = diffused.shape
    diffused = diffused.astype(np.int32)
    Q = Q.astype(np.int32)
    original = np.zeros_like(diffused, dtype=np.int32)

    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                # T[0,0] = (c[0,0] - Q[0,0]) mod F
                original[i, j] = modulo(diffused[i, j] - Q[i, j], F)
            elif i == 0:
                # T[0,j] = (c[0,j] - c[0,j-1] - Q[0,j]) mod F
                original[i, j] = modulo(diffused[i, j] - diffused[i, j - 1] - Q[i, j], F)
            else:
                # T[i,j] = (c[i,j] - c[i-1,j] - Q[i,j]) mod F
                original[i, j] = modulo(diffused[i, j] - diffused[i - 1, j] - Q[i, j], F)
    return original.astype(np.uint16)

def modulo(val, mod):

    return ((val % mod) + mod) % mod