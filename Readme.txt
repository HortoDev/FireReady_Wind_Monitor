FireReady Weather Monitor


Overview
  The FireReady Weather Monitor is designed for mining operations near towns and other infrastructure. It is crucial to ensure that dust and firing fumes move away from populated areas. This simple display provides real-time weather information, including temperature and wind direction, along with a handy "OK TO FIRE" or "DO NOT FIRE" message based on wind conditions.


Features
  Real-time Clock: Displays the current time.
  Temperature Display: Shows the current temperature.
  Wind Information: Provides wind speed and direction.
  Firing Status Alert: Displays "OK TO FIRE" when the wind direction is between 180° and 270° and "DO NOT FIRE" otherwise.
  Simple and Clear Interface: Easy-to-read OLED display.

How It Works
  The display uses a free weather API from WeatherAPI.com to fetch the latest weather data. The firing status alert helps ensure safe mining operations by indicating whether it is safe to fire based on wind direction.

Hardware Requirements
  Raspberry Pi Pico W
  128x64 OLED Display (SSD1309)
  Wi-Fi connection

Software Requirements
  MicroPython
  urequests library for making HTTP requests
  wifi_connect.py script for connecting to Wi-Fi

Setup and Usage
  Hardware Setup
    Connect the 128x64 OLED display to the Raspberry Pi Pico W according to your specific wiring configuration.

Software Setup
  Clone the Repository
    git clone https://github.com/yourusername/FireReady-Weather-Monitor.git
    cd FireReady-Weather-Monitor

Upload Code to Raspberry Pi Pico W
  Use an appropriate tool like Thonny to upload the following files to your Raspberry Pi Pico W:
    main.py (the main script)
    wifi_connect.py (Wi-Fi connection script)
    urequests.py (download from MicroPython-lib)


Update Location and API Key
  Edit main.py to update the location and API key

After uploading the files and making the necessary updates, run the main.py script on your Raspberry Pi Pico W.

Code Explanation
  Here is an overview of the main components of the code:
    Weather API Integration: Fetches weather data using the WeatherAPI.
    Time Synchronization: Sets the local time using an NTP server.
    OLED Display Updates: Updates the OLED display with the latest time, temperature, wind speed, and direction.
    Firing Status Alert: Displays "OK TO FIRE" or "DO NOT FIRE" based on wind direction.

Customization
  Update Firing Conditions: Modify the conditions for displaying "OK TO FIRE" or "DO NOT FIRE" by changing the range of wind direction degrees in the code.
  Change Location: Update the location variable in the code to fetch weather data for a different location.

License
  This project is licensed under the MIT License.

By Chris Horton
