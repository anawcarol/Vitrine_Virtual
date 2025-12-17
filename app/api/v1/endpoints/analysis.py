from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.schemas.video import AnalysisResponse
from app.services.yolo_service import YoloService
import shutil
import os

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_video(
    file: UploadFile = File(...),
    service: YoloService = Depends(YoloService)
):
    # 1. Validação simples
    if not file.filename.endswith((".mp4", ".avi", ".mov")):
        raise HTTPException(status_code=400, detail="Apenas arquivos de vídeo são permitidos.")

    # 2. Salvar arquivo temporário (O YOLO precisa ler do disco)
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = f"{temp_dir}/{file.filename}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 3. Chamar o Service (IA REAL RODANDO AGORA)
        print(f"🔄 Iniciando processamento do vídeo: {file.filename}")
        raw_data = await service.process_video(temp_path)
        print("✅ Processamento concluído!")

        # 4. Montar a Resposta (Mapper)
        return {
            "video_id": file.filename,
            "status": "success",
            "metrics_basic": {
                "fluxo": {
                    "label": "Fluxo Total",
                    "value": raw_data['fluxo'],
                    "unit": "pessoas"
                },

                "taxa_passagem": { 
                    "label": "Taxa de Passagem",
                    "value": raw_data['taxa_passagem'], # Esse nome tem que ser igual ao que o Service gerar
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

    except Exception as e:
        print(f"❌ Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Limpeza: Deleta o vídeo depois de processar para não lotar o HD
        if os.path.exists(temp_path):
            os.remove(temp_path)