
#define CH1 8 //Connect pin 8 to Night light
#define CH2 7 //Connect pin 7 to Day light
#define CH3 10 //testing setting dummy value to turn off lights

char rx_byte;

void setup() {
  Serial.begin(9600);
  
  pinMode(CH1, OUTPUT);
  pinMode(CH2, OUTPUT);
  pinMode(CH3, OUTPUT);
  
  digitalWrite(CH1, HIGH);
  digitalWrite(CH2, HIGH);
  digitalWrite(CH3, LOW);
}

void loop() {
  if (Serial.available() > 0) { //Checking if character is available
    rx_byte = Serial.read();
    
  }
  changeLight();
}

void changeLight() {
  if (rx_byte == '1') {
      digitalWrite(CH1, HIGH);
      digitalWrite(CH2, LOW);
      digitalWrite(CH3, HIGH);
    }
    
    else if (rx_byte == '2') {
      digitalWrite(CH1, LOW);
      digitalWrite(CH2, HIGH);
      digitalWrite(CH3, HIGH);
    }
    
    else if (rx_byte == '3') {
      digitalWrite(CH1, HIGH);
      digitalWrite(CH2, LOW);
      digitalWrite(CH3, HIGH);
    }
    
    else if (rx_byte == '4') {
      digitalWrite(CH1, HIGH);
      digitalWrite(CH2, HIGH);
      digitalWrite(CH3, LOW);
    }
    
    else { 
      ;
    }
}

