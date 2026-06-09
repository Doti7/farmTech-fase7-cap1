from datetime import datetime


def avaliar_alertas(umidade, ph, produtividade=None, visao_anomalia=False):
    alertas = []

    if umidade < 30:
        alertas.append("Umidade baixa detectada. Verificar irrigação e bomba.")

    if ph < 5.5 or ph > 7.0:
        alertas.append("pH fora da faixa ideal. Verificar correção do solo.")

    if produtividade is not None and produtividade < 2500:
        alertas.append("Produtividade prevista abaixo do esperado. Revisar manejo agrícola.")

    if visao_anomalia:
        alertas.append("Anomalia visual detectada. Realizar inspeção na plantação.")

    return alertas


def gerar_mensagem_alerta(alertas):
    if not alertas:
        return "Nenhum alerta crítico identificado."

    linhas = [
        "ALERTA FARMTECH - FASE 7",
        f"Data/hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "",
        "Condições críticas identificadas:",
        "",
    ]

    for alerta in alertas:
        linhas.append(f"- {alerta}")

    linhas.extend(
        [
            "",
            "Ações recomendadas:",
            "- Verificar sensores da área monitorada.",
            "- Registrar ação corretiva no sistema.",
            "- Acionar responsável técnico se o problema persistir.",
        ]
    )

    return "\n".join(linhas)


def simular_envio_sns(mensagem):
    """
    Simula o envio de alerta via Amazon SNS.

    Na arquitetura real, esta função seria substituída por boto3.client('sns').publish().
    """
    return {
        "status": "simulado",
        "servico": "Amazon SNS",
        "destino": "e-mail dos funcionários da fazenda",
        "mensagem": mensagem,
    }