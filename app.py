import os
import sys
import random
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent

FASE4_DIR = BASE_DIR / "fase4_dashboard_ml"
FASE4_BACKEND = FASE4_DIR / "backend_ml"

if str(FASE4_DIR) not in sys.path:
    sys.path.insert(0, str(FASE4_DIR))


st.set_page_config(
    page_title="FarmTech Fase 7",
    layout="wide",
)

st.title("FarmTech Solutions - Fase 7")
st.write(
    "Dashboard final de consolidação das Fases 1 a 6, integrando cálculo agrícola, "
    "banco de dados, IoT, machine learning, AWS e visão computacional."
)


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Visão Geral",
        "Fases 1 e 2",
        "Fase 3 - IoT",
        "Fase 4 - ML",
        "Fase 5 - AWS",
        "Fase 6 - Visão Computacional",
    ]
)


with tab1:
    st.header("Visão Geral do Sistema")

    st.markdown(
        """
        A Fase 7 consolida os serviços desenvolvidos nas fases anteriores em uma única aplicação.

        **Fases integradas:**

        - **Fase 1:** cálculo de área de plantio e manejo de insumos.
        - **Fase 2:** banco de dados estruturado para dados agrícolas.
        - **Fase 3:** sensores IoT e automação de irrigação.
        - **Fase 4:** dashboard, machine learning e previsão de produtividade.
        - **Fase 5:** serviço de alerta em AWS SNS.
        - **Fase 6:** visão computacional com YOLO/CNN.
        """
    )

    st.info("Esta dashboard funciona como central única de gestão agrícola da FarmTech.")


with tab2:
    st.header("Fases 1 e 2 - Área, Insumos e Banco de Dados")

    st.subheader("Cálculo de área e insumos")

    cultura = st.selectbox("Cultura", ["Café", "Milho", "Soja"])
    largura = st.number_input("Largura da área (m)", min_value=1.0, value=100.0)
    comprimento = st.number_input("Comprimento da área (m)", min_value=1.0, value=200.0)
    dose_insumo = st.number_input("Dose de insumo (kg por hectare)", min_value=0.0, value=120.0)

    area_m2 = largura * comprimento
    area_ha = area_m2 / 10000
    insumo_total = area_ha * dose_insumo

    col1, col2, col3 = st.columns(3)
    col1.metric("Área total", f"{area_m2:,.2f} m²")
    col2.metric("Área em hectares", f"{area_ha:.2f} ha")
    col3.metric("Insumo estimado", f"{insumo_total:.2f} kg")

    st.subheader("Banco de dados da Fase 4 importado")
    db_path = BASE_DIR / "fase2_banco_dados" / "db" / "farmtech.db"

    if db_path.exists():
        st.success(f"Banco encontrado: {db_path}")
    else:
        st.warning("Banco SQLite ainda não encontrado.")


with tab3:
    st.header("Fase 3 - IoT e Sensores")

    st.write("Simulação de leitura de sensores agrícolas baseada nas fases anteriores.")

    if st.button("Simular leitura de sensores"):
        umidade = random.uniform(10, 80)
        ph = random.uniform(4.5, 8.0)
        nitrogenio = random.choice([0, 1])
        fosforo = random.choice([0, 1])
        potassio = random.choice([0, 1])

        bomba_ligada = umidade < 30 or ph < 5.5 or ph > 7.0

        col1, col2, col3 = st.columns(3)
        col1.metric("Umidade", f"{umidade:.1f}%")
        col2.metric("pH", f"{ph:.2f}")
        col3.metric("Bomba", "Ligada" if bomba_ligada else "Desligada")

        st.write(
            {
                "nitrogenio": nitrogenio,
                "fosforo": fosforo,
                "potassio": potassio,
            }
        )

        if bomba_ligada:
            st.warning("Ação recomendada: verificar irrigação e condições do solo.")
        else:
            st.success("Condições dentro da faixa operacional.")

    dados_csv = BASE_DIR / "fase3_iot_sensores" / "dados.csv"
    if dados_csv.exists():
        st.subheader("Dados históricos da Fase 3")
        df_sensores = pd.read_csv(dados_csv)
        st.dataframe(df_sensores.head(20))
    else:
        st.info("Arquivo dados.csv da Fase 3 não encontrado.")


