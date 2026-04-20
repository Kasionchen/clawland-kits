#!/usr/bin/env python3
"""
MQ-2 Smoke/Combustible Gas Sensor Driver

Hardware connection:
  - VCC -> 5V
  - GND -> GND
  - AOUT -> GP26 (ADC pin)

Usage:
    from mq2_smoke import MQ2
    sensor = MQ2(pin=26)
    ppm = sensor.read()
"""

import machine
import ujson

class MQ2:
    # MQ-2 calibration values
    CLEAN_AIR_RL = 9.83  # Rs/Ro in clean air from datasheet
    
    def __init__(self, pin=26):
        self.adc = machine.ADC(machine.Pin(pin))
        self.adc.atten(machine.ADC.ATTN_11DB)  # Full range: 0-3.3V
        self Ro = 10.0  # Initialize Ro (will calibrate)
        self.last_reading = None
        
    def read_raw(self):
        """Read raw ADC value (0-4095 for 12-bit ADC)."""
        return self.adc.read()
    
    def read_voltage(self):
        """Read voltage (0.0 - 3.3V)."""
        raw = self.read_raw()
        return (raw / 4095.0) * 3.3
    
    def read_resistance(self):
        """Calculate sensor resistance in KOhm."""
        voltage = self.read_voltage()
        if voltage == 0:
            return float('inf')
        # Vcc = 5V, RL = 10K (load resistor)
        # Rs = ((5V - Vout) / Vout) * RL
        Rs = ((3.3 - voltage) / voltage) * 10.0
        return Rs
    
    def read_ppm(self):
        """Read gas concentration in PPM (parts per million)."""
        try:
            Rs = self.read_resistance()
            if Rs <= 0 or self.Ro <= 0:
                return 0
            
            # Calculate ratio Rs/Ro
            ratio = Rs / self.Ro
            
            # Convert ratio to PPM using simplified formula
            # Based on MQ-2 datasheet curve
            # Different gases have different curves:
            # LPG: y = 1000 * x^-2.1
            # Propane: y = 400 * x^-2.1
            # Smoke: y = 600 * x~-2.1
            
            # Use smoke curve as general indicator
            if ratio < 0.5:
                return 0
            
            # Simplified PPM calculation
            ppm = 1000 * (ratio ** -2.1)
            
            ppm = max(0, min(ppm, 10000))  # Clamp to sensor range
            
            self.last_reading = {
                'ppm': round(ppm, 1),
                'ratio': round(ratio, 3),
                'timestamp': 0  # Would use time module in actual implementation
            }
            
            return ppm
            
        except Exception as e:
            print(f"MQ2 read error: {e}")
            return 0
    
    def calibrate(self, samples=100):
        """Calibrate sensor Ro in clean air (call in fresh air)."""
        print("Calibrating MQ-2 in clean air...")
        readings = []
        for _ in range(samples):
            readings.append(self.read_resistance())
            # Small delay between readings
            for _ in range(100):
                pass
        
        self.Ro = sum(readings) / len(readings)
        print(f"Calibration complete. Ro = {self.Ro:.2f} KOhm")
        return self.Ro
    
    def get_json(self):
        """Return last reading as JSON string."""
        return ujson.dumps(self.last_reading) if self.last_reading else '{}'


if __name__ == '__main__':
    sensor = MQ2(pin=26)
    print("MQ-2 Smoke/Gas Sensor Test")
    print("-" * 40)
    print("Note: For accurate readings, calibrate first!")
    print()
    
    # Try to calibrate (call this in fresh air)
    # sensor.calibrate()
    
    while True:
        raw = sensor.read_raw()
        voltage = sensor.read_voltage()
        ppm = sensor.read_ppm()
        
        print(f"Raw ADC: {raw}")
        print(f"Voltage: {voltage:.3f}V")
        print(f"Smoke: {ppm:.1f} PPM")
        print("-" * 40)
        
        # Small delay
        for _ in range(100000):
            pass
