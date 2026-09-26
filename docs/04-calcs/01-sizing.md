---
doc_id: FLG-CAL-001
title: FloodGauge sizing calculations
project: FloodGauge
doc_type: Calculation
version: "0.3"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (range and geometry, depth and level error budgets, tube hydraulics, energy, airtime, alert latency, false readings, arm and clamps, mass, cables, submersion, installation, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($160); R16 from not met to met on paper
---

# FloodGauge sizing calculations

This v0.2 applies the decisions Amish accepted on 2026-09-25 (FLG-DDR-002): the lens moves to 4.6 m so that it clears a 4.3 m vehicle at the curb, R1 allows 2.5 to 5.0 m set per site, R3 is restated, the pilot cable route runs on the surface under a bolted steel cover, and an M8 through-bolt stops the arm turning. The FieldNode moves up to 3.0 m so that the street head's I2C cable stays short. On 2026-09-26 Amish approved a `budget_usd` of $160 to cover the priced BOM (FLG-DDR-002). On paper, FloodGauge now meets twelve of its seventeen requirements (nine by calculation, three by design), has three at risk, cannot verify one at TRL 3 and misses one. R3 is now met on paper. R12 (a 90 min surface-only installation) is still not met: the surface route removes the civil work, but fitting its cover brings the total to 120 min. The cover and the through-bolt take the FloodGauge-specific parts to $153.50, which the $160 budget covers, so R16 is met on paper. The three at risk are airtime at slow spreading factors (R7), immersion of the drain head (R9) and the operating environment inherited from FieldNode (R14). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [F2], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the gauge will warn anyone in time, and they are no substitute for tests of the heads, the enclosure or the alert chain. FloodGauge supplements official warnings. See FLG-PRC-001, Safety.

## Scope and method

The note checks every requirement in FLG-REQ-001 v0.5 against the design in FLG-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and derived dimensions, so the head height, arm, tube, cable runs and marker used here are the ones in the STEP files and in drawing FLG-DWG-001 Rev P2. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes the status table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is a street with a 150 mm curb and a catch basin 1.3 m deep beside a 60 mm street pole 4.9 m tall above the sidewalk, with tall vehicles in the curb lane, air from -20 to 50 °C, a private LoRaWAN gateway (TwinKit) on EU868, and the FieldNode core as costed and sized in its own repo (FND-CAL-001).

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Radar head | Distance accuracy ±2 mm; 60 mA at 3.3 V for 0.3 s per reading; half-power beam 25° with a PTFE lens; range up to 20 m | Range from [Acconeer](https://www.acconeer.com/products/); accuracy, current and beam are assumptions, since no data sheet could be checked in this session |
| Drain head | DFRobot A02YYUW: 3 to 450 cm, ±1 cm, 60° beam, 3.3 to 5 V, 8 mA or less, 100 ms response, -15 to 60 °C, IP67, UART | [DFRobot product page](https://www.dfrobot.com/product-1935.html), checked 2026-09-25; no built-in temperature compensation is stated, so none is assumed |
| Air temperature | Speed of sound 331.3 + 0.606 T m/s; calibration at 20 °C; ±3 K between air sensor and air column over the street; ±2 K for an NTC in the drain head | Standard approximation; sensor offsets assumed |
| Datum | Head height surveyed to ±5 mm (R13 limit); drain head face measured from the grate seat to ±3 mm; steel pole ±35 K from the survey day | R13; tape and level |
| Surface | ±3 mm residual ripple and rain splash after averaging 5 readings | Assumed |
| FieldNode | 15.36 Wh usable; core 4.0 mWh/day at 15 min reports; 16.0 mA s at 3.2 V per SF9 report; rails 90 %; allowance 100 mW design value, 115 mW ceiling; 2.41 kg; $126.00; autonomy at -20 °C is 0.70 of nominal | FND-CAL-001 |
| Controller | 5 mA at 3.3 V for 0.35 s per sampling cycle | Typical STM32WL-class figure; assumed |
| Radio | 20-byte payload plus 13 bytes overhead, 125 kHz, CR 4/5, 8-symbol preamble; EU868 1 % duty cycle; The Things Network fair use 30 s/day | FieldNode and TwinKit notes |
| Network | Gateway, network server and alert service 1 to 4.7 s (TwinKit worst 4.7 s); 2 to 10 s on a city or public server; 1 % uplink loss | TWK-CAL-001; assumed for public servers |
| Wind and loads | 35 m/s gust (q = 750 Pa); drag 2.0 on square tubes and 1.2 on the head; 6063-T6 class aluminium, E = 69 GPa, yield 214 MPa; band clamp preload 1,000 N, friction 0.3; misuse case of a 50 kg person hanging on the head | As FND-CAL-001; handbook values |
| Vehicles | Tall vehicles 4.0 to 4.3 m at the curb, 0.3 m clearance margin | Typical legal height limits; to confirm with the road authority |
| Through-bolt | M8 stainless A4-70, stress area 36.6 mm², shear 0.6 f_ub; pole wall 2.5 mm, f_u 360 MPa, bearing 2.5 f_u d t | Handbook values; pole wall assumed |
| Cables | 100 pF/m and 0.07 kg/m for outdoor 5-core cable | Assumed |

## A. Geometry and range (R1, R3)

- **Street range.** With the lens 4.6 m above the road, the radar sees 4.60 m to a dry road and 4.00 m at 600 mm depth, well inside its 20 m range [A1]. Over the whole R1 mounting band of 2.5 to 5.0 m the range runs from 1.9 to 5.0 m; at 5.0 m the assumed beam lights a circle of 1,108 mm radius, so the dry-road background matters more on tall sites [A1b]. R1 is met.
- **Curb echo.** An assumed 25° beam lights a circle of 1,020 mm radius on the road, which includes the curb 250 mm away. If the firmware picked the first echo, the curb top at 4,457 mm would read as 143 mm of water on a dry day [A2]. A beam narrow enough to miss the curb would need to be under 6.2° wide, which a small lens does not give [A3]. The street head therefore needs a recorded dry-road background at installation and tracking of the nadir peak; this is part of R10.
- **Drain range.** The drain head face is 300 mm below the road. The ultrasonic reads levels from 1,250 mm to 330 mm below the road (30 to 950 mm range, within the module's 30 to 4,500 mm), and the wet probe trips at 310 mm [A4]. The 50 mm level lies 10 mm below the tube mouth, in the beam path; the outlet invert is 100 mm above the floor, so the sump always holds water [A6].
- **R3 as restated.** Between 330 mm and 40 mm below the road (the grate underside), a 290 mm band, the only signal is the wet probe at one point [A5]. The drain head cannot rise higher, because the road slab and grate frame sit above it. In practice a basin in that band is surcharging, the wet probe says so, and the street head reads the water once it reaches the road. Under FLG-DDR-002, R3 now asks for a continuous reading from 50 mm above the basin floor to 330 mm below the road, plus a drain-full signal above that, so R3 is met on paper.
- **Vehicle clearance.** At 2.95 m (v0.1) the head was inside the envelope of a 4.0 to 4.3 m vehicle parked or passing at the curb. Under FLG-DDR-002 the reference lens height is 4.6 m, which clears a 4.3 m vehicle with the 0.3 m margin [A7]. Each site sets its own height within 2.5 to 5.0 m to the road authority's clearance rule. The site needs a pole about 4.9 m tall above the sidewalk; a shorter sign pole only suits a curb lane without tall vehicles.

## B. Street depth error (R2)

- **Radar.** The error budget is module ±2.0 mm (assumed), datum ±5.0 mm, pole expansion ±1.98 mm (the arm is now 4.71 m up) and surface ripple ±3.0 mm, which gives ±6.5 mm root sum square and ±12.0 mm if every term is at its worst at once [B1]. R2 (±10 mm) is met on paper by the root sum square, with the module accuracy still unverified.
- **Ultrasonic variant, uncompensated.** Calibrated at 20 °C, the range error is +349 mm at -20 °C and -231 mm at 50 °C, because the speed of sound runs from 319.2 to 361.6 m/s [B2].
- **Ultrasonic variant, compensated.** With an air sensor within ±3 K of the air column, the temperature term is ±24.4 mm and the total ±27.0 mm at the 4.6 m height [B3]. R2 is not met by the ultrasonic variant, which confirms the choice of radar (D3). Sun on the road makes the ±3 K figure itself optimistic.
- **Arm deflection.** The 40 x 40 x 2 mm arm (I = 73,365 mm⁴) moves 0.20 mm under a 1 kg bird at the head even without the brace [B4]; negligible.

## C. Drain level and stilling tube (R4, R3)

- **Error budget.** With the NTC in the drain head (±2 K) at the full 950 mm range, the temperature term is ±3.4 mm and the total ±11.0 mm [C1]. Without it (±10 K from a 20 °C calibration) the temperature term is ±16.8 mm and the total ±19.7 mm, just inside the target with no margin [C2]. R4 (±20 mm) is met on paper, and the NTC (BOM line 4, $0.50) is kept for margin.
- **Slots.** The 69 mm bore has 3,739 mm² of area. Forty slots of 5 x 50 mm in ten rows give 1,000 mm² per row and 10,000 mm² in all, 4.5 % of the wall [C3].
- **Lag.** With only the lowest row of slots wet, the level inside the tube lags the basin by 0.00 mm at 20 mm/min, 0.20 mm at 10 mm/s and 4.95 mm at an extreme 50 mm/s [C4]. The tube does not slow the reading; its job is to give the wide ultrasonic beam a clean path and to calm the surface.

## D. Energy (R8)

- **Per cycle.** A radar reading takes 59.4 mJ and an ultrasonic reading 12.0 mJ; with 90 % rail converters and 5.8 mJ for the controller, a cycle costs 85.1 mJ [D1].
- **Daily draw.** Normal sampling every 60 s is a 1.42 mW sensor load and 0.038 Wh/day with the FieldNode core. Event sampling every 10 s all day, with an uplink every minute, is 8.51 mW for the sensors plus 0.80 mW for the extra uplinks, 0.227 Wh/day in all [D2].
- **Against FieldNode.** Event sampling all day uses 9.3 % of the 100 mW FieldNode design allowance (115 mW ceiling) [D3]. The cell lasts 68 days without sun, or 47 days at -20 °C [D4]. R8 (5 days) is met with a wide margin.
- **Heat.** FieldNode's R3 finding (the cell too hot to charge on clear hot days) matters less here: even the 0.8 Wh a hot clear day stores without a shield exceeds the 0.227 Wh drawn [D5].

## E. Airtime (R7)

*Table 2. Airtime for a 20-byte reading [E1].*

| Spreading factor | Airtime per uplink | Normal mode (15 min) | Event mode (1 min) against 1 % (36 s/h) | Shortest interval under 1 % | Event minutes before The Things Network's 30 s/day |
| --- | --- | --- | --- | --- | --- |
| SF7 | 71.9 ms | 6.9 s/day | 4.3 s/h, met | 7 s | 344 |
| SF8 | 133.6 ms | 12.8 s/day | 8.0 s/h, met | 13 s | 138 |
| SF9 | 246.8 ms | 23.7 s/day | 14.8 s/h, met | 25 s | 27 |
| SF10 | 452.6 ms | 43.5 s/day | 27.2 s/h, met | 45 s | 0 (normal mode already over) |
| SF11 | 987.1 ms | 94.8 s/day | 59.2 s/h, **not met** | 99 s | 0 |
| SF12 | 1,810.4 ms | 173.8 s/day | 108.6 s/h, **not met** | 181 s | 0 |

- **R7 is at risk.** On a private gateway the 1 % duty cycle holds in event mode from SF7 to SF10, but not at SF11 or SF12, where the firmware must stretch event reporting to 99 s and 181 s. On The Things Network, an SF9 gauge in normal mode uses 23.7 of its 30 s a day and has room for only about 27 min of event reporting; at SF10 and slower even normal mode breaks the fair use limit (FieldNode R9). This supports D7: event reporting goes through a private or city gateway.

## F. Alert latency (R6)

The chain is: wait for the next sample, two confirming samples 10 s apart, about 1 s to wake and queue, the uplink, a possible duty-cycle wait of up to 24.4 s after a previous uplink, a repeat after a lost packet (1 %), and the gateway, network server and alert service.

*Table 3. Alert latency from a band crossing to the message leaving the alert service, 200,000 simulated events [F1].*

| Network | Case | Mean | 95th percentile | Largest simulated |
| --- | --- | --- | --- | --- |
| Private gateway | Slow rise from normal mode (60 s sampling) | 55 s | 82 s | 125 s |
| Private gateway | Already in event mode (10 s sampling) | 34 s | 52 s | 84 s |
| City or public server | Slow rise from normal mode | 58 s | 85 s | 134 s |
| City or public server | Already in event mode | 38 s | 55 s | 89 s |

- **R6 is met on paper.** The 95th percentile is 82 s on a private gateway and 85 s on a city server, against 120 s. The deterministic worst case without a lost packet is 110 s (60 + 20 + 1.2 + 24.4 + 4.7 s) [F2]; only a lost packet pushes an event past 120 s.
- **Depth at alert.** Water rising at 20 mm/min adds 37 mm between the crossing and the alert; at 100 mm/min, when the gauge is already sampling every 10 s, it adds 101 mm in 60 s [F3]. The 150 mm band therefore warns at roughly 190 to 250 mm in a fast flood. The partner city may want the first band lower for that reason.
- The TRL 2 figure of about 70 s typical and 110 s worst stands; the new 95th percentile is the figure R6 asks for.

## G. False readings (R10)

- **Tall objects.** A car roof (1.45 m), a van roof (2.00 m) and a person (1.75 m) under the head read as depths well above 600 mm and are rejected as out of range. A 0.5 m snow bank reads as 500 mm and needs the drain cross-check [G1].
- **Rules defined.** Reject depths above 600 mm; reject a step above 50 mm between 10 s samples unless the drain head is full or rising; require three consecutive readings above a band; subtract the dry-road background recorded at installation (A2); and flag a gauge that has been silent for 30 min [G2].
- **Status.** The rules cover the obvious cases, but the target (one false alert per gauge per year or fewer) can only be checked from a field log. R10 is not verifiable at TRL 3.

## H. Arm, brace and clamps (R15)

- **Wind twist.** Wind along the street at 35 m/s puts 42.3 N on the arm, 6.2 N on the head and 19.0 N on the brace, twisting the arm about the pole with 24.9 N·m [H1]. Two band clamps at 1,000 N preload hold 36.0 N·m by friction, a factor of only 1.45 [H2]. A twisted arm moves the head along the street, not up or down, so it does not bias the depth, but it would put the head over a different part of the gutter or the traffic lane.
- **Anti-rotation bolt (FLG-DDR-002).** An M8 A4-70 through-bolt through the lower clamp band and the pole carries 15.4 kN in shear per plane; the pole wall bears 18.0 kN with an assumed 2.5 mm wall. The lower of the two, acting as a couple across the 60 mm pole, resists 922 N·m, a factor of 37 against the wind twist [H2b]. Drilling the pole needs the asset owner's permission.
- **Misuse.** A 50 kg person hanging on the head gives 132 N·m at the brace joint and 36 MPa in the arm against 214 MPa (factor 5.9); the brace carries 1,213 N against a buckling load of 43,529 N [H3]. The upper clamp pulls 858 N against a band capacity of 2,000 N (factor 2.3), and 1,200 N of slip resistance holds 520 N down [H4].

## I. Mass on the pole (R15)

- **Items.** FieldNode 2.41 kg (FND-CAL-001), arm tube 0.66 kg and brace 0.25 kg (from the model), clamps 0.30 kg, saddle 0.10 kg, radar head 0.25 kg, street cable 0.21 kg (3 m), drain cable on the pole 0.18 kg, through-bolt 0.05 kg, marker plate 0.33 kg [I1].
- **Total.** 4.74 kg against 5.0 kg, a 5 % margin (v0.1: 4.62 kg) [I2]. R15 is met on paper. FieldNode's proposed 0.15 kg sun shield would take it to 4.89 kg, still inside the limit.

## J. Cables and ports (R11 context)

- **Street cable.** With the head at 4.6 m and the FieldNode center at 3.0 m, the run is 2,380 mm; with 300 mm of drip loops it fits a 3 m cable, and the I2C bus is about 350 pF against the 400 pF limit [J1]. Leaving the FieldNode at 2.35 m would have needed a 5 m cable and about 550 pF, over the limit, which is why the node moved up.
- **Drain cable.** The surface route is 4,100 mm; with 500 mm of loops it fits the 5 m cable, which carries UART and the analog wet probe [J2].
- **Ports.** The street head uses port A at 3.3 V (I2C) and the drain head port B at 5 V (UART plus the analog pin), consistent with FieldNode's one switched rail per port [J3].

## K. Submersion (R9)

- Water 600 mm above the road puts 0.90 m (8.8 kPa) over the drain head face; R9 asks for 2.0 m (19.6 kPa) for 72 h, while the stock module is rated IP67 (1 m for 30 min) [K1]. The electronics can be potted, but the transducer face cannot be potted over, so its own seal decides. R9 is at risk until a longer immersion rating or a test shows otherwise.

## L. Installation (R12)

- **Surface work.** Traffic protection 10 min, arm and brace from a mobile platform 15 min, anti-rotation bolt 5 min, FieldNode and street head 15 min, marker 5 min, survey and dry background 10 min, grate lift 5 min, two wall anchors drilled through the grate opening 20 min, tube and head 10 min, surface cable cover 25 min: 120 min in all [L1].
- **Cable route (FLG-DDR-002).** For pilots the drain cable leaves the basin at the grate frame and runs under 0.76 m of bolted steel cover across the gutter strip, up the curb face and across the sidewalk to a riser guard at the pole. The anchors go into the curb and sidewalk only, none into the road [L2]. The conduit (coring the basin wall and a 0.56 m trench) is kept for permanent sites installed with road works.
- **R12 is still not met,** now on time alone: 120 min against 90 min, with no civil work. A new proposal is in `docs/REVIEW.md`.

## M. Cost (R16)

- The BOM has 10 lines, all priced. FloodGauge-specific parts (lines 2 to 10) cost $153.50 against the $160 in `project.yaml` (approved by Amish on 2026-09-26; was $150), a $6.50 margin; with the $126.00 FieldNode core, a complete gauge costs $279.50 [M1]. The surface cable cover ($14.00, replacing the $8.00 conduit) and the through-bolt ($2.00) account for the rise from $145.50. R16 is met on paper. Radar module, housing and cover prices are indicative.

## Results

*Table 4. Requirement status (also written to `docs/04-calcs/results.csv`).*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R12 | Installation | 120 min on the surface route; no civil work | 90 min, surface only, no basin entry | **Not met** |
| R7 | Airtime | 23.7 s/day at SF9; event 1 % met SF7 to SF10, not SF11 or SF12 | 1 % always; TTN 30 s/day in normal mode | At risk |
| R9 | Drain head submersion | Potted head; transducer face seal IP67 only | IP68, 2 m, 72 h | At risk |
| R14 | Operating environment | FieldNode R2 and R3 heat findings (inherited); A02YYUW rated -15 to 60 °C | -20 to 50 °C | At risk |
| R10 | False readings | Rules defined; curb echo needs a recorded background | 1 false alert per year or fewer | Not verifiable at TRL 3 |
| R1 | Street depth range | Lens 4.60 m clears a 4.3 m vehicle; range 1.9 to 5.0 m over the band; module to 20 m | 0 to 600 mm; head 2.5 to 5.0 m per site | Met on paper |
| R2 | Street depth accuracy | Radar ±6.5 mm (sum ±12.0 mm), module accuracy assumed; ultrasonic variant ±27.0 mm | ±10 mm | Met on paper |
| R3 | Drain level range | Continuous from 1,250 to 330 mm below the road; wet probe at 310 mm | 50 mm above floor to 330 mm below road, drain-full above | Met on paper |
| R4 | Drain level accuracy | ±11.0 mm with NTC; ±19.7 mm without | ±20 mm | Met on paper |
| R6 | Alert latency | 82 s at the 95th percentile; 110 s worst without packet loss | 120 s, 95 % of events | Met on paper (private gateway) |
| R8 | Energy autonomy | 68 days nominal, 47 days at -20 °C | 5 days at event sampling | Met on paper |
| R13 | Level datum | Tape and radar dry-background survey; yearly marker check | ±5 mm | Met on paper |
| R15 | Mounting | 4.74 kg; twist factor 37 with the through-bolt | 40 to 60 mm poles; 5 kg | Met on paper |
| R16 | Cost | $153.50 FloodGauge-specific; $279.50 with FieldNode | $160 FloodGauge-specific | Met on paper |
| R5 | Sampling rate | 60 s and 10 s schedule in the sampling logic | 60 s; 10 s in events | Met by design |
| R11 | Privacy | Levels, status and battery only | No camera or microphone | Met by design |
| R17 | Open data | JSON or CSV through the gateway | Open format | Met by design |

Counts: 1 not met, 3 at risk, 1 not verifiable at TRL 3, 9 met on paper, 3 met by design.

## Changes in v0.3 (budget approved)

- `budget_usd` $150 to $160, approved by Amish on 2026-09-26 (FLG-DDR-002). R16 not met to met on paper, $6.50 margin.

## Changes in v0.2 (FLG-DDR-002)

- Lens height 2.95 m to 4.6 m; R1 band 2.5 to 3.5 m to 2.5 to 5.0 m, set per site. R1 stays met; the vehicle clearance problem is closed.
- FieldNode center 2.35 m to 3.0 m; street cable 2 m to 3 m (I2C about 250 to 350 pF).
- R3 restated; not met to met on paper.
- Cable route: conduit (civil work) to a surface cover for pilots. R12 installation 90 min plus civil work to 120 min with none; still not met.
- Anti-rotation M8 through-bolt: twist factor 1.45 to 37.
- Mass on the pole 4.62 kg to 4.74 kg.
- FloodGauge-specific cost $145.50 to $153.50; complete gauge $271.50 to $279.50. R16 met to not met.
- Street depth error, radar ±6.3 mm to ±6.5 mm (pole expansion over the taller height).

## Changes to the TRL 2 figures (v0.1)

- Parts cost: FloodGauge-specific $145.50 (was about $145) after adding an NTC to the drain head; complete gauge $271.50 (was about $271).
- Mass on the pole: 4.62 kg (was about 3.1 kg), because FieldNode is now 2.41 kg.
- FieldNode center lowered from 2.5 m to 2.35 m above the road in the model, so that its panel clears the knee brace (drawing FLG-DWG-001, Detail A).
- Alert latency: 82 s at the 95th percentile (TRL 2 gave 70 s typical and 110 s worst, which stand).
- Airtime: event reporting on The Things Network lasts about 27 min at SF9 (TRL 2 said about 24 min).
- R3 was "met by design" at TRL 2 and is not met; R12 was "at risk" and is not met.
