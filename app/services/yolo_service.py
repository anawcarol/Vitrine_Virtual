from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np

class YoloService:
    def __init__(self):
        # Carrega o modelo apenas uma vez
        self.model = YOLO('yolov8n.pt') 

    async def process_video(self, video_path: str):
        # AQUI VAI A LÓGICA PESADA (Preencheremos depois)
        # 1. Abrir Video
        # 2. Loop Frame a Frame
        # 3. Calcular Fluxo, Velocidade, Permanência
        # 4. Retornar Dicionário com dados brutos
        
        # Mock temporário para testar a API hoje
        return {
            "fluxo": 150,
            "permanencia": 45.2,
            "velocidade": 1.2
        }