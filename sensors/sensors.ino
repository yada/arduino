#include <DHT.h>

// init var to avoid first read random values
float temperature = 0;
float humidity = 0;
int luminosity = 0;

// Sensors PINs setup for DHT11
const int DHT11_DataPin = 2;
DHT dht(DHT11_DataPin, DHT11);

// Sensors PINs setup for LUMINOSITY
const int LUMINOSITY_DataPin = A0;

void setup() {
  Serial.begin(9600);   // Start serial communication
  while (!Serial) { }  // Optional: wait for Serial (safe on Mega)

  dht.begin();
}

void loop() {
  // Read DHT11 values
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Read LUMINOSITY value
  luminosity = analogRead(LUMINOSITY_DataPin);
  
  // Print all values collected
  Serial.println(String(temperature) + "," + String(humidity) + "," + String(luminosity));

  // Sleep 2mins before looping again
  delay(120000);
}

