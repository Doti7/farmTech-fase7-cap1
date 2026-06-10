# 🌾 FarmTech Solutions – Fase 7 (Capítulo 1)

## Integrantes

- Bernardo Naves Doti Avelar – RM566867
- Leticia Grossi Dornelas – RM568172
- Leonardo Borges Alves da Mota – RM566939
- David Eduardo da Silva Correia – RM567525
- Laura de Andrade Castilho – RM568507

---

# 📖 Sobre o Projeto

A FarmTech Solutions é uma plataforma de gestão agrícola desenvolvida ao longo das Fases 1 a 7 do projeto acadêmico da FIAP.

O objetivo da Fase 7 foi consolidar todas as soluções desenvolvidas anteriormente em uma única aplicação, permitindo que produtores e gestores agrícolas possam visualizar dados, analisar indicadores, prever produtividade, monitorar sensores e receber alertas operacionais através de uma dashboard centralizada.

O sistema integra:

- Cálculo de área agrícola e insumos;
- Banco de dados estruturado;
- Sensores IoT e automação de irrigação;
- Machine Learning para previsão de produtividade;
- Cloud Computing e sistema de alertas;
- Visão Computacional com Redes Neurais.

---

# 🎯 Objetivo da Fase 7

Consolidar todas as entregas das Fases 1 a 6 em um único projeto Python utilizando Streamlit como dashboard principal.

Além disso, implementar uma camada de alertas inspirada na arquitetura AWS SNS para auxiliar funcionários da fazenda na tomada de decisão a partir dos dados coletados.

---

# 🏗️ Arquitetura Geral

```text
Fase 1
(Cálculo de Área e Insumos)
            │
            ▼
Fase 2
(Banco de Dados)
            │
            ▼
Fase 3
(IoT e Sensores)
            │
            ▼
Fase 4
(Machine Learning)
            │
            ▼
Fase 5
(Alertas AWS SNS)
            │
            ▼
Fase 6
(Visão Computacional)
            │
            ▼
Dashboard Central
(Fase 7)
```

---

# 📂 Estrutura do Projeto

```text
farmTech-fase7-cap1
│
├── app.py
├── requirements.txt
├── README.md
│
├── fase1_area_insumos
├── fase2_banco_dados
├── fase3_iot_sensores
├── fase4_dashboard_ml
├── fase5_aws_alertas
├── fase6_visao_computacional
│
├── assets
├── data
└── docs
```

---

# 🚜 Fase 1 – Área de Plantio e Manejo de Insumos

Nesta fase foi desenvolvido um sistema para cálculo de área agrícola e estimativa de insumos necessários para diferentes culturas.

## Funcionalidades

- Cálculo de área total (m²);
- Conversão para hectares;
- Estimativa de insumos por hectare;
- Estrutura inicial de dados agrícolas.

## Tecnologias

- Python
- R

---

# 🗄️ Fase 2 – Banco de Dados Estruturado

Nesta fase foi desenvolvido o armazenamento estruturado dos dados agrícolas.

## Funcionalidades

- Modelagem de dados;
- Scripts SQL;
- Estrutura relacional;
- Persistência dos dados coletados.

## Arquivos Importados

- schema.sql
- seed_inicial.sql
- consultas_exemplo.sql
- farmtech.db

---

# 📡 Fase 3 – IoT e Automação Inteligente

Nesta fase foi implementada a simulação de sensores agrícolas e a lógica de irrigação automatizada.

## Sensores Simulados

- Umidade do solo
- pH do solo
- Nitrogênio (N)
- Fósforo (P)
- Potássio (K)

## Automação

A bomba de irrigação é ativada quando:

- A umidade está abaixo do limite;
- O pH está fora da faixa adequada;
- Existe deficiência nutricional.

## Funcionalidades Integradas na Dashboard

- Simulação de leitura dos sensores;
- Exibição dos dados históricos;
- Status da bomba de irrigação.

---

# 🤖 Fase 4 – Machine Learning

Nesta fase foi desenvolvido um modelo preditivo para estimativa de produtividade agrícola.

## Tecnologias

- Scikit-Learn
- Pandas
- Joblib
- Streamlit

