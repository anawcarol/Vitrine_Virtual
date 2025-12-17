import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
from typing import Dict, Any
import math

class YoloService:
    def __init__(self):
        # Carrega o modelo (Small é mais estável para permanência que o Nano)
        self.model = YOLO('yolov8n.pt')
        self.tracker = sv.ByteTrack()
        
        # Estruturas de dados originais
        self.dwell_times = []
        self.speeds = []
        self.tracking_data = {}

    async def process_video(self, video_path: str) -> Dict[str, Any]:
        try:
            video_info = sv.VideoInfo.from_video_path(video_path)
            fps = video_info.fps if video_info.fps > 0 else 30
        except:
            fps = 30
        
        stride = 3
        frame_generator = sv.get_video_frames_generator(video_path, stride=stride)
        
        # --- ADICIONADO: Variáveis de controle de tempo real ---
        current_time = 0.0
        time_per_step = stride / fps 

        for frame in frame_generator:
            # Detecção
            results = self.model(frame, classes=[0], verbose=False, conf=0.10)[0]
            detections = sv.Detections.from_ultralytics(results)

            # Rastreamento
            detections = self.tracker.update_with_detections(detections)
            
            # --- ALTERADO: Agora passamos o current_time para a função ---
            self._update_behavioral_metrics(detections, current_time, fps)
            
            # --- ADICIONADO: Incremento do cronômetro do vídeo ---
            current_time += time_per_step

        # --- CONSOLIDAÇÃO DOS DADOS (Foco na Permanência Real) ---
        
        total_fluxo = len(self.tracking_data)
        
        if total_fluxo == 0:
             return {
                "fluxo": 0, "permanencia": 0, "velocidade": 0,"taxa_passagem": 0,
                "ivu": 0, "janela": {"status": "Sem Dados", "horario": "--"}
            }

        # --- NOVO CÁLCULO DE PERMANÊNCIA REALISTA ---
        self.dwell_times = []
        for tracker_id in self.tracking_data:
            data_track = self.tracking_data[tracker_id]
            # Diferença entre última vez visto e primeira vez visto
            permanencia_absoluta = data_track['last_seen'] - data_track['first_seen']
            
            # Filtro para ignorar detecções fantasmas menores que 1 segundo
            if permanencia_absoluta > 1.0:
                self.dwell_times.append(permanencia_absoluta)

        avg_dwell = sum(self.dwell_times) / len(self.dwell_times) if self.dwell_times else 0
        
        # Métrica de Velocidade (Mantida como original)
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

    def _update_behavioral_metrics(self, detections: sv.Detections, current_time: float, fps: float):
        # Loop corrigido para 6 variáveis (Supervision update)
        for xyxy, mask, confidence, class_id, tracker_id, data in detections:
            if tracker_id is None: continue

            center_x = (xyxy[0] + xyxy[2]) / 2
            center_y = (xyxy[1] + xyxy[3]) / 2
            current_pos = (center_x, center_y)

            if tracker_id not in self.tracking_data:
                # --- ALTERADO: Salva o tempo de ENTRADA ---
                self.tracking_data[tracker_id] = {
                    'first_seen': current_time,
                    'last_seen': current_time,
                    'last_pos': current_pos
                }
            else:
                # --- ALTERADO: Atualiza apenas o tempo de SAÍDA (última vista) ---
                data_track = self.tracking_data[tracker_id]
                data_track['last_seen'] = current_time
                
                # Cálculo de Velocidade (Mantendo sua lógica de distância)
                last_x, last_y = data_track['last_pos']
                dist_px = math.sqrt((center_x - last_x)**2 + (center_y - last_y)**2)
                
                speed = dist_px * (fps / 2) # Ajuste pela velocidade de processamento
                if speed < 500: 
                    self.speeds.append(speed)
                
                data_track['last_pos'] = current_pos

    def _calculate_ivu(self, fluxo, permanencia, velocidade):
        score_fluxo = min(fluxo * 2.5, 100)
        score_perm = min(permanencia * 10, 100) 
        score_ritmo = max(100 - (velocidade * 20), 0)
        
        ivu = (score_fluxo * 0.4) + (score_perm * 0.4) + (score_ritmo * 0.2)
        return round(ivu, 1)

    def _calculate_opportunity(self, fluxo, permanencia):
        if fluxo < 20:
            return {"status": "Baixa Atividade (Área Fria)", "horario": "Agora"}
        elif 20 <= fluxo < 40:
            return {"status": "Fluxo Médio (Retenção)" if permanencia > 5 else "Fluxo Médio (Passagem)", "horario": "Agora"}
        else:
            return {"status": "Zona Viva (Multidão Retida)" if permanencia > 5 else "Alta Potência (Passagem Rápida)", "horario": "Agora"}