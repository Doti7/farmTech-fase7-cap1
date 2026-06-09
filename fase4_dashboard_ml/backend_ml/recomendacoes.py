"""
RECOMENDAÇÕES AGRÍCOLAS - PARTE 2 (FarmTech Fase 4)
Autor: Bernardo

Descrição:
    Este módulo recebe:
        - variáveis de manejo (umidade, pH, água, fertilizante)
        - produtividade prevista (kg/ha)

    E gera recomendações textuais de:
        - irrigação
        - fertilização
        - correção de solo (pH)
        - alerta geral de produtividade

    A ideia é mostrar como os modelos preditivos podem
    apoiar a tomada de decisão no campo.
"""

from typing import Dict


def gerar_recomendacoes(
    umidade: float,
    ph: float,
    agua_litros: float,
    fertilizante_kg_ha: float,
    produtividade_prevista: float,
) -> Dict[str, str]:
    """
    Gera recomendações simples baseadas em regras.

    Parâmetros:
        umidade: média da umidade do solo em %
        ph: média do pH do solo
        agua_litros: volume total de água aplicada
        fertilizante_kg_ha: dose total de fertilizante
        produtividade_prevista: produtividade estimada (kg/ha)

    Retorno:
        dicionário com recomendações textuais.
    """

    recomendacoes = {}

    # -----------------------
    # 1. Recomendações de umidade / irrigação
    # -----------------------
    if umidade < 20:
        recomendacoes["irrigacao"] = (
            "A umidade do solo está baixa. "
            "Considere aumentar o volume de irrigação ou reduzir o intervalo entre irrigações."
        )
    elif 20 <= umidade <= 35:
        recomendacoes["irrigacao"] = (
            "A umidade do solo está em uma faixa adequada. "
            "Mantenha o manejo atual de irrigação, monitorando variações climáticas."
        )
    else:
        recomendacoes["irrigacao"] = (
            "A umidade do solo está elevada. "
            "Avalie reduzir a irrigação para evitar encharcamento e problemas de raiz."
        )

    # -----------------------
    # 2. Recomendações de pH / correção de solo
    # -----------------------
    if ph < 5.5:
        recomendacoes["ph"] = (
            "O pH está ácido. "
            "Considere a aplicação de corretivos (como calcário) para elevar o pH e melhorar a disponibilidade de nutrientes."
        )
    elif 5.5 <= ph <= 6.5:
        recomendacoes["ph"] = (
            "O pH está em faixa considerada ideal para a maioria das culturas. "
            "Mantenha o monitoramento periódico."
        )
    else:
        recomendacoes["ph"] = (
            "O pH está acima do ideal. "
            "Avalie o histórico de correções e fertilizações nitrogenadas para evitar desequilíbrios."
        )

    # -----------------------
    # 3. Recomendações de fertilização
    # -----------------------
    if fertilizante_kg_ha < 100:
        recomendacoes["fertilizacao"] = (
            "A dose de fertilizante aplicada está relativamente baixa. "
            "Se a análise de solo indicar deficiência, considere aumentar a adubação, principalmente em estágios críticos da cultura."
        )
    elif 100 <= fertilizante_kg_ha <= 200:
        recomendacoes["fertilizacao"] = (
            "A dose de fertilizante está em uma faixa intermediária. "
            "Ajustes finos podem ser feitos com base em análises de folha e solo."
        )
    else:
        recomendacoes["fertilizacao"] = (
            "A dose de fertilizante está elevada. "
            "Verifique se há risco de desperdício ou impacto ambiental e considere distribuir melhor ao longo do ciclo."
        )

    # -----------------------
    # 4. Alerta geral baseado na produtividade prevista
    # -----------------------
    if produtividade_prevista < 2500:
        recomendacoes["produtividade"] = (
            f"A produtividade estimada é de aproximadamente {produtividade_prevista:.0f} kg/ha, "
            "abaixo do patamar desejado. "
            "Recomenda-se revisar manejo de irrigação, fertilização e possíveis fatores de estresse."
        )
    elif 2500 <= produtividade_prevista <= 4000:
        recomendacoes["produtividade"] = (
            f"A produtividade estimada é de aproximadamente {produtividade_prevista:.0f} kg/ha, "
            "dentro de uma faixa considerada aceitável para a cultura. "
            "Pequenos ajustes de manejo podem melhorar ainda mais o resultado."
        )
    else:
        recomendacoes["produtividade"] = (
            f"A produtividade estimada é de aproximadamente {produtividade_prevista:.0f} kg/ha, "
            "indicando um bom desempenho produtivo. "
            "Mantenha as boas práticas adotadas e continue monitorando as condições do solo e da cultura."
        )

    return recomendacoes


if __name__ == "__main__":
    # Exemplo rápido de uso
    rec = gerar_recomendacoes(
        umidade=24.0,
        ph=6.0,
        agua_litros=3200.0,
        fertilizante_kg_ha=150.0,
        produtividade_prevista=3600.0,
    )

    print("\nRECOMENDAÇÕES GERADAS:\n")
    for tema, texto in rec.items():
        print(f"- {tema.upper()}: {texto}\n")
