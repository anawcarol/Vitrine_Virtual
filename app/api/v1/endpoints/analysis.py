from fastapi import APIRouter, UploadFile, File, Depends
from app.schemas.video import AnalysisResponse
from app.services.yolo_service import YoloService

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_video(
    file: UploadFile = File(...),
    # Injeção de Dependência do Service
    service: YoloService = Depends(YoloService) 
):
    """
    Recebe um vídeo, processa com YOLOv8 e retorna métricas urbanas.
    """
    # 1. Salvar video temporariamente
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # 2. Chamar Service
    raw_data = await service.process_video(temp_path)
    
    # 3. Retornar JSON Estruturado (O Service de Metrics faria o cálculo do IVU aqui)
    return {
        "video_id": file.filename,
        "status": "success",
        "metrics_basic": {
            "fluxo": {"label": "Fluxo Total", "value": raw_data['fluxo'], "unit": "pessoas"},
            "permanencia": {"label": "Permanência Média", "value": raw_data['permanencia'], "unit": "segundos"}
        },
        "metrics_behavioral": {
             "velocidade": {"label": "Ritmo Médio", "value": raw_data['velocidade'], "unit": "m/s"}
        },
        "urban_vitality_index": 78.5, # Simulado
        "opportunity_window": {"status": "Alta Potência", "horario": "18:00"}
    }