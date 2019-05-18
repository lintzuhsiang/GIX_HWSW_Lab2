 int pedalPin = 7;
 int buttonPin = 6;
  int pedalState = 0;
  int pedalLastState = 0;
  int buttonState = 0;
  int GreenLED = 13;
  int RedLED = 12;
  int pedalCount = 0;
void setup() {
  Serial.begin(9600);
  pinMode(GreenLED,OUTPUT);
  pinMode(RedLED,OUTPUT);
  pinMode(pedalPin,INPUT_PULLUP);
  pinMode(buttonPin,INPUT_PULLUP);

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
    pedalCount = 0;
    Serial.println("button presses");
  }
  

}
