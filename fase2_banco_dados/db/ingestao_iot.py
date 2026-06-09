import sqlite3
from datetime import datetime, timedelta
import random

# Caminho do banco de dados SQLite
DB_PATH = "db/farmtech.db"


def criar_conexao():
    """
    Cria e retorna uma conexão com o banco de dados SQLite.
    Se o arquivo farmtech.db não existir, ele será criado automaticamente.
    """
    return sqlite3.connect(DB_PATH)


def inserir_leitura_sensor(conn, id_sensor, timestamp, valor):
    """
    Insere uma leitura na tabela leitura_sensor.
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO leitura_sensor (id_sensor, timestamp_leitura, valor)
        VALUES (?, ?, ?)
        """,
        (id_sensor, timestamp, valor),
    )
    conn.commit()


def popular_leituras_simuladas():
    """
    Simula leituras de dois sensores (umidade do solo e pH do solo)
    ao longo de vários dias e insere esses dados na tabela leitura_sensor.

    Premissas:
    - id_sensor = 1 -> umidade do solo (%)
    - id_sensor = 2 -> pH do solo
    - Leituras a cada 4 horas, durante 7 dias.
    """

    conn = criar_conexao()

    # Data/hora inicial das simulações
    inicio = datetime(2025, 10, 1, 8, 0, 0)

    # Simular 7 dias de leituras a cada 4 horas
    for dia in range(7):
        for hora in [8, 12, 16, 20]:
            ts = inicio + timedelta(days=dia, hours=hora - 8)

            # Simulação de umidade do solo (id_sensor = 1)
            # Valores entre 18% e 35%
            valor_umidade = random.uniform(18.0, 35.0)
            inserir_leitura_sensor(
                conn,
                id_sensor=1,
                timestamp=ts.strftime("%Y-%m-%d %H:%M:%S"),
                valor=round(valor_umidade, 2),
            )

            # Simulação de pH do solo (id_sensor = 2)
            # Valores entre 5.5 e 6.5
            valor_ph = random.uniform(5.5, 6.5)
            inserir_leitura_sensor(
                conn,
                id_sensor=2,
                timestamp=ts.strftime("%Y-%m-%d %H:%M:%S"),
                valor=round(valor_ph, 2),
            )

    conn.close()
    print("Leituras simuladas inseridas com sucesso!")


if __name__ == "__main__":
    popular_leituras_simuladas()

