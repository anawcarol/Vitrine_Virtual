from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from app.schemas.video import AnalysisResponse
from app.services.yolo_service import YoloService
from app.services.temp_service import WeatherService
from app.services.analise_service import AnaliseService
from app.core.validators import VideoValidator, validate_time_format
import shutil
import os

router = APIRouter()

@router.post("/complete-analysis", response_model=AnalysisResponse)
async def complete_analysis(
    file: UploadFile = File(...),
    start_time: str = Form(..., description="Hora de início (HH:MM:SS)"),
    month: int = Form(..., description="Mês do vídeo (1-12)"),
    
    yolo_service: YoloService = Depends(),
    weather_service: WeatherService = Depends(),
    analise_service: AnaliseService = Depends()
):
    # 1. Validações e Preparação
    validated_time = validate_time_format(start_time)
    await VideoValidator.validate_file(file)

    temp_path = f"temp_uploads/{file.filename}"
    os.makedirs("temp_uploads", exist_ok=True)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Execução dos Serviços
        
        # A) Visão Computacional
        print(f"🔄 Processando vídeo...")
        yolo_data = await yolo_service.process_video(temp_path, start_time=validated_time)
        
        # B) Clima Histórico
        print(f"☁️ Buscando clima...")
        weather_raw = await weather_service.get_historical_weather(month, validated_time.hour)
        # Extrai o dicionário de dados limpos do serviço de clima (se existir) ou usa fallback
        climate_data = weather_raw.get("data", {
            "month": month, "hour": validated_time.hour, 
            "temperature_avg_c": 0, "rain_probability_pct": 0, 
            "rain_volume_mm": 0, "thermal_comfort": "n/a", "rain_condition": "n/a"
        })

        # C) Inteligência Urbana (Gera 'analysis' com 'oportunidade_publica')
        print(f"🧠 Gerando diagnóstico...")
        urban_analysis = analise_service.gerar_diagnostico(yolo_data, weather_raw)

        # 3. Montagem da Resposta JSON
        return {
            "video_id": file.filename,
            "status": "success",
            
            "metrics_basic": {
                "fluxo": {
                    "label": "Fluxo Total",
                    "value": yolo_data['fluxo'],
                    "unit": "pessoas"
                },
                "permanencia": {
                    "label": "Permanência Média",
                    "value": yolo_data['permanencia'],
                    "unit": "segundos"
                }
            },
            
            "metrics_behavioral": {
                "velocidade": {
                    "label": "Ritmo Médio",
                    "value": yolo_data['velocidade'],
                    "unit": "m/s"
                }
            },
            
            "urban_vitality_index": yolo_data['ivu'],
            "opportunity_window": yolo_data['janela'],
            
            "context": {
                "local": "Setor Comercial Sul – Bloco C",
                "camera_type": "CFTV público",
                "analysis_version": "v1.0-hackathon"
            },
            
            "climate": {
                "month": climate_data.get("month"),
                "hour": climate_data.get("hour"),
                "temperature_avg_c": climate_data.get("temperature_avg_c"),
                "rain_probability_pct": climate_data.get("rain_probability_pct"),
                "rain_volume_mm": climate_data.get("rain_volume_mm"),
                "thermal_comfort": climate_data.get("thermal_comfort"),
                "rain_condition": climate_data.get("rain_condition")
            },
            
            # O bloco analysis conterá automaticamente 'oportunidade_publica' e 'recomendacoes'
            "analysis": urban_analysis
        }

    except Exception as e:
        print(f"❌ Erro Crítico: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)