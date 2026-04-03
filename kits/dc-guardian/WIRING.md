# Wiring Guide - DC Guardian Kit

> Complete assembly instructions with wiring diagrams for data center monitoring kit

---

## Prerequisites

Before starting, ensure you have:

- ✅ All components from [BOM.md](BOM.md)
- ✅ Basic tools: soldering iron, wire strippers, multimeter
- ✅ Downloaded PicoClaw OS image
- ✅ Clean, well-lit workspace

---

## Safety Warnings

⚠️ **Important Safety Notes**

1. **Power Off** - Always disconnect power before wiring
2. **Polarity Matters** - Double-check VCC and GND connections
3. **No Short Circuits** - Insulate all exposed connections
4. **ESD Protection** - Use anti-static wrist strap if available
5. **Test Before Deploy** - Verify all sensors work before enclosure assembly

---

## Component Layout

### Recommended Physical Placement

```
Data Center Floor Plan (example 50m² server room)

┌─────────────────────────────────────────┐
│                                         │
│   [RACK 1]     [RACK 2]     [RACK 3]   │
│                                         │
│         🔥 MQ-2 Smoke Sensor            │
│              (ceiling mount)            │
│                                         │
│   ┌──────────────────────────────┐     │
│   │  🧠 LicheeRV-Nano + DHT22    │     │
│   │     (wall mount, center)     │     │
│   └──────────────────────────────┘     │
│                                         │
│   💧 Water Sensor Rope (perimeter)     │
│                                         │
└─────────────────────────────────────────┘
```

---

## Pinout Reference

### LicheeRV-Nano GPIO Header

```
        ┌────────────────────┐
   3.3V │●  1   2  ●│ 5V
    SDA │●  3   4  ●│ 5V
    SCL │●  5   6  ●│ GND
   GPIO │●  7   8  ●│ TXD
    GND │●  9  10  ●│ RXD
   GPIO │● 11  12  ●│ GPIO
   GPIO │● 13  14  ●│ GND
   GPIO │● 15  16  ●│ GPIO
   3.3V │● 17  18  ●│ GPIO
   MOSI │● 19  20  ●│ GND
   MISO │● 21  22  ●│ GPIO
   SCLK │● 23  24  ●│ CE0
    GND │● 25  26  ●│ CE1
        └────────────────────┘
```

---

## Wiring Diagrams

### 1. DHT22 Temperature & Humidity Sensor

```
DHT22 Pinout:
┌─────────┐
│ ○ ○ ○ ○ │
│ 1 2 3 4 │
└─────────┘
  │ │ │ └─ NC (Not Connected)
  │ │ └─── GND
  │ └───── DATA
  └─────── VCC (3.3V-5V)

Connection:
┌──────────────┐         ┌──────────┐
│ LicheeRV-Nano│         │  DHT22   │
├──────────────┤         ├──────────┤
│     3.3V     │────────▶│   VCC    │
│    GPIO4     │◀───────▶│   DATA   │
│     GND      │────────▶│   GND    │
└──────────────┘         └──────────┘

Component Detail:
              3.3V ───┬─────────────── DHT22 VCC
                      │
                     10kΩ (pull-up resistor)
                      │
              GPIO4 ──┴─────────────── DHT22 DATA

              GND  ─────────────────── DHT22 GND

Note: Some DHT22 modules include built-in pull-up resistor.
      Check your module before adding external resistor.
```

### 2. MQ-2 Smoke Sensor

