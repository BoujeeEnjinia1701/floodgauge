---
doc_id: FLG-PRC-001
title: FloodGauge design precis
project: FloodGauge
doc_type: Design precis
version: "0.4"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; design choices adopted for TRL 3 pending Amish's review (FLG-DDR-001); numbers checked in FLG-CAL-001; parametric model and drawing FLG-DWG-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# FloodGauge design precis

## Summary

FloodGauge is a FieldNode core on an existing street pole next to a storm inlet, with two ranging heads: a 60 GHz radar head on a short arm over the gutter that measures water depth on the street, and an ultrasonic head in a slotted stilling tube inside the catch basin that sees the drain filling before the street floods. The node turns ranges into levels, raises its sampling rate when water rises, and sends levels only over LoRaWAN to an alert service that warns crews and residents at default depths of 150 mm and 300 mm. FLG-CAL-001 v0.2 gives an alert latency of 82 s at the 95th percentile (110 s worst case), a sensor load under 10 mW, 4.74 kg on the pole and $153.50 of FloodGauge-specific parts against the $150 budget ($279.50 with the $126.00 FieldNode core, which is costed in its own repo). Two requirements are not met: installation takes 120 min against 90 min (R12), and the parts are $3.50 over budget (R16). The design choices below were decided by Amish on 2026-09-25 (FLG-DDR-001 and FLG-DDR-002): the lens sits at 4.6 m to clear tall vehicles, pilots use a surface cable route under a bolted steel cover, and an M8 through-bolt stops the arm turning.

![Hero render](../media/hero.png)

Figure 1. Concept massing model beside a storm inlet, with a 1.75 m person for scale. CONCEPT, NOT FOR FABRICATION.

## How it works

1. **Range the street.** The street head (item 2) looks straight down at the gutter from 4.6 m, 250 mm past the curb face. The height is set per site within 2.5 to 5.0 m to the road authority's clearance rule; 4.6 m clears a 4.3 m vehicle at the curb with a 0.3 m margin. Water depth is the surveyed head height minus the measured range. The beam also lights the curb, so a dry-road background is recorded at installation and the firmware tracks the peak directly below the head (FLG-CAL-001, A2).
2. **Range the drain.** The drain head (item 4) sits at the top of a slotted 75 mm tube (item 5) fixed to the basin wall. Water in the tube follows the basin level (lag under 5 mm even at 50 mm/s), and the tube walls give the wide ultrasonic beam a clean path, so the head sees the water surface and not the basin walls. A wet probe on the head signals when the basin is full to the head, and an NTC in the head compensates the speed of sound.
3. **Decide on the node.** FieldNode (item 1), mounted 3.0 m above the road so that the street head's I2C cable stays within 3 m, samples both heads every 60 s. When either level rises faster than 20 mm/min or passes the first band, it samples every 10 s. It applies plausibility checks: a sudden 1 m "rise" on the street head with an empty drain is a parked vehicle or a person, not a flood.
4. **Report.** Normally one uplink every 15 min; in an event an uplink on each band crossing and then each minute. Payloads carry levels, rate of rise, battery and status only.
5. **Alert.** A gateway (TwinKit or a city LoRaWAN network) passes readings to an open alert service that sends crew notifications and opt-in resident messages and publishes open data.
6. **Check by eye.** A depth marker plate (item 8) with bands at 150 and 300 mm above the road lets residents and crews read depth directly and check the gauge. The alert service can add a first band below 150 mm, set with the partner city.

![Cutaway](../media/cutaway.png)

Figure 2. Section across the street through the inlet: street head over the gutter, stilling tube and drain head in the catch basin, surface cable cover to the pole. Water level is illustrative.

![Data flow](../media/flow.png)

Figure 3. Data flow from the water surface to an alert. Values are estimates or proposals.

## Main components

Table 1. Main components (numbers match the exploded view and `bom/bom.csv`)