with tab4:
    st.header("Fase 4 - Machine Learning e Produtividade")

    modelo_path = BASE_DIR / "fase4_dashboard_ml" / "backend_ml" / "modelos" / "modelo_regressao.pkl"
    metricas_path = BASE_DIR / "fase4_dashboard_ml" / "backend_ml" / "modelos" / "metricas_regressao.txt"

    if metricas_path.exists():
        st.subheader("Métricas do modelo")
        st.text(metricas_path.read_text(encoding="utf-8", errors="ignore"))
    else:
        st.warning("Arquivo de métricas não encontrado.")

    st.subheader("Simulador de produtividade")

    umidade_ml = st.number_input("Média da umidade do solo (%)", min_value=0.0, max_value=100.0, value=25.0)
    ph_ml = st.number_input("Média do pH do solo", min_value=0.0, max_value=14.0, value=6.0)
    agua_ml = st.number_input("Total de água aplicada (litros)", min_value=0.0, value=3000.0)
    fertilizante_ml = st.number_input("Total de fertilizante aplicado (kg/ha)", min_value=0.0, value=150.0)

    if st.button("Gerar previsão de produtividade"):
        try:
            import joblib

            modelo = joblib.load(modelo_path)
            entrada = pd.DataFrame(
                {
                    "media_umidade_solo": [umidade_ml],
                    "media_ph_solo": [ph_ml],
                    "total_agua": [agua_ml],
                    "total_fertilizante": [fertilizante_ml],
                }
            )
            pred = modelo.predict(entrada)[0]
            st.success(f"Produtividade estimada: {pred:.2f} kg/ha")

        except Exception as erro:
            st.warning("Não foi possível carregar o modelo original. Exibindo estimativa demonstrativa.")
            estimativa = (umidade_ml * 40) + (ph_ml * 200) + (agua_ml * 0.05) + (fertilizante_ml * 4)
            st.success(f"Produtividade estimada demonstrativa: {estimativa:.2f} kg/ha")
            st.caption(f"Detalhe técnico: {erro}")


with tab5:
    st.header("Fase 5 - AWS e Serviço de Alertas")

    st.write(
        "A integração prevista para a Fase 5 utiliza Amazon SNS para envio de alertas por e-mail "
        "quando sensores ou análises indicam condição crítica."
    )

    umidade_alerta = st.number_input("Umidade para alerta (%)", min_value=0.0, max_value=100.0, value=18.0)
    ph_alerta = st.number_input("pH para alerta", min_value=0.0, max_value=14.0, value=5.2)

    alertas = []

    if umidade_alerta < 30:
        alertas.append("Umidade baixa: verificar irrigação.")

    if ph_alerta < 5.5 or ph_alerta > 7.0:
        alertas.append("pH fora da faixa ideal: verificar correção do solo.")

    if alertas:
        st.warning("Alertas identificados:")
        for alerta in alertas:
            st.write(f"- {alerta}")
    else:
        st.success("Nenhum alerta crítico identificado.")

    st.info("Na próxima etapa vamos criar o módulo real de envio via AWS SNS.")


with tab6:
    st.header("Fase 6 - Visão Computacional")

    st.write(
        "A Fase 6 foi integrada por meio do notebook original e dos resultados gerados "
        "com YOLO/CNN para classificação e detecção visual."
    )

    img1 = BASE_DIR / "docs" / "fase6_assets" / "detections_test.png"
    img2 = BASE_DIR / "docs" / "fase6_assets" / "cnn_predictions.png"

    if img1.exists():
        st.subheader("Resultado YOLO")
        st.image(str(img1), use_container_width=True)

    if img2.exists():
        st.subheader("Predições CNN")
        st.image(str(img2), use_container_width=True)

    notebook_path = BASE_DIR / "fase6_visao_computacional" / "GrupoMultiAgents_pbl_fase6_ok.ipynb"

    if notebook_path.exists():
        st.success("Notebook original da Fase 6 encontrado e integrado ao repositório.")
    else:
        st.warning("Notebook da Fase 6 não encontrado.")