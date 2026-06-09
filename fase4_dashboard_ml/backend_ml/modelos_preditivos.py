"""
MODELOS PREDITIVOS - PARTE 2 (FarmTech Fase 4)
Autor: Bernardo

Descrição:
    Este módulo treina e compara três modelos de regressão:

        1. Regressão Linear
        2. Regressão Ridge
        3. Random Forest Regressor

    Todos têm o mesmo objetivo:
        → prever a produtividade agrícola (kg/ha)

    A partir das variáveis:
        - média de umidade do solo (media_umidade_solo)
        - média de pH do solo (media_ph_solo)
        - total de água aplicada (total_agua)
        - total de fertilizante aplicado (total_fertilizante)

    O script calcula:
        - MAE
        - MSE
        - RMSE
        - R²

    E salva:
        - os três modelos treinados
        - um arquivo de texto com o resumo das métricas
"""

import os
from math import sqrt

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from backend_ml.preprocessamento import montar_dataset_final

# Caminhos para salvar resultados
PASTA_MODELOS = "backend_ml/modelos"
RESULTADOS_PATH = os.path.join(PASTA_MODELOS, "resultados_parte2.txt")


def avaliar_modelo(modelo, X_test, y_test):
    """
    Recebe um modelo treinado, dados de teste e retorna as métricas:
        - MAE
        - MSE
        - RMSE
        - R²
    """
    previsoes = modelo.predict(X_test)

    mae = mean_absolute_error(y_test, previsoes)
    mse = mean_squared_error(y_test, previsoes)
    rmse = sqrt(mse)
    r2 = r2_score(y_test, previsoes)

    return mae, mse, rmse, r2


def treinar_modelos_preditivos():
    """
    Executa o fluxo completo da PARTE 2:

        1. Monta o dataset final (via montar_dataset_final)
        2. Separa treino e teste
        3. Treina:
            - LinearRegression
            - Ridge
            - RandomForestRegressor
        4. Calcula métricas
        5. Salva modelos e um arquivo texto com o resumo das métricas

    Retorna um dicionário com as métricas de cada modelo.
    """

    # Garante que a pasta existe
    os.makedirs(PASTA_MODELOS, exist_ok=True)

    # 1. Montar dataset
    print("[1] Carregando dataset consolidado para a Parte 2...")
    df = montar_dataset_final()

    colunas_features = [
        "media_umidade_solo",
        "media_ph_solo",
        "total_agua",
        "total_fertilizante",
    ]
    coluna_alvo = "produtividade_kg_ha"

    X = df[colunas_features]
    y = df[coluna_alvo]

    # 2. Separar treino e teste
    print("[2] Separando dados em treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    resultados = {}

    # 3.1 Regressão Linear
    print("[3] Treinando Regressão Linear...")
    modelo_lr = LinearRegression()
    modelo_lr.fit(X_train, y_train)
    lr_mae, lr_mse, lr_rmse, lr_r2 = avaliar_modelo(modelo_lr, X_test, y_test)
    resultados["Regressao Linear"] = (lr_mae, lr_mse, lr_rmse, lr_r2)

    # 3.2 Regressão Ridge
    print("[4] Treinando Regressão Ridge...")
    modelo_ridge = Ridge(alpha=1.0)
    modelo_ridge.fit(X_train, y_train)
    rd_mae, rd_mse, rd_rmse, rd_r2 = avaliar_modelo(modelo_ridge, X_test, y_test)
    resultados["Regressao Ridge"] = (rd_mae, rd_mse, rd_rmse, rd_r2)

    # 3.3 Random Forest
    print("[5] Treinando Random Forest Regressor...")
    modelo_rf = RandomForestRegressor(
        n_estimators=300,
        max_depth=6,
        random_state=42,
    )
    modelo_rf.fit(X_train, y_train)
    rf_mae, rf_mse, rf_rmse, rf_r2 = avaliar_modelo(modelo_rf, X_test, y_test)
    resultados["Random Forest"] = (rf_mae, rf_mse, rf_rmse, rf_r2)

    # 4. Salvar modelos
    print("[6] Salvando modelos treinados...")
    joblib.dump(modelo_lr, os.path.join(PASTA_MODELOS, "modelo_lr.pkl"))
    joblib.dump(modelo_ridge, os.path.join(PASTA_MODELOS, "modelo_ridge.pkl"))
    joblib.dump(modelo_rf, os.path.join(PASTA_MODELOS, "modelo_rf.pkl"))

    # 5. Salvar métricas em arquivo texto
    print("[7] Salvando métricas em arquivo de resultados...")
    with open(RESULTADOS_PATH, "w") as f:
        f.write("RESULTADOS - MODELOS PREDITIVOS (PARTE 2)\n\n")

        f.write("1) Regressão Linear\n")
        f.write(f"   MAE  = {lr_mae:.4f}\n")
        f.write(f"   MSE  = {lr_mse:.4f}\n")
        f.write(f"   RMSE = {lr_rmse:.4f}\n")
        f.write(f"   R²   = {lr_r2:.4f}\n\n")

        f.write("2) Regressão Ridge\n")
        f.write(f"   MAE  = {rd_mae:.4f}\n")
        f.write(f"   MSE  = {rd_mse:.4f}\n")
        f.write(f"   RMSE = {rd_rmse:.4f}\n")
        f.write(f"   R²   = {rd_r2:.4f}\n\n")

        f.write("3) Random Forest\n")
        f.write(f"   MAE  = {rf_mae:.4f}\n")
        f.write(f"   MSE  = {rf_mse:.4f}\n")
        f.write(f"   RMSE = {rf_rmse:.4f}\n")
        f.write(f"   R²   = {rf_r2:.4f}\n\n")

    print("\n[8] Treinamento concluído. Métricas registradas em:")
    print(f"   {RESULTADOS_PATH}\n")

    return resultados


if __name__ == "__main__":
    treinar_modelos_preditivos()
