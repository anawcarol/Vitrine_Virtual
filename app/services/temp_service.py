import httpx
from datetime import datetime
import calendar
from typing import Dict, Any

class WeatherService:
    # Coordenadas do Setor Comercial Sul - Brasília
    LAT = -15.7938
    LON = -47.8827
    
    # URL da API de Histórico (Melhor que a Sazonal para precisão estatística)
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    async def get_historical_weather(self, month: int, hour: int) -> Dict[str, Any]:
        """
        Busca temperatura e chuva históricas (2024) para criar estatísticas e dados para gráficos.
        """
        year = 2024
        start_date, end_date = self._get_month_range(year, month)

        # Adicionamos 'precipitation' na requisição
        params = {
            "latitude": self.LAT,
            "longitude": self.LON,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "temperature_2m,precipitation", # <--- O Pulo do Gato
            "timezone": "America/Sao_Paulo"
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                hourly = data.get("hourly", {})
                times = hourly.get("time", [])
                temps = hourly.get("temperature_2m", [])
                precips = hourly.get("precipitation", [])

                # Filtrar dados apenas para a HORA solicitada (ex: 14:00) de cada dia
                target_suffix = f"T{hour:02d}:00"
                
                filtered_temps = []
                filtered_precips = []
                chart_data = [] # Lista pronta para o gráfico do Front

                for t, temp, precip in zip(times, temps, precips):
                    if t.endswith(target_suffix) and temp is not None:
                        filtered_temps.append(temp)
                        filtered_precips.append(precip)
                        
                        # Formata dado para o gráfico (Dia vs Temperatura/Chuva)
                        # Ex: "2024-12-01" -> Dia 01
                        day_str = t.split("T")[0].split("-")[2] 
                        chart_data.append({
                            "day": day_str,
                            "temperature": temp,
                            "precipitation": precip
                        })

                if not filtered_temps:
                    return {"status": "no_data"}

                # Estatísticas
                avg_temp = sum(filtered_temps) / len(filtered_temps)
                avg_precip = sum(filtered_precips) / len(filtered_precips)
                
                # Chance de chuva: % de dias que a chuva foi maior que 0.1mm
                rainy_days = sum(1 for p in filtered_precips if p > 0.1)
                rain_chance = (rainy_days / len(filtered_precips)) * 100

                return {
                    "status": "success",
                    "summary": {
                        "avg_temp": round(avg_temp, 1),
                        "avg_precip_mm": round(avg_precip, 2), # Média de volume
                        "rain_chance_percent": round(rain_chance, 0), # Chance de chover
                        "month": month,
                        "hour": hour,
                        "location": "SCS - Brasília"
                    },
                    "chart_data": chart_data # O FRONT VAI AMAR ISSO AQUI
                }

            except Exception as e:
                print(f"Erro Weather API: {e}")
                return {"error": str(e), "status": "error"}

    def _get_month_range(self, year: int, month: int):
        last_day = calendar.monthrange(year, month)[1]
        return f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day}"