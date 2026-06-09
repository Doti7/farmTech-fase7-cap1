"""
VISUALIZAÇÕES PREDITIVAS - PARTE 2 (FarmTech Fase 4)
Autor: Bernardo

Descrição:
    Este módulo gera visualizações essenciais para análise preditiva:
        - gráfico de dispersão entre variáveis agrícolas e produtividade,
        - gráfico de resíduos dos modelos de regressão,
        - gráfico comparando valores reais vs previstos.

    As imagens geradas podem ser usadas:
        - no relatório,
        - na apresentação,
        - no dashboard (se desejado).
"""

import os
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from backend_ml.preprocessamento import montar_dataset_final

PASTA_SAIDA = "assets/prints_dashboard"


def gerar_graficos():
    """Gera visualizações e salva em PNG."""

    os.makedirs(PASTA_SAIDA, exist_ok=True)

    df = montar_dataset_final()

    # Seleção das variáveis
    features = [
        "media_umidade_solo",
        "media_ph_solo",
        "total_agua",
        "total_fertilizante",
    ]

    alvo = "produtividade_kg_ha"

    X = df[features]
    y = df[alvo]

    # Modelo simples para previsões (para os gráficos)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    # -----------------------------------------------------
    # 1. Dispersão das variáveis individuais vs produtividade
    # -----------------------------------------------------
    for coluna in features:
        plt.figure(figsize=(6, 4))
        plt.scatter(df[coluna], df[alvo], color="green", alpha=0.7)
        plt.xlabel(coluna)
        plt.ylabel("Produtividade (kg/ha)")
        plt.title(f"Relação entre {coluna} e produtividade")

        caminho = os.path.join(PASTA_SAIDA, f"scatter_{coluna}.png")
        plt.savefig(caminho, dpi=150, bbox_inches="tight")
        plt.close()

    # -----------------------------------------------------
    # 2. Gráfico de resíduos
    # -----------------------------------------------------
    residuos = y_test - y_pred

    plt.figure(figsize=(6, 4))
    plt.scatter(y_pred, residuos, color="purple", alpha=0.6)
    plt.axhline(0, color="black", linewidth=1)
    plt.xlabel("Produtividade prevista (kg/ha)")
    plt.ylabel("Resíduo")
    plt.title("Gráfico de Resíduos")

    caminho = os.path.join(PASTA_SAIDA, "grafico_residuos.png")
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()

    # -----------------------------------------------------
    # 3. Valores reais vs previstos
    # -----------------------------------------------------
    plt.figure(figsize=(6, 4))
    plt.scatter(y_test, y_pred, alpha=0.7, color="blue")
    plt.xlabel("Produtividade Real (kg/ha)")
    plt.ylabel("Produtividade Prevista (kg/ha)")
    plt.title("Real vs Previsto")

    caminho = os.path.join(PASTA_SAIDA, "real_vs_previsto.png")
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()

    print("Gráficos gerados com sucesso em:", PASTA_SAIDA)


if __name__ == "__main__":
    gerar_graficos()
