from pydantic import BaseModel
from typing import List, Dict, Optional, Union

# =========================
# Sub-estruturas Básicas
# =========================
class MetricBase(BaseModel):
    label: str
    value: Union[float, int, str]
    unit: Optional[str] = None

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
    thermal_comfort: str
    rain_condition: str

# =========================
# Blocos de Análise (NOVO FORMATO)
# =========================

class Recommendation(BaseModel):
    tipo: str  # comercio, urbano, cultura
    item: str
    porque: str

class Intervencao(BaseModel):
    acao: str
    objetivo: str

class OportunidadePublica(BaseModel):
    intervencoes_leves: List[Intervencao]
    objetivo_urbano: str

class AnalysisBlock(BaseModel):
    perfil: str # Mantemos para referência interna
    oportunidade_publica: OportunidadePublica
    recomendacoes: List[Recommendation]

# =========================
# Resposta Final da API
# =========================
class AnalysisResponse(BaseModel):
    video_id: str
    status: str

    metrics_basic: Dict[str, MetricBase]
    metrics_behavioral: Dict[str, MetricBase]

    urban_vitality_index: float
    opportunity_window: Dict[str, str]

    context: ContextBlock
    climate: ClimateBlock

    # O Bloco de Análise agora contém a estrutura que você pediu
    analysis: AnalysisBlock

    class Config:
        from_attributes = True