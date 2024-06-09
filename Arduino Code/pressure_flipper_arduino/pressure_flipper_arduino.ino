#include <Servo.h>
Servo flipperServo;
Servo pressureServo;

int flipper = 6;      // Flipper S(ervo Pin
int pressure = 4;     // Pressure Servo Pin
int solenoidPin = 3;  // Pressure Solenoid Pin

char messageChar;

void setup() {
  Serial.begin(115200);  // Serial for flipper
  flipperServo.attach(flipper);
  flipperServo.write(180);
  pressureServo.attach(pressure);
  pressureServo.write(90);
  pinMode(solenoidPin, OUTPUT);
  digitalWrite(solenoidPin, LOW);   
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming string
    String inputString = Serial.readStringUntil('\n');

    // Extract character from string)
    sscanf(inputString.c_str(), "$ %c", &messageChar);
    // Serial.println(messageChar);
  }
  
  // flipper station commands
  if (messageChar == 'F') {
    flipperServo.write(0); 
    delay(1000);
    flipperServo.write(180);
    delay(1000);
    messageChar = 'D';
    Serial.println("$D"); // message back to py script saying flipper sequence done
  }
  
  // pressure station commands
  if (messageChar == 'P') {
    digitalWrite(solenoidPin, HIGH); // press solenoid
    delay(1000);
    digitalWrite(solenoidPin, LOW); // lift solenoid
    delay(1000);
    pressureServo.write(0); // push coaster out w servo
    delay(2000);
    pressureServo.write(90); // return servo to original position
    delay(1000);
    messageChar = 'D';
    Serial.println("$D"); // message back to py script saying pressure sequence done
  } 
}
