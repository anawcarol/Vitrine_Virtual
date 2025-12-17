import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
from typing import Dict, Any
import math

class YoloService:
    def __init__(self):
        # Carrega o modelo nano
        self.model = YOLO('yolov8n.pt')
        self.tracker = sv.ByteTrack()
        
        # Estruturas de dados
        self.dwell_times = []
        self.speeds = []
        self.tracking_data = {}

    async def process_video(self, video_path: str) -> Dict[str, Any]:
        try:
            video_info = sv.VideoInfo.from_video_path(video_path)
            fps = video_info.fps if video_info.fps > 0 else 30
        except:
            fps = 30
        
        # Stride=3 para performance
        stride = 3
        frame_generator = sv.get_video_frames_generator(video_path, stride=stride)
        adjusted_fps = fps / stride

        for frame in frame_generator:
            # Detecção
            results = self.model(frame, classes=[0], verbose=False, conf=0.25)[0]
            detections = sv.Detections.from_ultralytics(results)

            # Rastreamento
            detections = self.tracker.update_with_detections(detections)
            
            # Coleta de métricas
            self._update_behavioral_metrics(detections, adjusted_fps)

        # --- CONSOLIDAÇÃO DOS DADOS ---
        
        # Métrica 1: Fluxo Total (IDs únicos)
        total_fluxo = len(self.tracking_data)
        
        # Fallback para vídeo vazio
        if total_fluxo == 0:
             return {
                "fluxo": 0, "permanencia": 0, "velocidade": 0,"taxa_passagem": 0,
                "ivu": 0, "janela": {"status": "Sem Dados", "horario": "--"}
            }

        # Métrica 2: Permanência Média
        avg_dwell = sum(self.dwell_times) / len(self.dwell_times) if self.dwell_times else 0
        
        # Métrica 3: Velocidade Média
        avg_speed_px = sum(self.speeds) / len(self.speeds) if self.speeds else 0
        avg_speed_m_s = round(avg_speed_px * 0.05, 2) 

        #métrica 4: Taxa de Passagem

        # 1. Primeiro, descobrimos quanto tempo CADA pessoa única ficou na tela
        tempos_por_pessoa = {}
        for tracker_id, data in self.tracking_data.items():
            # Calculamos o tempo total (frames que ela apareceu / FPS)
            tempos_por_pessoa[tracker_id] = data['frames_present'] / adjusted_fps

        # 2. Contamos quantas pessoas ficaram MAIS de 3 segundos (consideradas "paradas")
        pessoas_que_pararam = sum(1 for tempo in tempos_por_pessoa.values() if tempo > 3.0)
        
        # 3. Calculamos a taxa de quem apenas PASSOU (não parou)
        if total_fluxo > 0:
            # Garante que o valor fique entre 0 e 100
            taxa = ((total_fluxo - pessoas_que_pararam) / total_fluxo) * 100
            taxa = max(0, min(100, taxa)) 
        else:
            taxa = 0

        # Cálculo do IVU e Janela com NOVOS LIMIARES
        ivu_score = self._calculate_ivu(total_fluxo, avg_dwell, avg_speed_m_s)
        opp_window = self._calculate_opportunity(total_fluxo, avg_dwell)

        return {
            "fluxo": total_fluxo,
            "permanencia": round(avg_dwell, 1),
            "velocidade": avg_speed_m_s,
            "taxa_passagem": round(taxa, 1),
            "ivu": ivu_score,
            "janela": opp_window
        }

    def _update_behavioral_metrics(self, detections: sv.Detections, fps: float):
        # Loop corrigido para 6 variáveis (Supervision update)
        for xyxy, mask, confidence, class_id, tracker_id, data in detections:
            if tracker_id is None: continue

            center_x = (xyxy[0] + xyxy[2]) / 2
            center_y = (xyxy[1] + xyxy[3]) / 2
            current_pos = (center_x, center_y)

            if tracker_id not in self.tracking_data:
                self.tracking_data[tracker_id] = {
                    'frames_present': 1,
                    'last_pos': current_pos
                }
            else:
                data_track = self.tracking_data[tracker_id]
                data_track['frames_present'] += 1
                
                last_x, last_y = data_track['last_pos']
                dist_px = math.sqrt((center_x - last_x)**2 + (center_y - last_y)**2)
                
                speed = dist_px * fps 
                if speed < 500: 
                    self.speeds.append(speed)
                
                data_track['last_pos'] = current_pos
                time_sec = data_track['frames_present'] / fps
                self.dwell_times.append(time_sec)

    def _calculate_ivu(self, fluxo, permanencia, velocidade):
        """
        Cálculo ajustado para a nova régua:
        - Fluxo: 40 pessoas = Nota 100
        """
        # Ajuste: Multiplicador 2.5 (40 * 2.5 = 100 pontos)
        score_fluxo = min(fluxo * 2.5, 100)
        
        # Permanência: 10 segundos = Nota 100
        score_perm = min(permanencia * 10, 100) 
        
        # Ritmo: Velocidade alta penaliza
        score_ritmo = max(100 - (velocidade * 20), 0)
        
        ivu = (score_fluxo * 0.4) + (score_perm * 0.4) + (score_ritmo * 0.2)
        return round(ivu, 1)

    def _calculate_opportunity(self, fluxo, permanencia):
        """
        Classificação Baseada na Régua do Usuário:
        < 20: Baixa
        20 - 40: Média
        > 40: Alta
        """
        
        # 1. FLUXO BAIXO (< 20)
        if fluxo < 20:
            return {"status": "Baixa Atividade (Área Fria)", "horario": "Agora"}
        
        # 2. FLUXO MÉDIO (20 a 40)
        elif 20 <= fluxo < 40:
            if permanencia < 5:
                return {"status": "Fluxo Médio (Passagem)", "horario": "Agora"}
            else:
                return {"status": "Fluxo Médio (Retenção)", "horario": "Agora"}
                
        # 3. FLUXO ALTO (>= 40)
        else:
            if permanencia < 5:
                # Muita gente passando rápido = Vitrine Ouro
                return {"status": "Alta Potência (Passagem Rápida)", "horario": "Agora"}
            else:
                # Muita gente ficando = Praça de Alimentação / Evento
                return {"status": "Zona Viva (Multidão Retida)", "horario": "Agora"}