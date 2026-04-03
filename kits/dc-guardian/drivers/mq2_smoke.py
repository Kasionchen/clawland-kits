#!/usr/bin/env python3
"""
MQ-2 Smoke & Gas Sensor Driver for PicoClaw

Author: Clawland Community
License: MIT
"""

import time
import RPi.GPIO as GPIO
import spidev
from typing import Tuple, Optional


class MQ2Sensor:
    """
    MQ-2 Smoke & Gas Sensor Driver

    Features:
    - Detects: LPG, Propane, Methane, Alcohol, Hydrogen, Smoke
    - Detection range: 300-10000 ppm
    - Response time: < 10 seconds
    - Digital + Analog outputs
    """

    # Gas detection thresholds (ppm)
    GAS_THRESHOLDS = {
        "LPG": {"min": 300, "max": 5000},
        "Propane": {"min": 300, "max": 5000},
        "Methane": {"min": 300, "max": 10000},
        "Alcohol": {"min": 300, "max": 5000},
        "Hydrogen": {"min": 300, "max": 5000},
        "Smoke": {"min": 300, "max": 10000},
    }

    def __init__(self, digital_pin: int = 17, analog_pin: int = 18,
                 threshold_ppm: int = 1000):
        """
        Initialize MQ-2 sensor

        Args:
            digital_pin: GPIO pin for digital output (default: 17)
            analog_pin: GPIO pin for analog output (default: 18)
            threshold_ppm: Alarm threshold in ppm (default: 1000)
        """
        self.digital_pin = digital_pin
        self.analog_pin = analog_pin
        self.threshold_ppm = threshold_ppm
        self.spi = None

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(digital_pin, GPIO.IN)

        # Setup SPI for analog reading
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = 1000000
        except Exception as e:
            print(f"Warning: Could not initialize SPI for analog reading: {e}")
            self.spi = None

        # Warm-up time (MQ sensors need time to heat up)
        self.warmup_time = 20  # seconds

    def read_digital(self) -> bool:
        """
        Read digital output (gas detected or not)

        Returns:
            True if gas detected (concentration > threshold)
        """
        return GPIO.input(self.digital_pin) == GPIO.HIGH

    def read_analog(self) -> Optional[int]:
        """
        Read analog output (0-1023 ADC value)

        Returns:
            ADC value (0-1023) or None if SPI not available
        """
        if not self.spi:
            return None

        try:
            # MCP3008 ADC read
            adc_channel = self.analog_pin  # Assuming direct mapping
            if adc_channel < 0 or adc_channel > 7:
                return None

            # SPI transaction
            r = self.spi.xfer2([1, (8 + adc_channel) << 4, 0])
            adc_value = ((r[1] & 3) << 8) + r[2]
            return adc_value

        except Exception as e:
            print(f"Analog read error: {e}")
            return None

    def ppm_from_analog(self, analog_value: int) -> float:
        """
        Convert analog value to approximate PPM

        Args:
            analog_value: ADC value (0-1023)

        Returns:
            Approximate PPM value
        """
        # Simplified conversion (requires calibration for accuracy)
        # This is a rough approximation
        if analog_value <= 0:
            return 0

        # MQ-2 sensor curve approximation
        # VRL / RL = Rs / R0
        # PPM = (Rs/R0) ^ (1/b) * a

        # Simplified linear approximation
        # Adjust coefficients based on your specific sensor
        ppm = analog_value * 10  # Rough approximation
        return ppm

    def read(self) -> Tuple[bool, Optional[float]]:
        """
        Read both digital and analog values

        Returns:
            Tuple of (gas_detected_bool, ppm_value)
        """
        digital = self.read_digital()
        analog = self.read_analog()

        if analog is not None:
            ppm = self.ppm_from_analog(analog)
        else:
            ppm = None

        return digital, ppm

    def detect_gas_type(self, ppm: float) -> list:
        """
        Guess possible gas types based on PPM

        Args:
            ppm: Concentration in PPM

        Returns:
            List of possible gas types
        """
        possible_gases = []

        for gas, thresholds in self.GAS_THRESHOLDS.items():
            if thresholds["min"] <= ppm <= thresholds["max"]:
                possible_gases.append(gas)

        return possible_gases

    def get_status(self) -> dict:
        """
        Get sensor status and readings

        Returns:
            Dict with all sensor information
        """
        digital, ppm = self.read()

        status = {
            "sensor": "MQ-2",
            "digital_pin": self.digital_pin,
            "analog_pin": self.analog_pin,
            "gas_detected": digital,
            "ppm": ppm,
            "threshold_ppm": self.threshold_ppm,
            "alert": digital or (ppm is not None and ppm > self.threshold_ppm),
            "possible_gases": self.detect_gas_type(ppm) if ppm else [],
            "timestamp": time.time()
        }

        return status

    def calibrate(self, duration: int = 60):
        """
        Calibrate sensor in clean air

        Args:
            duration: Calibration duration in seconds
        """
        print(f"Calibrating MQ-2 sensor for {duration} seconds...")
        print("Ensure sensor is in clean air environment!")

        readings = []
        start_time = time.time()

        while time.time() - start_time < duration:
            analog = self.read_analog()
            if analog is not None:
                readings.append(analog)
            time.sleep(1)

        if readings:
            baseline = sum(readings) / len(readings)
            print(f"Calibration complete. Baseline analog value: {baseline:.2f}")
            return baseline
        else:
            print("Calibration failed: no readings obtained")
            return None

    def warm_up(self, wait: bool = True):
        """
        Wait for sensor warm-up

        Args:
            wait: If True, block until warm-up complete
        """
        print(f"MQ-2 sensor requires {self.warmup_time} seconds warm-up time")

        if wait:
            for i in range(self.warmup_time, 0, -1):
                print(f"Warming up... {i} seconds remaining", end='\r')
                time.sleep(1)
            print("\nWarm-up complete!")

    def close(self):
        """Clean up resources"""
        if self.spi:
            try:
                self.spi.close()
            except:
                pass

        try:
            GPIO.cleanup(self.digital_pin)
        except:
            pass

    def __del__(self):
        """Destructor - ensure cleanup"""
        self.close()


