from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from app.schemas.video import AnalysisResponse
from app.services.yolo_service import YoloService
from datetime import datetime, time
from typing import Optional
import shutil
import os

class VideoValidator:
    # Headers de formatos de vídeo comuns
    VIDEO_SIGNATURES = {
        'mp4': [
            b'\x00\x00\x00\x18ftypmp4',  # MP4
            b'\x00\x00\x00\x1cftypisom', # MP4 ISO
            b'\x00\x00\x00\x20ftypmp42', # MP4 v2
            b'\x00\x00\x00\x1cftypM4V',  # M4V
        ],
        'mov': [
            b'\x00\x00\x00\x14ftypqt',   # QuickTime
            b'moov',                      # MOV (alternative)
        ],
        'avi': [
            b'RIFF',                      # AVI (followed by file size and 'AVI ')
        ],
        'wmv': [
            b'\x30\x26\xB2\x75\x8E\x66\xCF\x11\xA6\xD9\x00\xAA\x00\x62\xCE\x6C',  # WMV/ASF
        ],
        'flv': [
            b'FLV\x01',                   # Flash Video
        ],
        'mkv': [
            b'\x1A\x45\xDF\xA3',          # Matroska/MKV
        ],
        'webm': [
            b'\x1A\x45\xDF\xA3',          # WebM (uses Matroska container)
        ],
        'mpeg': [
            b'\x00\x00\x01\xBA',          # MPEG-PS
            b'\x00\x00\x01\xB3',          # MPEG video stream
        ],
        '3gp': [
            b'\x00\x00\x00\x14ftyp3gp',  # 3GP
            b'\x00\x00\x00\x203gp',       # 3GP alternative
        ],
    }

    

    @staticmethod
    async def validate_video_upload(file: UploadFile) -> tuple[bool, str | None]:
        """
        Valida se o arquivo enviado é realmente um vídeo checando os bytes inciais do header.
        
        Args:
            file: Arquivo de upload do FastAPI
            
        Returns:
            tuple: (is_valid, detected_format)
        """
        try:
            # Lê os primeiros 32 bytes
            header = await file.read(32)
            
            # Volta o ponteiro para o início do arquivo
            await file.seek(0)
            
            # Checa contra todas as assinaturas conhecidas
            for format_name, signatures in VideoValidator.VIDEO_SIGNATURES.items():
                for signature in signatures:
                    if header.startswith(signature):
                        return True, format_name
                    
                    # Caso especial para AVI - precisa checar 'AVI ' no offset 8
                    if format_name == 'avi' and signature == b'RIFF':
                        if header.startswith(b'RIFF') and header[8:12] == b'AVI ':
                            return True, 'avi'
            
            return False, None
            
        except Exception as e:
            print(f"Erro ao validar arquivo: {e}")
            return False, None
        

router = APIRouter()

def validate_time_format(time_str: str) -> time:
    """
    Valida e converte string de tempo para objeto time.
    Aceita formatos: "14:30", "14:30:00", "2:30 PM"
    """
    try:
        # Tenta formato 24h com segundos
        return datetime.strptime(time_str, "%H:%M:%S").time()
    except ValueError:
        try:
            # Tenta formato 24h sem segundos
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            try:
                # Tenta formato 12h (AM/PM)
                return datetime.strptime(time_str, "%I:%M %p").time()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de hora inválido. Use HH:MM (ex: 14:30) ou HH:MM:SS (ex: 14:30:00)"
                )

@router.post("/analyze", response_model=AnalysisResponse)
       
async def analyze_video(
    file: UploadFile = File(...),
    start_time: str = Form(..., description="Hora de início do vídeo (formato: HH:MM ou HH:MM:SS)"),
    temperature: float = Form(..., description="Temperatura em graus Celsius"),
    service: YoloService = Depends(YoloService)
    ):

    # 1. Validação simples

    #if not file.filename.endswith((".mp4", ".avi", ".mov")):
        #raise HTTPException(status_code=400, detail="Apenas arquivos de vídeo são permitidos.")
            # Metodo para validar o arquivo de vídeo

    # 1. Validação de tempo
    try:
        validated_time = validate_time_format(start_time)
        print(f"⏰ Hora de início validada: {validated_time.strftime('%H:%M:%S')}")
    except HTTPException as e:
        raise e
    
    # 2. Validação de temperatura
    if not -50 <= temperature <= 60:  # Range razoável para temperaturas urbanas
        raise HTTPException(
            status_code=400,
            detail="Temperatura deve estar entre -50°C e 60°C"
        )
    
    print(f"🌡️ Temperatura registrada: {temperature}°C")

    # 3. Validação de conteúdo (bytes do header) - NÃO APENAS EXTENSÃO
    is_valid, detected_format = await VideoValidator.validate_video_upload(file)
    
    if not is_valid:
        raise HTTPException(
            status_code=400, 
            detail="Arquivo inválido. O conteúdo do arquivo não corresponde a nenhum formato de vídeo conhecido."
        )
    
    print(f"✅ Vídeo válido detectado: {detected_format.upper()}")


    # 4. Salvar arquivo temporário (O YOLO precisa ler do disco)
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = f"{temp_dir}/{file.filename}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 5. Chamar o Service (IA REAL RODANDO AGORA)
        print(f"🔄 Iniciando processamento do vídeo: {file.filename}")
        # Passar tempo e temperatura para o service
        raw_data = await service.process_video(
            temp_path, 
            start_time=validated_time,
            temperature=temperature
        )

        print("✅ Processamento concluído!")
        
        # 6. Montar a Resposta (Mapper)
        return {
            "video_id": file.filename,
            "status": "success",
            "start_time": validated_time.strftime("%H:%M:%S"), 
            "temperature": temperature,  
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