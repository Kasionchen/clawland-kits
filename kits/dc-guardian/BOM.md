# Bill of Materials - DC Guardian Kit

Complete parts list for building a data center monitoring kit that replaces $48K/year night shift operators.

## Core Components

| Qty | Component | Part Number | Unit Price | Total | Purchase Link |
|-----|-----------|-------------|------------|-------|---------------|
| 1 | LicheeRV-Nano (RISC-V + AI) | TH1520 | $35.00 | $35.00 | [Aliexpress](https://www.aliexpress.com/item/1005005778934567.html) |
| 1 | DHT22 Temperature/Humidity Sensor | AM2302 | $3.50 | $3.50 | [Amazon](https://www.amazon.com/AM2302-Wire-Temperature-Humidity-Sensor/dp/B0797W6H5J) |
| 1 | MQ-2 Smoke/Combustible Gas Sensor | MQ-2 | $2.00 | $2.00 | [Amazon](https://www.amazon.com/MQ-2-Combustible-Gas-Sensor/dp/B07DGGV3MZ) |
| 1 | Water Leak Sensor | YL-83 | $2.50 | $2.50 | [Amazon](https://www.amazon.com/Water-Leak-Detector-Sensor/dp/B07D9W1Z3H) |
| 1 | 10K Resistor (pull-up for DHT22) | 10KΩ | $0.10 | $0.10 | [Amazon](https://www.amazon.com/10K-Resistor-Pack/dp/B08F5F1Y5J) |
| 1 | Breadboard | 400-point | $3.00 | $3.00 | [Amazon](https://www.amazon.com/400-Point-Breadboard/dp/B07DJXNLXL) |
| 1 | Jumper Wires (M/M) | 40-piece | $2.00 | $2.00 | [Amazon](https://www.amazon.com/Jumper-Wires-Premium-40-Piece/dp/B07B4SL1J6) |
| 1 | 5V Power Adapter (3A) | USB-C 5V/3A | $5.00 | $5.00 | [Amazon](https://www.amazon.com/Charger-Adapter-Samsung-Galaxy-Pixel/dp/B08F5F1Y5J) |
| 1 | MicroSD Card (32GB) | 32GB Class 10 | $6.00 | $6.00 | [Amazon](https://www.amazon.com/Samsung-MicroSD-Adapter-MB-ME32GA/dp/B08F5F1Y5J) |

## Optional Components

| Qty | Component | Unit Price | Total | Notes |
|-----|-----------|------------|-------|-------|
| 1 | 3D Printed Enclosure | $5.00 | $5.00 | See [enclosure/](enclosure/) folder |
| 1 | LED Status Indicator | - | $0.50 | For visual status |

## Cost Summary

| Category | Cost |
|----------|------|
| Required Components | $59.10 |
| Optional Components | $5.50 |
| **Total** | **~$88.00** |

## Purchase Notes

1. **LicheeRV-Nano**: The main processing board with RISC-V CPU and AI accelerator. Make sure to get the variant with WiFi for remote alerts.
2. **DHT22**: Digital temperature and humidity sensor with standard 3-pin interface. Requires 10K pull-up resistor on data line.
3. **MQ-2**: Analog output gas sensor. Calibrate in fresh air before first use.
4. **Water Leak Sensor**: Two-wire sensor. Place on floor near potential water sources (HVAC, pipes).

## Supplier Alternatives

For faster shipping, consider these alternatives:
- **Seeed Studio**: [LicheeRV-Nano](https://www.seeedstudio.com/LicheeRV-Nano.html) - US-based, faster shipping
- **DFRobot**: [DHT22](https://www.dfrobot.com/product-174.html), [MQ-2](https://www.dfrobot.com/product-1244.html)

## Budget Alternatives

If cost is a concern:
- Replace LicheeRV-Nano with ESP32-S3 (~$8) but lose AI capabilities
- Use cheaper water leak sensors (~$1 each from AliExpress)

## Next Steps

After ordering parts, proceed to [WIRING.md](./WIRING.md) for assembly instructions.
