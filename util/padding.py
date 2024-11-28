import numpy as np

def insertar_datos_aleatorios(imagen):
    alto, ancho = imagen.shape
    R = np.random.randint(0, 256, (2, ancho), dtype=np.uint8)
    O = np.random.randint(0, 256, (alto + 2, 2), dtype=np.uint8)
    
    imagen_exp = np.vstack([R[0], imagen, R[1]])
    imagen_exp = np.hstack([O[:, 0].reshape(-1, 1), imagen_exp, O[:, 1].reshape(-1, 1)])
    
    return imagen_exp

def quitar_datos_aleatorios(imagen):
    return imagen[1:-1, 1:-1]