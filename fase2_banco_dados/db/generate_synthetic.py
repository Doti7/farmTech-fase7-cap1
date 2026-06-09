import os
import sqlite3
from datetime import datetime, timedelta
import random

import numpy as np


DB_PATH = os.path.join("db", "farmtech.db")
SCHEMA_PATH = os.path.join("db", "schema.sql")
SEED_PATH = os.path.join("db", "seed_inicial.sql")


def exec_sql_file(conn, path):
    with open(path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def ensure_db():
    os.makedirs("db", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    # Cria schema
    exec_sql_file(conn, SCHEMA_PATH)

    # Garante o seed base (campo 1, sensores 1 e 2, etc)
    # Usamos INSERT OR IGNORE pra não duplicar se já existir.
    seed = open(SEED_PATH, "r", encoding="utf-8").read()
    seed = seed.replace("INSERT INTO", "INSERT OR IGNORE INTO")
    conn.executescript(seed)

    conn.commit()
    return conn


def generate(
    n_safras: int = 60,
    start_date: str = "2025-10-01",
    days_between_readings: int = 3,
    readings_per_safra: int = 12,
    campo_id: int = 1,
    sensor_umidade_id: int = 1,
    sensor_ph_id: int = 2,
    seed: int = 42,
):
    random.seed(seed)
    np.random.seed(seed)

    conn = ensure_db()
    cur = conn.cursor()

    # Descobre último id_safra e id_leitura/id_evento/id_resultado
    last_safra = cur.execute("SELECT COALESCE(MAX(id_safra), 0) FROM safra").fetchone()[0]
    last_leitura = cur.execute("SELECT COALESCE(MAX(id_leitura), 0) FROM leitura_sensor").fetchone()[0]
    last_evento = cur.execute("SELECT COALESCE(MAX(id_evento), 0) FROM evento_manejo").fetchone()[0]
    last_resultado = cur.execute("SELECT COALESCE(MAX(id_resultado), 0) FROM resultado_safra").fetchone()[0]

    base_dt = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(1, n_safras + 1):
        id_safra = last_safra + i

        cultura = random.choice(["Soja", "Milho", "Café"])
        area_ha = round(random.uniform(8.0, 20.0), 2)

        dt_inicio = base_dt + timedelta(days=15 * i)
        dt_fim = dt_inicio + timedelta(days=random.randint(90, 140))

        # SAFRA
        cur.execute(
            """
            INSERT OR IGNORE INTO safra (id_safra, id_campo, cultura, data_inicio, data_fim, area_ha)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (id_safra, campo_id, cultura, dt_inicio.date().isoformat(), dt_fim.date().isoformat(), area_ha),
        )

        # Leituras: umidade e pH ao longo da safra
        umidades = []
        phs = []

        for r in range(readings_per_safra):
            t = dt_inicio + timedelta(days=r * days_between_readings)

            # umidade tende a variar entre 15 e 45
            um = float(np.clip(np.random.normal(loc=28, scale=6), 12, 55))
            # pH tende a variar entre 5.2 e 6.8
            ph = float(np.clip(np.random.normal(loc=6.0, scale=0.35), 4.8, 7.5))

            umidades.append(um)
            phs.append(ph)

            last_leitura += 1
            cur.execute(
                """
                INSERT INTO leitura_sensor (id_leitura, id_sensor, timestamp_leitura, valor)
                VALUES (?, ?, ?, ?)
                """,
                (last_leitura, sensor_umidade_id, t.strftime("%Y-%m-%d %H:%M:%S"), um),
            )

            last_leitura += 1
            cur.execute(
                """
                INSERT INTO leitura_sensor (id_leitura, id_sensor, timestamp_leitura, valor)
                VALUES (?, ?, ?, ?)
                """,
                (last_leitura, sensor_ph_id, t.strftime("%Y-%m-%d %H:%M:%S"), ph),
            )

        # Manejo: irrigação + fertilização (1–3 eventos)
        n_irrig = random.randint(1, 3)
        total_irrig = 0.0
        for _ in range(n_irrig):
            last_evento += 1
            t = dt_inicio + timedelta(days=random.randint(1, 60))
            vol = float(np.clip(np.random.normal(loc=3200, scale=700), 1000, 6000))
            total_irrig += vol

            cur.execute(
                """
                INSERT INTO evento_manejo
                (id_evento, id_campo, id_safra, data_evento, tipo_evento, volume_litros, produto, dose_kg_ha, observacoes)
                VALUES (?, ?, ?, ?, 'irrigacao', ?, NULL, NULL, ?)
                """,
                (last_evento, campo_id, id_safra, t.strftime("%Y-%m-%d %H:%M:%S"), vol, "Irrigação registrada"),
            )

        n_fert = random.randint(1, 2)
        total_fert = 0.0
        for _ in range(n_fert):
            last_evento += 1
            t = dt_inicio + timedelta(days=random.randint(10, 80))
            dose = float(np.clip(np.random.normal(loc=140, scale=35), 50, 250))
            total_fert += dose

            cur.execute(
                """
                INSERT INTO evento_manejo
                (id_evento, id_campo, id_safra, data_evento, tipo_evento, volume_litros, produto, dose_kg_ha, observacoes)
                VALUES (?, ?, ?, ?, 'fertilizacao', NULL, ?, ?, ?)
                """,
                (last_evento, campo_id, id_safra, t.strftime("%Y-%m-%d %H:%M:%S"), "NPK", dose, "Fertilização registrada"),
            )

        # Produtividade: cria relação “aprendível” pro modelo
        media_um = float(np.mean(umidades))
        media_ph = float(np.mean(phs))

        # fórmula simples: melhora com umidade adequada, pH próximo de 6, irrig e fert moderados, + ruído
        produtividade = (
            2500
            + 35 * (media_um - 25)
            + 420 * (-(abs(media_ph - 6.0)))
            + 0.10 * total_irrig
            + 3.5 * total_fert
            + np.random.normal(0, 120)
        )

        produtividade = float(np.clip(produtividade, 1800, 6000))

        last_resultado += 1
        cur.execute(
            """
            INSERT INTO resultado_safra (id_resultado, id_safra, produtividade_kg_ha, data_colheita, observacoes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (last_resultado, id_safra, produtividade, (dt_fim + timedelta(days=3)).date().isoformat(), "Resultado sintético"),
        )

    conn.commit()
    conn.close()
    print(f"OK: Geradas {n_safras} safras sintéticas em {DB_PATH}")


if __name__ == "__main__":
    generate()