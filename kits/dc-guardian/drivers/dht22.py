#!/usr/bin/env python3
"""
DHT22 Temperature and Humidity Sensor Driver

Hardware connection:
  - VCC -> 3.3V
  - GND -> GND
  - DATA -> GP10 (with 10K pull-up resistor to 3.3V)

Usage:
    from dht22 import DHT22
    sensor = DHT22(pin=10)
    temp, humidity = sensor.read()
"""

import time
import machine
import ujson

class DHT22:
    def __init__(self, pin=10):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.last_reading = None
        
    def read(self):
        """Read temperature and humidity from DHT22 sensor."""
        try:
            # DHT22 requires a specific read sequence
            # Step 1: Send start signal
            pin = self.pin
            pin.init(machine.Pin.OUT)
            pin.value(0)
            time.sleep_ms(20)  # Pull low for at least 18ms
            
            # Step 2: Switch to input and wait for response
            pin.init(machine.Pin.IN, machine.Pin.PULL_UP)
            
            # Step 3: Read response signal
            timeout = 100  # 100us timeout
            while pin.value() == 1:
                timeout -= 1
                if timeout == 0:
                    return None, None
            
            # Step 4: Read 40 bits (5 bytes)
            data = []
            for i in range(40):
                while pin.value() == 0:
                    pass
                time.sleep_us(30)
                bit = pin.value()
                data.append(bit)
                while pin.value() == 1:
                    pass
            
            # Step 5: Parse data
            humidity = (data[0:16].count(1) / 16) * 100
            temperature = ((data[16:32].count(1) / 16) * 100) - 40
            
            self.last_reading = {
                'temperature': round(temperature, 1),
                'humidity': round(humidity, 1),
                'timestamp': time.time()
            }
            
            return temperature, humidity
            
        except Exception as e:
            print(f"DHT22 read error: {e}")
            return None, None
    
    def get_json(self):
        """Return last reading as JSON string."""
        return ujson.dumps(self.last_reading) if self.last_reading else '{}'


if __name__ == '__main__':
    sensor = DHT22(pin=10)
    print("DHT22 Temperature/Humidity Sensor Test")
    print("-" * 40)
    
    while True:
        temp, humidity = sensor.read()
        if temp is not None:
            print(f"Temperature: {temp:.1f}°C")
            print(f"Humidity: {humidity:.1f}%")
        else:
            print("Failed to read sensor")
        time.sleep(2)
