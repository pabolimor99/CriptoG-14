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

def scramble_image(P, S):

    M, N = P.shape

    scrambled = np.zeros_like(P)

    for r in range(M):
        for c in range(N):

            j = np.where(S[r] == c)[0][0]

            m = (r - S[0, j]) % M
            n = S[m, j]

            scrambled[m, n] = P[r, c]

    return scrambled


def descramble_image(scrambled, S):

    M, N = scrambled.shape

    descrambled = np.zeros_like(scrambled)

    for m in range(M):
        for n in range(N):

            j = np.where(S[m] == n)[0][0]

            r = (m + S[0, j]) % M
            c = S[r, j]

            descrambled[r, c] = scrambled[m, n]
    return descrambled
