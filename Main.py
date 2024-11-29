# Importando as bibliotecas 
from Library.SECCAO import ImageCropperApp
import tkinter as tk
import cv2 
import numpy as np
from PIL import Image

# Determinação do vídeo
cap = cv2.VideoCapture("Midia/Uberabinha.mp4")
 
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
left, top, right, bottom= app.infos()
# Loop principal
while (frame_atual < num_frames): 
    # Coleta dos frames
    ret, frame = cap.read() # coleta dos frames
    frame_resize=frame[top:bottom,left:right]
    frame_resize=cv2.resize(frame_resize, (500,500), interpolation = cv2.INTER_LINEAR) # redimensionamento do frame
    frame_tela = cv2.rectangle(frame,  (left, top), (right, bottom), (255,0,0), 3)
    ##############################################
    if frame_atual==1:
        cv2.imwrite('Midia/fig_sem_carros.png', frame_resize)
        img_sem_carros=cv2.imread("Midia/fig_sem_carros.png", 1)
        
    ##############################################
    if frame_atual % 50 == 0: 
        if img_50_frames is not None:
            img_atual = img_50_frames
            cv2.imwrite('Midia/fig_frame_atual.png', img_atual)
        cv2.imwrite('Midia/fig_50_frames.png', frame_resize)
        img_50_frames=frame_resize
        bool_img=True

        
    cv2.imshow("Video", frame_tela) 
    frame_atual+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break