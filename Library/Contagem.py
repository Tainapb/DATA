import numpy as np
import cv2

# -------------------- Classe para Rastreamento de Objetos --------------------
class TrackedObject:
    def __init__(self, object_id, centroid):
        self.id = object_id
        self.centroid = centroid  # (x, y)
        self.previous_centroid = centroid
        self.disappeared = 0  # Contador de frames onde o objeto não foi detectado

class ObjectTracker:
    def __init__(self, max_disappeared=50, distance_threshold=80):
        self.next_object_id = 0
        self.objects = dict()  # object_id -> TrackedObject
        self.max_disappeared = max_disappeared
        self.distance_threshold = distance_threshold
        self.counted_ids = set()
        self.contador = 0

    def update(self, centroids, line_coefficients):
        A, B, C = line_coefficients

        if len(centroids) == 0:
            # Nenhum centroide detectado: aumentar contador de desaparecimento para todos os objetos
            for object_id in list(self.objects.keys()):
                self.objects[object_id].disappeared += 1
                if self.objects[object_id].disappeared > self.max_disappeared:
                    del self.objects[object_id]
            return

        if len(self.objects) == 0:
            # Registrar todos os centroides como novos objetos
            for centroid in centroids:
                self.objects[self.next_object_id] = TrackedObject(self.next_object_id, centroid)
                self.next_object_id += 1
        else:
            object_ids = list(self.objects.keys())
            object_centroids = [obj.centroid for obj in self.objects.values()]

            # Calcular a matriz de distância entre objetos atuais e novos centroides
            D = np.linalg.norm(np.array(object_centroids)[:, np.newaxis] - np.array(centroids), axis=2)

            # Encontrar as menores distâncias e suas correspondências
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            assigned_objects = set()
            assigned_centroids = set()

            for row, col in zip(rows, cols):
                if row in assigned_objects or col in assigned_centroids:
                    continue
                if D[row, col] > self.distance_threshold:
                    continue

                object_id = object_ids[row]
                self.objects[object_id].previous_centroid = self.objects[object_id].centroid
                self.objects[object_id].centroid = centroids[col]
                self.objects[object_id].disappeared = 0

                # Verificar cruzamento da linha
                self.check_crossing(
                    object_id,
                    self.objects[object_id].previous_centroid,
                    self.objects[object_id].centroid,
                    A, B, C
                )

                assigned_objects.add(row)
                assigned_centroids.add(col)

            # Identificar objetos que não foram atualizados
            unassigned_objects = set(range(len(object_ids))) - assigned_objects
            for row in unassigned_objects:
                object_id = object_ids[row]
                self.objects[object_id].disappeared += 1
                if self.objects[object_id].disappeared > self.max_disappeared:
                    del self.objects[object_id]

            # Registrar novos centroides que não foram associados a nenhum objeto
            unassigned_centroids = set(range(len(centroids))) - assigned_centroids
            for col in unassigned_centroids:
                self.objects[self.next_object_id] = TrackedObject(self.next_object_id, centroids[col])
                self.next_object_id += 1

    def check_crossing(self, object_id, previous_pos, current_pos, A, B, C):
        """
        Verifica se um objeto cruzou a linha definida pela equação Ax + By + C = 0.

        Args:
            object_id (int): ID único do objeto.
            previous_pos (tuple): Posição anterior do objeto (x, y).
            current_pos (tuple): Posição atual do objeto (x, y).
            A (float): Coeficiente A da equação da linha.
            B (float): Coeficiente B da equação da linha.
            C (float): Constante C da equação da linha.

        Retorna:
            None
        """
        # Calcula o valor da equação da reta para posições anterior e atual
        D_anterior = A * previous_pos[0] + B * previous_pos[1] + C
        D_atual = A * current_pos[0] + B * current_pos[1] + C

        # Verifica se houve mudança de lado
        if D_anterior * D_atual < 0 or (D_anterior == 0 and D_atual != 0):
            if object_id not in self.counted_ids:
                self.contador += 1
                self.counted_ids.add(object_id)
                print(f"Objeto {object_id} cruzou a linha. Total: {self.contador}")

    def draw_tracks(self, frame):
        for obj in self.objects.values():
            cv2.circle(frame, obj.centroid, 5, (0, 255, 0), -1)
            cv2.putText(frame, str(obj.id), (obj.centroid[0] - 10, obj.centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)