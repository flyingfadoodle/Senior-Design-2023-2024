#include <Servo.h>
Servo laserDoor;

#define fanPWM 6 // Pin for Controlling Fan PWM
#define laserDoorPin 9 // Laser Door Servo Pin


char messageChar; 
int pos = 0;

void setup() {
  Serial.begin(115200); // serial w/ baud rate 115200
  laserDoor.attach(laserDoorPin);
  laserDoor.write(0);
}

void loop() {
  if (Serial.available() > 0){
    // Read the incoming string
    String inputString = Serial.readStringUntil('\n');

    // Extract character from string
    sscanf(inputString.c_str(), "$ %c", &messageChar);
    // Serial.println(messageChar); // for debugging if necessary
  }

  // Door Open
  if (messageChar == 'O') {
    analogWrite(fanPWM, 0);
    delay(500);
    for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees 90 degrees in steps of 1 degree
      laserDoor.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }
    messageChar = 'D'; 
    Serial.println("door open");
    Serial.println("$D");
  }

  // Door Close
  if (messageChar == 'C') {
    analogWrite(fanPWM, 127);
    delay(250);
    for (pos = 180; pos >= 0; pos -= 1) { // goes from 90 degrees to 0 degrees in steps of 1 degree
      laserDoor.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }
    messageChar = 'D';
    Serial.println("door close");
    Serial.println("$D");
  }
}