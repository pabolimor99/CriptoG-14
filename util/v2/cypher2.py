import numpy as np
from util.v2.difusion2 import pixel_adaptive_diffusion, inverse_pixel_adaptive_diffusion
from util.v2.scrambling2 import gen_matrix, scramble_image, descramble_image
from util.v2.difusion2 import generate_diffusion_matrix

def encrypt_image(image, key):
    height, width = image.shape
    x0, r = key

    S = gen_matrix(height, width, x0, r)

    Q = generate_diffusion_matrix(height, width, x0, r)

    scrambled_image = scramble_image(image, S)

    encrypted_image = pixel_adaptive_diffusion(scrambled_image, Q)

    return encrypted_image, S, Q


def decrypt_image(encrypted_image, key):
    height, width = encrypted_image.shape
    x0, r= key
    
    S = gen_matrix(height, width, x0, r)

    Q = generate_diffusion_matrix(height, width, x0, r)
    
    diffused_image = inverse_pixel_adaptive_diffusion(encrypted_image, Q)

    original_image = descramble_image(diffused_image, S)

    return original_image