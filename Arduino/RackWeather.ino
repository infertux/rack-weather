/*
  MKR ENV Shield - Read Sensors

  This reads the sensors on-board the MKR ENV shield
  and prints them to the Serial Monitor.

  The circuit:
  - Arduino MKR board
  - Arduino MKR ENV Shield attached
*/

#include <Arduino_MKRENV.h>
#include "prometheus.h"

const int loopDelay = 15; // in seconds

volatile int counter = 0;

void setup() {
  Serial.begin(115200);

  if (!ENV.begin()) {
    while (!Serial);
    Serial.println("Failed to initialize MKR ENV shield!");
    while (1);
  }
}

void loop() {
  prometheusDebug("counter = " + String(counter));

  float temperature = ENV.readTemperature();
  temperature -= 0.5; // XXX: calibration

  float humidity    = ENV.readHumidity();
  float pressure    = ENV.readPressure(MILLIBAR);
  float illuminance = ENV.readIlluminance();

  prometheusPrintMetric("temperature_celsius", "Temperature", temperature);
  prometheusPrintMetric("humidity_percent", "Relative humidity", humidity);
  prometheusPrintMetric("pressure_pascals", "Pressure", pressure);
  prometheusPrintMetric("illuminance_lux", "Illuminance", illuminance);
  // prometheusPrintMetric("fan_status{id=\"medium\"}", "", 1);
  Serial.println(); // tell web server this is the end of the HTTP response
  Serial.flush(); // we're getting truncated buffered output at times without this

  counter++;

  delay(loopDelay*1000);
}
