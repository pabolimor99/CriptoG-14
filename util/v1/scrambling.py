import numpy as np

def logistic_sine_map(x0, r, iterations):
    seq = []
    x = x0
    for _ in range(iterations):
        x = (r * x * (1 - x) + (4 - r) * np.sin(np.pi * x) / 4) % 1
        seq.append(x)
    return np.array(seq)

#TODO: Utilizar mismo scrambling que el paper
def generate_scrambling_matrix(height, width, x0, r):
    seq_x = logistic_sine_map(x0, r, height)
    seq_y = logistic_sine_map(x0, r, width)
    indices_x = np.argsort(seq_x)
    indices_y = np.argsort(seq_y)
    return indices_x, indices_y



#TODO: Utilizar mismo scrambling que el paper
def scramble_image(image, indices_x, indices_y):
    scrambled = image[indices_x, :]
    scrambled = scrambled[:, indices_y]
    return scrambled

def invert_permutation(indices):
    inverse = np.zeros_like(indices)
    for i, idx in enumerate(indices):
        inverse[idx] = i
    return inverse