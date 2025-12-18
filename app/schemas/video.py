from pydantic import BaseModel
from typing import List, Dict, Optional, Union

# =========================
# Sub-estruturas
# =========================
class MetricBase(BaseModel):
    label: str
    value: Union[float, int, str]
    unit: Optional[str] = None

class Recommendation(BaseModel):
    tipo: str
    item: str
    porque: str

class AnalysisBlock(BaseModel):
    perfil: str
    recomendacoes: List[Recommendation]

class ContextBlock(BaseModel):
    local: str
    camera_type: str
    analysis_version: str

class ClimateBlock(BaseModel):
    month: int
    hour: int
    temperature_avg_c: float
    rain_probability_pct: float
    rain_volume_mm: float
    thermal_comfort: str # Ex: "quente", "agradável"
    rain_condition: str  # Ex: "seco", "chuvoso"

# =========================
# Resposta Final (O JSON que você pediu)
# =========================
class AnalysisResponse(BaseModel):
    video_id: str
    status: str

    # Métricas Quantitativas
    metrics_basic: Dict[str, MetricBase]
    metrics_behavioral: Dict[str, MetricBase]

    # Índices
    urban_vitality_index: float
    opportunity_window: Dict[str, str]

    # Metadados Novos
    context: ContextBlock
    climate: ClimateBlock

    # Mantendo a inteligência (Recomendações)
    analysis: AnalysisBlock

    class Config:
        from_attributes = True