#include <WiFi.h>
#include <WiFiUdp.h>
#include <FastLED.h>

#define LED_PIN 2  // Pin connected to the data line of the WS2812B
#define NUM_LEDS 900  // Total number of LEDs in the strip
#define NUM_BYTES 300  // Total number of LEDs in the strip
#define LED_TYPE WS2811
#define COLOR_ORDER BRG

CRGB leds[NUM_LEDS];
uint8_t Data[NUM_LEDS * 3];

const char* ssid = "lil"; // Replace with your network SSID
const char* password = "12345678an";           // Replace with your network password
const IPAddress staticIP(192, 168, 1, 234);   // Static IP for the ESP8266
const IPAddress gateway(192, 168, 1, 1);      // Default gateway
const IPAddress subnet(255, 255, 255, 0);      // Subnet mask

unsigned int localPort = 8266;  // Local port to listen for UDP packets
WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  
  // Set static IP
  WiFi.config(staticIP, gateway, subnet);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.print("ESP IP Address: ");
  Serial.println(WiFi.localIP());

  // Start UDP
  udp.begin(localPort);
  Serial.printf("Listening for UDP packets on port %d\n", localPort);

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(255);

  // Initialize all LEDs to be off
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    byte startByte = udp.read();
    
    if (startByte == 0xAA) {   // Check for sync byte (0xAA)
      udp.read(Data, NUM_BYTES * 3);  // Read RGB data
      
      for (int i = 0; i < NUM_BYTES; i++) {
        byte r = Data[i * 3];
        byte g = Data[i * 3 + 1];
        byte b = Data[i * 3 + 2];
        leds[i*3] = CRGB(r, g, b);  // Set color for LED
        leds[i*3+1] = CRGB(r, g, b);  // Set color for LED
        leds[i*3+2] = CRGB(r, g, b);  // Set color for LED
      }
      
      // for (int i = 0; i < NUM_LEDS; i++) {
      //   byte r = Data[i * 3];
      //   byte g = Data[i * 3 + 1];
      //   byte b = Data[i * 3 + 2];
      //   leds[i] = CRGB(r, g, b);  // Set color for LED
      // }

      FastLED.show();

      // // Send acknowledgment back to Python server
      // udp.beginPacket(udp.remoteIP(), udp.remotePort());
      // udp.write("ACK");
      // udp.write(Data);
      // udp.endPacket();
    }
  }
}