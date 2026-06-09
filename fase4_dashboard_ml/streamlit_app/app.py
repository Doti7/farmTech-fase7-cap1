"""
DASHBOARD STREAMLIT - FARMTECH FASE 4
Autor: Bernardo
Descrição:
    Este dashboard apresenta:
        - métricas do modelo treinado,
        - previsão de produtividade,
        - gráfico de correlação simples,
        - formulário para simular cenários agrícolas.

"""
import os
import sys

# Garante que a raiz do projeto esteja no PYTHONPATH quando o Streamlit roda
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

from backend_ml.preprocessamento import montar_dataset_final


# ---------------------------
# Carregar modelo treinado
# ---------------------------
MODELO_PATH = "backend_ml/modelos/modelo_regressao.pkl"
METRICAS_PATH = "backend_ml/modelos/metricas_regressao.txt"

modelo = None
metricas_texto = ""

if os.path.exists(MODELO_PATH):
    modelo = joblib.load(MODELO_PATH)

if os.path.exists(METRICAS_PATH):
    with open(METRICAS_PATH, "r") as f:
        metricas_texto = f.read()


# ---------------------------
# Dashboard
# ---------------------------
st.set_page_config(page_title="Assistente Agrícola Inteligente", layout="wide")

st.title("🌾 Assistente Agrícola Inteligente – FarmTech Solutions")
st.write("Dashboard interativo da Fase 4 – Previsão Inteligente na Agricultura.")


# ===========================
# SEÇÃO 1 – MÉTRICAS DO MODELO
# ===========================
st.header("📊 Métricas do Modelo de Regressão")

if metricas_texto:
    st.text(metricas_texto)
else:
    st.warning("Nenhuma métrica encontrada. Treine o modelo primeiro.")


# ===========================
# SEÇÃO 2 – GRÁFICO DE CORRELAÇÃO
# ===========================
st.header("📈 Correlação entre Variáveis Agrícolas")

df = montar_dataset_final()

if not df.empty:
    fig, ax = plt.subplots(figsize=(6, 4))
    corr = df.corr(numeric_only=True)
    ax.imshow(corr, cmap="Greens")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    st.pyplot(fig)
else:
    st.warning("Dataset vazio. Execute a ingestão e o treinamento.")


# ===========================
# SEÇÃO 3 – SIMULAÇÃO DE CENÁRIOS
# ===========================
st.header("🔮 Simulador de Produtividade Agrícola")

col1, col2 = st.columns(2)

with col1:
    umidade = st.number_input(
        "Média da Umidade do Solo (%)", min_value=0.0, max_value=100.0, value=25.0
    )
    ph = st.number_input(
        "Média do pH do Solo", min_value=0.0, max_value=14.0, value=6.0
    )

with col2:
    agua = st.number_input(
        "Total de Água Aplicada (litros)", min_value=0.0, value=3000.0
    )
    fertilizante = st.number_input(
        "Total de Fertilizante Aplicado (kg/ha)", min_value=0.0, value=150.0
    )


if st.button("Gerar Previsão"):
    if modelo is None:
        st.error("Modelo não encontrado. Treine o modelo primeiro.")
    else:
        entrada = pd.DataFrame(
            {
                "media_umidade_solo": [umidade],
                "media_ph_solo": [ph],
                "total_agua": [agua],
                "total_fertilizante": [fertilizante],
            }
        )
        pred = modelo.predict(entrada)[0]
        st.success(f"🌱 Produtividade Estimada: **{pred:.2f} kg/ha**")


st.markdown("---")
st.caption("Desenvolvido para a Fase 4 – FIAP • FarmTech Solutions")

