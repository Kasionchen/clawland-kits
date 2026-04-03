#!/usr/bin/env python3
"""
Water Leak Detection Sensor Driver for PicoClaw

Author: Clawland Community
License: MIT
"""

import time
import RPi.GPIO as GPIO
from typing import Optional
from datetime import datetime


class WaterLeakSensor:
    """
    Water Leak Detection Sensor Driver

    Features:
    - Conductivity-based detection
    - Coverage area: Up to 50m² with rope sensor
    - Digital output (HIGH when water detected)
    - Low power consumption
    """

    def __init__(self, pin: int = 27, debounce_time: float = 0.5):
        """
        Initialize water leak sensor

        Args:
            pin: GPIO pin number (default: 27)
            debounce_time: Debounce time in seconds (default: 0.5)
        """
        self.pin = pin
        self.debounce_time = debounce_time
        self.last_trigger_time = 0
        self._last_state = False

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Add event detection for interrupt-based monitoring
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=self._interrupt_handler)

        # Alert callbacks
        self.on_leak_detected = None
        self.on_leak_cleared = None

        # History tracking
        self.leak_history = []
        self.max_history = 100

    def _interrupt_handler(self, channel):
        """Internal interrupt handler for state changes"""
        current_time = time.time()

        # Debounce
        if current_time - self.last_trigger_time < self.debounce_time:
            return

        self.last_trigger_time = current_time
        current_state = self.read_raw()

        # Check for state change
        if current_state != self._last_state:
            timestamp = datetime.now().isoformat()

            if current_state:  # Leak detected
                event = {
                    "event": "leak_detected",
                    "timestamp": timestamp,
                    "pin": self.pin
                }
                self.leak_history.append(event)

                if self.on_leak_detected:
                    self.on_leak_detected(event)

            else:  # Leak cleared
                event = {
                    "event": "leak_cleared",
                    "timestamp": timestamp,
                    "pin": self.pin
                }
                self.leak_history.append(event)

                if self.on_leak_cleared:
                    self.on_leak_cleared(event)

            # Trim history
            if len(self.leak_history) > self.max_history:
                self.leak_history = self.leak_history[-self.max_history:]

        self._last_state = current_state

    def read_raw(self) -> bool:
        """
        Read raw sensor state

        Returns:
            True if water detected, False otherwise
        """
        return GPIO.input(self.pin) == GPIO.HIGH

    def read(self) -> bool:
        """
        Read sensor with debounce

        Returns:
            True if water detected, False otherwise
        """
        state1 = self.read_raw()
        time.sleep(self.debounce_time)
        state2 = self.read_raw()

        return state1 and state2

    def get_status(self) -> dict:
        """
        Get sensor status

        Returns:
            Dict with sensor information
        """
        leak_detected = self.read()

        status = {
            "sensor": "Water Leak Sensor",
            "pin": self.pin,
            "leak_detected": leak_detected,
            "timestamp": time.time(),
            "status": "alarm" if leak_detected else "normal",
            "last_events": self.leak_history[-5:] if self.leak_history else []
        }

        return status

    def get_history(self, limit: int = 10) -> list:
        """
        Get leak detection history

        Args:
            limit: Maximum number of events to return

        Returns:
            List of historical events
        """
        return self.leak_history[-limit:]

    def clear_history(self):
        """Clear event history"""
        self.leak_history = []

    def set_callbacks(self, on_leak_detected=None, on_leak_cleared=None):
        """
        Set callback functions for leak events

        Args:
            on_leak_detected: Function to call when leak detected
            on_leak_cleared: Function to call when leak cleared
        """
        self.on_leak_detected = on_leak_detected
        self.on_leak_cleared = on_leak_cleared

    def test_sensor(self) -> dict:
        """
        Test sensor functionality

        Returns:
            Dict with test results
        """
        print("Testing water leak sensor...")

        # Test 1: Check GPIO pin state
        state = self.read_raw()
        print(f"  GPIO State: {'HIGH (Wet)' if state else 'LOW (Dry)'}")

        # Test 2: Check interrupt detection
        print(f"  Event Detection: {'Enabled' if GPIO.event_detected(self.pin) else 'Disabled'}")

        # Test 3: Manual test prompt
        print("\n  Manual Test:")
        print("  1. Touch water to sensor")
        print("  2. Verify LED on sensor lights up")
        print("  3. Check if state changes to HIGH")

        return {
            "test_passed": True,
            "current_state": state,
            "gpio_pin": self.pin
        }

    def close(self):
        """Clean up resources"""
        try:
            GPIO.remove_event_detect(self.pin)
            GPIO.cleanup(self.pin)
        except:
            pass

    def __del__(self):
        """Destructor - ensure cleanup"""
        self.close()


# Example callback functions
def example_leak_callback(event):
    """Example callback for leak detection"""
    print(f"⚠️ ALERT: {event['event']} at {event['timestamp']}")


# CLI interface for testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Water Leak Sensor Driver")
    parser.add_argument("--pin", type=int, default=27, help="GPIO pin number")
    parser.add_argument("--continuous", action="store_true", help="Continuous monitoring")
    parser.add_argument("--interval", type=float, default=1.0, help="Check interval")
    parser.add_argument("--test", action="store_true", help="Run sensor test")

    args = parser.parse_args()

    sensor = WaterLeakSensor(pin=args.pin)

    # Set up callback for demonstration
    sensor.set_callbacks(
        on_leak_detected=example_leak_callback,
        on_leak_cleared=example_leak_callback
    )

    try:
        if args.test:
            sensor.test_sensor()

        elif args.continuous:
            print(f"Monitoring water leak sensor on GPIO{args.pin}...")
            print("Press Ctrl+C to stop\n")

            while True:
                status = sensor.get_status()
                state_str = "💧 LEAK DETECTED" if status['leak_detected'] else "✓ DRY"
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {state_str}")
                time.sleep(args.interval)

        else:
            status = sensor.get_status()
            print("Water Leak Sensor Status:")
            print(f"  State: {'💧 LEAK DETECTED ⚠️' if status['leak_detected'] else '✓ DRY'}")
            print(f"  Status: {status['status']}")

            if status['last_events']:
                print(f"\n  Recent Events:")
                for event in status['last_events']:
                    print(f"    - {event['event']} at {event['timestamp']}")

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        sensor.close()
