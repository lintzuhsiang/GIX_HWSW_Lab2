#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#ifndef STASSID
#define STASSID "shine"
#define STAPSK  "11111111"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;
const int pedalPin = D1;
const  int buttonPin = D4;
  int pedalState = 0;
  int pedalLastState = 0;
  int buttonState = 0;
  bool startPost = false;
  bool buttonLastState = true;
  unsigned long buttonTime = 0;
  const int GreenLED = D3;
  const int RedLED = D2;
  const int Speaker = D7;
  int pedalCount = 0;
unsigned long pedaltime = 2000;

void setup() {
//  Serial.begin(115200);
Serial.begin(115200);
  pinMode(GreenLED,OUTPUT);
  pinMode(RedLED,OUTPUT);
  pinMode(pedalPin,INPUT_PULLUP);
  pinMode(buttonPin,INPUT_PULLUP);
  digitalWrite(RedLED,HIGH); //turn on device and RED led alway on
  pinMode(Speaker,OUTPUT);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

 while (WiFi.status() != WL_CONNECTED) {
     digitalWrite(RedLED,LOW);
    delay(250);
        digitalWrite(RedLED,HIGH);
    delay(250);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void PostJSON(int pedalCount){
     StaticJsonBuffer<300> JSONbuffer;
    JsonObject& JSONencoder = JSONbuffer.createObject();
    JSONencoder["patient_id"]="PAT001";
    JSONencoder["device_id"]="PED001";
//    JSONencoder["pedal"] = pedalCount;
    
   char JSONmessageBuffer[300];
   JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
   Serial.println(JSONmessageBuffer);
  HTTPClient http;
      http.begin("http://spimo.azurewebsites.net/paddle_count");
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
  
//   if(buttonState == 0){
//    pedaltime = millis();
////    if (buttonState == 0 and millis()-pedaltime > 2000){    //press reset button over two seconds
//    pedalCount = 0;
//    tone(Speaker,1000); //1000Hz
//    Serial.println("button presses and buzzer sound");
//    delay(1000); //buzzer for 1 second
//    noTone(Speaker);
////   }
//  }
  
  Serial.print("button State: ");
  Serial.println(buttonState);
Serial.print("button Last State: ");
Serial.println(buttonLastState);
Serial.print("startPost: ");
Serial.println(startPost);

  if(WiFi.status()==WL_CONNECTED){
    while(buttonState == 0){
      if(buttonLastState){
        buttonTime = millis();
        buttonLastState = false;
      }
      tone(Speaker,1000);
      Serial.print(millis());
      Serial.print("  ");
      Serial.println(buttonTime);
      if(buttonState ==0 and millis() - buttonTime > 1000){ //start or stop to post when press longer than 0.5 second
         startPost = !startPost;
         buttonLastState = true;
//         Serial.print("startPost reverse: ");
//         Serial.println(startPost);
         break;
//      }else if(buttonState == 0 and millis() - buttonTime > 500){
//        pedalCount = 0;
//        buttonLastState =true;
      }
    }
    noTone(Speaker);
   
    
    
  if(pedalLastState != pedalState and startPost){ //and after press button
    if(pedalState==0){
      digitalWrite(GreenLED,HIGH);
       pedalCount ++; 
       Serial.println("pressed");
     PostJSON(pedalCount);
    }else{      
      digitalWrite(GreenLED,LOW);
     
    }
  }
  pedalLastState = pedalState;
  if(startPost){  //if press start button, green led will blink
    digitalWrite(GreenLED,HIGH);
    delay(200);
    digitalWrite(GreenLED,LOW);
    delay(200);
  }
 
  }else{
    Serial.println("not connect to Wifi...");
    digitalWrite(RedLED,LOW);
    delay(100);
    digitalWrite(RedLED,HIGH);
    delay(100);
    
  }
 
  delay(100);
}
