import httpx
from datetime import datetime, timedelta
import calendar
from typing import Dict, Any

class TempService:
    # Coordenadas do Setor Comercial Sul - Brasília
    LAT = -15.7938
    LON = -47.8827
    
    # URL da API de Histórico
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    async def get_avg_temperature(self, month: int, hour: int) -> Dict[str, Any]:
        """
        Busca a temperatura média histórica para um mês e horário específicos em Brasília.
        Usa o ano de 2024 como base estatística.
        """
        # 1. Definir o intervalo de datas (Mês escolhido no ano de 2024)
        year = 2024
        start_date, end_date = self._get_month_range(year, month)

        # 2. Montar a URL da API Open-Meteo
        params = {
            "latitude": self.LAT,
            "longitude": self.LON,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "temperature_2m",
            "timezone": "America/Sao_Paulo"
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                # 3. Processar os dados
                hourly_data = data.get("hourly", {})
                times = hourly_data.get("time", [])
                temps = hourly_data.get("temperature_2m", [])

                # 4. Filtrar apenas o horário solicitado
                target_temps = []
                target_suffix = f"T{hour:02d}:00"

                for t, temp in zip(times, temps):
                    if t.endswith(target_suffix) and temp is not None:
                        target_temps.append(temp)

                # 5. Calcular a média
                if not target_temps:
                    return {"avg_temp": 0, "status": "no_data"}

                avg_temp = sum(target_temps) / len(target_temps)

                return {
                    "avg_temp": round(avg_temp, 1),
                    "month": month,
                    "hour": hour,
                    "location": "SCS - Brasília",
                    "status": "success"
                }

            except Exception as e:
                print(f"Erro na API de Clima: {e}")
                return {"error": str(e), "status": "error"}

    def _get_month_range(self, year: int, month: int):
        """Retorna o primeiro e último dia do mês"""
        last_day = calendar.monthrange(year, month)[1]
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day}"
        return start_date, end_date