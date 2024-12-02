
from util.v1.difusion import pixel_adaptive_diffusion, inverse_pixel_adaptive_diffusion
from util.v1.scrambling import generate_scrambling_matrix, scramble_image, invert_permutation
import numpy as np
#from util.scrambling import gen_matrix, scramble_image, descramble_image
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

    #TODO: Utilizar mismo scrambling que el paper

    inv_indices_x = invert_permutation(indices_x)
    inv_indices_y = invert_permutation(indices_y)

    unscrambled = diffused_image[inv_indices_x, :]
    unscrambled = unscrambled[:, inv_indices_y]

    return unscrambled



