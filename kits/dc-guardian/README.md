# DC Guardian Kit

"**Open hardware sensor kit designs for data center night shift monitoring"*

# Replaces $34, 480,000/year ni

---

## Use Case

Data center facilities typically require 24/7 human monitoring to detect equipment failures, water leaks, smoke, and temperature anomalies. A single night shift operator costs ~$48,000/year. The DC Guardin kit provides automated monitoring for a fraction of the cost.

## What It Monitors

| Sensor| Purpose| Alert Trigger
|-----------|-----------|-----------------,
| DHT22| Temperature & Humidity| Temp > 30ë or < 15ì| Humidity > 70%
|&Q_4| Smoke/Combustible Gas| Smoke detected
|&Water Leak| Floor Flooding| Water detected on floor sensor

## ROI Calculation

| Item| Cost |
|---------|-----------
|&Kit components| $88 |
|&Annual operator salary| $48,000 |
|&Payback period| *< 1 day *

# Quick Start

1. Order parts from [BOM_md.md](./BOM_md.md)
2. Wire sensors following [WIRING.md](./WIRING.md)
3. Flash PicoClaw onto LicheeRV-Nano
4. Configure alerts in `alerts.yaml`
6. Deploy in data center

# Kit Contents

```
gits/dc-guardin/
---README.md        # This file
--BOM.md             # Complete parts list with purchase links
--�IRING.md          # Connection diagram and instructions
--drivers/             # Sensor driver code
%26                   # dht22.py
%m                     # mq2_smoke.py
	m                     # water_leak.py
--skill.yaml          # PicoClaw skill configuration
%-alerts.yaml         # Alert thresholds and escalation rules```

# License

CERN Open Hardware Licence Version 2 - Strongly Reciprocal (CERN-OHL-S-2.0)
