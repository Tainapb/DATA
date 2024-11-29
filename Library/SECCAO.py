import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageCropperApp:
    def __init__(self, root, image):
        self.root = root
        self.root.title("Selecione uma área da imagem")
        self.image = image
        self.tk_image = ImageTk.PhotoImage(self.image)
        # Configurar o Canvas
        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height)
        self.canvas.pack()

        # Mostrar a imagem no Canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        
        # Variáveis para rastrear a seleção
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect_id = None

        # Eventos do mouse
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
    
    def on_button_press(self, event):
        # Inicia a seleção
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')
    def on_mouse_drag(self, event):
        # Atualiza o retângulo de seleção
        cur_x = event.x
        cur_y = event.y
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        # Conclui a seleção
        self.end_x = event.x
        self.end_y = event.y
        self.crop_and_save(self.start_x, self.start_y, self.end_x, self.end_y)
    def crop_and_save(self, left, top, right, bottom):
        # Corrigir as coordenadas se necessário
        left, top = max(left, 0), max(top, 0)
        right, bottom = min(right, self.image.width), min(bottom, self.image.height)
        #print(left, top, right, bottom)
        # Remove o retângulo de seleção após a conclusão
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        # Fecha a janela após a operação
        self.root.destroy()
    def infos(self):
        return (self.start_x, self.start_y, self.end_x, self.end_y)

