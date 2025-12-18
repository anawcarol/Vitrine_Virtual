from typing import Dict, Any, List
from app.schemas.video import AnalysisBlock, Recommendation

class AnaliseService:
    
    def gerar_diagnostico(self, metrics: Dict[str, Any], weather: Dict[str, Any]) -> AnalysisBlock:
        """
        Orquestra a análise: Define perfil pelo YOLO e adiciona contexto do CLIMA.
        """
        # 1. Definir Perfil (Lógica do seu arquivo analise.py)
        perfil = self._definir_perfil(metrics)
        
        # 2. Gerar Recomendações Base (Lógica do seu arquivo analise.py)
        recs_list_dict = self._gerar_recomendacoes_base(perfil)
        
        # Converte para o objeto Schema Recommendation
        recs_objs = [Recommendation(**r) for r in recs_list_dict]

        # 3. Enriquecimento Climático (O "Pulo do Gato")
        # Se estiver muito quente ou chovendo, adicionamos recomendações extras
        weather_summary = weather.get('summary', {})
        temp = weather_summary.get('avg_temp', 25)
        chuva_prob = weather_summary.get('rain_chance_percent', 0)

        if temp > 29:
            recs_objs.append(Recommendation(
                tipo="conforto", 
                item="Sombreadores / Aspersores", 
                porque=f"Calor excessivo ({temp}°C) reduz permanência."
            ))
        
        if chuva_prob > 40:
             recs_objs.append(Recommendation(
                tipo="infraestrutura", 
                item="Coberturas / Toldos Retráteis", 
                porque=f"Alta chance de chuva ({chuva_prob}%) neste mês/horário."
            ))

        return AnalysisBlock(perfil=perfil, recomendacoes=recs_objs)

    # --- Lógica Original do seu analise.py ---

    def _definir_perfil(self, m: Dict[str, Any]) -> str:
        fluxo = m["fluxo"]
        permanencia = m["permanencia"]
        velocidade = m["velocidade"]

        if fluxo < 20:
            return "area_fria"

        if fluxo >= 40 and permanencia < 5:
            return "corredor_passagem"

        if fluxo >= 40 and permanencia >= 5:
            return "zona_viva"

        if 20 <= fluxo < 40 and permanencia >= 8:
            return "ponto_permanencia"

        if fluxo >= 30 and velocidade < 0.8:
            return "congestionada"

        return "uso_misto"

    def _gerar_recomendacoes_base(self, profile: str) -> List[Dict[str, str]]:
        if profile == "corredor_passagem":
            return [
                {"tipo": "comercio", "item": "café take-away / conveniência", "porque": "alto fluxo e baixa permanência"},
                {"tipo": "urbano", "item": "sinalização + iluminação", "porque": "melhora segurança e legibilidade do percurso"},
            ]

        if profile == "zona_viva":
            return [
                {"tipo": "comercio", "item": "alimentação (praça/bares)", "porque": "alto fluxo com permanência"},
                {"tipo": "cultura", "item": "feiras / pocket shows", "porque": "há retenção natural; eventos ampliam permanência"},
            ]

        if profile == "ponto_permanencia":
            return [
                {"tipo": "comercio", "item": "cafés, livrarias, coworking", "porque": "boa permanência indica interesse"},
                {"tipo": "urbano", "item": "bancos/sombra/wifi", "porque": "reforça conforto para permanecer"},
            ]

        if profile == "area_fria":
            return [
                {"tipo": "cultura", "item": "ativação cultural temporária", "porque": "baixo fluxo precisa de motivo para ir"},
                {"tipo": "urbano", "item": "iluminação + arte urbana", "porque": "aumenta sensação de segurança e atratividade"},
            ]

        if profile == "congestionada":
            return [
                {"tipo": "urbano", "item": "organização do espaço (fluxos/filas)", "porque": "velocidade baixa sugere conflito de circulação"},
                {"tipo": "comercio", "item": "quiosques ordenados", "porque": "funciona, mas precisa reduzir atrito no fluxo"},
            ]

        return [
            {"tipo": "comercio", "item": "mix flexível", "porque": "padrão intermediário"},
            {"tipo": "urbano", "item": "micro-mobiliário", "porque": "ajuda a testar aumento de permanência"},
        ]