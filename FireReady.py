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

#WEATHER API 
# Set up API details - Change Location Here
weather_api_url = "http://api.weatherapi.com/v1/current.json"
api_key = "3ebf8bd03a9042e299b32549242804"
location = "Brisbane"

#TIMEZONE OFFSET 
# Brisbane timezone offset in seconds (UTC+10)
BRISBANE_OFFSET = 10 * 3600

#WEATHER API CALL
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

#TIME SETUP
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
            return val - NTP_DELTA + BRISBANE_OFFSET
        except:
            return None

    t = _ntp_time()
    if t:
        tm = time.localtime(t)
        RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
        print("Time set to:", tm)
    else:
        print("Failed to set time")

#WIND DATA SETUP

def degrees_to_compass(degrees):
    compass_brackets = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((degrees / 22.5) + 0.5) % 16
    return compass_brackets[index]

#MAIN CODE
def update_display(temperature, wind_direction, wind_speed):
    # Get current time
    current_time = time.localtime()

    # Clear the display
    OLED.fill(0)  # 0 is usually the color code for black in displays

    # Draw a rectangle around the edges of the screen
    OLED.rect(0, 0, 128, 64, OLED.white)

    # Display location
    OLED.text(location, 5, 18, OLED.white)

    #FIRING STATUS BASED OFF WIND DEGREES - SET WIND GO AND NO GO DEGREES HERE
    # Display firing status
    if wind_direction is not None:
        if 180 <= wind_direction <= 270:
            OLED.text("OK TO FIRE", 20, 30, OLED.white)
        else:
            OLED.text("DO NOT FIRE", 20, 30, OLED.white)
    
    # Display time
    OLED.text(f"{current_time[3]:02}:{current_time[4]:02}:{current_time[5]:02}", 5, 5, OLED.white)
    
    # Display temperature
    if temperature is not None:
        OLED.text(f"{temperature}C", 85, 5, OLED.white)
    
    # Display wind direction and speed
    if wind_direction is not None and wind_speed is not None:
        wind_compass = degrees_to_compass(wind_direction)
        OLED.text(f"Wind: {wind_speed} kph", 5, 40, OLED.white)
        OLED.text(f"Dir: {wind_compass} {wind_direction}deg", 5, 50, OLED.white)
    
    # Update display
    OLED.show()

#SET REFRESH INTERVALS
weather_update_interval = 600  # 10 minutes
time_update_interval = 3600    # 1 hour

last_weather_update = time.time() - weather_update_interval
last_time_update = time.time() - time_update_interval

temperature = None
wind_direction = None
wind_speed = None

while True:
    current_time = time.time()
    
    if current_time - last_time_update >= time_update_interval:
        set_time()
        last_time_update = current_time

    if current_time - last_weather_update >= weather_update_interval:
        temperature, wind_direction, wind_speed = get_weather()
        last_weather_update = current_time
    
    # Update display every minute
    update_display(temperature, wind_direction, wind_speed)
    time.sleep(1)  # Sleep for a minute before updating the display again
