import cv2
import numpy as np
import tkinter as tk
from Library.UI import ImageCropperApp, LineSelectorApp
from PIL import Image, ImageTk

# -------------------- Funções Auxiliares --------------------
def configurar_video(caminho_video):
    cap = cv2.VideoCapture(caminho_video)
    if not cap.isOpened():
        raise FileNotFoundError("Não foi possível abrir o vídeo.")
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Erro ao ler o primeiro frame do vídeo.")
    h, w, c = frame.shape
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return cap, frame, h, w, num_frames

def selecionar_area_e_linha(frame):
    # Seleção da área de interesse
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    root.deiconify()
    app = ImageCropperApp(root, image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    root.mainloop()
    bounding_box = app.infos()

    # Verificar se as coordenadas estão corretas
    if None in bounding_box:
        raise ValueError("Área de interesse não foi selecionada corretamente.")

    # Seleção da linha
    root = tk.Tk()
    root.withdraw()
    root.deiconify()
    line_app = LineSelectorApp(root, image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    root.mainloop()
    A, B, C = line_app.get_line_equation()

    return bounding_box, (A, B, C)

def processar_frame(frame, top, bottom, left, right, dim=(500, 500)):
    frame_recortado = frame[top:bottom, left:right]
    if frame_recortado.size == 0:
        raise ValueError("A área selecionada está vazia. Verifique as coordenadas de recorte.")
    return cv2.resize(frame_recortado, dim, interpolation=cv2.INTER_LINEAR)

def detectar_centroides(img1, img2):
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

    lista_centros = []

    for contour in contornos:
        area = cv2.contourArea(contour)
        if area > 14000:  # Limite mínimo para considerar um carro
            # Obter a caixa delimitadora (bounding box)
            x, y, w, h = cv2.boundingRect(contour)

            # Encontrar o centroide do contorno
            cx = int(x + w / 2)
            cy = int(y + h / 2)

            lista_centros.append((cx, cy))  # Apenas (x, y)

    return lista_centros
