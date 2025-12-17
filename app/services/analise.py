def _analyze(self, metrics):
    profile = self._place_profile(metrics)
    recs = self._recommend(profile, metrics)
    return {"perfil": profile, "recomendacoes": recs}

def _place_profile(self, m):
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

def _recommend(self, profile, m):
    # você pode retornar objetos (melhor pra JSON)
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