| # | Component | Decided choice (FLG-DDR-001, FLG-DDR-002) | Notes |
| --- | --- | --- | --- |
| 1 | FieldNode core | Lab shared node: IP65 enclosure, 6 W panel as hood, 6 Ah LiFePO4 cell, MPPT board with 3.3, 5 and 12 V switched rails, STM32WL-class LoRaWAN, two M12 sensor ports | Center 3.0 m above the road, facing the street; 2.41 kg and $126.00 per FND-CAL-001 |
| 2 | Street radar head | 60 GHz pulsed coherent radar module (Acconeer XM125 class) behind a PTFE lens in a sealed IP67 housing | D3; accuracy, current and price not yet checked against a data sheet |
| 3 | Sensor arm | 40 x 40 x 2 mm aluminium tube 805 mm, 25 mm square knee brace at 45°, two band clamps 400 mm apart, M8 anti-rotation through-bolt at the lower clamp | Head 250 mm past the curb face over the gutter (D5); lens 4.6 m, per site 2.5 to 5.0 m (DDR-002) |
| 4 | Drain head | Waterproof ultrasonic ranger (A02YYUW: 3 to 450 cm, ±1 cm, IP67) with a two-electrode wet probe and an NTC, potted in a sealed cap | Face 300 mm below the road; the transducer face keeps its IP67 seal, so R9 is at risk |
| 5 | Stilling tube | 75 mm OD PVC, 940 mm long, 40 slots 5 x 50 mm, two stainless wall brackets, mouth 60 mm above the basin floor | Reachable from the surface with the grate lifted |
| 6 | Sensor cables | Two outdoor cables with M12 5-pin plugs to the FieldNode ports: 3 m (street, I2C) and 5 m (drain) | Drip loops at every entry |
| 7 | Surface cable cover | Pilot route: out at the grate frame, under a galvanized steel angle across the gutter strip and up the curb face, under a beveled steel cover across the sidewalk, and up a riser guard at the pole (0.76 m of cover) | Anchors in the curb and sidewalk only; permanent sites use a 25 mm conduit laid with road works (DDR-002) |
| 8 | Depth marker plate | Aluminium plate with amber band (150 to 300 mm) and red band (300 to 450 mm) above road level | Visual check and resident information |
| 9 | Alert service | Open software on the gateway or a small server (not modeled) | Part of the software license (MIT) |

![Exploded view](../media/exploded.png)

Figure 4. Exploded view with BOM numbers. The existing street and basin are not shown.

## First-order numbers

The values below are from FLG-CAL-001 v0.2 and its script, with the DDR-002 decisions applied.

Table 2. Key numbers at TRL 3

