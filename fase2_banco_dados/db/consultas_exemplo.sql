-- ======================================================================
-- CONSULTAS DE APOIO - FARMTECH FASE 4
-- Descrição:
--   Este arquivo tem algumas consultas SQL usadas na fase 4 do projeto
--   FarmTech Solutions
-- ======================================================================


-- ----------------------------------------------------------------------
-- 1) VERIFICAÇÃO DA ESTRUTURA DO BANCO
--    (útil para mostrar que as tabelas foram criadas corretamente)
-- ----------------------------------------------------------------------

-- Listar as tabelas existentes no banco (SQLite)
SELECT
    name        AS nome_tabela,
    type        AS tipo_estrutura
FROM
    sqlite_master
WHERE
    type IN ('table', 'view')
ORDER BY
    name;


-- ----------------------------------------------------------------------
-- 2) DADOS CADASTRAIS BÁSICOS
--    (campos, safras, sensores)
-- ----------------------------------------------------------------------

-- 2.1) Listar campos/talhões cadastrados
SELECT
    id_campo,
    nome_campo,
    localizacao,
    area_ha
FROM
    campo
ORDER BY
    id_campo;


-- 2.2) Listar safras por campo
SELECT
    s.id_safra,
    c.nome_campo,
    s.cultura,
    s.data_inicio,
    s.data_fim,
    s.area_ha
FROM
    safra s
    JOIN campo c ON s.id_campo = c.id_campo
ORDER BY
    s.id_safra;


-- 2.3) Sensores instalados em cada campo
SELECT
    se.id_sensor,
    c.nome_campo,
    se.tipo,
    se.unidade_medida,
    se.profundidade_cm,
    se.descricao
FROM
    sensor se
    JOIN campo c ON se.id_campo = c.id_campo
ORDER BY
    se.id_sensor;


-- ----------------------------------------------------------------------
-- 3) LEITURAS DOS SENSORES (SÉRIE TEMPORAL)
-- ----------------------------------------------------------------------

-- 3.1) Leituras mais recentes (independente do sensor)
SELECT
    s.tipo          AS tipo_sensor,
    l.timestamp_leitura,
    l.valor
FROM
    leitura_sensor l
    JOIN sensor s ON l.id_sensor = s.id_sensor
ORDER BY
    l.timestamp_leitura DESC
LIMIT 20;


-- 3.2) Histórico completo de umidade do solo (id_sensor = 1)
SELECT
    l.timestamp_leitura,
    l.valor        AS umidade_percentual
FROM
    leitura_sensor l
WHERE
    l.id_sensor = 1
ORDER BY
    l.timestamp_leitura;


-- 3.3) Histórico completo de pH do solo (id_sensor = 2)
SELECT
    l.timestamp_leitura,
    l.valor        AS ph_solo
FROM
    leitura_sensor l
WHERE
    l.id_sensor = 2
ORDER BY
    l.timestamp_leitura;


-- ----------------------------------------------------------------------
-- 4) EVENTOS DE MANEJO (IRRIGAÇÃO E FERTILIZAÇÃO)
-- ----------------------------------------------------------------------

-- 4.1) Todos os eventos ordenados por data
SELECT
    e.id_evento,
    c.nome_campo,
    s.cultura,
    e.data_evento,
    e.tipo_evento,
    e.volume_litros,
    e.produto,
    e.dose_kg_ha,
    e.observacoes
FROM
    evento_manejo e
    LEFT JOIN safra s  ON e.id_safra = s.id_safra
    LEFT JOIN campo c  ON e.id_campo = c.id_campo
ORDER BY
    e.data_evento;


-- 4.2) Eventos de irrigação separados dos de fertilização
SELECT
    e.id_evento,
    e.tipo_evento,
    e.data_evento,
    e.volume_litros,
    e.produto,
    e.dose_kg_ha,
    s.cultura,
    c.nome_campo
FROM
    evento_manejo e
    LEFT JOIN safra s ON e.id_safra = s.id_safra
    LEFT JOIN campo c ON e.id_campo = c.id_campo
WHERE
    e.tipo_evento IN ('irrigacao', 'fertilizacao')
ORDER BY
    e.data_evento;
    

-- ----------------------------------------------------------------------
-- 5) RESULTADO DE SAFRA E VISÃO GERENCIAL
-- ----------------------------------------------------------------------

-- 5.1) Produtividade por campo e safra
SELECT
    c.nome_campo,
    s.cultura,
    r.produtividade_kg_ha,
    r.data_colheita,
    r.observacoes
FROM
    resultado_s_
