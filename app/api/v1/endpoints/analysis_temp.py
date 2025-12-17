from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.temp_service import TempService

router = APIRouter()

@router.get("/historical-weather")
async def get_historical_weather(
    month: int = Query(..., ge=1, le=12, description="Mês para análise (1-12)"),
    hour: int = Query(..., ge=0, le=23, description="Hora de interesse (0-23)"),
    service: TempService = Depends()
):
    """
    Retorna a média histórica de temperatura para um mês e horário específico no SCS (Brasília).
    """
    result = await service.get_avg_temperature(month, hour)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=502, detail="Erro ao comunicar com serviço de meteorologia")
    
    return result