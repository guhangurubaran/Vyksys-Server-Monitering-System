import machine
import time

print("Initializing I2C Bus Scan...")

# Set up the I2C bus using your physical pins 1 and 2
i2c = machine.I2C(0, scl=machine.Pin(2), sda=machine.Pin(1), freq=100000)

# Scan for connected device addresses
devices = i2c.scan()

if len(devices) == 0:
    print("❌ No I2C devices found. Check sensor power connections.")
else:
    print(f"✅ Success! Found {len(devices)} I2C device(s).")
    for device in devices:
        print(f"Device detected at Hex Address: {hex(device)}")
        
        import machine
import time
from mpu6050 import MPU6050

# Re-initialize our verified I2C bus
i2c = machine.I2C(0, scl=machine.Pin(2), sda=machine.Pin(1), freq=100000)

# Initialize the sensor driver
sensor = MPU6050(i2c)

print("Starting Live Vibration Stream... Flick or tilt the sensor to see changes!")
time.sleep(1)

while True:
    data = sensor.get_values()
    # Print formatted G-forces on X, Y, and Z axes
    print("Vibration -> X: {:.2f}g | Y: {:.2f}g | Z: {:.2f}g".format(data["AcX"], data["AcY"], data["AcZ"]))
    time.sleep(1.0)




