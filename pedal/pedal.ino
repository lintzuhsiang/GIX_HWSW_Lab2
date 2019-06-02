

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#ifndef STASSID
#define STASSID "shine"
#define STAPSK  "11111111"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;
const int pedalPin = D8;
const  int buttonPin = D7;
  int pedalState = 0;
  int pedalLastState = 0;
  int buttonState = 0;
  const int GreenLED = D1;
  const int RedLED = D3;
  const int Speaker = D5;
  int pedalCount = 0;
unsigned long pedaltime = 2000;

void setup() {
//  Serial.begin(115200);
Serial.begin(57600);
  pinMode(GreenLED,OUTPUT);
  pinMode(RedLED,OUTPUT);
  pinMode(pedalPin,INPUT_PULLUP);
  pinMode(buttonPin,INPUT_PULLUP);
  digitalWrite(RedLED,HIGH); //turn on device and RED led alway on
  pinMode(Speaker,OUTPUT);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void PostJSON(int pedalCount){
//    char pedalChar[16];
//    itoa(pedalCount,pedalChar,10);
     StaticJsonBuffer<300> JSONbuffer;
    JsonObject& JSONencoder = JSONbuffer.createObject();
    JSONencoder["patient_id"]="001";
    JSONencoder["device_id"]="002";
    JSONencoder["pedal"] = pedalCount;
    
   char JSONmessageBuffer[300];
   JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
   Serial.println(JSONmessageBuffer);
  HTTPClient http;
      http.begin("http://spimo.azurewebsites.net/access_db");
      http.addHeader("Content-Type","application/json");
      int httpCode = http.POST(JSONmessageBuffer);
      String payload = http.getString();
      Serial.print("httpCode: ");
      Serial.println(httpCode);
      Serial.print("payload: ");
      Serial.println(payload);
      http.end(); 
}

void loop() {
  pedalState = digitalRead(pedalPin);
  buttonState = digitalRead(buttonPin);
  
   if(buttonState == 0){
    pedaltime = millis();
    if (buttonState == 0 and millis()-pedaltime > 2000){    //press reset button over two seconds
    pedalCount = 0;
    tone(Speaker,1000); //1000Hz
    Serial.println("button presses and buzzer sound");
    delay(1000); //buzzer for 1 second
    noTone(Speaker);
   }
  }
  
  Serial.println(pedalCount);
  if(WiFi.status()==WL_CONNECTED){
  if(pedalLastState != pedalState){
    if(pedalState==1){
      digitalWrite(GreenLED,HIGH);
       pedalCount ++; 
     PostJSON(pedalCount);
    }else{      
      digitalWrite(GreenLED,LOW);
     
    }
  }
  pedalLastState = pedalState;
  }else{
    Serial.println("not connect to Wifi...");
  }

  delay(30000);
}
