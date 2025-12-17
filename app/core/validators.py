from fastapi import UploadFile, HTTPException
from datetime import datetime, time

class VideoValidator:
    # Headers de formatos de vídeo comuns (Magic Numbers)
    VIDEO_SIGNATURES = {
        'mp4': [
            b'\x00\x00\x00\x18ftypmp4', b'\x00\x00\x00\x1cftypisom',
            b'\x00\x00\x00\x20ftypmp42', b'\x00\x00\x00\x1cftypM4V',
        ],
        'mov': [b'\x00\x00\x00\x14ftypqt', b'moov'],
        'avi': [b'RIFF'],
        'wmv': [b'\x30\x26\xB2\x75\x8E\x66\xCF\x11\xA6\xD9\x00\xAA\x00\x62\xCE\x6C'],
        'flv': [b'FLV\x01'],
        'mkv': [b'\x1A\x45\xDF\xA3'],
        'webm': [b'\x1A\x45\xDF\xA3'],
        '3gp': [b'\x00\x00\x00\x14ftyp3gp', b'\x00\x00\x00\x203gp'],
    }

    @staticmethod
    async def validate_file(file: UploadFile) -> str:
        """
        Valida bytes reais do arquivo. Retorna o formato se válido, ou levanta HTTPException.
        """
        try:
            header = await file.read(32)
            await file.seek(0)  # Reseta o ponteiro para o início
            
            for format_name, signatures in VideoValidator.VIDEO_SIGNATURES.items():
                for signature in signatures:
                    if header.startswith(signature):
                        # Validação extra para AVI
                        if format_name == 'avi' and signature == b'RIFF':
                            if header[8:12] != b'AVI ':
                                continue
                        return format_name
            
            raise HTTPException(
                status_code=400, 
                detail="Arquivo inválido ou corrompido. Assinatura de vídeo não reconhecida."
            )
            
        except Exception as e:
            if isinstance(e, HTTPException): raise e
            raise HTTPException(status_code=400, detail=f"Erro na leitura do arquivo: {str(e)}")

def validate_time_format(time_str: str) -> time:
    """Valida formatos de hora HH:MM ou HH:MM:SS"""
    formats = ["%H:%M:%S", "%H:%M", "%I:%M %p"]
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
            
    raise HTTPException(
        status_code=400,
        detail="Formato de hora inválido. Use HH:MM (ex: 14:30) ou HH:MM:SS"
    )