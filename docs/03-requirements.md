---
doc_id: FLG-PRS-001
title: FloodGauge product requirements and specifications
project: FloodGauge
doc_type: Product requirements and specifications
version: "0.9"
status: Draft
date: 2026-10-31
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
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Status from FLG-CAL-001 v0.6 (sizing.py rerun); R16 cost USD 205.50 with the tamper-resistant fixings priced"
- version: "0.9"
  date: 2026-10-31
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: renamed from FLG-REQ-001 to the product requirements and specifications (PRS); every requirement renumbered PR-001 to PR-017 (old R numbers kept in the Was column), traced to the user requirements in FLG-URS-001, with tolerance and units; PR-018 and PR-019 added for UR-017 and UR-010; status from FLG-CAL-001 v0.7; PR-015 now at risk and PR-006 limited to SF9 and SF10 after the independent review"
---

# FloodGauge product requirements and specifications

What the design must do, each requirement traced to a user need in FLG-URS-001. The targets are proposals for review with a co-design partner. Method: STANDARDS section 22. The product requirements were written as R1 to R17 in versions 0.1 to 0.8 of FLG-REQ-001 and are renumbered here as PR-001 to PR-017; the Was column keeps the old number so earlier documents and the calculation note still match.

These requirements are checked by calculation in FLG-CAL-001 v0.7, on the constructable design of FLG-DDR-003, which is concept option A in FLG-OPT-001 (the two other options, B and C, are scored there against the same user requirements). The design choices behind them were decided by Amish on 2026-09-25 (FLG-DDR-001 and FLG-DDR-002). Three targets changed at TRL 3: PR-016 covers FloodGauge-specific parts only, with the FieldNode core costed in its own repo (DDR-001 D1); PR-001 allows a mounting height of 2.5 to 5.0 m, set per site to the road authority's clearance rule; and PR-003 is restated to the reach of the drain head plus a drain-full signal (both DDR-002). On 2026-10-02 Amish relaxed PR-012 to 120 min for the pilot surface route, keeping 90 min for permanent sites (FLG-DEC-001, item 5). On 2026-09-26 Amish set `budget_usd` to $160 (DDR-002); on 2026-10-01 he described budgets as hypothetical value-engineering targets, so PR-016 is reported over or under the $160 target rather than as met or not met. The status column states "not met" plainly.

