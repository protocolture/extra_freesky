#include <WiFi.h>  // WiFi.h for Pico W from the Earle Philhower RP2040 core
#include <GxEPD2_BW.h>
#include <Adafruit_GFX.h>

// E-ink display setup (for 2.9-inch Waveshare)
GxEPD2_BW<GxEPD2_290, GxEPD2_290::HEIGHT> display(GxEPD2_290(/*CS=*/ 9, /*DC=*/ 8, /*RST=*/ 12, /*BUSY=*/ 7));

// Wi-Fi Credentials
const char* ssid = "your-ssid";
const char* password = "your-password";

// Wi-Fi server on port 80
WiFiServer server(80);

// Function to display a message on the e-ink display
void displayMessage(String message) {
  display.init();
  display.setRotation(1);
  display.fillScreen(GxEPD_WHITE);
  
  // Display the message
  display.setTextColor(GxEPD_BLACK);
  display.setCursor(10, 50);  // Position in the center area
  display.setTextSize(2);
  display.print(message);
  
  display.display(false);  // Refresh the display
  display.hibernate();     // Put display in low-power mode
}

// Function to connect to Wi-Fi with a message if it fails
bool connectToWiFi() {
  Serial.print("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  
  int retryCount = 0;
  int maxRetries = 20; // Max retry attempts before failure
  
  while (WiFi.status() != WL_CONNECTED && retryCount < maxRetries) {
    delay(1000);
    Serial.print(".");
    retryCount++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connected to Wi-Fi");
    Serial.println(WiFi.localIP());
    return true;
  } else {
    Serial.println("Wi-Fi Connection Failed");
    displayMessage("Wi-Fi Connection Failed");  // Display the failure message
    return false;
  }
}

// Function to update the display with percentage and message
void updateDisplay(int value, String message) {
  // Clear the display
  display.init();
  display.setRotation(1);
  display.fillScreen(GxEPD_WHITE);
  
  // Calculate reverse percentage
  int remainingPercentage = 100 - value;
  int progressBarWidth = map(remainingPercentage, 0, 100, 0, 128); // Scale to display width
  
  // Draw progress bar
  display.fillRect(10, 50, progressBarWidth, 20, GxEPD_BLACK);
  
  // Display remaining percentage text
  display.setTextColor(GxEPD_BLACK);
  display.setCursor(10, 10);
  display.setTextSize(2);
  display.print("Remaining: ");
  display.print(remainingPercentage);
  display.println("%");
  
  // Display warning message
  display.setCursor(10, 80);
  display.setTextSize(1);
  display.print(message);
  
  display.display(false);  // Refresh display
  display.hibernate();     // Put display in low-power mode
}

void setup() {
  Serial.begin(115200);
  
  // Display "Initializing" on the screen
  displayMessage("Initializing...");
  
  // Attempt to connect to Wi-Fi
  if (!connectToWiFi()) {
    // Stop further execution if Wi-Fi connection fails
    while (true) {
      delay(1000);
    }
  }
  
  // Start server if Wi-Fi connection is successful
  server.begin();
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.accept();  // Updated to use accept() instead of available()
  
  if (client) {
    Serial.println("Client connected");
    String request = client.readStringUntil('\r');
    client.flush();
    
    // Parse value and message from request (assuming POST request format)
    int valueIndex = request.indexOf("value=");
    int messageIndex = request.indexOf("message=");
    
    if (valueIndex != -1 && messageIndex != -1) {
      String valueStr = request.substring(valueIndex + 6, request.indexOf('&', valueIndex));
      String messageStr = request.substring(messageIndex + 8);
      
      int value = valueStr.toInt();  // Convert value to integer
      
      // Update display
      updateDisplay(value, messageStr);
    }
    
    // Send HTTP response to client
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println();
    client.println("<h1>Update Received</h1>");
    client.stop();
  }
}
