#!/usr/bin/env python3
"""
Water Leak Sensor Driver

Hardware connection:
  - VCC -> 3.3V
  - GND -> GND
  - Signal -> GP11 (with internal pull-down)

Usage:
    from water_leak import WaterLeakSensor
    sensor = WaterLeakSensor(pin=11)
    is_leaking = sensor.read()
"""

import machine
import ujson

class WaterLeakSensor:
    def __init__(self, pin=11):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.last_reading = None
        
    def read(self):
        """Read water leak sensor state.
        
        Returns:
            bool: True if water detected, False otherwise
        """
        try:
            value = self.pin.value()
            is_leaking = value == 1
            
            self.last_reading = {
                'leak_detected': is_leaking,
                'timestamp': 0  # Would use time module in actual implementation
            }
            
            return is_leaking
            
        except Exception as e:
            print(f"Water leak sensor error: {e}")
            return False
    
    def is_leaking(self):
        """Alias for read() for clearer API."""
        return self.read()
    
    def get_json(self):
        """Return last reading as JSON string."""
        return ujson.dumps(self.last_reading) if self.last_reading else '{}'


if __name__ == '__main__':
    sensor = WaterLeakSensor(pin=11)
    print("Water Leak Sensor Test")
    print("-" * 40)
    print("Place sensor contacts in water to test...")
    print()
    
    while True:
        if sensor.read():
            print("💧 WATER LEAK DETECTED!")
        else:
            print("✓ No water detected")
        
        # Small delay
        for _ in range(500000):
            pass
