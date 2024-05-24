import time
import urequests as requests
from pico_driver import OLED_2inch42
from machine import Pin, I2C, RTC
import usocket as socket
import struct
from wifi_connect import connect

# Initialize OLED display
OLED = OLED_2inch42()

# Connect to Wi-Fi
ip = connect()

# Set up API details
weather_api_url = "http://api.weatherapi.com/v1/current.json"
api_key = "your key here"
location = "your location here"

def get_weather():
    try:
        response = requests.get(f"{weather_api_url}?key={api_key}&q={location}&aqi=no")
        weather_data = response.json()
        temperature = weather_data["current"]["temp_c"]
        wind_direction = weather_data["current"]["wind_degree"]
        wind_speed = weather_data["current"]["wind_kph"]
        return temperature, wind_direction, wind_speed
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None, None, None

def set_time():
    NTP_DELTA = 2208988800
    host = "pool.ntp.org"

    def _ntp_time():
        try:
            addr = socket.getaddrinfo(host, 123)[0][-1]
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            msg = b'\x1b' + 47 * b'\0'
            s.sendto(msg, addr)
            msg, addr = s.recvfrom(48)
            s.close()
            val = struct.unpack("!I", msg[40:44])[0]
            return val - NTP_DELTA
        except:
            return None

    t = _ntp_time()
    if t:
        tm = time.localtime(t)
        RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
        print("Time set to:", tm)
    else:
        print("Failed to set time")

def display_data():
    # Set current time
    set_time()
    current_time = time.localtime()

    # Get weather data
    temperature, wind_direction, wind_speed = get_weather()

    # Clear the display
    OLED.fill(0)  # 0 is usually the color code for black in displays
    
    # Display time
    OLED.text(f"Time: {current_time[3]:02}:{current_time[4]:02}:{current_time[5]:02}", 0, 0, OLED.white)
    
    # Display temperature
    if temperature is not None:
        OLED.text(f"Temp: {temperature}C", 0, 20, OLED.white)
    
    # Display wind direction and speed
    if wind_direction is not None and wind_speed is not None:
        OLED.text(f"Wind: {wind_speed} kph", 0, 40, OLED.white)
        OLED.text(f"Dir: {wind_direction}°", 0, 50, OLED.white)
    
    # Update display
    OLED.show()

while True:
    display_data()
    time.sleep(60)  # Update every minute
