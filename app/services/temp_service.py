import httpx
from datetime import datetime
import calendar
from typing import Dict, Any

class WeatherService:
    LAT = -15.7938
    LON = -47.8827
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    async def get_historical_weather(self, month: int, hour: int) -> Dict[str, Any]:
        year = 2024 # Ano base estatístico
        start_date, end_date = self._get_month_range(year, month)

        params = {
            "latitude": self.LAT,
            "longitude": self.LON,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "temperature_2m,precipitation",
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

                target_suffix = f"T{hour:02d}:00"
                
                filtered_temps = []
                filtered_precips = []

                for t, temp, precip in zip(times, temps, precips):
                    if t.endswith(target_suffix) and temp is not None:
                        filtered_temps.append(temp)
                        filtered_precips.append(precip)

                if not filtered_temps:
                    return {"status": "no_data"}

                # Médias Estatísticas
                avg_temp = sum(filtered_temps) / len(filtered_temps)
                avg_precip = sum(filtered_precips) / len(filtered_precips)
                
                rainy_days = sum(1 for p in filtered_precips if p > 0.1)
                rain_prob = (rainy_days / len(filtered_precips)) * 100

                # Lógica de Conforto Térmico (Brasília)
                if avg_temp < 18: comfort = "frio"
                elif 18 <= avg_temp < 24: comfort = "agradável"
                elif 24 <= avg_temp < 29: comfort = "quente"
                else: comfort = "muito quente"

                # Lógica de Condição de Chuva
                rain_cond = "chuvoso" if rain_prob > 30 else "seco"

                return {
                    "status": "success",
                    "data": {
                        "month": month,
                        "hour": hour,
                        "temperature_avg_c": round(avg_temp, 1),
                        "rain_probability_pct": round(rain_prob, 1),
                        "rain_volume_mm": round(avg_precip, 2),
                        "thermal_comfort": comfort,
                        "rain_condition": rain_cond
                    }
                }

            except Exception as e:
                print(f"Erro Weather API: {e}")
                # Fallback em caso de erro para não quebrar a API
                return {
                    "status": "error",
                    "data": {
                        "month": month, "hour": hour, 
                        "temperature_avg_c": 25.0, "rain_probability_pct": 0, 
                        "rain_volume_mm": 0, "thermal_comfort": "n/a", "rain_condition": "n/a"
                    }
                }

    def _get_month_range(self, year: int, month: int):
        last_day = calendar.monthrange(year, month)[1]
        return f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day}"