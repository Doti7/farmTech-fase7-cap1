"""
PREPROCESSAMENTO DE DADOS AGRÍCOLAS - FARMTECH FASE 4
Autor: Bernardo
Descrição:
    Esse módulo centraliza todo o pré-processamento necessário
    para preparar os dados que serão usados nos modelos de regressão.

    Ele unifica:
        - leituras de sensores
        - eventos de manejo (irrigação, fertilização)
        - produtividade final da safra

    O objetivo é transformar os dados brutos do banco
    em um DataFrame organizado e pronto para treinar modelos de ML.
"""

import sqlite3
import pandas as pd
import numpy as np


# Caminho do banco SQLite
DB_PATH = "db/farmtech.db"


def carregar_dados_brutos():
    """
    Lê as tabelas principais do banco de dados
    e retorna DataFrames separados.
    """

    conn = sqlite3.connect(DB_PATH)

    df_campo = pd.read_sql_query("SELECT * FROM campo", conn)
    df_safra = pd.read_sql_query("SELECT * FROM safra", conn)
    df_sensor = pd.read_sql_query("SELECT * FROM sensor", conn)
    df_leituras = pd.read_sql_query("SELECT * FROM leitura_sensor", conn)
    df_manejo = pd.read_sql_query("SELECT * FROM evento_manejo", conn)
    df_resultado = pd.read_sql_query("SELECT * FROM resultado_safra", conn)

    conn.close()

    return {
        "campo": df_campo,
        "safra": df_safra,
        "sensor": df_sensor,
        "leituras": df_leituras,
        "manejo": df_manejo,
        "resultado": df_resultado,
    }


def processar_leituras(df_sensor, df_leituras):
    """
    Consolida as leituras dos sensores em uma forma mais útil.

    Para cada safra, calculamos:
        - média de umidade
        - média de pH
    """

    df = df_leituras.merge(df_sensor, on="id_sensor", how="left")

    # Média de cada sensor por safra
    df_agg = (
        df.groupby(["id_campo", "tipo"])
        .agg(media_valor=("valor", "mean"))
        .reset_index()
    )

    # Separar em colunas
    tabela_final = {}

    for tipo_sensor in df_agg["tipo"].unique():
        tabela_final[tipo_sensor] = df_agg[df_agg["tipo"] == tipo_sensor][
            ["id_campo", "media_valor"]
        ].rename(columns={"media_valor": f"media_{tipo_sensor}"})

    # Mesclar sensores em uma tabela única
    df_final = None
    for tabela in tabela_final.values():
        if df_final is None:
            df_final = tabela
        else:
            df_final = df_final.merge(tabela, on="id_campo", how="left")

    return df_final


def processar_manejo(df_manejo):
    """
    Consolida eventos de manejo por safra:
        - litros totais de irrigação
        - kg/ha totais de fertilização
    """

    df_agg = df_manejo.groupby("id_safra").agg(
        total_agua=("volume_litros", "sum"),
        total_fertilizante=("dose_kg_ha", "sum"),
    )

    return df_agg.reset_index()


def montar_dataset_final():
    """
    Monta o dataset final unificado usado para treinar modelos.

    Retorna:
        DataFrame pronto para ML contendo:
        - média de umidade do solo
        - média de pH
        - total irrigado
        - total fertilizante
        - produtividade final
    """

    dados = carregar_dados_brutos()

    df_safra = dados["safra"]
    df_resultado = dados["resultado"]

    df_sensores = processar_leituras(
        dados["sensor"], dados["leituras"]
    )

    df_manejo = processar_manejo(dados["manejo"])

    # Merge geral
    df = (
        df_safra.merge(df_sensores, on="id_campo", how="left")
        .merge(df_manejo, on="id_safra", how="left")
        .merge(df_resultado, on="id_safra", how="left")
    )

    # Tratamento simples de valores nulos
    df = df.fillna(0)

    return df


if __name__ == "__main__":
    # Gerar and visualizar o dataset consolidado
    df = montar_dataset_final()
    print("\n===== DATASET FINAL PARA MACHINE LEARNING =====\n")
    print(df.head())

