from fastapi import UploadFile, HTTPException
from datetime import datetime, time

class VideoValidator:
    # Headers de formatos de vídeo comuns (Magic Numbers)
    VIDEO_SIGNATURES = {
    'mp4': [
        b'\x00\x00\x00\x18ftypmp4',
        b'\x00\x00\x00\x1cftypmp41',
        b'\x00\x00\x00\x1cftypmp42',
        b'\x00\x00\x00\x20ftypmp42',
        b'\x00\x00\x00\x1cftypisom',
        b'\x00\x00\x00\x20ftypisom',
        b'\x00\x00\x00\x1cftypM4V',
        b'\x00\x00\x00\x20ftypM4V',
        b'\x00\x00\x00\x1cftypMSNV',  # Sony PSP
        b'\x00\x00\x00\x1cftypM4A',   # M4A audio (também container MP4)
        b'\x00\x00\x00\x1cftypM4P',   # iTunes protected
        b'\x00\x00\x00\x1cftypM4B',   # iTunes audiobook
        b'\x00\x00\x00\x1cftypF4V',   # Flash MP4
        b'\x00\x00\x00\x1cftypF4P',   # Flash protected
        b'\x00\x00\x00\x1cftypF4A',   # Flash audio
        b'\x00\x00\x00\x1cftypF4B',   # Flash audiobook
        b'\x00\x00\x00\x1cftypavc1',  # AVC/H.264
        b'\x00\x00\x00\x1cftypMp41',
        b'\x00\x00\x00\x1cftypMp42',
        b'ftyp',  # Genérico - qualquer variante ftyp
    ],
    'mov': [
        b'\x00\x00\x00\x14ftypqt',
        b'\x00\x00\x00\x20ftypqt',
        b'moov',
        b'mdat',
        b'wide',
        b'free',
    ],
    'avi': [
        b'RIFF',
        b'AVI ',
    ],
    'wmv': [
        b'\x30\x26\xB2\x75\x8E\x66\xCF\x11\xA6\xD9\x00\xAA\x00\x62\xCE\x6C',
        b'\x30\x26\xB2\x75\x8E\x66\xCF\x11',  # Versão curta
    ],
    'flv': [
        b'FLV\x01',
        b'FLV\x04',
        b'FLV\x05',
    ],
    'mkv': [
        b'\x1A\x45\xDF\xA3',
    ],
    'webm': [
        b'\x1A\x45\xDF\xA3',
    ],
    '3gp': [
        b'\x00\x00\x00\x14ftyp3gp',
        b'\x00\x00\x00\x203gp',
        b'\x00\x00\x00\x1cftyp3gp4',
        b'\x00\x00\x00\x1cftyp3gp5',
        b'\x00\x00\x00\x1cftyp3gp6',
        b'\x00\x00\x00\x1cftyp3gp7',
        b'\x00\x00\x00\x1cftyp3ge6',
        b'\x00\x00\x00\x1cftyp3ge7',
        b'\x00\x00\x00\x1cftyp3gg6',
    ],
    'ogv': [
        b'OggS',
    ],
    'ts': [
        b'\x47',  # MPEG-TS (Transport Stream)
    ],
    'mts': [
        b'\x47',  # AVCHD
    ],
    'm2ts': [
        b'\x47',  # Blu-ray BDAV
    ],
    'vob': [
        b'\x00\x00\x01\xBA',  # MPEG-PS (DVD)
    ],
    'mpg': [
        b'\x00\x00\x01\xBA',  # MPEG-1/2
        b'\x00\x00\x01\xB3',
    ],
    'mpeg': [
        b'\x00\x00\x01\xBA',
        b'\x00\x00\x01\xB3',
    ],
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