```
MQ-2 Module Pinout:
┌─────────────────┐
│ VCC GND A0 D0   │
└─────────────────┘

Connection:
┌──────────────┐         ┌──────────┐
│ LicheeRV-Nano│         │   MQ-2   │
├──────────────┤         ├──────────┤
│     5V       │────────▶│   VCC    │
│     GND      │────────▶│   GND    │
│    GPIO17    │◀───────▶│   D0     │ (Digital Output)
│    GPIO18    │◀───────▶│   A0     │ (Analog Output)
└──────────────┘         └──────────┘

Wiring Detail:
              5V   ──────────────────── MQ-2 VCC
              GND  ──────────────────── MQ-2 GND
              GPIO17 ────────────────── MQ-2 D0 (Digital)
              GPIO18 ────────────────── MQ-2 A0 (Analog)

Sensitivity Adjustment:
- Turn potentiometer clockwise to INCREASE sensitivity
- Turn counter-clockwise to DECREASE sensitivity
- LED on module indicates power status
```

### 3. Water Leak Detection Sensor

```
Water Sensor Pinout:
┌─────────────┐
│ VCC GND OUT │
└─────────────┘

Connection:
┌──────────────┐         ┌────────────┐
│ LicheeRV-Nano│         │   Water    │
│              │         │   Sensor   │
├──────────────┤         ├────────────┤
│    3.3V      │────────▶│    VCC     │
│     GND      │────────▶│    GND     │
│    GPIO27    │◀───────▶│    OUT     │
└──────────────┘         └────────────┘

Wiring Detail:
              3.3V ──────────────────── Water VCC
              GND  ──────────────────── Water GND
              GPIO27 ────────────────── Water OUT

Sensor Rope Installation:
┌─────────────────────────────────┐
│  Server Room Floor              │
│                                 │
│  ═══════════════════════════   │  ← Rope sensor along
│  ║                       ║      │     perimeter
│  ║   [RACK 1] [RACK 2]   ║      │
│  ║                       ║      │
│  ═══════════════════════════   │
│         ↑                       │
│    [Water Sensor Module]        │
└─────────────────────────────────┘

Note: Water rope should be placed in areas
      where leaks are most likely (under
      AC units, near pipes, etc.)
```

### 4. Optional: Status LED & Buzzer

```
Status Indicators:

LED Circuit:
              GPIO22 ───[330Ω]───┬───[LED+]───┐
                                   │            │
                                  GND ◀────────┘

Buzzer Circuit:
              GPIO23 ──────────────┬───[Buzzer+]───┐
                                   │                │
                                  GND ◀────────────┘

Wiring Detail:
              GPIO22 ──[330Ω]──▶ LED Anode (+)
              GPIO23 ──────────▶ Buzzer (+)
              GND  ────────────▶ LED Cathode (-)
              GND  ────────────▶ Buzzer (-)

LED Color Codes:
- 🔴 Red LED: Alarm/Critical
- 🟢 Green LED: Normal
- 🟡 Yellow LED: Warning
```

---

## Complete Wiring Schematic

### ASCII Art Full Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     LicheeRV-Nano                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  3.3V ─────┬───────────────────────────────▶ DHT22 VCC     │
│            │                                                │
│           [10kΩ]                                           │
│            │                                                │
│  GPIO4 ────┴───────────────────────────────▶ DHT22 DATA    │
│  GND  ─────────────────────────────────────▶ DHT22 GND     │
│                                                             │
│  5V   ─────────────────────────────────────▶ MQ-2 VCC      │
│  GND  ─────────────────────────────────────▶ MQ-2 GND      │
│  GPIO17 ──────────────────────────────────▶ MQ-2 D0        │
│  GPIO18 ──────────────────────────────────▶ MQ-2 A0        │
│                                                             │
│  3.3V ─────────────────────────────────────▶ Water VCC     │
│  GND  ─────────────────────────────────────▶ Water GND     │
│  GPIO27 ──────────────────────────────────▶ Water OUT      │
│                                                             │
│  GPIO22 ──[330Ω]──▶ LED (+)                                │
│  GND  ─────────────▶ LED (-)                                │
│                                                             │
│  GPIO23 ──────────▶ Buzzer (+)                             │
│  GND  ─────────────▶ Buzzer (-)                            │
│                                                             │
│  USB-C 5V/2A ─────▶ Power Input                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Assembly

### Phase 1: Prepare Components (15 min)

