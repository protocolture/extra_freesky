#include <WiFi.h>
#include <TFT_eSPI.h>
#include <WebServer.h>
#include <Wire.h>
#include <CST816S.h>

// Wi-Fi credentials
const char* ssid = "";
const char* password = "";

// Create instances for TFT display and WebServer
TFT_eSPI tft = TFT_eSPI();
WebServer server(80);

// CST816S touch controller setup
CST816S touch(6, 7, 13, 5);  // SDA = 6, SCL = 7, RST = 13, IRQ = 5

// Variables for O2, Degrees Celsius, Suit Integrity, and External Pressure
float o2 = 21.0;  // O2 percentage
int degreesCelsius = 25;  // Degrees Celsius (-10 to 250 range)
bool suitIntegrity = true;  // Suit integrity: true (green), false (red)
bool externalPressure = true;  // External pressure: true (green), false (red)

// Screen state tracking and touch cooldown
int currentScreen = 0;  // 0: O2, 1: Temperature, 2: Suit Integrity, 3: External Pressure
unsigned long lastTouchTime = 0;  // Track time of last touch

// Function to initialize the CST816S touch controller
void initTouchController() {
  Wire.begin(6, 7);  // Set up I2C with SDA = 6, SCL = 7
  touch.begin();     // Initialize the CST816S touch controller
  Serial.println("CST816S touch controller initialized.");
}

// Function to check for touch events from the CST816S controller
bool getTouch() {
  unsigned long currentTime = millis();
  if (currentTime - lastTouchTime >= 2000 && touch.available()) {  // 1-2 sec cooldown
    lastTouchTime = currentTime;
    return true;
  }
  return false;
}

// Function to handle POST requests for setting variables
// Function to handle POST requests for setting variables
void handleSetVariables() {
  bool refreshNeeded = false;

  // Update O2 level
  if (server.hasArg("o2")) {
    o2 = server.arg("o2").toFloat();
    refreshNeeded = true;
  }

  // Update temperature
  if (server.hasArg("temp")) {
    degreesCelsius = server.arg("temp").toInt();
    refreshNeeded = true;
  }

  // Update suit integrity
  if (server.hasArg("suit")) {
    suitIntegrity = server.arg("suit").toInt() == 1;
    refreshNeeded = true;
  }

  // Update external pressure
  if (server.hasArg("pressure")) {
    externalPressure = server.arg("pressure").toInt() == 1;
    refreshNeeded = true;
  }

  // Send confirmation response
  server.send(200, "application/json", "{\"status\":\"Variables updated\"}");

  // Refresh the current screen if any values were updated
  if (refreshNeeded) {
    switch (currentScreen) {
      case 0:
        drawO2Screen();
        break;
      case 1:
        drawTemperatureScreen();
        break;
      case 2:
        drawSuitIntegrityScreen();
        break;
      case 3:
        drawExternalPressureScreen();
        break;
    }
  }
}


// Function to simulate the BIOS loading screen
void showLoadingScreen() {
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_ORANGE);  // Set text color to amber
  tft.setTextSize(1);  // Reduced font size

  const char* messages1[] = {
    " Loading Weyland Yutani SUITOS....",
    " 64K RAM Detected...",
    " 40MHz Processor Ready...",
    " SUITOS NOMINAL."
  };

  for (int i = 0; i < 4; i++) {
    int x = (tft.width() - 240) / 2 + 8;  // Center the text, shift right by 8
    int y = (tft.height() / 2) + (i * 30) - (4 * 15);  // Adjust y position
    tft.setCursor(x, y);
    tft.println(messages1[i]);
    delay(1500);  // Simulate loading time
  }

  tft.fillScreen(TFT_BLACK);

  const char* messages2[] = {
    " Running Self-Diagnostics...",
    " Initializing Pressure Sensors...",
    " Initializing Suit Integrity..."
  };

  for (int i = 0; i < 3; i++) {
    int x = (tft.width() - 240) / 2 + 8;  // Center the text and shift right by 8
    int y = (tft.height() / 2) + (i * 30) - (4 * 15);  // Adjust y position
    tft.setCursor(x, y);
    tft.println(messages2[i]);
    delay(1500);  // Simulate loading time
  }

  tft.fillScreen(TFT_BLACK);

  const char* messages3[] = {
    " Tests Passed: Seals Integrity OK.",
    " Tests Passed: Suit Condition OK.",
    " Tests Passed: Pressure Levels OK."
  };

  for (int i = 0; i < 3; i++) {
    int x = (tft.width() - 240) / 2 + 8;  // Center the text and shift right by 8
    int y = (tft.height() / 2) + (i * 30) - (4 * 15);  // Adjust y position
    tft.setCursor(x, y);
    tft.println(messages3[i]);
    delay(1500);  // Simulate loading time
  }

  tft.fillScreen(TFT_BLACK);

  tft.setCursor(36, 100);  // Adjusted to shift right by 8 total
  tft.println(" System Check Complete!");
  tft.setCursor(36, 130);
  tft.println(" Booting...");

  // Blink the last dot for "Booting..."
  for (int j = 0; j < 3; j++) {
    delay(250);
    tft.setCursor(36 + strlen("Booting...") * 6, 130);  // Position the cursor at the end of the message
    tft.print(".");  // Print the dot
    delay(250);
    tft.fillRect(36 + strlen("Booting...") * 6, 130, 10, 10, TFT_BLACK);  // Clear the dot
  }

  // Wait 10 seconds after "Booting..."
  delay(10000);

  tft.fillScreen(TFT_BLACK);  // Clear the screen after loading
}

