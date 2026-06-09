
"""
TREINAMENTO DE MODELO DE REGRESSÃO - FARMTECH FASE 4
Autor: Bernardo
Descrição:
    Este script treina um modelo simples de regressão
    para estimar a produtividade agrícola (kg/ha)
    com base em variáveis como:

        - média de umidade do solo (media_umidade_solo)
        - média de pH do solo (media_ph_solo)
        - total irrigado (litros)
        - total fertilizante aplicado (kg/ha)

    O objetivo é demonstrar a etapa de Machine Learning
    da Fase 4 da FarmTech Solutions.

    O modelo é salvo em:
        backend_ml/modelos/modelo_regressao.pkl
"""

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from .preprocessamento import montar_dataset_final

# Caminho onde o modelo será salvo
MODELO_PATH = "backend_ml/modelos/modelo_regressao.pkl"
METRICAS_PATH = "backend_ml/modelos/metricas_regressao.txt"


def treinar_modelo():
    """
    Executa todo o pipeline de:
        - montar dataset final
        - separar treino/teste
        - treinar modelo
        - calcular métricas
        - salvar modelo
    """

    print("\n[1] Carregando dataset consolidado...")
    df = montar_dataset_final()

    # Seleção das features
    features = [
        "media_umidade_solo",
        "media_ph_solo",
        "total_agua",
        "total_fertilizante",
    ]

    # A variável-alvo
    alvo = "produtividade_kg_ha"

    # Dataset filtrado
    X = df[features]
    y = df[alvo]

    print(f"[2] Dataset possui {len(df)} linhas.")

    # Separar treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    print("[3] Treinando modelo de Regressão Linear...")
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # Previsões
    y_pred = modelo.predict(X_test)

    # Métricas
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    print("\n[4] Métricas do modelo:")
    print(f"   - MAE  = {mae:.4f}")
    print(f"   - MSE  = {mse:.4f}")
    print(f"   - RMSE = {rmse:.4f}")
    print(f"   - R²   = {r2:.4f}")

    # Garantir que a pasta existe
    os.makedirs("backend_ml/modelos", exist_ok=True)

    # Salvar o modelo treinado
    joblib.dump(modelo, MODELO_PATH)

    # Salvar métricas em arquivo
    with open(METRICAS_PATH, "w") as f:
        f.write("MÉTRICAS DO MODELO DE REGRESSÃO - FARMTECH FASE 4\n\n")
        f.write(f"MAE  = {mae:.4f}\n")
        f.write(f"MSE  = {mse:.4f}\n")
        f.write(f"RMSE = {rmse:.4f}\n")
        f.write(f"R²   = {r2:.4f}\n")

    print(f"\n[5] Modelo salvo em: {MODELO_PATH}")
    print(f"[6] Métricas salvas em: {METRICAS_PATH}")

    return modelo


if __name__ == "__main__":
    treinar_modelo()
