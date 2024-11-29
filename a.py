# Importando as bibliotecas 
from Library.SECCAO import ImageCropperApp
from Processamento import contornos, plot_image
from yo import yolo_infos
import tkinter as tk
import cv2 
import numpy as np
from PIL import Image

# Determinação do vídeo
cap = cv2.VideoCapture("Midia/Uberabinha.mp4")
var_1 = False
var_2 = False
contador = 0 

# Frame de trabalho
frame_atual = 1
# Determinação do primeiro frame
ret,frame=cap.read()
# Determinação das propriedades 
h,w,c=frame.shape
# Conversão do frame de bgr para rgb
frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# Conversão 
frame=Image.fromarray(frame)
# Quantidade de frames no vídeo Q 
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
img_50_frames = None

# Rotina principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperApp(root,image=frame)
    root.mainloop()

left, top, right, bottom = app.infos()

# Leitura do primeiro frame
ret, prev_frame = cap.read()
if not ret:
    print("Erro ao ler o vídeo.")
    cap.release()
    exit()

frame_resize = prev_frame[top:bottom, left:right]
frame_resize = cv2.resize(frame_resize, (500, 500), interpolation=cv2.INTER_LINEAR)  # redimensionamento do frame

# Convertendo o primeiro frame para escala de cinza
prev_gray = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2GRAY)
prev = frame_resize

while (frame_atual< num_frames):
    ret, current_frame = cap.read()
    if not ret:
        break  # Se não houver mais frames, sair do loop

    frame_resize = current_frame[top:bottom, left:right]
    frame_resize = cv2.resize(frame_resize, (500, 500), interpolation=cv2.INTER_LINEAR)  # redimensionamento do frame
    frame_tela = cv2.rectangle(current_frame, (left, top), (right, bottom), (255, 0, 0), 3)

    # Convertendo o frame atual para escala de cinza
    current_gray = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2GRAY)

     ##############################################
    if frame_atual % 20 == 0: 
        prev_gray = current_gray
    # Subtração entre o frame atual e o anterior
    frame_diff = cv2.absdiff(current_gray, prev_gray)

    # Opcional: Realizar uma binarização para destacar as mudanças
    _, thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

    # Exibir a diferença
    white_pixels = cv2.countNonZero(thresh)  # Contando os pixels brancos

    if (white_pixels >1000) and (var_1 == False) and (var_2 == False):
        var_1 = True
    if (var_1 == True) and (white_pixels < 500):
        var_2 = True
    if (var_1 == True) and (var_2 == True):
        contador += 1
        #contornos(frame_resize, prev)
        lista_contornos=contornos(frame_resize, prev)
        print(lista_contornos)
        
        '''for i in range(len(lista_contornos)):
            x, y, w, h = lista_contornos[i]
            plot_image(frame_resize[y:y+10 + h+50, x:x + w+70])
            #name = 'Frames_Yolo/frame_' + str(frame_atual)+'_'+str(x)+'.png'
            #cv2.imwrite(name, frame_resize[y:y + h+50, x:x + w+50])
            #yolo_infos(frame_resize[y:y + h, x:x + w+50])'''

        var_1 = False
        var_2 = False

    # Imprimir os resultados
    #print(f"Quantidade de pixels brancos: {white_pixels}")
    #print(f"Contador de mudanças: {contador}")

    # Exibir o vídeo com a subtração
    cv2.imshow("Frame Difference", frame_resize)
    frame_atual+=1

    # Atualizar o frame anterior para a próxima iteração
    prev_gray = current_gray

    # Esperar pela tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
