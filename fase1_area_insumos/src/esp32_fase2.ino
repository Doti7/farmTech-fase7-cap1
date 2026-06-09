#include <DHT.h>

const int PIN_BUTTON_N = 15;    // botão que representa Nitrogênio (N)
const int PIN_BUTTON_P = 2;     // botão que representa Fósforo (P)
const int PIN_BUTTON_K = 13;    // botão que representa Potássio (K)
const int PIN_LDR = 35;         // ADC do LDR (simula pH)
const int PIN_DHT = 21;         // DHT22
const int PIN_PUMP_RELAY = 27;  // relé que controla a bomba (ativo em LOW)

#define MY_DHTTYPE DHT22
DHT myDht(PIN_DHT, MY_DHTTYPE);

// --- Parâmetros de decisão (ajustáveis) ---
const float HUMIDITY_THRESHOLD_STRICT = 42.0;   // abaixo disso --> aciona se pH ok
const float HUMIDITY_THRESHOLD_LOOSE  = 47.0;   // abaixo disso --> aciona se muitos nutrientes faltando

const float PH_SAFE_MIN = 4.8;   // fora disso: bloqueia irrigação
const float PH_SAFE_MAX = 7.2;
const float PH_IDEAL_MIN = 5.2;  // ideal para ligar junto com umidade seca
const float PH_IDEAL_MAX = 6.5;

// --- Leitura / filtro ---
const int ADC_SAMPLES = 6;        // média simples no ADC
const unsigned long LOOP_DELAY_MS = 1000;

// Estado global
bool rainFlag = false;  // controle via serial (chuva prevista)
bool pumpOn = false;

// Debounce / state tracking for buttons
unsigned long lastDebounceTimeN = 0;
unsigned long lastDebounceTimeP = 0;
unsigned long lastDebounceTimeK = 0;
const unsigned long DEBOUNCE_DELAY = 50; // ms

bool lastButtonStateN = HIGH;
bool lastButtonStateP = HIGH;
bool lastButtonStateK = HIGH;

bool nutrientN_present = true;
bool nutrientP_present = true;
bool nutrientK_present = true;

// --- Funções utilitárias ---

// Faz média de várias leituras ADC para suavizar ruído
int readAdcAvg(int pin) {
  long sum = 0;
  for (int i = 0; i < ADC_SAMPLES; ++i) {
    sum += analogRead(pin);
    delay(4);
  }
  int avg = sum / ADC_SAMPLES;
  return avg;
}

// Converte ADC (0..4095) para pH (0..14) com mapeamento levemente não-linear
float convertAdcToPH(int rawAdc) {
  // normaliza 0..1
  float norm = rawAdc / 4095.0f;
  // aplicamos uma pequena curva exponencial para evitar linearidade óbvia
  float curved = powf(norm, 1.12f); // ajuste sutil
  float ph = 14.0f * (1.0f - curved); // inversão: mais luz -> pH menor (definição arbitrária)
  if (ph < 0.0f) ph = 0.0f;
  if (ph > 14.0f) ph = 14.0f;
  return ph;
}

// Le a serial e altera flag de chuva: comando "RAIN ON" ou "RAIN OFF"
void processSerialCommands() {
  while (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toUpperCase();
    if (cmd == "RAIN ON" || cmd == "RAIN=1") {
      rainFlag = true;
      Serial.println("[SERIAL] Previsao de chuva: SIM");
    } else if (cmd == "RAIN OFF" || cmd == "RAIN=0") {
      rainFlag = false;
      Serial.println("[SERIAL] Previsao de chuva: NAO");
    } else {
      Serial.print("[SERIAL] Comando nao reconhecido: ");
      Serial.println(cmd);
      Serial.println("Use: RAIN ON / RAIN OFF");
    }
  }
}

// Le e debouceia um botão com pullup; retorna true se pressionado (LOW)
bool readButtonDebounced(int pin, bool &lastState, unsigned long &lastMillisVar, unsigned long now) {
  bool raw = digitalRead(pin);
  if (raw != lastState) {
    lastMillisVar = now;
  }
  if ((now - lastMillisVar) > DEBOUNCE_DELAY) {
    // estado estável
    // atualiza lastState e retorna se está pressionado
    lastState = raw;
  }
  return (lastState == LOW); // LOW = pressionado (porque usamos INPUT_PULLUP)
}

