export interface Metric {
    value: number;
    label: string;
    unit: string;
  }
  
  export interface Recommendation {
    tipo: string;
    item: string;
    porque: string;
  }
  
  export interface Intervencao {
    acao: string;
    objetivo: string;
  }
  
  export interface ReportData {
    video_id: string;
    status: string;
    metrics_basic: {
      fluxo: Metric;
      permanencia: Metric;
    };
    metrics_behavioral: {
      velocidade: Metric;
    };
    urban_vitality_index: number;
    opportunity_window: {
      status: string;
      horario: string;
    };
    context: {
      local: string;
      camera_type: string;
      analysis_version: string;
    };
    climate: {
      month: number;
      hour: number;
      temperature_avg_c: number;
      rain_probability_pct: number;
      rain_volume_mm: number;
      thermal_comfort: string;
      rain_condition: string;
    };
    analysis: {
      perfil: string;
      oportunidade_publica: {
        intervencoes_leves: Intervencao[];
        objetivo_urbano: string;
      };
      recomendacoes: Recommendation[];
    };
  }