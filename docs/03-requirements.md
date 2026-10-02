---
doc_id: FLG-REQ-001
title: FloodGauge requirements
project: FloodGauge
doc_type: Requirements
version: "0.7"
status: Draft
date: '2026-10-02'
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from FLG-CAL-001; R16 restated to FloodGauge-specific parts under FLG-DDR-001 D1
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from FLG-CAL-001 v0.4 (constructable design, FLG-DDR-003); R16 reported against the value-engineering target
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R12 relaxed to 120 min for the pilot surface route (90 min at permanent sites), now met on paper; R15 fix named; first alert band 100 mm (decisions of 2026-10-02)"
---

# FloodGauge requirements

These requirements are checked by calculation in FLG-CAL-001 v0.4, on the constructable design of FLG-DDR-003. The design choices behind them were decided by Amish on 2026-09-25 (FLG-DDR-001 and FLG-DDR-002). Three targets have changed at TRL 3: R16 covers FloodGauge-specific parts only, with the FieldNode core costed in its own repo (DDR-001 D1); R1 allows a mounting height of 2.5 to 5.0 m, set per site to the road authority's clearance rule; and R3 is restated to the reach of the drain head plus a drain-full signal (both DDR-002). On 2026-10-02 Amish relaxed R12 to 120 min for the pilot surface route, keeping 90 min for permanent sites (FLG-DEC-001, item 5). On 2026-09-26 Amish set `budget_usd` to $160 (DDR-002); on 2026-10-01 he described budgets as hypothetical value-engineering targets, so R16 is reported over or under the $160 target rather than as met or not met. The status column states "not met" plainly.

