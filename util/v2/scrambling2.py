import numpy as np
from util.v1.scrambling import logistic_sine_map

def gen_matrix(h, w, x0, r):

    a = logistic_sine_map(x0, r, h)
    b = logistic_sine_map(x0, r, w)

    indices_x = np.argsort(a)
    indices_y = np.argsort(b)

    S = np.tile(indices_y, (h, 1))

    for i in range(h):
        S[i] = np.roll(S[i], indices_x[i])

    return S

def scramble_image(image, S):

    M, N = image.shape

    scrambled = np.zeros_like(image)

    for r in range(M):
        for c in range(N):

            j = np.where(S[r, :] == c)[0][0]

            m = ((r - S[0,j] - 1) % M) + 1
            n = S[m -1, j]

            scrambled[m-1, n-1] = image[r, c]

    return scrambled

def descramble_image(scrambled, S):

    M, N = scrambled.shape

    original = np.zeros_like(scrambled)

    for m in range(M):
        for n in range(N):

            j = np.where(S[m, :] == n)[0][0]

            r = ((m + S[0, j] - 1) % M) + 1
            c = S[r - 1, j]

            original[r - 1, c - 1] = scrambled[m, n]

    return original