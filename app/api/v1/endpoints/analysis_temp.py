from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.temp_service import WeatherService # Atualizado import

router = APIRouter()

@router.get("/historical-weather")
async def get_historical_weather(
    month: int = Query(..., ge=1, le=12, description="Mês (1-12)"),
    hour: int = Query(..., ge=0, le=23, description="Hora (0-23)"),
    service: WeatherService = Depends()
):
    """
    Retorna inteligência climática:
    - Temperatura média
    - Volume de chuva e chance de chuva (%)
    - 'chart_data': Array pronto para gráficos de linha no Frontend
    """
    result = await service.get_historical_weather(month, hour)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=502, detail="Erro na API de Clima")
    
    return result