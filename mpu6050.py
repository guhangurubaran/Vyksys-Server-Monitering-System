import machine

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Wake up the MPU6050 (it starts in sleep mode)
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

    def get_raw_values(self):
        # Read 14 bytes of data starting from accelerometer register 0x3B
        return self.i2c.readfrom_mem(self.addr, 0x3B, 14)

    def get_values(self):
        raw = self.get_raw_values()
        # Convert bytes to signed 16-bit integers
        def to_int(high, low):
            val = (high << 8) | low
            return val if val < 32768 else val - 65536

        return {
            "AcX": to_int(raw[0], raw[1]) / 16384.0, # Convert to g-force
            "AcY": to_int(raw[2], raw[3]) / 16384.0,
            "AcZ": to_int(raw[4], raw[5]) / 16384.0,
            "Tmp": to_int(raw[6], raw[7]) / 340.0 + 36.53,
            "GyX": to_int(raw[8], raw[9]),
            "GyY": to_int(raw[10], raw[11]),
            "GyZ": to_int(raw[12], raw[13])
        }
