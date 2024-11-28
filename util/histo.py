from matplotlib import pyplot as plt

def mostrar_histogramas(imagen_original, imagen_cifrada, imagen_descifrada):
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.hist(imagen_original.ravel(), bins=256, range=[0, 256], color='blue', alpha=0.5)
    plt.title('Histograma de la Imagen Original')
    plt.xlabel('Intensidad de píxeles')
    plt.ylabel('Frecuencia')

    plt.subplot(1, 3, 2)
    plt.hist(imagen_cifrada.ravel(), bins=256, range=[0, 256], color='red', alpha=0.5)
    plt.title('Histograma de la Imagen Cifrada')
    plt.xlabel('Intensidad de píxeles')
    plt.ylabel('Frecuencia')

    plt.subplot(1, 3, 3)
    plt.hist(imagen_descifrada.ravel(), bins=256, range=[0, 256], color='green', alpha=0.5)
    plt.title('Histograma de la Imagen Descifrada')
    plt.xlabel('Intensidad de píxeles')
    plt.ylabel('Frecuencia')

    plt.tight_layout()
    plt.show()