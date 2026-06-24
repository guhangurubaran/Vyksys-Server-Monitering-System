import machine
import time
import dht
import network
import socket
from mpu6050 import MPU6050

# --- Configuration ---
WIFI_SSID = "Picnichome007"
WIFI_PASSWORD = "Picnichome15541"

# 1. Initialize Hardware
i2c = machine.I2C(0, scl=machine.Pin(2), sda=machine.Pin(1), freq=100000)
vibration_sensor = MPU6050(i2c)
climate_sensor = dht.DHT22(machine.Pin(3))

# 2. Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)

print("Connected! IP Address:", wlan.ifconfig()[0])

# 3. Set up Web Server Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# HTML Template for the dashboard
def get_html(temp, humid, mx, my, mz):
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>HVAC Telemetry</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="2"> <style>
            body {{ font-family: Arial, sans-serif; text-align: center; background: #f4f4f4; padding: 20px; }}
            .card {{ background: white; padding: 20px; margin: 15px auto; max-width: 400px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; }}
            p {{ font-size: 1.2em; color: #555; }}
        </style>
    </head>
    <body>
        <h1>Unified HVAC Monitoring</h1>
        <div class="card">
            <h2>🌍 Climate</h2>
            <p>Temperature: <strong>{temp:.1f}&deg;F</strong></p>
            <p>Humidity: <strong>{humid:.1f}%</strong></p>
        </div>
        <div class="card">
            <h2>🎛️ Vibration</h2>
            <p>X-Axis: <strong>{mx:.2f}g</strong></p>
            <p>Y-Axis: <strong>{my:.2f}g</strong></p>
            <p>Z-Axis: <strong>{mz:.2f}g</strong></p>
        </div>
    </body>
    </html>"""
    return html

# 4. Main Server Loop
while True:
    try:
        # Accept incoming browser connections
        conn, addr = s.accept()
        request = conn.recv(1024)
        
        # Read sensors
        try:
            climate_sensor.measure()
            temp_c = climate_sensor.temperature()
            temp_f = (temp_c * 9/5) + 32
            humidity = climate_sensor.humidity()
        except OSError:
            temp_f, humidity = 0.0, 0.0  # Fallback if sensor misbehaves
            
        motion = vibration_sensor.get_values()
        
        # Generate and send response
        response = get_html(temp_f, humidity, motion["AcX"], motion["AcY"], motion["AcZ"])
        conn.send('HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n')
        conn.sendall(response)
        conn.close()
        
    except Exception as e:
        print("Error handling request:", e)