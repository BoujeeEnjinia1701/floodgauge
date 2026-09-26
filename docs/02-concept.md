---
doc_id: FLG-PRC-001
title: FloodGauge design precis
project: FloodGauge
doc_type: Design precis
version: "0.2"
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
---

# FloodGauge design precis

## Summary

FloodGauge is a FieldNode core on an existing street pole next to a storm inlet, with two ranging heads: a 60 GHz radar head on a short arm over the gutter that measures water depth on the street, and an ultrasonic head in a slotted stilling tube inside the catch basin that sees the drain filling before the street floods. The node turns ranges into levels, raises its sampling rate when water rises, and sends levels only over LoRaWAN to an alert service that warns crews and residents at proposed depths of 150 mm and 300 mm. First-order estimates give about 70 s typical alert latency and a sensor load of a few milliwatts, but parts cost about $271 including the $126 FieldNode core, above the $150 budget. Every choice below is proposed, awaiting Amish.

![Hero render](../media/hero.png)

Figure 1. Concept massing model beside a storm inlet, with a 1.75 m person for scale. CONCEPT, NOT FOR FABRICATION.

## How it works

1. **Range the street.** The street head (item 2) looks straight down at the gutter from about 2.95 m. Water depth is the surveyed head height minus the measured range.
2. **Range the drain.** The drain head (item 4) sits at the top of a slotted 75 mm tube (item 5) fixed to the basin wall. Water in the tube follows the basin level, and the tube walls give the wide ultrasonic beam a clean path, so the head sees the water surface and not the basin walls. A wet probe on the head signals when the basin is full to the head.
3. **Decide on the node.** FieldNode (item 1) samples both heads every 60 s. When either level rises faster than 20 mm/min or passes the first band, it samples every 10 s. It applies plausibility checks: a sudden 1 m "rise" on the street head with an empty drain is a parked vehicle or a person, not a flood.
4. **Report.** Normally one uplink every 15 min; in an event an uplink on each band crossing and then each minute. Payloads carry levels, rate of rise, battery and status only.
5. **Alert.** A gateway (TwinKit or a city LoRaWAN network) passes readings to an open alert service that sends crew notifications and opt-in resident messages and publishes open data.
6. **Check by eye.** A depth marker plate (item 8) with bands at 150 and 300 mm above the road lets residents and crews read depth directly and check the gauge.

![Cutaway](../media/cutaway.png)

Figure 2. Section across the street through the inlet: street head over the gutter, stilling tube and drain head in the catch basin, conduit under the sidewalk. Water level is illustrative.

![Data flow](../media/flow.png)

Figure 3. Data flow from the water surface to an alert. Values are estimates or proposals.

## Main components

Table 1. Main components (numbers match the exploded view and `bom/bom.csv`)

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | FieldNode core | Lab shared node: IP65 enclosure, 6 W panel as hood, 6 Ah LiFePO4 cell, MPPT board with 3.3, 5 and 12 V switched rails, STM32WL-class LoRaWAN, two M12 sensor ports | Mounted about 2.5 m up the pole, facing the street |
| 2 | Street radar head | 60 GHz pulsed coherent radar module (Acconeer XM125 class) behind a PTFE lens in a sealed IP67 housing | Proposed, awaiting Amish (radar versus ultrasonic) |
| 3 | Sensor arm | 40 x 40 mm aluminium tube, about 0.8 m, two pole band clamps and a knee brace | Head 250 mm past the curb face over the gutter; proposed, awaiting Amish |
| 4 | Drain head | Waterproof ultrasonic ranger (A02YYUW class: 3 to 450 cm, ±1 cm, IP67) with a two-electrode wet probe, potted in a sealed cap | Stock IP67 module does not meet R9 on its own |
| 5 | Stilling tube | 75 mm PVC, slotted, about 1 m, two stainless wall brackets, bottom 60 mm above the basin floor | Reachable from the surface with the grate lifted |
| 6 | Sensor cables | Two outdoor cables with M12 5-pin plugs to the FieldNode ports | Drip loops at every entry |
| 7 | Conduit | 25 mm conduit cored through the basin wall and run under the sidewalk to the back of the pole, with a steel riser guard | Civil work; needs the asset owner |
| 8 | Depth marker plate | Aluminium plate with amber band (150 to 300 mm) and red band (300 to 450 mm) above road level | Visual check and resident information |
| 9 | Alert service | Open software on the gateway or a small server (not modeled) | Part of the software license (MIT) |

![Exploded view](../media/exploded.png)

Figure 4. Exploded view with BOM numbers. The existing street and basin are not shown.

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

Table 2. First-order estimates

