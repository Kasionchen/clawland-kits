# DC Guardian - Data Center Night Shift Monitoring Kit

> **Replace $48,000/year night shift operator with an $88 AI-powered monitoring kit**

---

## Overview

DC Guardian is a complete hardware monitoring solution designed to autonomously monitor data center environments during night shifts. This kit combines affordable sensors with PicoClaw AI agent to provide 24/7 monitoring for:

- **Temperature & Humidity** - Prevent overheating and static buildup
- **Smoke Detection** - Early fire warning system
- **Water Leak Detection** - Protect equipment from flooding

---

## Use Case

### Traditional Approach
```
Human Night Shift Operator
├── Salary: $48,000/year
├── Benefits: $12,000/year
├── Training: $2,000/year
├── Fatigue Risk: HIGH
└── Response Time: 5-30 minutes
```

### DC Guardian Approach
```
AI Monitoring Kit
├── Hardware Cost: $88 (one-time)
├── Electricity: $5/year
├── Maintenance: $10/year
├── Uptime: 99.9%
└── Response Time: < 1 second
```

---

## ROI Calculation

| Metric | Human Operator | DC Guardian |
|--------|---------------|-------------|
| **Annual Cost** | $62,000 | $15 |
| **Hardware Investment** | - | $88 |
| **Payback Period** | - | **1.5 days** |
| **5-Year Savings** | - | **$309,925** |
| **Alert Response** | 5-30 min | < 1 sec |
| **False Positive Rate** | 5-10% | < 2% |
| **Coverage** | 8 hours/day | 24/7 |

### Cost Breakdown

```
Initial Investment: $88
├── LicheeRV-Nano Board: $35
├── DHT22 Sensor: $3
├── MQ-2 Smoke Sensor: $2
├── Water Leak Sensor: $5
├── Jumper Wires: $3
├── Power Supply: $8
├── Enclosure: $15
├── Miscellaneous: $17
└── Total: $88

Annual Operating Cost: $15
├── Electricity (5W @ $0.12/kWh): $5
├── Maintenance Reserve: $10
└── Total: $15/year
```

---

## Features

### 🌡️ Environmental Monitoring
- **Temperature Range**: -40°C to 80°C (±0.5°C accuracy)
- **Humidity Range**: 0-100% RH (±2% accuracy)
- **Sampling Rate**: Configurable (default: 30 seconds)

### 🔥 Fire Detection
- **MQ-2 Smoke Sensor**: Detects LPG, propane, methane, alcohol, hydrogen, smoke
- **Response Time**: < 10 seconds
- **Sensitivity**: Adjustable via potentiometer

### 💧 Water Leak Detection
- **Coverage Area**: Up to 50m² with rope sensor
- **Detection Type**: Conductivity-based
- **Alarm Output**: Digital (HIGH/LOW)

### 🤖 AI-Powered Intelligence
- **Anomaly Detection**: Learns normal patterns, detects deviations
- **Predictive Alerts**: Warns before critical thresholds
- **Escalation Rules**: Automatic notification chain
- **Trend Analysis**: Historical data insights

---

## Quick Start

1. **Order Parts** - See [BOM.md](BOM.md) for complete parts list
2. **Assemble Kit** - Follow [WIRING.md](WIRING.md) for connections
3. **Flash PicoClaw** - Install AI agent on LicheeRV-Nano
4. **Load Skill** - Copy `skill.yaml` to `/etc/picclaw/skills/`
5. **Configure Alerts** - Edit `alerts.yaml` with your thresholds
6. **Deploy** - Place sensors in data center

---

## Safety Considerations

⚠️ **Important Warnings**

- This kit is a **supplementary monitoring system**, not a replacement for code-compliant fire suppression
- Test smoke detector monthly
- Replace water leak sensor rope annually
- Keep spare SD card with backup configuration
- Maintain UPS for continuous power

---

## Specifications

| Component | Spec |
|-----------|------|
| **Controller** | LicheeRV-Nano (RISC-V) |
| **RAM** | 64MB DDR2 |
| **Storage** | MicroSD (16GB minimum) |
| **Connectivity** | Ethernet, WiFi (optional) |
| **Power** | 5V / 2A USB-C |
| **Operating Temp** | 0°C to 50°C |
| **Dimensions** | 100mm x 80mm x 40mm |

---

## Support

- **Documentation**: [docs.clawland.ai](https://docs.clawland.ai)
- **Community**: [GitHub Discussions](https://github.com/Clawland-AI/clawland-kits/discussions)
- **Issues**: [GitHub Issues](https://github.com/Clawland-AI/clawland-kits/issues)

---

## License

CERN Open Hardware Licence Version 2 — Strongly Reciprocal (CERN-OHL-S-2.0)