1. **Unpack all components**
   - Verify against [BOM.md](BOM.md)
   - Inspect for damage

2. **Prepare jumper wires**
   - Cut to appropriate lengths
   - Strip 5mm insulation from ends
   - Tin wires with solder (optional)

3. **Prepare enclosure**
   - Drill holes for sensors cables
   - Install mounting standoffs
   - Add ventilation for LicheeRV-Nano

### Phase 2: Wire Core Components (30 min)

1. **Connect DHT22**
   ```bash
   # Test command (after PicoClaw installation)
   picclaw sensor read dht22 --pin 4
   ```

2. **Connect MQ-2 Smoke Sensor**
   ```bash
   # Test smoke detection
   picclaw sensor read mq2 --pin-digital 17 --pin-analog 18
   ```

3. **Connect Water Leak Sensor**
   ```bash
   # Test water detection
   picclaw sensor read water --pin 27
   ```

### Phase 3: Wire Optional Components (15 min)

1. **Connect Status LED**
   ```bash
   # Test LED
   picclaw gpio write 22 1  # Turn on
   picclaw gpio write 22 0  # Turn off
   ```

2. **Connect Buzzer**
   ```bash
   # Test buzzer
   picclaw gpio write 23 1  # Beep
   sleep 1
   picclaw gpio write 23 0  # Off
   ```

### Phase 4: Install Software (10 min)

1. **Flash PicoClaw OS**
   ```bash
   # Download image
   wget https://releases.clawland.ai/picclaw-latest.img.gz
   gunzip picclaw-latest.img.gz

   # Flash to MicroSD (replace /dev/sdX with your device)
   sudo dd if=picclaw-latest.img of=/dev/sdX bs=4M status=progress
   sync
   ```

2. **Copy Skill Configuration**
   ```bash
   # Mount MicroSD
   sudo mount /dev/sdX1 /mnt

   # Copy skill files
   sudo cp skill.yaml /mnt/etc/picclaw/skills/
   sudo cp alerts.yaml /mnt/etc/picclaw/

   # Unmount
   sudo umount /mnt
   ```

### Phase 5: Test & Deploy (20 min)

1. **Boot PicoClaw**
   - Insert MicroSD into LicheeRV-Nano
   - Connect Ethernet cable
   - Power on

2. **Verify All Sensors**
   ```bash
   # SSH into device
   ssh root@picclaw.local

   # Check sensor status
   picclaw status

   # Test all sensors
   picclaw test --all
   ```

3. **Configure Alerts**
   - Edit `/etc/picclaw/alerts.yaml`
   - Set notification endpoints
   - Test alert delivery

4. **Mount in Enclosure**
   - Secure LicheeRV-Nano
   - Route sensor cables
   - Close enclosure

---

## Troubleshooting

### Common Issues

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| **DHT22 reads NaN** | Bad connection or timing | Check wiring, add pull-up resistor |
| **MQ-2 always HIGH** | Sensitivity too high | Adjust potentiometer |
| **Water sensor false alarms** | Rope too sensitive | Dry rope, adjust threshold |
| **No network** | Ethernet not connected | Check cable, verify DHCP |
| **Random reboots** | Power supply insufficient | Use 2A+ power supply |

---

## Cable Management

### Best Practices

```
Inside Enclosure:
┌──────────────────────┐
│  [LicheeRV-Nano]     │
│        │             │
│   [Cable Ties]       │
│        │             │
│  [Sensor Cables]     │
│        │             │
│   [Exit Holes]       │
└──────────────────────┘

Tips:
- Bundle cables with ties
- Leave slack for strain relief
- Label each cable
- Use cable glands for external cables
```

---

## Next Steps

After successful wiring:

1. ✅ Test all sensors with `picclaw test --all`
2. ✅ Configure alerts in `alerts.yaml`
3. ✅ Deploy in data center
4. ✅ Monitor for 24 hours before production use

Continue to [skill.yaml](skill.yaml) for PicoClaw configuration.
