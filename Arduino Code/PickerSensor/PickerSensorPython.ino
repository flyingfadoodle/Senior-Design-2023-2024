#include <Arduino.h>
#include <Wire.h>
#include <vl53l4cd_class.h>

#define DEV_I2C Wire
#define SerialPort Serial
#define MEASUREMENTS 10  // Number of measurements to take

VL53L4CD sensor_vl53l4cd_sat(&DEV_I2C, A1);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  SerialPort.begin(115200);
  while (!SerialPort); // Wait for Serial port to connect
  SerialPort.println("Sensor Ready...");

  DEV_I2C.begin();

  sensor_vl53l4cd_sat.begin();
  sensor_vl53l4cd_sat.VL53L4CD_Off();
  sensor_vl53l4cd_sat.InitSensor();
  sensor_vl53l4cd_sat.VL53L4CD_SetRangeTiming(200, 0);
}

void loop() {
  if (SerialPort.available()) {
    String command = SerialPort.readStringUntil('\n');
    if (command == "$M") {
      float totalDistance = 0;
      int validMeasurements = 0;

      for (int i = 0; i < MEASUREMENTS; ++i) {
        sensor_vl53l4cd_sat.VL53L4CD_StartRanging();
        
        uint8_t NewDataReady = 0;
        VL53L4CD_Result_t results;
        uint8_t status;

        // Wait for new data to be ready
        do {
          status = sensor_vl53l4cd_sat.VL53L4CD_CheckForDataReady(&NewDataReady);
        } while (!NewDataReady);

        digitalWrite(LED_BUILTIN, HIGH); // LED on

        sensor_vl53l4cd_sat.VL53L4CD_GetResult(&results);
        sensor_vl53l4cd_sat.VL53L4CD_ClearInterrupt(); // Clear interrupt for next measurement

        digitalWrite(LED_BUILTIN, LOW); // LED off

        if ((!status) && (NewDataReady != 0) && (results.range_status == 0)) {
          totalDistance += results.distance_mm;
          ++validMeasurements;
        }

        sensor_vl53l4cd_sat.VL53L4CD_StopRanging(); // Stop ranging

        // Wait for a bit to spread the measurements over 1 second
        delay(25); // This delay may need adjustment for precise timing
      }

      if (validMeasurements > 0) {
        float averageDistance = totalDistance / validMeasurements;
        SerialPort.print("$M");
        SerialPort.println(averageDistance);
      } else {
        SerialPort.println("Measurement Error");
      }

      SerialPort.println("$D"); // Indicate to the PC that the measurements are complete
    }
  }
}