Table 1. Product requirements and specifications at TRL 3

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-009 | Performance | Street depth range and mounting height | Measure water depth on the street at the gauge point, with the head mounted at the height the road authority's clearance rule sets for the site | 0 to 600 depth; head 2,500 to 5,000 above the road | range | mm | Range calculation against sensor data (CAL), TRL 3 | Met on paper: reference lens at 4.6 m clears a 4.3 m vehicle; range 1.9 to 5.0 m over the band, radar to 20 m | R1 |
| PR-002 | UR-001, UR-003 | Performance | Street depth accuracy | Street depth error over -20 to 50 °C air, still water | 10 | max, plus or minus | mm | Error budget (CAL), TRL 3; bench test over a tank at TRL 4 | Met on paper with radar: 6.5 mm root sum square (12.0 mm worst-case sum), module accuracy assumed. **Not met** by the ultrasonic variant (27.0 mm compensated at 4.6 m) | R2 |
| PR-003 | UR-002 | Performance | Catch basin level range | Continuous reading from 50 mm above the basin floor to 330 mm below the road, plus a drain-full signal above that | 1,250 to 330 below road; drain-full trip at 310 | range | mm | Geometry of stilling tube and head (CAL), TRL 3 | Met on paper: continuous from 1,250 to 330 mm below the road; wet probe trips at 310 mm | R3 |
| PR-004 | UR-002, UR-003 | Performance | Drain level accuracy | Catch basin level error | 20 | max, plus or minus | mm | Error budget (CAL), TRL 3 | Met on paper: 11.0 mm with the NTC in the head (19.7 mm without) | R4 |
| PR-005 | UR-005 | Performance | Sampling rate | Sample every 60 s normally; every 10 s when level is above the first alert band or rising faster than 20 mm/min | 60 normal; 10 in an event | max interval | s | Sampling logic review (CAL), TRL 3 | Met by design | R5 |
| PR-006 | UR-004 | Performance | Alert latency | Time from threshold crossing to a message at the alert service, 95 % of events | 120 | max | s | Latency simulation (CAL), TRL 3 | Met on paper at SF9 and SF10 on a private gateway: 82 s at the 95th percentile (85 s on a city server); 110 s worst case without a lost packet. Not met at SF11 (123 s) and SF12 (201 s) in event mode (independent review) | R6 |
| PR-007 | UR-013 | Electrical | Radio airtime within network rules | Within the EU868 1 % duty cycle always; within The Things Network fair use (30 s uplink airtime per day) in normal mode | 1 % duty; 30 s/day | max | % and s/day | Airtime calculation (CAL), TRL 3 | **At risk:** normal mode 23.7 s/day at SF9; event mode within 1 % at SF7 to SF10 but not at SF11 or SF12 unless reporting stretches to 99 s or 181 s; normal mode exceeds fair use at SF10 and slower | R7 |
| PR-008 | UR-006 | Electrical | Energy autonomy | Run on stored energy with no sun at event-mode sampling | 5 | min | days | Power budget against FieldNode (CAL), TRL 3 | Met on paper: 68 days nominal, 47 days at -20 °C; 9.3 % of the FieldNode 100 mW allowance | R8 |
| PR-009 | UR-007 | Materials | Survive submersion of the drain head | IP68 to 2 m for 72 h in stormwater with silt | IP68, 2 m, 72 h | min | rating, m, h | Enclosure design review (CAL), TRL 3; immersion test at TRL 4 | **At risk:** electronics potted, but the transducer face keeps the module's IP67 seal | R9 |
| PR-010 | UR-011 | Software | Reject false readings | No alert caused by a vehicle, person or debris under the street head | 1 false alert per gauge per year | max | alerts/year | Plausibility logic review (CAL), TRL 3; field log at TRL 4 | To verify at TRL 4: rules defined, including a recorded dry-road background against the curb echo | R10 |
| PR-011 | UR-012 | Software | Privacy | The device records levels, status and battery only; no camera or microphone; no image or audio leaves the device | 0 cameras and microphones | exact | count | Design review (BOM, PRC), TRL 3 | Met by design | R11 |
| PR-012 | UR-008 | Usability | Installation | Two-person crew, from the surface; no road drilling; no entry into the catch basin. 120 min on the pilot surface cable route (relaxed on 2026-10-02, FLG-DEC-001 item 5); 90 min at permanent sites built on the conduit route with road works | 120 pilot; 90 permanent | max | min | Installation sequence review (CAL, BLD), TRL 3 | Met on paper for the pilot route: 120 min, with no civil work (DDR-002) | R12 |
| PR-013 | UR-014 | Performance | Level datum | Head height surveyed to the road surface at the gauge point; checked yearly against the depth marker | 5 | max, plus or minus | mm | Survey method (CAL), TRL 3 | Met on paper: tape survey plus a recorded dry-road radar reading | R13 |
| PR-014 | UR-006, UR-007 | Materials | Operating environment | Work in air from -20 to 50 °C with UV, rain and road spray; FieldNode charges only from 0 to 45 °C | -20 to 50 | range | °C | Material and cell review (CAL), TRL 3 | **At risk:** inherits FieldNode's interior heat finding (FND R2, R3); the drain head module is rated -15 to 60 °C | R14 |
| PR-015 | UR-009, UR-010 | Physical architecture | Mounting and mass on the pole | Fit 40 to 60 mm poles with band clamps; total added mass on the pole | 5.0 | max | kg | Mass from the CAD model (CAL), TRL 3; weigh at TRL 4 | **At risk:** 4.994 kg (margin 0.006 kg, inside the accuracy of an estimate from model volumes); twist factor 1.8 with the M8 A4-80 anti-rotation through-bolt, 1.45 on friction alone on a 60 mm pole and 0.97 on a 40 mm pole | R15 |
| PR-016 | UR-016 | Cost | Cost | FloodGauge-specific parts at quantity 1; FieldNode costed separately (FND-CAL-001) | 160 | max | USD | Priced BOM (bom/bom.csv), TRL 3 | Over target by $45.50: $205.50 for the constructable design ($344.50 with the $139.00 FieldNode core) | R16 |
| PR-017 | UR-015 | Software | Open data | Levels published in an open, documented format through the gateway | JSON or CSV | exact | format | Design review (PRC), TRL 3 | Met by design | R17 |
| PR-018 | UR-017 | Safety | Tamper resistance | Every fixing within reach from the sidewalk needs a security tool: security (snake-eye) nuts on the eight masonry anchors and pin-Torx security screws on the marker band clamps | 10 of 10 fixings within reach | min | count | CAD model and BOM review (CAL, BLD), TRL 3 | Met by design (new in this version; the fixings were added in FLG-DDR-003) | |
| PR-019 | UR-010 | Safety | Cover profile and edges | Surface cable covers project no more than the hat-section height, and every exposed edge of a made part is broken | 16 | max | mm | CAD model (cad_check edge breaks) and drawing FLG-DWG-001, TRL 3 | Met by design: hat section 16 mm high with 2 mm sheet; edges broken in the model | |

