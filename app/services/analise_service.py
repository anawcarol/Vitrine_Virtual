from typing import Dict, Any, List
from app.schemas.video import AnalysisBlock, Recommendation, OportunidadePublica, Intervencao

class AnaliseService:
    
    def gerar_diagnostico(self, metrics: Dict[str, Any], weather: Dict[str, Any]) -> AnalysisBlock:
        """
        Gera o diagnóstico completo cruzando métricas visuais (YOLO) e climáticas.
        """
        # 1. Definição do Perfil Urbano
        perfil = self._definir_perfil(metrics)
        
        # 2. Extração de Dados Climáticos
        # O WeatherService retorna um dict com chave 'data' ou 'summary'
        weather_data = weather.get('data', weather.get('summary', {}))
        
        # Extraímos valores numéricos para lógica da Oportunidade Pública
        temp_val = weather_data.get('temperature_avg_c', weather_data.get('avg_temp', 25))
        chuva_prob = weather_data.get('rain_probability_pct', weather_data.get('rain_chance_percent', 0))

        # 3. Gerar Oportunidade Pública (Foco: Governo/Urbanismo)
        opp_publica = self._gerar_oportunidade_publica(perfil, temp_val, chuva_prob)

        # 4. Gerar Recomendações (Foco: Cultural/Comercial/Climático)
        # AQUI MUDOU: Passamos o objeto weather_data completo para ler "quente"/"chuvoso"
        recs_list = self._gerar_recomendacoes_culturais(perfil, weather_data)

        return AnalysisBlock(
            perfil=perfil,
            oportunidade_publica=opp_publica,
            recomendacoes=recs_list
        )

    def _definir_perfil(self, m: Dict[str, Any]) -> str:
        fluxo = m["fluxo"]
        permanencia = m["permanencia"]
        velocidade = m["velocidade"]
        
        if fluxo < 20: return "area_fria"
        if fluxo >= 40 and permanencia < 5: return "corredor_passagem"
        if fluxo >= 40 and permanencia >= 5: return "zona_viva"
        if 20 <= fluxo < 40 and permanencia >= 8: return "ponto_permanencia"
        if fluxo >= 30 and velocidade < 0.8: return "congestionada"
        
        return "uso_misto"

    def _gerar_oportunidade_publica(self, perfil: str, temp: float, chuva: float) -> OportunidadePublica:
        intervencoes = []
        objetivo = ""

        # Lógica por Perfil
        if perfil == "corredor_passagem":
            objetivo = "Converter corredor de passagem em espaço de permanência progressiva"
            intervencoes.append(Intervencao(acao="Instalação de Parklets", objetivo="Criar pontos de pausa rápida sem bloquear fluxo"))
            intervencoes.append(Intervencao(acao="Reforço de iluminação peatonal", objetivo="Aumentar segurança visual no trajeto rápido"))

        elif perfil == "zona_viva":
            objetivo = "Qualificar a permanência e organizar o uso intenso"
            intervencoes.append(Intervencao(acao="Ampliação de lixeiras e zeladoria", objetivo="Manter salubridade com alto fluxo"))
            intervencoes.append(Intervencao(acao="Mobiliário fixo antivandalismo", objetivo="Democratizar o descanso"))

        elif perfil == "area_fria":
            objetivo = "Atrair fluxo inicial através de acupuntura urbana"
            intervencoes.append(Intervencao(acao="Iluminação Cênica / Instagramável", objetivo="Atrair curiosidade e fluxo noturno"))
            intervencoes.append(Intervencao(acao="Liberação para Arte Urbana", objetivo="Ressignificar a identidade do local"))

        elif perfil == "ponto_permanencia":
            objetivo = "Conectar fluxo de passagem com áreas de estar consolidadas"
            intervencoes.append(Intervencao(acao="Melhoria de calçadas/acessibilidade", objetivo="Facilitar o acesso de quem deseja parar"))
            intervencoes.append(Intervencao(acao="Pontos de Wi-Fi Público", objetivo="Estender o tempo de permanência produtiva"))
            
        elif perfil == "congestionada":
            objetivo = "Reordenar fluxos para reduzir conflitos"
            intervencoes.append(Intervencao(acao="Alargamento de calçadas ou faixas exclusivas", objetivo="Melhorar a fluidez do pedestre"))

        else: # uso misto
            objetivo = "Monitorar e incentivar diversidade de usos"
            intervencoes.append(Intervencao(acao="Micro-praças temporárias", objetivo="Testar vocação do espaço"))

        # Lógica Climática (Numérica) para Obras Públicas
        if temp > 28:
            intervencoes.insert(0, Intervencao(
                acao="Instalação de sombreamento e arborização",
                objetivo="Aumentar conforto térmico e estimular permanência"
            ))
        
        if chuva > 40:
            intervencoes.append(Intervencao(
                acao="Estruturas de cobertura leve/toldos",
                objetivo="Proteger pedestres e garantir uso em dias chuvosos"
            ))

        return OportunidadePublica(intervencoes_leves=intervencoes, objetivo_urbano=objetivo)

    def _gerar_recomendacoes_culturais(self, perfil: str, climate: Dict[str, Any]) -> List[Recommendation]:
        """
        Gera recomendações baseadas no perfil urbano E nas condições climáticas (conforto/chuva).
        """
        recs_data = []

        # 1. Recomendações baseadas no Perfil (Sua lógica solicitada)
        if perfil == "corredor_passagem":
            recs_data.append({
                "tipo": "cultura",
                "item": "Intervenções artísticas visuais (grafite, instalações)",
                "porque": "Baixo tempo de permanência exige impacto rápido"
            })
            # Adicionei uma extra comercial para complementar
            recs_data.append({
                "tipo": "comercio", 
                "item": "Café take-away / conveniência", 
                "porque": "Compatível com alto fluxo e pressa"
            })

        elif perfil == "zona_viva":
            recs_data.append({
                "tipo": "cultura",
                "item": "Shows de pequeno porte / feiras gastronômicas",
                "porque": "Há público disposto a permanecer e consumir"
            })
            recs_data.append({
                "tipo": "comercio",
                "item": "Bares e Restaurantes com mesas",
                "porque": "Espaço validado para aglomeração social"
            })

        elif perfil == "ponto_permanencia":
            recs_data.append({
                "tipo": "cultura",
                "item": "Exposições temporárias / oficinas abertas",
                "porque": "Permanência média favorece fruição moderada"
            })
            recs_data.append({
                "tipo": "servico",
                "item": "Coworking ou áreas de estudo",
                "porque": "Ambiente propício para foco e estadia"
            })

        elif perfil == "area_fria":
            recs_data.append({
                "tipo": "cultura",
                "item": "Eventos-âncora (cinema ao ar livre, festivais)",
                "porque": "Necessário criar motivo externo forte para atração"
            })
            recs_data.append({
                "tipo": "comercio",
                "item": "Lojas de destino específico",
                "porque": "Cliente vai até lá propositalmente, independe de fluxo de rua"
            })
        
        elif perfil == "congestionada":
             recs_data.append({
                "tipo": "urbano",
                "item": "Quiosques ordenados lineares",
                "porque": "Atende demanda comercial sem bloquear a passagem estreita"
            })

        else: # uso misto
             recs_data.append({
                "tipo": "geral",
                "item": "Mix flexível de comércio e serviço",
                "porque": "Perfil híbrido permite testar diferentes vocações"
            })

        # 2. Recomendações baseadas no Clima (Sua lógica solicitada)
        # Usamos .get para evitar erros se o campo não existir
        thermal_comfort = climate.get("thermal_comfort", "agradável")
        rain_condition = climate.get("rain_condition", "seco")

        if thermal_comfort == "quente" or thermal_comfort == "muito quente":
            recs_data.append({
                "tipo": "lazer",
                "item": "Atividades noturnas / Espaços sombreados",
                "porque": "Calor excessivo reduz uso diurno do espaço"
            })

        if rain_condition == "chuvoso":
            recs_data.append({
                "tipo": "lazer",
                "item": "Atividades indoor ou estruturadas com cobertura",
                "porque": "Chuva reduz drasticamente a permanência em áreas abertas"
            })

        # Conversão final para o Objeto Recommendation (Pydantic)
        return [Recommendation(**r) for r in recs_data]