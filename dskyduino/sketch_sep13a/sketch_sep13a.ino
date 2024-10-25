#include <GxEPD2_BW.h>
#include <Adafruit_GFX.h>

// E-ink display setup (for 2.9-inch Waveshare HAT)
GxEPD2_BW<GxEPD2_290, GxEPD2_290::HEIGHT> display(GxEPD2_290(/*CS=*/ 9, /*DC=*/ 8, /*RST=*/ 12, /*BUSY=*/ 13));

void setup() {
  Serial.begin(115200);
  while (!Serial);  // Wait for serial connection
  Serial.println("Starting e-ink display test...");

  // Initialize the display
  Serial.println("Attempting display init...");
  display.init();
  Serial.println("Display initialized");

  // Clear the screen to white
  display.fillScreen(GxEPD_WHITE);
  Serial.println("Screen cleared");
  
  // Set text properties
  display.setTextColor(GxEPD_BLACK);
  display.setCursor(10, 50);
  display.setTextSize(2);
  display.print("Hello, HAT!");

  // Refresh the display
  display.display(false);
  Serial.println("Display updated");

  delay(500);  // Allow time for e-ink refresh
  display.hibernate();  // Put display into low-power mode
  Serial.println("Display put to sleep.");
}

void loop() {
  // Nothing to do here
}
