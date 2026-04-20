# Wiring Diagram - DC Guardian Kit

This guide shows how to connect all sensors to the LicheeRV-Nano board.

## Pin Mapping

### LicheeRV-Nano GPIO Header

```
    3.3V  [1] [2]  5V
    GP10  [3] [4]  5V
    GP11  [5] [6]  GND
    GP12  [7] [8]  GP18
    GND   [9] [10] GP19
    GP13  [11][12] GP16
    GP15  [13][14] GND
    GP16  [15][16] GP17
    3.3V  [17][18] GP18
    GP20  [19][20] GND
    GP21  [21][22] GP19
    GP22  [23][24] GP26
    GND   [25][26] GP27
```

### Sensor Connection Table

| Sensor | VCC | GND | Data/Signal | Board Pin |
|--------|-----|-----|-------------|-----------|
| DHT22 | 3.3V | GND | DATA | GP10 |
| MQ-2 | 5V | GND | AOUT | GP26 (ADC) |
| Water Leak | 3.3V | GND | DOUT | GP11 |
| LED (Status) | - | GND | Signal | GP17 (via 220Ω resistor) |

## ASCII Wiring Diagram

```
                    LicheeRV-Nano
                   +----------------+
                   |                |
    +--------------+3.3V            |
    |              |                |
    |         +----+GND             |
    |         |    |                |
    |         |    |                |
    |    +----+----+--+             |
    |    |         DHT22           |
    |    |         (Temp/Hum)      |
    |    |  10KΩ                    |
    |    +--+|data                  |
    |       | |                    |
    +-------+-+--------------------+
            |
    +-------+---------------------+
    |       |     MQ-2 Sensor     |
    |       +-----+---+-----------+
    |             |   |           |
    |         +---+---+---+       |
    |         |  VCC   AOUT|      |
    |         |  GND   DOUT|      |
    |         +-----------+       |
    |                 |           |
    +-----------------|-----------+
                      |
                  ADC GP26

    +---------------------------+
    |      Water Leak Sensor     |
    +-----------+---------------+
    |   VCC     |     GND       |
    +-----------++--------------+
                |
           GP11 |
           DOUT|
                |
         +------+------+
         |   LED       |
         |  (via 220Ω) |
         +-------------+
```

## Detailed Connection Steps

### 1. DHT22 (Temperature & Humidity)

```
DHT22 Pin 1 (VCC)  → 3.3V
DHT22 Pin 2 (DATA) → GP10 + 10KΩ pull-up to 3.3V
DHT22 Pin 3 (NC)   → Not connected
DHT22 Pin 4 (GND)  → GND
```

### 2. MQ-2 (Smoke Sensor)

```
MQ-2 VCC  → 5V
MQ-2 GND  → GND
MQ-2 AOUT → GP26 (ADC pin)
MQ-2 DOUT → Not used (using analog for sensitivity)
```

### 3. Water Leak Sensor

```
Water Leak Red (+)   → 3.3V
Water Leak Black (-) → GND
Water Leak Signal    → GP11 (with internal pull-down)
```

### 4. Status LED (Optional)

```
LED Anode (+) → GP17 (via 220Ω resistor)
LED Cathode (-) → GND
```

## Wiring Tips

1. **Use color-coded wires**: Red for VCC, Black for GND, Other colors for signals
2. **Keep wires short**: Minimize cable length to reduce interference
3. **Secure connections**: Use solder or ferrules for permanent installations
4. **Label everything**: Mark each wire at both ends

## Fritzing Diagram

For a visual Fritzing diagram, see [wiring.fzz](./wiring.fzz)

## Testing Connections

After wiring, test each sensor individually:

```bash
# Test DHT22
python3 drivers/dht22.py

# Test MQ-2
python3 drivers/mq2_smoke.py

# Test Water Leak
python3 drivers/water_leak.py
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| DHT22 reads N/A | Missing pull-up | Add 10KΩ resistor between DATA and VCC |
| MQ-2 always reads 0 | Wrong ADC pin | Verify GP26 is ADC-enabled |
| Water leak false positives | Sensitivity too high | Adjust threshold in alerts.yaml |
| No response from sensors | Power issue | Check 5V and 3.3V rails |

## Next Steps

After wiring, proceed to [skill.yaml](./skill.yaml) for PicoClaw configuration.