| Quantity | Value | Basis | Requirement |
| --- | --- | --- | --- |
| Street head range | 4.60 m to dry road, 4.00 m at 600 mm depth; 1.9 to 5.0 m over the R1 band | Lens 4.6 m above the road | R1 met on paper |
| Street depth error, radar | ±6.5 mm root sum square, ±12.0 mm worst-case sum | Module ±2 mm (assumed), datum ±5 mm, pole expansion ±2.0 mm, ripple ±3 mm | R2 met on paper |
| Street depth error, ultrasonic variant | +349 to -231 mm uncompensated over -20 to 50 °C; ±27.0 mm compensated | Speed of sound 331.3 + 0.606 T m/s | R2 not met by this variant |
| Drain level error | ±11.0 mm with the NTC, ±19.7 mm without | ±10 mm module ([DFRobot](https://www.dfrobot.com/product-1935.html)), 950 mm range | R4 met on paper |
| Drain reading range | 50 mm above the floor to 330 mm below the road; wet probe at 310 mm | Head face 300 mm below the road, 30 mm blind zone | R3 (restated) met on paper |
| Energy per sampling cycle | 85.1 mJ | Radar 59.4 mJ, ultrasonic 12.0 mJ, rails 90 %, controller 5.8 mJ | |
| Sensor load | 1.42 mW at 60 s; 9.3 mW with 10 s sampling and 1 min uplinks all day | 1,440 or 8,640 cycles a day | R8 met: 68 days without sun |
| Uplink airtime | 23.7 s/day normal at SF9; 14.8 s/h in an event | 246.8 ms per 20-byte uplink | R7 at risk at SF11 and SF12 |
| Alert latency | 82 s at the 95th percentile, 110 s worst case without a lost packet | Simulation of 200,000 events | R6 met on paper |
| Arm twist | Factor 37 with the M8 through-bolt; 1.45 on clamp friction alone | 35 m/s gust along the street | R15 met on paper |
| Installation | 120 min, surface only, no civil work | Task list in FLG-CAL-001, L1 | R12 not met |
| Mass on the pole | 4.74 kg | FieldNode 2.41 kg plus arm, bolt, head, cables and marker | R15 met on paper |
| Parts cost | $153.50 FloodGauge-specific; $279.50 with FieldNode | `bom/bom.csv` | R16 not met ($3.50 over) |

![Drawing](../cad/drawings/FLG-DWG-001.png)

Figure 5. General arrangement FLG-DWG-001, Rev P2, from `cad/src/model.py`. PRELIMINARY, NOT FOR FABRICATION.

## Key design choices

Decided by Amish, 2026-09-25: go with recommendation (FLG-DDR-001, D1 to D9, and FLG-DDR-002, N1 to N5).

1. **Two heads on one node** (street and drain), because each head misses one of the two ways streets flood (FLG-PRB-001). Street head only remains the fallback where no cable route to the basin exists. (D2)
2. **Radar for the street head.** FLG-CAL-001 confirms that a compensated ultrasonic head misses R2 (±19.5 mm). The ultrasonic head stays documented as a lower-cost variant. (D3)
3. **Ultrasonic in a stilling tube for the drain,** with the wet probe as a second signal and an NTC for temperature. (D4)
4. **Arm over the gutter,** lens height set per site within 2.5 to 5.0 m to the road authority's clearance rule; 4.6 m in the reference design, where tall vehicles use the curb lane. The arm carries an M8 through-bolt so wind cannot turn it. (D5; DDR-002 N2 and N4)
5. **Alert bands at 150 mm and 300 mm** above the road ([NWS](https://www.weather.gov/safety/flood-turn-around-dont-drown)), plus a drain-full alert from the wet probe, as defaults to be set with the partner city. In a fast flood the 150 mm band warns at about 190 to 250 mm (FLG-CAL-001, F3), so the alert service also supports a first band below 150 mm, its depth set with the partner city. (D6; DDR-002 N5)
6. **Private or city LoRaWAN gateway for event reporting** (TwinKit or the city network), with The Things Network for pilots only. (D7)
7. **Levels only, no imaging.** (D8)
8. **Surface cable route for pilots,** under a bolted steel cover anchored to the curb and sidewalk, with the conduit kept for permanent sites laid with road works. (DDR-002 N3)

The FieldNode core is costed in its own repo, and R16 covers FloodGauge-specific parts only (D1). The pitch and problem lines are unchanged (D9).

## Safety

> **Safety:** Work beside live traffic. Install only with the road and pole owner's permission, with traffic management and high-visibility clothing as local rules require.
>
> **Safety:** Catch basins are confined spaces that can hold toxic or oxygen-poor air and fast-rising water. The design is installed from the surface; never enter a basin. Lifting a grate can crush fingers and strain backs; use a grate hook and two people. Stormwater carries sewage and chemicals: wear gloves and eye protection and wash after work.
>
> **Safety:** Work at height on the pole needs a mobile elevating platform for the arm at 4.7 m, a second person and clearance from overhead power lines. Drilling the pole for the anti-rotation bolt needs the asset owner's permission.
>
> **Safety:** An arm over the gutter can be struck by trucks, buses or their mirrors at the curb if it is too low (FLG-CAL-001, A7). Mount it at the height the road authority requires (4.6 m in the reference design) and always fit the anti-rotation through-bolt so that wind cannot swing it over the traffic lane.
>
> **Safety:** The surface cable cover crosses the sidewalk. Keep it low and beveled, anchor it firmly and mark it so that it is not a trip hazard.
>
> **Safety:** FieldNode holds a LiFePO4 cell of about 19 Wh. Fuse it, charge only between 0 and 45 °C, and never install a swollen, damaged or wet cell.
>
> **Safety:** FloodGauge supplements official warnings and must never be presented as the only warning. A dead battery, a blocked tube or a lost radio link can hide a flood. The alert service must report when a gauge goes silent.

## Open questions

- [ ] Radar module accuracy, current draw, beam width with the lens, price and radio certification for fixed outdoor use at 60 GHz in the pilot country (assumed in FLG-CAL-001).
- [ ] Pilot partner and city (FLG-DDR-001, O1).
- [ ] Whether the surface cable cover survives street cleaning, snow ploughs and parked-car wheels at the curb.
- [ ] Silt and debris in the stilling tube: slot size, cleaning interval, and whether the tube clogs in the first storm.
- [ ] Plausibility logic for vehicles, people, snow and floating debris under the street head.
- [ ] Theft and vandalism protection with the FieldNode at 3.0 m.
- [ ] Alert governance: who receives alerts, who acts, and how residents opt in and out.
- [ ] Datum survey method and how often to recheck it.
