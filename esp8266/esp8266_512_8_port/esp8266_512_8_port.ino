#include <FastLED.h>

#define LED_PIN D2  // Pin connected to the data line of the WS2812B
#define WS2811_MAT_PIN D1
#define WS2811_COL 32
#define WS2811_ROW 16
#define NUM_LEDS 512  // Total number of LEDs in the strip
#define LED_TYPE WS2812B
#define LED_TYPE_MAT WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];
CRGB ws_matrix[WS2811_COL];

uint8_t Data[NUM_LEDS * (3)];
uint16_t Mat_Data[WS2811_COL];

CLEDController *controller1;
CLEDController *controller2;

void setup() {
  Serial.begin(2000000);

  // Define 8 pins as inputs
  //pinMode(D1, INPUT);
  //pinMode(D2, INPUT);
  //pinMode(D3, INPUT);
  //pinMode(D4, INPUT);
  //pinMode(D5, INPUT);
  pinMode(D6, INPUT_PULLDOWN_16);
  //pinMode(D7, INPUT);
  //pinMode(D8, INPUT);


  // controller1 = &FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  // controller1->setCorrection(TypicalLEDStrip);  // Optional: Set color correction

  // // Initialize the second LED strip and store its controller
  // controller2 = &FastLED.addLeds<LED_TYPE_MAT, WS2811_MAT_PIN, COLOR_ORDER>(ws_matrix, WS2811_COL);
  // controller2->setCorrection(TypicalLEDStrip);  // Optional: Set color correction

  // // Set initial brightness levels
  // controller1->setBrightness(9);  // Set brightness for strip 1
  // controller2->setBrightness(9);  // Set brightness for strip 1



  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE_MAT, WS2811_MAT_PIN, COLOR_ORDER>(ws_matrix, WS2811_COL).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(9);
  // FastLED[1].setBrightness(12);

  // Initialize all LEDs to be off
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  fill_solid(ws_matrix, WS2811_COL, CRGB::Black);
  // controller1->show(); 
  // controller2->show(); 
  FastLED.show();
}

void loop() {
  for (int i = 0; i < WS2811_COL; i++) {
    fill_solid(ws_matrix, WS2811_COL, CRGB::Black);
    leds[i] = CRGB(255, 255, 255);  // Set color for LED
    //controller2->show(); 
    //FastLED.show();

    delayMicroseconds(1);
    uint16_t pinStates = 0;

    // Read pins and store their states in a 16-bit variable (bit-mapped)
    //pinStates |= (digitalRead(D1) << 0);    // Pin D1 as bit 0
    //pinStates |= (digitalRead(D2) << 1);    // Pin D2 as bit 1
    //pinStates |= (digitalRead(D3) << 2);    // Pin D3 as bit 2
    //pinStates |= (digitalRead(D4) << 3);    // Pin D4 as bit 3
    //pinStates |= (digitalRead(D5) << 4);    // Pin D5 as bit 4
    pinStates |= (digitalRead(D6) << 5);    // Pin D6 as bit 5
    //pinStates |= (digitalRead(D7) << 6);    // Pin D7 as bit 6
    //pinStates |= (digitalRead(D8) << 7);    // Pin D8 as bit 7
    //pinStates |= (digitalRead(D9) << 8);    // Pin D9 as bit 8
    //pinStates |= (digitalRead(D10) << 9);   // Pin D10 as bit 9
    //pinStates |= (digitalRead(D11) << 10);  // Pin D11 as bit 10
    //pinStates |= (digitalRead(D12) << 11);  // Pin D12 as bit 11
    //pinStates |= (digitalRead(D13) << 12);  // Pin D13 as bit 12
    //pinStates |= (digitalRead(D14) << 13);  // Pin D14 as bit 13
    //pinStates |= (digitalRead(D15) << 14);  // Pin D15 as bit 14
    //pinStates |= (digitalRead(D16) << 15);  // Pin D16 as bit 15
    Mat_Data[i] = pinStates;
  }

    Serial.write(0xAA);
    Serial.write((uint8_t*)Mat_Data, WS2811_COL * 2);  // Send all data in one go


  if (Serial.available() > 0) {
    byte startByte = Serial.read();  // Read the synchronization byte
    if (startByte == 0xAA) {         // Check for sync byte (0xAA)
      Serial.readBytes(Data, NUM_LEDS * (3));

      for (int i = 0; i < NUM_LEDS; i++) {
        // Read 3 bytes for each LED (RGB values)
        byte r = Data[i * 3];
        byte g = Data[i * 3 + 1];
        byte b = Data[i * 3 + 2];
        leds[i] = CRGB(r, g, b);  // Set color for LED
      }
      //controller1->show();
      FastLED.show();

    }
  }
}
