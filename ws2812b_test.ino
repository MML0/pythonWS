const int sensorPin = D1; // Pin connected to the sensor wire
const int ledPin = LED_BUILTIN; // Built-in LED pin
const int sampleSize = 10; // Number of samples for moving average
const int threshold = 1; // Change threshold for touch detection

long readings[sampleSize]; // Array for moving average
int readIndex = 0; // Current index for the readings
long total = 0; // Total of the readings
long lastReading = 0; // Last capacitance reading

void setup() {
  Serial.begin(115200);
  
  // Set up sensor and LED pins
  pinMode(sensorPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH); // Initialize LED off
  
  // Initialize readings to 0
  for (int i = 0; i < sampleSize; i++) {
    readings[i] = 0;
  }
}

void loop() {
  long capacitance = capacitiveSensor(sensorPin);
  
  // Update the moving average
  total -= readings[readIndex];
  readings[readIndex] = capacitance;
  total += readings[readIndex];
  readIndex = (readIndex + 1) % sampleSize;

  long averageCapacitance = total / sampleSize;

  // Calculate the rate of change
  long change = capacitance - averageCapacitance;

  // Print values for debugging
  Serial.print("Capacitance: ");
  Serial.print(capacitance);
  Serial.print(" | Average: ");
  Serial.print(averageCapacitance);
  Serial.print(" | Change: ");
  Serial.println(change);

  // Check for significant change and turn LED on or off
  if ((change) > threshold) {
    Serial.println("Touched!");
    digitalWrite(ledPin, LOW);  // Turn the LED on (LOW is on for built-in LED)
    delay(100);                 // Small delay for visual feedback
  } else {
    digitalWrite(ledPin, HIGH);  // Turn the LED off (HIGH is off for built-in LED)
  }

  delay(10); // Adjust the delay as needed
}

// Function to read capacitance
long capacitiveSensor(int pin) {
  long start = millis();
  long count = 0;

  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);
  delay(1);
  pinMode(pin, INPUT);
  
  while (digitalRead(pin) == HIGH) {
    count++;
    if (count > 10000) {
      break;
    }
  }
  
  return count;
}