Table 1. Requirements and status at TRL 3

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (FLG-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Measure water depth on the street at the gauge point | 0 to 600 mm above the road surface, head mounted 2.5 to 5.0 m above the road at the height the road authority's clearance rule sets for the site | Range calculation against sensor data | Met on paper: reference lens at 4.6 m clears a 4.3 m vehicle; range 1.9 to 5.0 m over the band, radar to 20 m |
| R2 | Street depth accuracy | ±10 mm over -20 to 50 °C air, still water | Error budget; later bench test over a tank | Met on paper with radar: ±6.5 mm root sum square (±12.0 mm worst-case sum), module accuracy assumed. **Not met** by the ultrasonic variant (±27.0 mm compensated at 4.6 m) |
| R3 | Measure water level in the catch basin | Continuous reading from 50 mm above the basin floor to 330 mm below the road, plus a drain-full signal above that | Geometry of stilling tube and head | Met on paper: continuous from 1,250 to 330 mm below the road; wet probe trips at 310 mm |
| R4 | Drain level accuracy | ±20 mm | Error budget | Met on paper: ±11.0 mm with the NTC in the head (±19.7 mm without) |
| R5 | Sampling rate | Every 60 s normally; every 10 s when level is above the first alert band or rising faster than 20 mm/min | Sampling logic review | Met by design |
| R6 | Alert latency | 120 s or less from threshold crossing to message at the alert service, 95 % of events | Latency budget | Met on paper: 82 s at the 95th percentile on a private gateway (85 s on a city server); 110 s worst case without a lost packet |
| R7 | Radio airtime within network rules | Within EU868 1 % duty cycle always; within The Things Network fair use (30 s uplink airtime per day) in normal mode | Airtime calculation | **At risk:** normal mode 23.7 s/day at SF9; event mode within 1 % at SF7 to SF10 but not at SF11 or SF12 unless reporting stretches to 99 s or 181 s; normal mode exceeds fair use at SF10 and slower |
| R8 | Energy autonomy | 5 days without sun at event-mode sampling | Power budget against FieldNode | Met on paper: 68 days nominal, 47 days at -20 °C; 9.3 % of the FieldNode 100 mW allowance |
| R9 | Survive submersion of the drain head | IP68, 2 m, 72 h, stormwater with silt | Enclosure design review; later immersion test | **At risk:** electronics potted, but the transducer face keeps the module's IP67 seal |
| R10 | Reject false readings | No alert caused by a vehicle, person or debris under the street head; target 1 false alert per gauge per year or fewer | Plausibility logic review; later field log | Not verifiable at TRL 3: rules defined, including a recorded dry-road background against the curb echo |
| R11 | Privacy | Levels, status and battery only; no camera or microphone; no images or audio leave the device | Design review | Met by design |
| R12 | Installation | Two-person crew, from the surface; no road drilling; no entry into the catch basin. 120 min or less on the pilot surface cable route (relaxed on 2026-10-02, FLG-DEC-001 item 5); 90 min or less at permanent sites built on the conduit route with road works | Installation sequence review | Met on paper for the pilot route: 120 min, with no civil work (DDR-002) |
| R13 | Level datum | Head height surveyed to the road surface at the gauge point within ±5 mm; checked yearly against the depth marker | Survey method | Met on paper: tape survey plus a recorded dry-road radar reading |
| R14 | Operating environment | -20 to 50 °C air; UV, rain and road spray; FieldNode charges only from 0 to 45 °C | Material and cell review | **At risk:** inherits FieldNode's interior heat finding (FND R2, R3); the drain head module is rated -15 to 60 °C |
| R15 | Mounting | Fits 40 to 60 mm poles with band clamps; total added mass on the pole 5 kg or less | Mass estimate | Met on paper: 4.99 kg (0.01 kg margin); twist factor 37 with the M8 anti-rotation through-bolt (1.45 on friction alone) |
| R16 | Cost | FloodGauge-specific parts $160 or less at quantity 1; FieldNode costed separately (FND-CAL-001) | Priced BOM | Over the value-engineering target by $30.50: $190.50 for the constructable design ($329.50 with the $139.00 FieldNode core) |
| R17 | Open data | Levels published in an open, documented format (JSON or CSV) through the gateway | Design review | Met by design |

## Assumptions

- The road surface at the gauge point is the datum for street depth. Depth equals the surveyed head height minus the measured range.
- "Event" means water above the first alert band or rising faster than 20 mm/min.
- FieldNode figures (usable energy, allowance, airtime per uplink, mass, cost, charge temperature window) come from FND-CAL-001 in the FieldNode repo.
- Alert depths of 150 mm and 300 mm follow NWS guidance on water that can knock over an adult and carry away a car ([NWS](https://www.weather.gov/safety/flood-turn-around-dont-drown)). They are defaults under FLG-DDR-001 D6, to be set locally with the partner city. Under FLG-DDR-002 the alert service also supports a first band below 150 mm; Amish set it at 100 mm on 2026-10-02 unless the partner's own practice says otherwise (FLG-DEC-001, item 6).
- The remaining assumptions for every status above are in FLG-CAL-001, Table 1.

## Requirements not met or at risk

- **R12:** the surface cable route (DDR-002) removes the coring and trenching, but fitting its cover takes the installation to 120 min. Amish relaxed R12 to 120 min for the pilot route on 2026-10-02 (FLG-DEC-001, item 5), so it is met on paper; 90 min stays the target at permanent sites.
- **R7 at risk:** slow spreading factors need a longer event interval; event reporting belongs on a private or city gateway (D7).
- **R9 at risk:** the transducer face seal decides immersion survival.
- **R14 at risk:** interior heat in FieldNode, and the drain module's -15 °C lower rating.
- **R2** would not be met if the ultrasonic street variant were used.
- **R15 thin margin:** 4.99 kg against 5.0 kg on estimated masses after the parts added for construction (FLG-DDR-003); weigh at TRL 4. Decided 2026-10-02 (FLG-DEC-001, item 3): if the weighed mass is over 5.0 kg, the bracket plate goes to 2.5 mm.
- **R16:** the $160 is a value-engineering target (Amish, 2026-10-01), not a limit; the constructable design is estimated at $190.50, $30.50 over it.
