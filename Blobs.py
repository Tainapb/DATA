import cv2 
import numpy as np
import matplotlib.pyplot as plt


img_sem_modais = cv2.imread("Midia/fig_sem_carros.png")
img_atual = cv2.imread("Midia/fig_frame_atual.png")
img_50frames = cv2.imread("Midia/fig_50_frames.png")

# Converter para HSV
img_hsv_sem_modais = cv2.cvtColor(img_sem_modais, cv2.COLOR_BGR2HSV)
img_hsv_atual = cv2.cvtColor(img_atual, cv2.COLOR_BGR2HSV)
img_hsv_50frames = cv2.cvtColor(img_50frames, cv2.COLOR_BGR2HSV)

# Separar a componente V (brilho)
v_sem_modais = img_hsv_sem_modais[:, :, 2]
v_frame_atual = img_hsv_atual[:, :, 2]
v_50frames = img_hsv_50frames[:, :, 2] 

# Subtrair os frames e criar a imagem binária
imagem_subtraida_1 = cv2.absdiff(v_sem_modais, v_50frames)
imagem_subtraida_2 = cv2.absdiff(v_50frames, v_frame_atual)
_, imagem_bin_1 = cv2.threshold(imagem_subtraida_1, 40, 255, cv2.THRESH_BINARY)

imagem_bin_2 = np.where(imagem_subtraida_2 > 30, 255, 0).astype(np.uint8)
kernel = np.ones((3,3), np.uint8)
dilate_img_1 = cv2.dilate(imagem_bin_1, kernel=kernel, iterations=1)
erode_img_1 = cv2.erode(dilate_img_1, kernel=kernel, iterations=1)

kernel = np.ones((5, 5), np.uint8)  # Ajuste o tamanho do kernel conforme necessário
imagem_processada = cv2.morphologyEx(imagem_bin_1, cv2.MORPH_OPEN, kernel)
# -------------------------------------------------------------------------------------
contornos, _ = cv2.findContours(erode_img_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
imagem_colorida = img_atual
for contour in contornos:
    area = cv2.contourArea(contour)
    if area > 14000:  # Limite mínimo para considerar um carro
        # Obter a caixa delimitadora (bounding box)
        x, y, w, h = cv2.boundingRect(contour)

        # Encontrar o centroide do contorno
        cx = int(x + w / 2)
        cy = int(y + h / 2)

        # Desenhar contorno e o centroide no frame
        cv2.circle(img_atual, (cx, cy), 5, (0, 255, 0), -1)
        cv2.rectangle(img_atual, (x, y), (x + w, y + h), (255, 0, 0), 2)
plt.figure(figsize=(10, 7))

# Plotar a imagem 
plt.subplot(2, 2, 1)
plt.imshow(imagem_subtraida_1, cmap='gray')


plt.subplot(2, 2, 2)
plt.imshow(imagem_processada, cmap='gray')


plt.subplot(2, 2, 3)
plt.imshow(erode_img_1, cmap='gray')


plt.subplot(2, 2, 4)
plt.imshow(img_atual, cmap='gray')
plt.show()
