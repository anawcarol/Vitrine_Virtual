from pydantic import BaseModel
from typing import List, Dict, Optional

class MetricBase(BaseModel):
    label: str
    value: float | str
    unit: Optional[str] = None

class AnalysisResponse(BaseModel):
    video_id: str
    status: str
    
    # Camada 1
    metrics_basic: Dict[str, MetricBase]
    
    # Camada 2
    metrics_behavioral: Dict[str, MetricBase]
    
    # Camada 3 (O Ouro)
    urban_vitality_index: float
    opportunity_window: Dict[str, str] # Ex: {"melhor_horario": "18h"}
    
    class Config:
        from_attributes = True