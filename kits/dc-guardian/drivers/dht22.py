#!/usr/bin/env python3
"""
DHT22 Temperature & Humidity Sensor Driver for PicoClaw

Author: Clawland Community
License: MIT
"""

import time
import board
import adafruit_dht
from typing import Tuple, Optional


class DHT22Sensor:
    """
    DHT22/AM2302 Temperature & Humidity Sensor Driver

    Features:
    - Temperature range: -40°C to 80°C (±0.5°C)
    - Humidity range: 0-100% RH (±2%)
    - Sampling rate: 0.5 Hz (every 2 seconds)
    """

    def __init__(self, pin: int = 4):
        """
        Initialize DHT22 sensor

        Args:
            pin: GPIO pin number (default: 4)
        """
        self.pin = pin
        self.sensor = None
        self.last_read_time = 0
        self.min_interval = 2.0  # Minimum 2 seconds between reads

        try:
            # Map GPIO pin to board pin
            pin_map = {
                4: board.D4,
                5: board.D5,
                6: board.D6,
                12: board.D12,
                13: board.D13,
                16: board.D16,
                17: board.D17,
                18: board.D18,
                19: board.D19,
                20: board.D20,
                21: board.D21,
                22: board.D22,
                23: board.D23,
                24: board.D24,
                25: board.D25,
                26: board.D26,
                27: board.D27,
            }

            board_pin = pin_map.get(pin)
            if board_pin is None:
                raise ValueError(f"Unsupported GPIO pin for DHT22: {pin}")
            self.sensor = adafruit_dht.DHT22(board_pin, use_pulseio=False)

        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to initialize DHT22 on pin {pin}: {e}")

    def read(self) -> Tuple[Optional[float], Optional[float]]:
        """
        Read temperature and humidity from sensor

        Returns:
            Tuple of (temperature_celsius, humidity_percent)
            Returns (None, None) if read fails
        """
        # Enforce minimum interval between reads
        current_time = time.time()
        time_since_last = current_time - self.last_read_time

        if time_since_last < self.min_interval:
            time.sleep(self.min_interval - time_since_last)

        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            self.last_read_time = time.time()

            return temperature, humidity

        except RuntimeError as e:
            # DHT sensors often fail to read, retry is normal
            print(f"DHT22 read error: {e}")
            return None, None

        except Exception as e:
            print(f"DHT22 unexpected error: {e}")
            return None, None

    def read_temperature(self) -> Optional[float]:
        """Read temperature only (Celsius)"""
        temp, _ = self.read()
        return temp

    def read_humidity(self) -> Optional[float]:
        """Read humidity only (percent)"""
        _, humidity = self.read()
        return humidity

    def read_fahrenheit(self) -> Optional[float]:
        """Read temperature in Fahrenheit"""
        temp_c, humidity = self.read()
        if temp_c is not None:
            return temp_c * 9/5 + 32
        return None

    def get_status(self) -> dict:
        """
        Get sensor status and readings

        Returns:
            Dict with temperature, humidity, and status
        """
        temp, humidity = self.read()

        status = {
            "sensor": "DHT22",
            "pin": self.pin,
            "temperature_celsius": temp,
            "temperature_fahrenheit": temp * 9/5 + 32 if temp is not None else None,
            "humidity_percent": humidity,
            "timestamp": time.time(),
            "status": "ok" if temp is not None and humidity is not None else "error"
        }

        return status

    def check_thresholds(self, temp_high: float = 30.0, temp_low: float = 18.0,
                        humidity_high: float = 70.0, humidity_low: float = 30.0) -> dict:
        """
        Check if readings exceed thresholds

        Args:
            temp_high: High temperature threshold (°C)
            temp_low: Low temperature threshold (°C)
            humidity_high: High humidity threshold (%)
            humidity_low: Low humidity threshold (%)

        Returns:
            Dict with alert status
        """
        temp, humidity = self.read()

        alerts = {
            "temperature_high": temp > temp_high if temp is not None else False,
            "temperature_low": temp < temp_low if temp is not None else False,
            "humidity_high": humidity > humidity_high if humidity is not None else False,
            "humidity_low": humidity < humidity_low if humidity is not None else False,
            "current_temperature": temp,
            "current_humidity": humidity,
            "thresholds": {
                "temp_high": temp_high,
                "temp_low": temp_low,
                "humidity_high": humidity_high,
                "humidity_low": humidity_low
            }
        }

        return alerts

    def close(self):
        """Clean up sensor resources"""
        if self.sensor:
            try:
                self.sensor.exit()
            except:
                pass

    def __del__(self):
        """Destructor - ensure cleanup"""
        self.close()


# CLI interface for testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DHT22 Sensor Driver")
    parser.add_argument("--pin", type=int, default=4, help="GPIO pin number")
    parser.add_argument("--continuous", action="store_true", help="Continuous reading")
    parser.add_argument("--interval", type=float, default=5.0, help="Read interval (seconds)")

    args = parser.parse_args()

    sensor = DHT22Sensor(pin=args.pin)

    try:
        def format_reading(value: Optional[float], unit: str) -> str:
            return f"{value:.1f}{unit}" if value is not None else f"N/A{unit}"

        if args.continuous:
            print(f"Reading DHT22 on GPIO{args.pin} every {args.interval} seconds...")
            print("Press Ctrl+C to stop\n")

            while True:
                status = sensor.get_status()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                      f"Temp: {format_reading(status['temperature_celsius'], '°C')} "
                      f"({format_reading(status['temperature_fahrenheit'], '°F')}) "
                      f"Humidity: {format_reading(status['humidity_percent'], '%')}")
                time.sleep(args.interval)

        else:
            status = sensor.get_status()
            print("DHT22 Sensor Status:")
            print(f"  Temperature: {format_reading(status['temperature_celsius'], '°C')} "
                  f"({format_reading(status['temperature_fahrenheit'], '°F')})")
            print(f"  Humidity: {format_reading(status['humidity_percent'], '%')}")
            print(f"  Status: {status['status']}")

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        sensor.close()
