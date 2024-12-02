import cv2
import numpy as np
import pathlib

contador = 0

# Função para verificar cruzamento de linha inclinada
def check_crossing(object_id, previous_pos, current_pos, A, B, C):
    """
    Checks if an object has crossed a line defined by the equation Ax + By + C = 0.

    Args:
        object_id (int): The unique identifier of the object.
        previous_pos (tuple): The previous position of the object as a tuple (x, y).
        current_pos (tuple): The current position of the object as a tuple (x, y).
        A (float): The coefficient A in the line equation.
        B (float): The coefficient B in the line equation.
        C (float): The constant term C in the line equation.

    Returns:
        None
    """
    global contador
    # Calcula o valor da equação da reta para posições anterior e atual
    D_anterior = A * previous_pos[0] + B * previous_pos[1] + C
    D_atual = A * current_pos[0] + B * current_pos[1] + C
    # print(f"Objeto {object_id}: D_anterior={D_anterior}, D_atual={D_atual}")
    # Verifica se houve mudança de lado
    if D_anterior * D_atual < 0 or (D_anterior == 0 and D_atual != 0) :
        if object_id not in counted_ids:
            contador += 1
            counted_ids.add(object_id)
            print(f"Objeto {object_id} cruzou a linha. Total: {contador}")


if __name__ == '__main__':
    # Defina a equação da reta Ax + By + C = 0
    A = 1    # Coeficiente de x
    B = -1   # Coeficiente de y
    C = 0    # Termo constante
    counted_ids = set()
    previous_centroids = {}
    current_centroids = {}

    # Inicialização do vídeo ou captura de frames
    cap = cv2.VideoCapture(pathlib.Path.cwd() / 'Dados' / 'Uberabinha.mp4')  # Substitua pelo caminho do seu vídeo

    # Inicialização do rastreador (exemplo simplificado usando detecção simulada)
    # Para uso real, integre com um algoritmo de detecção e rastreamento, como YOLO + Deep SORT

    while True:
        # Capture frame a frame
        ret, frame = cap.read()
        if not ret:
            break

        # **Processamento de Detecção e Rastreamento**
        # Aqui, você deve implementar a detecção de objetos e atribuir IDs únicos
        # Para fins de exemplo, vamos simular alguns centroides
        # Exemplo:
        # current_centroids = {1: (100, 100), 2: (150, 200), ...}

        # *** Simulação de centroides para demonstração ***
        # REMOVA esta parte e integre com seu método de detecção real
        # Vamos simular que o objeto com ID 1 está se movendo de (50, 50) para (150, 150)
        # e o objeto com ID 2 está se movendo de (200, 50) para (100, 150)
        # (A = 1, B = -1, C = 0 define a linha y = x)
        import time
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        current_centroids = {}
        # Simulação: apenas um objeto se movendo diagonalmente cruzando y=x
        current_centroids[1] = (frame_number * 2, 300 + frame_number * 2)  # Objeto 1
        current_centroids[2] = (800 - frame_number * 2, frame_number * 2)  # Objeto 2
        current_centroids[3] = (frame_number * 2, 300 - frame_number * 2)  # Objeto 3
        current_centroids[4] = (800 - frame_number * 2, 300 - frame_number * 2)  # Objeto 4
        current_centroids[5] = (400, 300)  # Objeto 5 (não cruza a linha)
        current_centroids[6] = (frame_number * 2 -20, frame_number * 1 +20)
        

        # *** Fim da simulação ***

        # Verificar cruzamento para cada objeto
        for object_id, current_pos in current_centroids.items():
            previous_pos = previous_centroids.get(object_id)
            if previous_pos:
                check_crossing(object_id, previous_pos, current_pos, A, B, C)
        
        # Atualizar previous_centroids para o próximo frame
        previous_centroids = current_centroids.copy()

        # **Desenhar a Reta de Contagem**
        # Para desenhar a reta, precisamos de dois pontos. Vamos calcular dois pontos na imagem.
        height, width = frame.shape[:2]
        # Escolha valores de x para calcular y
        x1, x2 = 0, width
        # Calcule y usando a equação da reta: y = (-A/B)x - C/B
        if B != 0:
            y1 = int((-A * x1 - C) / B)
            y2 = int((-A * x2 - C) / B)
        else:
            # Linha vertical: x = -C/A
            x_vert = int(-C / A)
            y1, y2 = 0, height
            x1, x2 = x_vert, x_vert

        # Desenhar a linha
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # **Desenhar Centroides e IDs**
        for object_id, pos in current_centroids.items():
            cv2.circle(frame, pos, 5, (0, 0, 255), -1)
            cv2.putText(frame, str(object_id), (pos[0] + 10, pos[1]), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # **Exibir o Contador**
        cv2.putText(frame, f'Contador: {contador}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Exibir o frame
        cv2.imshow('Frame', frame)

        # Sair com 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberação de recursos
    cap.release()
    cv2.destroyAllWindows()
