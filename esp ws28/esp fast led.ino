#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <FastLED.h>

#define LED_PIN D2  // Pin connected to the data line of the WS2812B
#define NUM_LEDS 1024  // Total number of LEDs in the strip
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

#define T0H 350  // 350 ns for 0 high
#define T0L 900  // 900 ns for 0 low
#define T1H 700  // 700 ns for 1 high
#define T1L 550  // 550 ns for 1 low



CRGB leds[NUM_LEDS];

uint8_t Data[NUM_LEDS * (3)];

const char* ssid = "net emam limited edition";          // Replace with your network SSID
const char* password = "12345678an";  // Replace with your network password

unsigned int localPort = 8266;  // Local port to listen for UDP packets

WiFiUDP udp;
//byte packetBuffer[NUM_LEDS * (3)];  // Buffer to hold incoming data

void setup() {
  Serial.begin(115200);
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Start UDP
  udp.begin(localPort);
  Serial.printf("Listening for UDP packets on port %d\n", localPort);
  
  //pinMode(LED_PIN, OUTPUT);
  //digitalWrite(LED_PIN, LOW);  

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(9);

  // Initialize all LEDs to be off
  fill_solid(leds, NUM_LEDS, CRGB::Black);

  FastLED.show();
}



void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    // Read the sync byte first
    byte startByte = udp.read();
    
    if (startByte == 0xAA) {   // Check for sync byte (0xAA)
      // Read RGB data for NUM_LEDS
      udp.read(Data, NUM_LEDS * 3);  // Read the number of bytes (NUM_LEDS * 3 for RGB)
      //sendLEDData(); 
      // Loop through and set the LED colors
      for (int i = 0; i < NUM_LEDS; i++) {
        byte r = Data[i * 3];
        byte g = Data[i * 3 + 1];
        byte b = Data[i * 3 + 2];
        leds[i] = CRGB(r, g, b);  // Set color for LED
      }

      // // Update the LEDs with the new data
      FastLED.show();
    }
  }


}