| Quantity | Estimate | Basis and assumptions | Requirement |
| --- | --- | --- | --- |
| Street head range | about 2.95 m to dry road, 2.35 m at 600 mm depth | Head underside at 2.95 m | R1 met |
| Ultrasonic temperature error, uncompensated, at 2.95 m | about ±100 mm over 0 to 40 °C | Speed of sound 331.3 + 0.606 T m/s: 331 m/s at 0 °C, 343 m/s at 20 °C, 356 m/s at 40 °C, about ±3.5 % from a 20 °C calibration | Why R2 points to radar |
| Ultrasonic error with air temperature compensation | about ±15 mm at 2.95 m | Assumes ±3 K between the node's air sensor and the air column (sun on the road makes this uncertain) | R2 not met by ultrasonic |
| Radar temperature error | negligible | Radar ranging uses the speed of light, which air temperature barely changes | R2 met on paper; module accuracy to be checked on the data sheet |
| Drain head error | about ±15 mm | ±10 mm module accuracy ([DFRobot](https://www.dfrobot.com/product-1935.html)) plus about ±5 mm residual temperature error over 1 m, compensated | R4 met on paper |
| Energy per sampling cycle, both heads | about 70 mJ | Radar assumed 60 mA at 3.3 V for 0.3 s (about 59 mJ, unverified); ultrasonic 8 mA or less at 5 V for 0.3 s (about 12 mJ) | |
| Average sensor load | about 1.2 mW at 60 s; about 7 mW if sampling every 10 s all day | 1,440 or 8,640 cycles per day | R8 met against about 115 mW FieldNode allowance |
| Uplink airtime | about 24 s/day normal (96 uplinks at about 0.25 s, SF9); about 15 s per hour of event at 1 min reporting | FieldNode airtime estimate | R7: EU868 1 % (36 s/h) met; TTN fair use 30 s/day exceeded after about 24 min of event |
| Alert latency | about 70 s typical, about 110 s worst case | Up to 60 s wait for the next sample (30 s mean), two confirming samples at 10 s, about 1 s on air, 10 to 30 s in the network and alert service (assumed) | R6 met on paper, thin margin |
| Mass on the pole | about 3.1 kg | FieldNode about 1.7 kg, arm and clamps about 1.2 kg, head about 0.2 kg | R15 met |
| Parts cost | about $271 per gauge | `bom/bom.csv`; FieldNode $126, FloodGauge-specific parts about $145 | R16 not met |

## Key design choices

All proposed, awaiting Amish.

1. **Two heads on one node** (street and drain) rather than one. Options: (a) both heads, (b) street head only, (c) drain head only. Recommendation: (a), because each head misses one of the two ways streets flood (FLG-PRB-001); (b) is the fallback where no cable route to the basin exists.
2. **Radar for the street head** rather than ultrasonic. Radar avoids the temperature error and has range to spare. Ultrasonic saves about $31 and is proven at city scale by FloodNet, but misses R2 without compensation. Recommendation: radar, with an ultrasonic variant documented as a lower-cost option.
3. **Ultrasonic in a stilling tube for the drain** rather than radar. The range is short and sheltered from sun, so temperature error is small, and the tube fixes the wide-beam problem. Recommendation: ultrasonic, with the wet probe as a second signal.
4. **Arm over the gutter** rather than a head over the sidewalk. Over the gutter the gauge sees ponding from a blocked inlet first, but it needs road authority consent for the overhang and must reject parked vehicles. Recommendation: over the gutter at 2.95 m or higher, subject to local clearance rules.
5. **Alert bands at 150 mm and 300 mm** above the road, from NWS guidance ([NWS](https://www.weather.gov/safety/flood-turn-around-dont-drown)), plus a drain-full alert from the wet probe. Recommendation: use these as defaults and set local values with the partner city.
6. **Private or city LoRaWAN gateway for event reporting** (TwinKit or the city network), with The Things Network only for pilots. Recommendation: private gateway, because of the fair use limit in Table 2.
7. **Levels only, no imaging.** Recommendation: keep, as the README and R11 state.

## Safety

> **Safety:** Work beside live traffic. Install only with the road and pole owner's permission, with traffic management and high-visibility clothing as local rules require.
>
> **Safety:** Catch basins are confined spaces that can hold toxic or oxygen-poor air and fast-rising water. The design is installed from the surface; never enter a basin. Lifting a grate can crush fingers and strain backs; use a grate hook and two people. Stormwater carries sewage and chemicals: wear gloves and eye protection and wash after work.
>
> **Safety:** Work at height on the pole needs a stable ladder or platform, a second person and clearance from overhead power lines.
>
> **Safety:** FieldNode holds a LiFePO4 cell of about 19 Wh. Fuse it, charge only between 0 and 45 °C, and never install a swollen, damaged or wet cell.
>
> **Safety:** FloodGauge supplements official warnings and must never be presented as the only warning. A dead battery, a blocked tube or a lost radio link can hide a flood. The alert service must report when a gauge goes silent.

## Open questions

- [ ] Radar module accuracy, current draw and radio certification for fixed outdoor use at 60 GHz in the pilot country.
- [ ] How to route the drain head cable to the pole without trenching, or whether a second FieldNode in the basin (with its radio underground) is better.
- [ ] Silt and debris in the stilling tube: slot size, cleaning interval, and whether the tube clogs in the first storm.
- [ ] Plausibility logic for vehicles, people, snow and floating debris under the street head.
- [ ] Theft and vandalism protection at 2.5 m.
- [ ] Alert governance: who receives alerts, who acts, and how residents opt in and out.
- [ ] Datum survey method and how often to recheck it.