# CLI interface for testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MQ-2 Smoke & Gas Sensor Driver")
    parser.add_argument("--digital-pin", type=int, default=17, help="Digital GPIO pin")
    parser.add_argument("--analog-pin", type=int, default=18, help="Analog GPIO pin")
    parser.add_argument("--threshold", type=int, default=1000, help="PPM threshold")
    parser.add_argument("--continuous", action="store_true", help="Continuous reading")
    parser.add_argument("--interval", type=float, default=1.0, help="Read interval")
    parser.add_argument("--calibrate", action="store_true", help="Calibrate sensor")
    parser.add_argument("--warmup", action="store_true", help="Wait for warm-up")

    args = parser.parse_args()

    sensor = MQ2Sensor(
        digital_pin=args.digital_pin,
        analog_pin=args.analog_pin,
        threshold_ppm=args.threshold
    )

    try:
        if args.warmup:
            sensor.warm_up(wait=True)

        if args.calibrate:
            sensor.calibrate()

        elif args.continuous:
            print(f"Reading MQ-2 sensor every {args.interval} seconds...")
            print("Press Ctrl+C to stop\n")

            while True:
                status = sensor.get_status()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                      f"Gas: {'DETECTED' if status['gas_detected'] else 'CLEAR'} "
                      f"PPM: {status['ppm']:.1f if status['ppm'] else 'N/A'} "
                      f"Alert: {'⚠️ YES' if status['alert'] else '✓ NO'}")
                time.sleep(args.interval)

        else:
            status = sensor.get_status()
            print("MQ-2 Sensor Status:")
            print(f"  Gas Detected: {'YES ⚠️' if status['gas_detected'] else 'NO ✓'}")
            print(f"  PPM: {status['ppm']:.1f if status['ppm'] else 'N/A'}")
            print(f"  Threshold: {status['threshold_ppm']} PPM")
            print(f"  Alert: {'YES ⚠️' if status['alert'] else 'NO ✓'}")
            if status['possible_gases']:
                print(f"  Possible Gases: {', '.join(status['possible_gases'])}")

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        sensor.close()
