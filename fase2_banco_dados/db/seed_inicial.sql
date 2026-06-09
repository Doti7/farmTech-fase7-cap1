-- ==========================================
-- DADOS INICIAIS - FARMTECH FASE 4
-- ==========================================

-- 1. Campos (talhões)
INSERT INTO campo (id_campo, nome_campo, localizacao, area_ha) VALUES
(1, 'Campo Experimental 1', 'Fazenda Boa Esperança - GO', 10.5);

-- 2. Safras
INSERT INTO safra (id_safra, id_campo, cultura, data_inicio, data_fim, area_ha) VALUES
(1, 1, 'Soja', '2025-10-01', NULL, 10.5);

-- 3. Sensores instalados
INSERT INTO sensor (id_sensor, id_campo, tipo, unidade_medida, profundidade_cm, descricao) VALUES
(1, 1, 'umidade_solo', '%', 20, 'Sensor de umidade do solo a 20cm'),
(2, 1, 'ph_solo', 'pH', 20, 'Sensor de pH do solo a 20cm');

-- 4. Leituras de sensores (exemplo)
INSERT INTO leitura_sensor (id_leitura, id_sensor, timestamp_leitura, valor) VALUES
(1, 1, '2025-10-01 08:00:00', 25.5),
(2, 1, '2025-10-01 12:00:00', 23.0),
(3, 1, '2025-10-01 16:00:00', 21.7),
(4, 2, '2025-10-01 08:00:00', 5.8),
(5, 2, '2025-10-01 12:00:00', 5.9),
(6, 2, '2025-10-01 16:00:00', 6.0);

-- 5. Eventos de manejo (irrigação e fertilização)
INSERT INTO evento_manejo (id_evento, id_campo, id_safra, data_evento, tipo_evento,
                           volume_litros, produto, dose_kg_ha, observacoes)
VALUES
(1, 1, 1, '2025-10-02 06:00:00', 'irrigacao', 3000.0, NULL, NULL, 'Irrigação por aspersão'),
(2, 1, 1, '2025-10-05 07:30:00', 'fertilizacao', NULL, 'NPK 10-10-10', 150.0, 'Adubação de cobertura');

-- 6. Resultado de safra (produtividade final)
INSERT INTO resultado_safra (id_resultado, id_safra, produtividade_kg_ha, data_colheita, observacoes) VALUES
(1, 1, 3600.0, '2026-02-15', 'Safra dentro da média histórica');

