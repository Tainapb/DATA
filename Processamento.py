import cv2 
import numpy as np
import matplotlib.pyplot as plt


def contornos(img1, img2):
    
    # Converter para HSV
    img_hsv_1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    img_hsv_2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    # Separar a componente V (brilho)
    v1 = img_hsv_1[:, :, 2]
    v2 = img_hsv_2[:, :, 2]
    # Subtrair os frames e criar a imagem binária
    imagem_subtraida_1 = cv2.absdiff(v1, v2)
    _, binarizada = cv2.threshold(imagem_subtraida_1, 20, 255, cv2.THRESH_BINARY)

    kernel = np.ones((9,9), np.uint8)
    dilate = cv2.dilate(binarizada, kernel=kernel, iterations=1)
    erode = cv2.erode(dilate, kernel=kernel, iterations=2)
    contornos, _ = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Definir os pontos da linha inclinada
    x1, y1 = 0, 100  # Ponto inicial da linha
    x2, y2 = img_hsv_1.shape[0],100   # Ponto final da linha
    
    lista_centros = []

    for contour in contornos:
        area = cv2.contourArea(contour)
        if area > 14000:  # Limite mínimo para considerar um carro
        # Obter a caixa delimitadora (bounding box)
            x, y, w, h = cv2.boundingRect(contour)

            # Encontrar o centroide do contorno
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            # Desenhar contorno e o centroide no frame
            #cv2.circle(img1, (cx, cy), 5, (0, 255, 0), -1)
            #cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
            lista_centros.append((x, y, w, h))
            
    '''# Desenhar a linha inclinada
    cv2.line(img1, (x1, y1), (x2, y2), (0, 0, 255), 2)

    plt.figure(figsize=(10, 7))
    # Plotar a imagem 
    plt.subplot(2, 2, 1)
    plt.imshow(erode, cmap='gray')
    plt.show()'''

    return lista_centros


def plot_image(img):
    plt.figure(figsize=(10, 7))
    plt.subplot(2, 2, 1)
    plt.imshow(img, cmap='gray')
    return plt.show()
