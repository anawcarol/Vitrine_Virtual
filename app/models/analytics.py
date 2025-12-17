from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.core.database import Base
from datetime import datetime

class VideoAnalysis(Base):
    __tablename__ = "video_analysis"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    processed_at = Column(DateTime, default=datetime.utcnow)
    
    # Métricas Básicas (Camada 1)
    total_flow = Column(Integer) # Fluxo Total
    average_dwell_time = Column(Float) # Permanência média (segundos)
    
    # Métricas Comportamentais (Camada 2)
    average_speed = Column(Float) # Velocidade média (m/s)
    zone_usage = Column(JSON) # JSON com dados do Heatmap/Zonas
    recurrence_rate = Column(Float) # Taxa de recorrência estimada
    
    # Métricas Estratégicas (Camada 3)
    ivu_score = Column(Float) # Índice de Vitalidade Urbana (0-100)
    activation_potential = Column(String) # "Passagem", "Ativável", "Viva"