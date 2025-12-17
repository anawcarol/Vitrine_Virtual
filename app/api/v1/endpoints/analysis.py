from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from app.schemas.video import AnalysisResponse
from app.services.yolo_service import YoloService
from app.core.validators import VideoValidator, validate_time_format
import shutil
import os

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_video(
    file: UploadFile = File(...),
    start_time: str = Form(..., description="Hora de início do vídeo (HH:MM:SS)"),
    service: YoloService = Depends(YoloService)
):
    """
    Endpoint principal: Recebe vídeo, valida formato e hora, e processa métricas de fluxo/IVU.
    """
    
    # 1. Validações (via core/validators.py)
    validated_time = validate_time_format(start_time)
    print(f"⏰ Hora de início validada: {validated_time}")

    detected_format = await VideoValidator.validate_file(file)
    print(f"✅ Formato detectado: {detected_format.upper()}")

    # 2. Arquivo Temporário
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = f"{temp_dir}/{file.filename}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 3. Processamento (Service)
        print(f"🔄 Iniciando YOLOv8 no arquivo: {file.filename}")
        
        # Chamada limpa (sem temperatura)
        raw_data = await service.process_video(
            temp_path, 
            start_time=validated_time
        )

        print("✅ Análise concluída com sucesso!")
        
        # 4. Mapper de Resposta
        return {
            "video_id": file.filename,
            "status": "success",
            "start_time": validated_time.strftime("%H:%M:%S"),
            "metrics_basic": {
                "fluxo": {
                    "label": "Fluxo Total",
                    "value": raw_data['fluxo'],
                    "unit": "pessoas"
                },
                "taxa_passagem": { 
                    "label": "Taxa de Passagem",
                    "value": raw_data.get('taxa_passagem', 0),
                    "unit": "%"
                },
                "permanencia": {
                    "label": "Permanência Média",
                    "value": raw_data['permanencia'],
                    "unit": "segundos"
                }
            },
            "metrics_behavioral": {
                "velocidade": {
                    "label": "Ritmo Médio",
                    "value": raw_data['velocidade'],
                    "unit": "m/s"
                }
            },
            "urban_vitality_index": raw_data['ivu'],
            "opportunity_window": raw_data['janela']
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"❌ Erro Crítico: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)