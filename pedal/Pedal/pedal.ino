int pedalPin = 7;
 int buttonPin = 6;
  int pedalState = 0;
  int pedalLastState = 0;
  int buttonState = 0;
  int GreenLED = 13;
  int RedLED = 12;
  int pedalCount = 0;
unsigned long pedaltime = 2000;

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#ifndef STASSID
#define STASSID "shine"
#define STAPSK  "11111111"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

void setup() {
  Serial.begin(115200);
  pinMode(GreenLED,OUTPUT);
  pinMode(RedLED,OUTPUT);
  pinMode(pedalPin,INPUT_PULLUP);
  pinMode(buttonPin,INPUT_PULLUP);
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


void loop() {
  pedalState = digitalRead(pedalPin);
  buttonState = digitalRead(buttonPin);
  
  Serial.println(pedalCount);
  if(pedalLastState != pedalState){
    if(pedalState==1){
      digitalWrite(GreenLED,HIGH);
      digitalWrite(RedLED,LOW);
    }else{
      
      digitalWrite(GreenLED,LOW);
      digitalWrite(RedLED,HIGH);
      pedalCount ++; 
    }
  }
  pedalLastState = pedalState;
  
  if(buttonState == 0){
    pedaltime = millis();
    if (buttonState == 0 and millis()-pedaltime > 2000){    //press reset button over two seconds
    pedalCount = 0;
    Serial.println("button presses");
   }
  }
   if(WiFi.status()==WL_CONNECTED){
    HTTPClient http;
    http.begin("http://jsonplaceholder.typicode.com/users");
//    http.begin("http://postman-echo.com/post");
    http.addHeader("Content-Type","text/plain");
//    http.addHeader("Content-Type","application/json");
   // String pedal_count; = "bar1";
   // String  = "bar2";
   // String string;
   // string = "pedal="+foo1+"&foo2="+foo2;
//    int httpCode = http.POST(string);
    int httpCode = http.POST("Message from ESP8266");
    String payload = http.getString();
    Serial.print("httpCode: ");
    Serial.println(httpCode);
    Serial.print("payload: ");
    Serial.println(payload);
    http.end();
  }else{
    Serial.println('error');
  }
  delay(30000);
}