void setPump(bool on) {
  pumpOn = on;
  digitalWrite(PIN_PUMP_RELAY, on ? LOW : HIGH); // relé ativo em LOW
}

// --- Setup ---
void setup() {
  Serial.begin(115200);
  delay(200);

  // pinos
  pinMode(PIN_BUTTON_N, INPUT_PULLUP);
  pinMode(PIN_BUTTON_P, INPUT_PULLUP);
  pinMode(PIN_BUTTON_K, INPUT_PULLUP);

  pinMode(PIN_PUMP_RELAY, OUTPUT);
  digitalWrite(PIN_PUMP_RELAY, HIGH); // desligado inicialmente

  analogReadResolution(12); // ADC 12-bit -> 0..4095

  // iniciar DHT
  myDht.begin();

  Serial.println("FarmTech - ESP32 Irrigacao Inteligente (versao custom)");
  Serial.println("Comandos: RAIN ON / RAIN OFF");
}

// --- Loop principal ---
void loop() {
  unsigned long now = millis();

  // processa comandos da serial (possivel previsao de chuva)
  processSerialCommands();

  // le botoes (debounce)
  bool btnN = readButtonDebounced(PIN_BUTTON_N, lastButtonStateN, lastDebounceTimeN, now);
  bool btnP = readButtonDebounced(PIN_BUTTON_P, lastButtonStateP, lastDebounceTimeP, now);
  bool btnK = readButtonDebounced(PIN_BUTTON_K, lastButtonStateK, lastDebounceTimeK, now);

  // se botao pressionado (LOW) -> nutriente presente
  nutrientN_present = btnN;
  nutrientP_present = btnP;
  nutrientK_present = btnK;

  // leitura LDR (pH simulado)
  int rawAdc = readAdcAvg(PIN_LDR);
  float phValue = convertAdcToPH(rawAdc);

  // leitura DHT22 (umidade)
  float humidity = myDht.readHumidity();
  if (isnan(humidity)) {
    Serial.println("[ERRO] Falha leitura DHT22");
    humidity = 100.0; // assume úmido para evitar acionamento indevido
  }

  // conta quantos nutrientes estao faltando (false == falta)
  int missingCount = 0;
  if (!nutrientN_present) missingCount++;
  if (!nutrientP_present) missingCount++;
  if (!nutrientK_present) missingCount++;

  // logica de decisao (documente isso no README.md)
  bool ph_ok_for_irrigation = (phValue >= PH_IDEAL_MIN && phValue <= PH_IDEAL_MAX);
  bool ph_within_safe = (phValue >= PH_SAFE_MIN && phValue <= PH_SAFE_MAX);

  bool shouldIrrigate = false;

  // regra 1: se muito seco e pH ideal -> rega
  if (humidity < HUMIDITY_THRESHOLD_STRICT && ph_ok_for_irrigation) {
    shouldIrrigate = true;
  }

  // regra 2: se seco (um pouco menos) e faltam >=2 nutrientes -> rega
  if (humidity < HUMIDITY_THRESHOLD_LOOSE && missingCount >= 2) {
    shouldIrrigate = true;
  }

  // bloqueios
  if (!ph_within_safe) {
    shouldIrrigate = false; // pH fora da faixa segura -> nao regar
  }
  if (rainFlag) {
    shouldIrrigate = false; // chuva prevista
  }

  // acionar bomba
  setPump(shouldIrrigate);

  // imprimir status no Serial (formato legivel)
  Serial.print("[STATUS] N:"); Serial.print(nutrientN_present ? "PRESENTE" : "FALTA");
  Serial.print(" | P:"); Serial.print(nutrientP_present ? "PRESENTE" : "FALTA");
  Serial.print(" | K:"); Serial.print(nutrientK_present ? "PRESENTE" : "FALTA");
  Serial.print(" || pH:"); Serial.print(phValue, 2);
  Serial.print(" (ADC="); Serial.print(rawAdc); Serial.print(")");
  Serial.print(" || Umid:"); Serial.print(humidity, 1);
  Serial.print("% || Missing:"); Serial.print(missingCount);
  Serial.print(" || RainFlag:"); Serial.print(rainFlag ? "YES" : "NO");
  Serial.print(" || BOMBA:"); Serial.println(pumpOn ? "ON" : "OFF");

  // pequeno delay antes proxima iteracao
  delay(LOOP_DELAY_MS);
}
