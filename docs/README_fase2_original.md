# FarmTech-Fase2

# 🌾 FarmTech Solutions – Fase 2 (RM566867)
Repositório do projeto de irrigação inteligente (ESP32 no Wokwi) + análises Python/R.

## Estrutura
- `src/ativ1Fiap.py` – áreas/insumos (Café e Milho) e exporta `dadosR.csv`.
- `src/esp32_fase2.ino` – lógica de irrigação (N, P, K em botões; pH via LDR; umidade via DHT22; relé da bomba).
- `R/analise.R` – estatísticas (média e desvio) sobre os dados do CSV.
- `wokwi/diagram.json` – (opcional) circuito do simulador.
- `docs/` – PDFs (resumo Embrapa e relatório Cap.2).
- `VIDEO_LINK.txt` – link do vídeo (não listado).

## Sensores (simulados)
| Real | Simulado | Pino |
|---|---|---|
| Nitrogênio (N) | Botão | 15 |
| Fósforo (P)    | Botão | 2  |
| Potássio (K)   | Botão | 13 |
| pH do solo     | LDR   | 35 |
| Umidade        | DHT22 | 21 |
| Bomba          | Relé  | 27 |

## Regras de irrigação (cultura: Café)
- Liga se **umidade < 42%** e **pH entre 5.2 e 6.5**  
- OU se **umidade < 47%** e **≥2 nutrientes faltando**  
- Bloqueia se **pH fora de 4.8–7.2** ou **chuva prevista** (`RAIN ON` no Serial)

## Como testar no Wokwi
1. Crie projeto ESP32 e cole `src/esp32_fase2.ino`.
2. Adicione botões (15/2/13), LDR (35), DHT22 (21), relé (27).
3. Start Simulation → abra o Serial.
4. Comandos: `RAIN ON` / `RAIN OFF`.

## Python → CSV
Rode `src/ativ1Fiap.py`, preencha áreas/ruas, gere `dadosR.csv`.

## R (estatística)
No RStudio, garanta que `dadosR.csv` esteja no Working Directory e rode `R/analise.R`.

## Vídeo
Cole aqui o link (não listado) e em `VIDEO_LINK.txt`.
