#include <DHT.h>

// Pinos do hardware (sinta-se livre para alterar se necessário)
const int PIN_BTN_N   = 15;  // Botão de Nitrogênio
const int PIN_BTN_P   = 2;   // Botão de Fósforo
const int PIN_BTN_K   = 13;  // Botão de Potássio
const int PIN_LDR     = 35;  // LDR para pH (entrada analógica)
const int PIN_DHT     = 21;  // DHT22 (umidade)
const int PIN_PUMP    = 27;  // Relé / LED que aciona a bomba (ativo em HIGH)

// Instancia o sensor de umidade
DHT sensorDHT(PIN_DHT, DHT22);

// Flag de previsão de chuva
bool flagChuva = false;

// Converte valor do LDR (0–4095) para escala de pH (0–14) com leve não linearidade
float lerPH() {
  int raw = analogRead(PIN_LDR);
  float proporcao = raw / 4095.0f;
  // Ajuste exponencial para não ficar linear demais
  float curvado = powf(proporcao, 1.15f);
  float ph = 14.0f * (1.0f - curvado);
  if (ph < 0.0f) ph = 0.0f;
  if (ph > 14.0f) ph = 14.0f;
  return ph;
}

// Configuração inicial
void setup() {
  Serial.begin(115200);
  pinMode(PIN_BTN_N, INPUT_PULLUP);
  pinMode(PIN_BTN_P, INPUT_PULLUP);
  pinMode(PIN_BTN_K, INPUT_PULLUP);
  pinMode(PIN_PUMP, OUTPUT);
  digitalWrite(PIN_PUMP, LOW);  // garante bomba desligada
  sensorDHT.begin();
  Serial.println("Sistema de irrigacao pronto. Use 'RAIN ON' ou 'RAIN OFF' para ativar/desativar previsao de chuva.");
}

// Loop principal
void loop() {
  // Verifica se há comandos na serial
  while (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    comando.toUpperCase();
    if (comando == "RAIN ON") {
      flagChuva = true;
      Serial.println("Previsao de chuva ativada.");
    } else if (comando == "RAIN OFF") {
      flagChuva = false;
      Serial.println("Previsao de chuva desativada.");
    }
  }

  // Leitura dos botões (HIGH significa que o nutriente está faltando, pois usamos pull-up)
  bool faltaN = digitalRead(PIN_BTN_N);
  bool faltaP = digitalRead(PIN_BTN_P);
  bool faltaK = digitalRead(PIN_BTN_K);
  int faltando = (faltaN ? 1 : 0) + (faltaP ? 1 : 0) + (faltaK ? 1 : 0);

  // Leitura dos sensores
  float umidade = sensorDHT.readHumidity();
  float phSolo  = lerPH();

  // Lógica de irrigação (ajuste as faixas conforme sua cultura/necessidade)
  bool acionarBomba = false;
  if (!flagChuva) {
    // Regra 1: umidade muito baixa e pH dentro do ideal
    if (umidade < 43.0f && phSolo >= 5.3f && phSolo <= 6.6f) {
      acionarBomba = true;
    }
    // Regra 2: um pouco menos seco, mas com dois ou mais nutrientes faltando
    else if (umidade < 48.0f && faltando >= 2) {
      acionarBomba = true;
    }
    // Bloqueia se pH fora da faixa segura
    if (phSolo < 4.7f || phSolo > 7.3f) {
      acionarBomba = false;
    }
  } else {
    // Com chuva prevista, não aciona a bomba
    acionarBomba = false;
  }

  // Aciona ou desliga a bomba (LED/relé)
  digitalWrite(PIN_PUMP, acionarBomba ? HIGH : LOW);

  // Log periódico no monitor serial
  static unsigned long ultimaSaida = 0;
  unsigned long agora = millis();
  if (agora - ultimaSaida >= 1000) {
    ultimaSaida = agora;
    Serial.print("Umidade: ");
    Serial.print(umidade);
    Serial.print("% | pH: ");
    Serial.print(phSolo);
    Serial.print(" | N: ");
    Serial.print(faltaN ? "Falta" : "Ok");
    Serial.print(" | P: ");
    Serial.print(faltaP ? "Falta" : "Ok");
    Serial.print(" | K: ");
    Serial.print(faltaK ? "Falta" : "Ok");
    Serial.print(" | Chuva: ");
    Serial.print(flagChuva ? "Sim" : "Nao");
    Serial.print(" | Bomba: ");
    Serial.println(acionarBomba ? "Ligada" : "Desligada");
  }

  delay(50);
}
