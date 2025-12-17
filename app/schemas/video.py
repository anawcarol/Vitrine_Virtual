from pydantic import BaseModel
from typing import List, Dict, Optional

class MetricBase(BaseModel):
    label: str
    value: float | str
    unit: Optional[str] = None

class AnalysisResponse(BaseModel):
    video_id: str
    status: str
    
    # Apenas hora de início (temperatura foi removida daqui)
    start_time: str  
    
    # Camada 1
    metrics_basic: Dict[str, MetricBase]
    
    # Camada 2
    metrics_behavioral: Dict[str, MetricBase]
    
    # Camada 3 (O Ouro)
    urban_vitality_index: float
    opportunity_window: Dict[str, str]
    
    class Config:
        from_attributes = True