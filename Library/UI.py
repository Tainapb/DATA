import tkinter as tk
from PIL import Image, ImageTk

# -------------------- Classe para Seleção da Área de Interesse --------------------
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
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline='red'
        )
    
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
    
    def crop_and_save(self, start_x, start_y, end_x, end_y):
        # Ordenar as coordenadas
        left = min(start_x, end_x)
        right = max(start_x, end_x)
        top = min(start_y, end_y)
        bottom = max(start_y, end_y)
        
        # Corrigir as coordenadas se necessário
        left = max(left, 0)
        top = max(top, 0)
        right = min(right, self.image.width)
        bottom = min(bottom, self.image.height)
        
        # Remove o retângulo de seleção após a conclusão
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        # Fecha a janela após a operação
        self.root.destroy()
        
        # Salva as coordenadas ordenadas
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
    
    def infos(self):
        return (self.left, self.top, self.right, self.bottom)

# -------------------- Classe para Seleção de Linha --------------------
class LineSelectorApp:
    def __init__(self, root, image):
        self.root = root
        self.image = image
        self.canvas = tk.Canvas(root, width=image.width, height=image.height)
        self.canvas.pack()
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.line_points = []
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if len(self.line_points) < 2:
            self.line_points.append((event.x, event.y))
            self.canvas.create_oval(
                event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="red"
            )
            if len(self.line_points) == 2:
                self.canvas.create_line(
                    self.line_points[0], self.line_points[1], fill="blue", width=2
                )
                self.root.destroy()  # Interrompe o loop sem fechar a janela

    def get_line_equation(self):
        (x1, y1), (x2, y2) = self.line_points
        if x1 == x2:  # Evitar divisão por zero (linha vertical)
            A = 1
            B = 0
            C = -x1
        else:
            A = y2 - y1
            B = x1 - x2
            C = x2 * y1 - x1 * y2
        return A, B, C