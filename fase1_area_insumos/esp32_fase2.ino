#include <DHT.h>

// Pinos (sinta-se livre para mudar um ou dois e refletir no README)
const int PIN_BUTTON_N = 15;
const int PIN_BUTTON_P = 2;
const int PIN_BUTTON_K = 13;
const int PIN_LDR = 35;          // ADC
const int PIN_DHT = 21;          // DHT22
const int PIN_PUMP_RELAY = 27;   // ativo em LOW

#define MY_DHTTYPE DHT22
DHT myDht(PIN_DHT, MY_DHTTYPE);

// Thresholds customizados
const float HUMIDITY_THRESHOLD_STRICT = 42.0;
const float HUMIDITY_THRESHOLD_LOOSE  = 47.0;
const float PH_SAFE_MIN = 4.8, PH_SAFE_MAX = 7.2;
const float PH_IDEAL_MIN = 5.2, PH_IDEAL_MAX = 6.5;

const int   ADC_SAMPLES = 6;
const unsigned long LOOP_DELAY_MS = 1000;
const unsigned long DEBOUNCE_DELAY = 50;

bool rainFlag = false, pumpOn = false;

unsigned long tN=0, tP=0, tK=0;
bool lastN=HIGH, lastP=HIGH, lastK=HIGH;

bool readDebounced(int pin, bool &last, unsigned long &t, unsigned long now){
  bool raw = digitalRead(pin);
  if(raw != last) t = now;
  if(now - t > DEBOUNCE_DELAY) last = raw;
  return (last == LOW); // INPUT_PULLUP: LOW=pressionado
}

int readAdcAvg(int pin){
  long s=0; for(int i=0;i<ADC_SAMPLES;i++){ s+=analogRead(pin); delay(4); }
  return s/ADC_SAMPLES;
}

// mapeamento não-linear ADC -> pH (0..14)
float adcToPH(int raw){
  float norm = raw/4095.0f;
  float curved = powf(norm, 1.12f);
  float ph = 14.0f * (1.0f - curved);
  if(ph<0) ph=0; if(ph>14) ph=14;
  return ph;
}

void serialRain(){
  while(Serial.available()){
    String s = Serial.readStringUntil('\n'); s.trim(); s.toUpperCase();
    if(s=="RAIN ON" || s=="RAIN=1"){ rainFlag=true;  Serial.println("[SERIAL] Chuva: SIM"); }
    else if(s=="RAIN OFF"|| s=="RAIN=0"){ rainFlag=false; Serial.println("[SERIAL] Chuva: NAO"); }
    else { Serial.print("[SERIAL] ? "); Serial.println(s); }
  }
}

void setPump(bool on){ pumpOn=on; digitalWrite(PIN_PUMP_RELAY, on?LOW:HIGH); }

void setup(){
  Serial.begin(115200);
  pinMode(PIN_BUTTON_N, INPUT_PULLUP);
  pinMode(PIN_BUTTON_P, INPUT_PULLUP);
  pinMode(PIN_BUTTON_K, INPUT_PULLUP);
  pinMode(PIN_PUMP_RELAY, OUTPUT); digitalWrite(PIN_PUMP_RELAY, HIGH);
  analogReadResolution(12);
  myDht.begin();
  Serial.println("ESP32 - Irrigacao Inteligente (custom)");
  Serial.println("Use: RAIN ON / RAIN OFF");
}

void loop(){
  unsigned long now=millis();
  serialRain();

  bool hasN = readDebounced(PIN_BUTTON_N, lastN, tN, now);
  bool hasP = readDebounced(PIN_BUTTON_P, lastP, tP, now);
  bool hasK = readDebounced(PIN_BUTTON_K, lastK, tK, now);

  int   adc = readAdcAvg(PIN_LDR);
  float ph  = adcToPH(adc);
  float um  = myDht.readHumidity();
  if(isnan(um)){ Serial.println("[ERRO] DHT22"); um=100.0; }

  int missing = (!hasN) + (!hasP) + (!hasK);

  bool ph_ok   = (ph>=PH_IDEAL_MIN && ph<=PH_IDEAL_MAX);
  bool ph_safe = (ph>=PH_SAFE_MIN  && ph<=PH_SAFE_MAX);

  bool irrigar = false;
  if(um < HUMIDITY_THRESHOLD_STRICT && ph_ok)           irrigar = true;
  if(um < HUMIDITY_THRESHOLD_LOOSE  && missing >= 2)    irrigar = true;

  if(!ph_safe) irrigar=false;
  if(rainFlag) irrigar=false;

  setPump(irrigar);

  Serial.print("N:");Serial.print(hasN?"OK":"FALTA");
  Serial.print(" P:");Serial.print(hasP?"OK":"FALTA");
  Serial.print(" K:");Serial.print(hasK?"OK":"FALTA");
  Serial.print(" | pH:");Serial.print(ph,2);
  Serial.print(" (ADC=");Serial.print(adc);Serial.print(")");
  Serial.print(" | Umid%:");Serial.print(um,1);
  Serial.print(" | Missing:");Serial.print(missing);
  Serial.print(" | Chuva:");Serial.print(rainFlag?"SIM":"NAO");
  Serial.print(" | Bomba:");Serial.println(pumpOn?"LIGADA":"DESLIGADA");

  delay(LOOP_DELAY_MS);
}
