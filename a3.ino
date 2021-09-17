const int ledPin = 2;
const int ldrPin = A0;
const int tmpPin = A1;
float temp;
unsigned long previousTime = 0;
const unsigned long eventInterval = 10000;
char buffer[30];

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(ldrPin, INPUT);
  pinMode(tmpPin, INPUT);
}

void loop() {
  unsigned long currentTime = millis();
  if (currentTime-previousTime >= eventInterval){
    int lightData = analogRead(A0);
    int tempData = analogRead(A1);
    tempData = -(tempData * 110)/1023;
    //Serial.println(lightData);
    //Serial.println(tempData);
    
    sprintf(buffer,"IOT Reading (ldr,tmp): %04d,%04d",lightData,tempData);
    Serial.println(buffer);
    previousTime=currentTime;
  }

  int ldrStatus = analogRead(A0);
  int tmpStatus = analogRead(A1);

    if (Serial.available()>0){
     int lightStatus = Serial.parseInt();
     switch (lightStatus)
     {
      case 1:
        digitalWrite(2, HIGH);
        break;
      case 2:
        digitalWrite(2, LOW);
        break;
      default:
         break;
        }
      }
}
