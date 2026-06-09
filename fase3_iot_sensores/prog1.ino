#include <DHT.h>

// ================= PINOS =================
#define DHTPIN   23
#define DHTTYPE  DHT22
#define LDR_PIN  34        // AO do módulo LDR
#define RELAY_PIN 18       // IN do relé (ajustado p/ seu circuito)

// Botões NPK (usar INPUT_PULLUP)
#define BTN_N 15
#define BTN_P 2
#define BTN_K 4

// ================ OBJETOS ================
DHT dht(DHTPIN, DHTTYPE);

// ======= PARÂMETROS DA CULTURA (ex.: tomate) =======
float PH_MIN = 6.0;
float PH_MAX = 7.0;
float UMID_MIN = 60.0;   // % mínima desejada

// ======= AJUSTES GERAIS =======
const unsigned long INTERVALO_MS = 2000; // período de leitura
unsigned long t0 = 0;
int contadorRegistros = 1;              // CONTADOR ADICIONADO
const int MAX_REGISTROS = 10000;        // LIMITE DE 10 MIL


// Mapeia ADC (0..4095) para pH (0..14) — ajuste livre se quiser
float mapPh(int adc) {
  float ph = (adc / 4095.0f) * 14.0f;
  if (ph < 0) ph = 0;
  if (ph > 14) ph = 14;
  return ph;
}



void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // relé desligado no boot

  pinMode(BTN_N, INPUT_PULLUP);
  pinMode(BTN_P, INPUT_PULLUP);
  pinMode(BTN_K, INPUT_PULLUP);

  // LDR no pino 34 (somente entrada analógica) — não precisa pinMode

  // Inicializa o gerador de números aleatórios
  randomSeed(analogRead(0));

  Serial.println("\n===========================================");
  Serial.println("         DADOS CSV PARA ORACLE");
  Serial.println("===========================================");
  Serial.println("ID,UMIDADE,PH,LDR_ADC,N_STATUS,P_STATUS,K_STATUS,UMIDADE_BAIXA,PH_FORA_FAIXA,NUTRIENTE_BAIXO,BOMBA_LIGADA");
  Serial.println("-------------------------------------------");
}

void loop() {

  // ========== VERIFICA SE JÁ COLETOU 10 MIL ==========
  if (contadorRegistros >= MAX_REGISTROS) {
    Serial.print("\r\n===========================================\r\n");
    Serial.printf("    COLETA FINALIZADA! %d REGISTROS\r\n", contadorRegistros);
    Serial.print("===========================================\r\n");
    Serial.print("Sistema pausado. Reset para nova coleta.\r\n");
    
    // Para o sistema - pisca LED do relé para indicar fim
    while (true) {
      digitalWrite(RELAY_PIN, HIGH);
      delay(500);
      digitalWrite(RELAY_PIN, LOW);
      delay(500);
    }
  }
  // leitura a cada INTERVALO_MS
  if (millis() - t0 < INTERVALO_MS) return;
  t0 = millis();

  // -------- Sensores RANDOMICOS --------
  // Umidade aleatória entre 30% e 90%
  float umid = random(300, 901) / 10.0;
  
  // LDR ADC aleatório entre 0 e 4095
  int ldrAdc = random(0, 4096);
  float ph = mapPh(ldrAdc);

  // Botões aleatórios: 50% chance de estar OK (HIGH) ou BAIXO (LOW)
  bool N_ok = random(0, 2) == 1;  // 50% chance de ser true
  bool P_ok = random(0, 2) == 1;  // 50% chance de ser true
  bool K_ok = random(0, 2) == 1;  // 50% chance de ser true

  // -------- Lógica de decisão --------
  bool umidade_baixa   = (umid < UMID_MIN);
  bool ph_fora_da_faixa = (ph < PH_MIN) || (ph > PH_MAX);
  bool nutriente_baixo = (!N_ok) || (!P_ok) || (!K_ok);

  bool ligar_bomba = umidade_baixa || ph_fora_da_faixa || nutriente_baixo;

  digitalWrite(RELAY_PIN, ligar_bomba ? HIGH : LOW);

  // -------- Logs bonitinhos --------
    Serial.printf("%d,%.2f,%.2f,%d,%d,%d,%d,%d,%d,%d,%d\r\n",
    contadorRegistros, umid, ph, ldrAdc,
    N_ok ? 1 : 0, P_ok ? 1 : 0, K_ok ? 1 : 0,
    umidade_baixa ? 1 : 0, ph_fora_da_faixa ? 1 : 0,
    nutriente_baixo ? 1 : 0, ligar_bomba ? 1 : 0
  );
  contadorRegistros++;

}