Status values: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- The road surface at the gauge point is the datum for street depth. Depth equals the surveyed head height minus the measured range.
- "Event" means water above the first alert band or rising faster than 20 mm/min.
- FieldNode figures (usable energy, allowance, airtime per uplink, mass, cost, charge temperature window) come from FND-CAL-001 in the FieldNode repo.
- Alert depths of 150 mm and 300 mm follow NWS guidance on water that can knock over an adult and carry away a car ([NWS](https://www.weather.gov/safety/flood-turn-around-dont-drown)). They are defaults under FLG-DDR-001 D6, to be set locally with the partner city. Under FLG-DDR-002 the alert service also supports a first band below 150 mm; Amish set it at 100 mm on 2026-10-02 unless the partner's own practice says otherwise (FLG-DEC-001, item 6).
- The remaining assumptions for every status above are in FLG-CAL-001, Table 1.

## Requirements not met or at risk

- **PR-012 (was R12):** the surface cable route (DDR-002) removes the coring and trenching, but fitting its cover takes the installation to 120 min. Amish relaxed it to 120 min for the pilot route on 2026-10-02 (FLG-DEC-001, item 5), so it is met on paper; 90 min stays the target at permanent sites.
- **PR-007 at risk:** slow spreading factors need a longer event interval; event reporting belongs on a private or city gateway (D7).
- **PR-009 at risk:** the transducer face seal decides immersion survival.
- **PR-014 at risk:** interior heat in FieldNode, and the drain module's -15 °C lower rating.
- **PR-002** would not be met if the ultrasonic street variant were used.
- **PR-015 at risk:** 4.994 kg against 5.0 kg on masses taken from the model volumes after the parts added for construction (FLG-DDR-003); the margin of 6 g is inside the accuracy of the estimate (independent review), so it is no longer called met on paper; weigh at TRL 4. The twist factor of 37 in earlier versions was wrong (FLG-DDR-004 F2): it is 1.8 on the bolt, and friction alone gives only 0.97 on a 40 mm pole.
- **PR-006 limited to SF9 and SF10:** event-mode alerts take 123 s at SF11 and 201 s at SF12 (FLG-CAL-001 F4). Decided 2026-10-02 (FLG-DEC-001, item 3): if the weighed mass is over 5.0 kg, the bracket plate goes to 2.5 mm.
- **PR-016:** the $160 is a value-engineering target (Amish, 2026-10-01), not a limit; the constructable design is estimated at $205.50, $45.50 over it.
- **PR-010:** cannot be verified before a field log exists (TRL 4).
