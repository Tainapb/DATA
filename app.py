from yo import yolo_infos
import tkinter as tk
import cv2
import numpy as np
import pathlib
import argparse
from collections import deque
from Library.Contagem import ObjectTracker, TrackedObject
from Library.Aux import processar_frame, detectar_centroides, configurar_video, selecionar_area_e_linha

# -------------------- Função Principal de Processamento --------------------
def detectar_movimento(caminho_video, objeto):
    limites = {
        'pessoas': (2000, 300),
        'carros': (1500, 700),
        'bikes': (1000, 400)
    }
    
    if objeto not in limites:
        raise ValueError(f"Objeto inválido: {objeto}. Escolha entre 'pessoas', 'carros' ou 'bikes'.")
    
    limite_superior, limite_inferior = limites[objeto]
    
    cap, frame, h, w, num_frames = configurar_video(caminho_video)
    (left, top, right, bottom), line_coefficients = selecionar_area_e_linha(frame)
    A, B, C = line_coefficients
    print(f"Equação da linha: {A}x + {B}y + {C} = 0")
    
    # Inicializar o rastreador
    tracker = ObjectTracker()

    # Ler o próximo frame para iniciar a comparação
    ret, prev_frame = cap.read()
    if not ret:
        print("Erro ao ler o vídeo.")
        cap.release()
        return

    try:
        prev_frame_resized = processar_frame(prev_frame, top, bottom, left, right)
    except ValueError as e:
        print(f"Erro no recorte do frame: {e}")
        cap.release()
        return

    frame_atual = 1
    intervalo_de_frames = 5  # Ajuste conforme necessário (e.g., 30 para pular frames)

    while frame_atual < num_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_atual)

        ret, current_frame = cap.read()
        if not ret:
            break

        try:
            # Processamento do frame atual
            current_frame_resized = processar_frame(current_frame, top, bottom, left, right)
        except ValueError as e:
            print(f"Erro no recorte do frame {frame_atual}: {e}")
            frame_atual += intervalo_de_frames
            continue

        # Detectar centroides entre o frame anterior e o atual
        lista_centros = detectar_centroides(prev_frame_resized, current_frame_resized)
        # print(lista_centros)

        # Atualizar o rastreador com os centroides detectados
        tracker.update(lista_centros, line_coefficients)

        # Desenhar a linha de contagem
        if B != 0:
            # Calcular dois pontos na linha para desenhar
            y_start = int((-C - A * 0) / B)
            y_end = int((-C - A * w) / B)
            cv2.line(current_frame_resized, (0, y_start), (w, y_end), (255, 0, 0), 2)
        else:
            # Linha vertical
            x = int(-C / A)
            cv2.line(current_frame_resized, (x, 0), (x, h), (255, 0, 0), 2)

        # Desenhar os rastros dos objetos
        tracker.draw_tracks(current_frame_resized)

        # Exibir o contador
        cv2.putText(current_frame_resized, f"Contagem: {tracker.contador}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Exibir o frame processado
        cv2.imshow("Contagem de Carros", current_frame_resized)

        # Atualizar o frame anterior
        prev_frame_resized = current_frame_resized.copy()

        # Controle de saída
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_atual += intervalo_de_frames

    cap.release()
    cv2.destroyAllWindows()
    print(f"Total de mudanças detectadas para {objeto}: {tracker.contador}")

# -------------------- Execução do Script --------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Processa um arquivo de vídeo.")
    parser.add_argument('video_file', type=str, help="Nome do arquivo de vídeo para processar")
    parser.add_argument('objeto', type=str, choices=['pessoas', 'carros', 'bikes'], help="Tipo de objeto para detecção")
    args = parser.parse_args()

    video_path = pathlib.Path(__file__).parent / 'Midia' / args.video_file
    print(f"Processando o arquivo de vídeo {video_path} para detecção de {args.objeto}")
    if not video_path.exists():
        print(f"O arquivo de vídeo {video_path} não foi encontrado.")
        exit(1)

    detectar_movimento(str(video_path), args.objeto)