## Funcionalidades

- Carregamento do modelo treinado;
- Exibição das métricas do modelo;
- Simulação de cenários agrícolas;
- Previsão de produtividade.

## Métricas Obtidas

O modelo apresenta:

- MAE
- MSE
- RMSE
- R²

As métricas podem ser visualizadas diretamente pela dashboard.

---

# ☁️ Fase 5 – Cloud Computing e Alertas

O objetivo desta fase foi simular uma arquitetura de mensageria baseada em AWS SNS para alertar funcionários da fazenda quando condições críticas forem detectadas.

## Regras de Negócio

O sistema gera alertas quando:

### Umidade Baixa

```text
Umidade < 30%
```

### pH Fora da Faixa

```text
pH < 5.5
ou
pH > 7.0
```

### Produtividade Baixa

```text
Produtividade prevista abaixo do esperado
```

### Anomalias Visuais

Detectadas pela Visão Computacional.

## Exemplo de Alerta

```text
ALERTA FARMTECH - FASE 7

Condições críticas identificadas:

- Umidade baixa detectada.
- pH fora da faixa ideal.

Ações recomendadas:

- Verificar sensores.
- Verificar irrigação.
- Registrar ação corretiva.
```

## Arquitetura Prevista

```text
Dashboard
    │
    ▼
AWS SNS
    │
    ▼
E-mail / SMS
    │
    ▼
Funcionários da Fazenda
```

---

# 👁️ Fase 6 – Visão Computacional

Nesta fase foi desenvolvido um sistema de classificação e detecção visual utilizando Redes Neurais Convolucionais (CNN) e YOLO.

## Objetivo

Monitorar visualmente o ambiente agrícola e detectar padrões relevantes para suporte à tomada de decisão.

## Tecnologias

- Python
- TensorFlow
- Keras
- YOLOv5

## Resultados Integrados

A dashboard apresenta:

- Detecções YOLO;
- Predições CNN;
- Curvas de treinamento;
- Matriz de confusão.

## Arquivos Utilizados

- GrupoMultiAgents_pbl_fase6_ok.ipynb
- detections_test.png
- cnn_predictions.png
- cnn_confusion_matrix.png

---

# 🖥️ Dashboard Central da Fase 7

A dashboard foi desenvolvida utilizando Streamlit e consolida todas as fases do projeto.

## Abas Disponíveis

### Visão Geral

Apresentação do sistema.

### Fases 1 e 2

- Área agrícola;
- Insumos;
- Banco de dados.

### Fase 3

- Sensores;
- Irrigação;
- Histórico de leituras.

### Fase 4

- Machine Learning;
- Produtividade.

### Fase 5

- Sistema de Alertas.

### Fase 6

- Visão Computacional.

---

# ▶️ Como Executar

## Instalação

```bash
pip install -r requirements.txt
```

## Executar Dashboard

```bash
streamlit run app.py
```

---

# 📸 Evidências

## Dashboard Principal

Inserir print da tela inicial.

## Fase 3 – Sensores

Inserir print da aba IoT.

## Fase 4 – Machine Learning

Inserir print da previsão de produtividade.

## Fase 5 – Alertas

Inserir print do alerta gerado.

## Fase 6 – Visão Computacional

Inserir print dos resultados YOLO e CNN.

---

# 🎥 Vídeo Demonstrativo

Link do vídeo no YouTube (não listado):

```text
https://youtu.be/8yRllN6v7JM
```

---

# 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-Learn
- TensorFlow
- Keras
- YOLOv5
- SQLite
- SQL
- AWS SNS (arquitetura simulada)
- R

---

# ✅ Conclusão

A Fase 7 consolidou todas as etapas desenvolvidas anteriormente em uma única solução integrada para gestão agrícola.

A plataforma permite calcular áreas de cultivo, armazenar informações em banco de dados, monitorar sensores IoT, prever produtividade utilizando Machine Learning, gerar alertas operacionais e visualizar resultados provenientes de modelos de Visão Computacional.

O resultado é uma solução unificada capaz de apoiar a tomada de decisão no contexto do agronegócio, demonstrando a integração entre análise de dados, automação, inteligência artificial e computação em nuvem.
