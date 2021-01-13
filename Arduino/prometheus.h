void prometheusPrintMetric(String label, String description, float value) {
  const String name = "arduino_" + label;

  Serial.println("# HELP " + name + " " + description);
  Serial.println("# TYPE " + name + " gauge");
  Serial.print(name + " "); Serial.println(value);
}

void prometheusDebug(String message) {
  // messages starting with this prefix shall be ignored by prometheus_exporter
  const String prefix = "DEBUG: ";
  Serial.println(prefix + message);
  Serial.flush();
}
