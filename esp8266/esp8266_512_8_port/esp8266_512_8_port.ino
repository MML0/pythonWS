  #include <FastLED.h>

  #define LED_PIN D2      // Pin connected to the data line of the WS2812B
  #define NUM_LEDS 512    // Total number of LEDs in the strip
  #define LED_TYPE WS2812B
  #define COLOR_ORDER GRB

  CRGB leds[NUM_LEDS];

  uint8_t Data[NUM_LEDS * (3)];

  void setup() {
    Serial.begin(2000000);  
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
    FastLED.setBrightness(9);

    // Initialize all LEDs to be off
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.show();  // Show initial LED state (off)
  }

  void loop() {
    if (Serial.available() > 0) {
      byte startByte = Serial.read();  // Read the synchronization byte
      if (startByte == 0xAA) {         // Check for sync byte (0xAA)
        Serial.readBytes(Data, NUM_LEDS * (3));

        for (int i = 0; i < NUM_LEDS; i++) {
          // Read 3 bytes for each LED (RGB values)
          byte r = Data[i*3];
          byte g = Data[i*3+1];
          byte b = Data[i*3+2];
          leds[i] = CRGB(r, g, b);  // Set color for LED
        }
        FastLED.show();  // Update the LED strip with new data
      }
    }
  }
