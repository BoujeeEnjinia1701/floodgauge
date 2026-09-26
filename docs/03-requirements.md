---
doc_id: FLG-REQ-001
title: FloodGauge requirements
project: FloodGauge
doc_type: Requirements
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
  change: First measurable requirements for TRL 2, with status against the concept
---

# FloodGauge requirements

These are first-pass requirements for the concept. Targets are proposals for review, awaiting Amish and the co-design partner, and will be checked by calculation at TRL 3. The status column gives the first-order result from FLG-PRC-001; "not met" is stated plainly.

Table 1. Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Measure water depth on the street at the gauge point | 0 to 600 mm above the road surface, head mounted 2.5 to 3.5 m above the road | Range calculation against sensor data sheet | Met on paper (radar range up to 20 m) |
| R2 | Street depth accuracy | ±10 mm over -20 to 50 °C air, still water | Error budget; later bench test over a tank | Met on paper with radar (data sheet accuracy unverified); **not met** by an uncompensated ultrasonic head (about ±100 mm) |
| R3 | Measure water level in the catch basin | From 50 mm above the basin floor to the underside of the grate | Geometry of stilling tube and head | Met by design |
| R4 | Drain level accuracy | ±20 mm | Error budget | Met on paper with temperature compensation (about ±15 mm, estimate) |
| R5 | Sampling rate | Every 60 s normally; every 10 s when level is above the first alert band or rising faster than 20 mm/min | Firmware sketch review | Met by design |
| R6 | Alert latency | 120 s or less from threshold crossing to message at the alert service, 95 % of events | Latency budget | Met on paper with a private gateway: about 70 s typical, about 110 s worst case (estimate); thin margin |
| R7 | Radio airtime within network rules | Within EU868 1 % duty cycle always; within The Things Network fair use (30 s uplink airtime per day) in normal mode | Airtime calculation | Normal mode met (about 24 s/day); **not met** on The Things Network during events longer than about 24 min at 1 min reporting |
| R8 | Energy autonomy | 5 days without sun at event-mode sampling | Power budget against FieldNode | Met on paper (sensor load about 7 mW worst case against about 115 mW FieldNode allowance) |
| R9 | Survive submersion of the drain head | IP68, 2 m, 72 h, stormwater with silt | Enclosure design review | **Not met** by the stock ultrasonic module (IP67); potted housing proposed |
| R10 | Reject false readings | No alert caused by a vehicle, person or debris under the street head; target 1 false alert per gauge per year or fewer | Plausibility logic review; later field log | Unverified |
| R11 | Privacy | Levels, status and battery only; no camera or microphone; no images or audio leave the device | Design review | Met by design |
| R12 | Installation | Two-person crew, 90 min or less, from the surface; no road drilling; no entry into the catch basin | Installation sequence review | **At risk:** the conduit from basin to pole needs a core through the basin wall and a trench or bore under the sidewalk |
| R13 | Level datum | Head height surveyed to the road surface at the gauge point within ±5 mm; checked yearly against the depth marker | Survey method | Met by design (method to be written at TRL 3) |
| R14 | Operating environment | -20 to 50 °C air; UV, rain and road spray; FieldNode charges only from 0 to 45 °C | Material and cell review | Met on paper, inherited from FieldNode |
| R15 | Mounting | Fits 40 to 60 mm poles with band clamps; total added mass on the pole 5 kg or less | Mass estimate | Met on paper (about 3.1 kg, estimate) |
| R16 | Cost | Parts for one complete gauge $150 or less at quantity 1 | Priced BOM | **Not met:** about $271 including the $126 FieldNode core; FloodGauge-specific parts about $145 |
| R17 | Open data | Levels published in an open, documented format (JSON or CSV) through the gateway | Design review | Met by design |

## Assumptions

- The road surface at the gauge point is the datum for street depth. Depth equals the surveyed head height minus the measured range.
- "Event" means water above the first alert band or rising faster than 20 mm/min.
- FieldNode figures (energy allowance, airtime per uplink, charge temperature window) are taken from the FieldNode README and design precis and are themselves estimates.
- Alert depths of 150 mm and 300 mm follow NWS guidance on water that can knock over an adult and carry away a car ([NWS](https://www.weather.gov/safety/flood-turn-around-dont-drown)). They are proposed defaults, awaiting Amish and the partner city.

## Requirements not met or at risk

- **R16 cost:** about $271 against $150. See REVIEW.md for the proposed options.
- **R9 submersion:** the stock drain sensor is IP67; the head needs potting or a sealed housing rated for longer immersion.
- **R7 airtime:** long events exceed The Things Network fair use limit; a private or city gateway is needed for event reporting.
- **R12 installation:** routing the drain head cable to the pole is civil work, not a 90 min job.
- **R2** would not be met if an ultrasonic street head were chosen instead of radar.