// Function to get the color for the O2 progress bar based on percentage
uint16_t getO2Color(float percentage) {
  if (percentage >= 75) return TFT_BLUE;
  if (percentage >= 50) return TFT_GREEN;
  if (percentage >= 25) return TFT_YELLOW;
  if (percentage >= 5) return TFT_ORANGE;
  return TFT_RED;
}

// Function to get the color for the temperature ring based on degrees Celsius (-10 to 250)
uint16_t getTempColor(int temperature) {
  int colorRange = map(temperature, -10, 250, 0, 255);  // Map the temperature to a range of 0 (cold) to 255 (hot)
  return tft.color565(colorRange, 0, 255 - colorRange); // Blue to Red transition
}

// Function to draw the O2 screen with a circular progress bar
void drawO2Screen() {
  tft.fillScreen(TFT_BLACK);

  int centerX = 120;
  int centerY = 120;
  int radius = 110;
  int thickness = 15;

  uint16_t o2Color = getO2Color(o2);

  int startAngle = 0;
  int endAngle = map(o2, 0, 100, 0, 360);
  tft.drawArc(centerX, centerY, radius, radius - thickness, startAngle, endAngle, o2Color, TFT_BLACK, false);
  
  tft.setTextColor(TFT_ORANGE, TFT_BLACK);  // Set text color to amber
  tft.setCursor(centerX - 30, centerY - 10);
  tft.setTextSize(2);
  tft.printf("%.1f%% O2", o2);
}

// Function to draw the temperature screen with a circular progress bar (-10 to 250°C)
void drawTemperatureScreen() {
  tft.fillScreen(TFT_BLACK);

  int centerX = 120;
  int centerY = 120;
  int radius = 110;
  int thickness = 15;

  uint16_t tempColor = getTempColor(degreesCelsius);

  int startAngle = 0;
  int endAngle = map(degreesCelsius, -10, 250, 0, 360);
  tft.drawArc(centerX, centerY, radius, radius - thickness, startAngle, endAngle, tempColor, TFT_BLACK, false);
  
  tft.setTextColor(TFT_ORANGE, TFT_BLACK);  // Set text color to amber
  tft.setCursor(centerX - 50, centerY - 10);
  tft.setTextSize(2);
  tft.printf("%dC Temp", degreesCelsius);
}

// Function to draw the suit integrity screen with a green/red ring
void drawSuitIntegrityScreen() {
  tft.fillScreen(TFT_BLACK);

  int centerX = 120;
  int centerY = 120;
  int radius = 110;
  int thickness = 15;

  uint16_t suitColor = suitIntegrity ? TFT_GREEN : TFT_RED;

  tft.drawArc(centerX, centerY, radius, radius - thickness, 0, 360, suitColor, TFT_BLACK, false);
  
  tft.setTextColor(TFT_ORANGE, TFT_BLACK);  // Set text color to amber
  tft.setCursor(centerX - 50, centerY - 10);
  tft.setTextSize(1);  // Reduced font size
  tft.println("Suit Integrity");
}

// Function to draw the external pressure screen with a green/red ring
void drawExternalPressureScreen() {
  tft.fillScreen(TFT_BLACK);

  int centerX = 120;
  int centerY = 120;
  int radius = 110;
  int thickness = 15;

  uint16_t pressureColor = externalPressure ? TFT_GREEN : TFT_RED;

  tft.drawArc(centerX, centerY, radius, radius - thickness, 0, 360, pressureColor, TFT_BLACK, false);
  
  tft.setTextColor(TFT_ORANGE, TFT_BLACK);  // Set text color to amber
  tft.setCursor(centerX - 60, centerY - 10);
  tft.setTextSize(1);  // Reduced font size
  tft.println("External Pressure");
}

// Function to rotate between screens on touch
void rotateScreen() {
  currentScreen = (currentScreen + 1) % 4;  // Cycle between 0, 1, 2, and 3
  
  switch (currentScreen) {
    case 0:
      drawO2Screen();
      break;
    case 1:
      drawTemperatureScreen();
      break;
    case 2:
      drawSuitIntegrityScreen();
      break;
    case 3:
      drawExternalPressureScreen();
      break;
  }
}

// Function to check touch input from the CST816S controller
void checkTouchInput() {
  if (getTouch()) {  // Check if the screen is tapped with a cooldown
    rotateScreen();  // Rotate screens on touch
  }
}

void setup() {
  // Initialize the serial monitor and display
  Serial.begin(115200);
  tft.init();
  tft.setRotation(3);  // Set rotation to position 3
  tft.fillScreen(TFT_BLACK);

  // Initialize the CST816S touch controller
  initTouchController();

  // Show loading screen
  showLoadingScreen();

  // Connect to Wi-Fi
  tft.setTextColor(TFT_ORANGE, TFT_BLACK);  // Set text color to amber
  tft.setCursor(20, 250);
  tft.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    tft.print(".");  // Show dots on the display as progress
  }

  // Display the connected status
  tft.fillScreen(TFT_BLACK);
  tft.setCursor(20, 50);
  tft.println("Connected!");
  tft.println(WiFi.localIP());

  // Start the web server and configure the POST route
  server.on("/set", HTTP_POST, handleSetVariables);  // Handle POST requests to update variables
  server.begin();
  Serial.println("Web server started!");

  // Start with the O2 screen
  drawO2Screen();
}

void loop() {
  // Handle client requests
  server.handleClient();

  // Check if the screen was tapped
  checkTouchInput();
}
