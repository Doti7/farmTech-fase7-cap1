-- ==========================================
-- SCHEMA DO BANCO DE DADOS - FARMTECH FASE 4
-- ==========================================

-- Tabela de campos / talhões
CREATE TABLE campo (
    id_campo        INTEGER PRIMARY KEY,
    nome_campo      VARCHAR(100) NOT NULL,
    localizacao     VARCHAR(255),
    area_ha         DECIMAL(10,2)
);

-- Tabela de safras/ciclos produtivos
CREATE TABLE safra (
    id_safra        INTEGER PRIMARY KEY,
    id_campo        INTEGER NOT NULL,
    cultura         VARCHAR(100) NOT NULL,  -- ex: Soja, Milho
    data_inicio     DATE NOT NULL,
    data_fim        DATE,
    area_ha         DECIMAL(10,2),
    FOREIGN KEY (id_campo) REFERENCES campo(id_campo)
);

-- Tabela de sensores instalados no campo
CREATE TABLE sensor (
    id_sensor       INTEGER PRIMARY KEY,
    id_campo        INTEGER NOT NULL,
    tipo            VARCHAR(50) NOT NULL,   -- 'umidade_solo', 'ph_solo', 'temperatura_ar', etc.
    unidade_medida  VARCHAR(20),            -- '%', 'pH', '°C', etc.
    profundidade_cm INTEGER,                -- profundidade do sensor de solo, se aplicável
    descricao       VARCHAR(255),
    FOREIGN KEY (id_campo) REFERENCES campo(id_campo)
);

-- Leituras dos sensores (série temporal)
CREATE TABLE leitura_sensor (
    id_leitura         INTEGER PRIMARY KEY,
    id_sensor          INTEGER NOT NULL,
    timestamp_leitura  DATETIME NOT NULL,
    valor              DECIMAL(10,3) NOT NULL,
    FOREIGN KEY (id_sensor) REFERENCES sensor(id_sensor)
);

-- Eventos de manejo: irrigação, fertilização, etc.
CREATE TABLE evento_manejo (
    id_evento       INTEGER PRIMARY KEY,
    id_campo        INTEGER NOT NULL,
    id_safra        INTEGER,
    data_evento     DATETIME NOT NULL,
    tipo_evento     VARCHAR(50) NOT NULL,  -- 'irrigacao', 'fertilizacao'
    volume_litros   DECIMAL(10,2),         -- se for irrigação
    produto         VARCHAR(100),          -- fertilizante utilizado
    dose_kg_ha      DECIMAL(10,2),         -- dose aplicada
    observacoes     VARCHAR(255),
    FOREIGN KEY (id_campo) REFERENCES campo(id_campo),
    FOREIGN KEY (id_safra) REFERENCES safra(id_safra)
);

-- Resultado final da safra
CREATE TABLE resultado_safra (
    id_resultado        INTEGER PRIMARY KEY,
    id_safra            INTEGER NOT NULL,
    produtividade_kg_ha DECIMAL(10,2) NOT NULL,
    data_colheita       DATE NOT NULL,
    observacoes         VARCHAR(255),
    FOREIGN KEY (id_safra) REFERENCES safra(id_safra)
);

