---
doc_id: FLG-STM-001
title: FloodGauge STEM check
project: FloodGauge
doc_type: STEM check
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: Initial check at the kit 1.9.1 upgrade, with the independent review; one detail failure fixed under the standing instruction (FLG-DDR-004 F1)
---

# FloodGauge STEM check

Verdict: the working principles of all three concept options sit within known science. Of 32 claims, 15 are within known science and 17 are plausible and wait for a data sheet, a weighed mass or a TRL 4 test; none fails outright. The independent review (below) changed five verdicts and statuses. One detail failed on the first pass and was fixed under Amish's standing instruction of 2026-10-23: the solid ring floats of option C sank (FLG-DDR-004 F1). The check stays open until the plausible rows are closed. Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`; the full sizing is in FLG-CAL-001.

## Claims checked

Table 1. Claims, governing science and verdicts. S rows belong to option A (the current design), B rows to option B and C rows to option C. First-order checks use the geometry in `cad/src/model.py`; values marked "assumed" are listed under Assumptions below.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | A: the street radar (60 GHz, module range 20 m) reaches the dry road 4.6 m below the lens and the water surface in between | Physics | Waves and radar | Free-space propagation of a 60 GHz pulse; module range 20 m (Acconeer product page, as cited in FLG-PRB-001, 2026-09-25) | 5 m <= 20 m | Within known science | FLG-CAL-001 A1b |
| S2 | A: street depth error stays within 10 mm when the radar module is accurate to 2 mm (assumed) and datum, pole expansion and ripple add 5, 2 and 3 mm | Physics | Measurement error | Root sum square of independent errors; the 2 mm module accuracy is assumed (S3), so the budget holds only if the module meets it | 2 mm <= 7.88 mm: the module may be as poor as 7.9 mm before the 10 mm limit is reached, but pole bow in the sun (about 3 mm for a 5 K difference across the pole, independent review) and the worst-case sum of 12 mm are not inside the RSS | Plausible, to confirm at TRL 3 |  |
| S3 | A: a 60 GHz carrier (wavelength 5.00 mm) gives a 2 mm range accuracy | Physics | Waves and radar | Coherent radar reads range from the phase of the echo: a 1 mm change in range shifts the phase by 4 pi / lambda = 2.52 rad, so 2 mm is several radians of phase | Phase argument supports mm-level accuracy, but the module's guaranteed accuracy, beam width through the PTFE lens and curb echo rejection are not in a data sheet yet | Plausible, to confirm at TRL 3 |  |
| S4 | A: speed of sound c = 331.3 + 0.606 T (m/s) used to compensate the drain ranger over -20 to 50 C | Physics | Acoustics | Ideal gas: c = sqrt(gamma R T / M) with gamma 1.4, R 287.05 J/(kg K); worst deviation 0.34 % over the range | claimed 361.6 m/s at 50 C, estimate 360 m/s at 50 C (ratio 1.00) | Within known science | FLG-CAL-001 B2 |
| S5 | A: drain level error stays within 20 mm at the 950 mm maximum range, with the NTC correcting air temperature to 2 K (10 mm module accuracy, 3 mm datum) | Physics | Acoustics | Two-way time of flight, c = 331.3 + 0.606 T; root sum square of module, temperature and datum errors (an uncompensated 10 K swing would add 16.8 mm); if the module accuracy is plus or minus (1 cm + 0.3 % of range) the error is about 13.6 mm, and humidity in a saturated basin adds a further 0.3 to 1 % to c, both to check on the data sheet | 11 mm <= 20 mm | Within known science | FLG-CAL-001 C1 |
| S6 | A: the ultrasonic ranger (60 degree beam) reads the water surface 0.3 m to 1.25 m below it inside a 69 mm bore tube | Physics | Acoustics | The axial echo off the water is the shortest path for a smooth wall; but slot edges, joints, the cable loop and drops inside the tube can return an echo before the water echo, so the first echo is not always the water | Smooth-wall geometry supports it; echoes from the slot edges, the cable loop and condensation on the face are not excluded by the module (independent review), so the wet probe and a recorded empty-tube background are needed | Plausible, to confirm at TRL 3 |  |
| S7 | A: the slotted stilling tube follows a basin rising at 10 mm/s with a lag head under 5 mm even with only the lowest slot row wet | Physics | Fluid mechanics | Orifice flow, v = Q / (Cd A) with Cd 0.6, head = v^2 / 2 g | 0.198 mm <= 5 mm | Within known science | FLG-CAL-001 C4 |
| S8 | A: the 40 x 40 x 1.6 mm aluminium arm survives a 50 kg person hanging on the head (misuse case) | Physics | Strength of materials | Cantilever to the top brace pin, sigma = M / Z; 6063-T6 class yield 214 MPa (typical, assumed) | 60 MPa <= 214 MPa | Within known science | FLG-CAL-001 H3 |
| S9 | A: the 25 x 25 x 1.6 mm knee brace and its pins carry the same load | Physics | Strength of materials | L/r = 37 is below the Euler range, so Johnson inelastic buckling (28533 N) and pin bearing in 1.6 mm walls (11520 N) apply; the Euler value (73 kN) is not valid | 1504 N <= 1.152e+04 N | Within known science | FLG-CAL-001 H3 |
| S10 | A: two band clamps alone hold the arm against the twist of a 35 m/s wind along the street (60 mm pole; on a 40 mm pole friction gives 24.0 N m) | Physics | Strength of materials | Coulomb friction, mu 0.30, 1 kN preload per band (FieldNode assumption); wind drag, q = 0.5 rho v^2 | 24.8 N m <= 36 N m | Plausible, to confirm at TRL 3 | S11 carries the twist as a second path; on a 40 mm pole it is the only one |
| S11 | A: the M8 A4-80 anti-rotation through-bolt holds the arm against the same twist | Physics | Strength of materials | The bolt bends as a 21.7 mm cantilever out of the pole wall through the spacer (independent review corrected the first couple model): M = f_y Z, f_y 600 MPa (A4-80), stress-area section; plate load 52 mm from the pole axis | 24.8 N m <= 44.6 N m | Plausible, to confirm at TRL 3 | FLG-CAL-001 H2b; FLG-DDR-004 F2 (class raised from A4-70 to A4-80) |
| S12 | A: the added mass on the pole stays at or under 5 kg | Engineering and technology | Mass budget | Sum of part volumes times density from the CAD model plus FieldNode 2.45 kg and cables (FLG-CAL-001 I1, I2) | 4.994 kg <= 5 kg | Plausible, to confirm at TRL 3 | weigh at TRL 4; FLG-DEC-001 item 3 (bracket plate to 2.5 mm) |
| S13 | A: pole expansion moves the lens by about 2 mm over a 35 K swing | Physics | Thermodynamics | Linear expansion, dL = alpha L dT with steel alpha 12e-6 per K | claimed 2 mm, estimate 1.98 mm (ratio 1.01) | Within known science | FLG-CAL-001 B1 |
| S14 | A: stored energy runs the sensors for 5 days without sun at event sampling | Physics | Energy balance | Usable 15.36 Wh (FND-CAL-001), draw from the sampling cycle energy of FLG-CAL-001 D1 to D4; days at -20 C used | 5 days <= 47 days | Within known science | FLG-CAL-001 D4 |
| S15 | A: normal-mode uplinks (every 15 min, 20-byte payload, SF9) stay within The Things Network fair use of 30 s airtime per day | Engineering and technology | Radio | LoRa time on air (Semtech formula); fair use 30 s/day (The Things Network, checked 2026-10-31) | 23.7 s/day <= 30 s/day | Plausible, to confirm at TRL 3 | FLG-CAL-001 E1; PR-007 stays at risk at SF10 and slower |
| S16 | A: event-mode uplinks every 60 s at SF9 stay within the EU868 1 % duty cycle | Engineering and technology | Radio | Duty cycle = time on air / interval; limit 1 % (EU868 sub-band, ETSI EN 300 220; text not reopened, see FLG-REG-001) | 0.41 % <= 1 % | Within known science | FLG-CAL-001 E1 |
| S17 | A: the drain head face, 0.9 m under water in the worst design flood, stays inside the 1 m rating of its IP67 module | Physics | Fluid mechanics | Hydrostatic head p = rho g h; IP67 is 1 m for 30 min (IEC 60529) | 0.9 m <= 1 m | Plausible, to confirm at TRL 3 | PR-009 stays at risk: 72 h duration unverified (FLG-CAL-001 K1) |
| S18 | A: the drain head survives 72 h under silty stormwater at 2 m (IP68) | Engineering and technology | Ingress protection | IP68 is defined by agreement with the maker, not by the code; the potted electronics are sealed but the transducer face keeps the stock IP67 seal | Not shown by calculation; needs the module maker's rating or an immersion test at TRL 4. Pressure at 2 m is 19.6 kPa | Plausible, to confirm at TRL 3 |  |
| S19 | A: stainless A4 fasteners in a 6063 aluminium arm and bracket survive road-salt spray for the life of the pilot | Chemistry | Corrosion | Galvanic couple of stainless steel and aluminium; the cathode (fastener) is small and the anode (aluminium) large, the favourable area ratio, and anodising or sleeves separate them | Favourable area ratio and crush sleeves; chloride splash can still pit the aluminium at the contact, to confirm with a coating or an isolating washer at TRL 3 | Plausible, to confirm at TRL 3 |  |
| S20 | A: the PVC stilling tube stays below its service temperature in a shaded basin | Chemistry | Materials | PVC-U typical maximum continuous service temperature 60 C (manufacturer data, to confirm for the chosen pipe); PVC-U also turns brittle in the cold, so impacts at -20 C are a handling risk | 35 C <= 60 C | Within known science | BOM item 5 |
| S21 | A: 5 x 50 mm slots in the stilling tube stay open in silty, leaf-laden stormwater for a season | Biology | Fouling | Slots 5 mm wide pass silt but clog with leaf litter and biofilm over weeks in warm standing water; 40 slots in 10 rows leave 75 % of the open area if a quarter clog | Open area is 10000 mm2 against a 3739 mm2 bore, so a quarter clogged still passes the flow of S7; cleaning interval to assess | Plausible, to confirm at TRL 3 |  |
| S22 | A: an event-mode alert reaches the service within 120 s at SF10 on a private gateway, worst case without a lost packet (10 s sample, two confirming samples, wake, airtime, duty-cycle wait, 4.7 s network) | Mathematics | Timing budget | Sum of the delays; SF11 gives about 134 s and SF12 about 217 s, so PR-006 holds to SF10 only (independent review) | 81 s <= 120 s | Within known science | FLG-CAL-001 F4 |
| S23 | A: the street head's I2C bus stays within 400 pF on a 3 m cable | Engineering and technology | Electrical interface | Bus capacitance = cable length x pF/m + 50 pF: 350 pF at an assumed 100 pF/m; a 150 pF/m cable gives 500 pF | Passes at the assumed cable; the real cable's capacitance is on its data sheet | Plausible, to confirm at TRL 3 |  |
| B1 | B: a 0 to 20 kPa vented transducer covers 600 mm in the street (5.9 kPa) and the 1.25 m basin range (12.3 kPa) | Physics | Fluid mechanics | Hydrostatic pressure p = rho g h, gauge pressure against the vented atmosphere | 12.26 kPa <= 20 kPa | Within known science | FLG-OPT-001 Table 1 |
| B2 | B: street depth error stays within 10 mm (0.25 % of a 20 kPa range, 0 to 40 C water density, 5 g/l silt, 5 mm datum) | Physics | Measurement error | Root sum square; water density 999.8 to 992.2 kg/m3; silt density rise = SSC (1 - rho_w / rho_s), rho_s 2.65; accuracy class assumed | 8.7 mm <= 10 mm | Plausible, to confirm at TRL 3 | FLG-OPT-001 Table 2 |
| B3 | B: the vented cable keeps the atmospheric reference dry for years | Chemistry | Humidity and condensation | A vented gauge transducer breathes through its cable; condensation or water in the vent tube shifts the zero | Desiccant or a PTFE vent membrane is the usual remedy; lifetime in a flooded basin is not shown | Plausible, to confirm at TRL 3 |  |
| B4 | B: a stand pipe on the curb face does not split or crush the transducer when street water freezes at -20 C | Physics | Phase change | Water expands about 9 % on freezing and can split a closed pipe; the bottom cap has four drain holes, so only a film freezes | Drain holes leave no standing column after an event; a trapped film is expected to be harmless, to confirm | Plausible, to confirm at TRL 3 |  |
| C1 | C: the street float (hollow shell, 42 mm OD) floats with its magnet at under 70 % of its volume submerged | Physics | Fluid mechanics | Archimedes: weight (shell 29.2 g, plus about 3 g of foam) = displaced water; solid ring first pass was 44.4 g against 33.7 g of buoyancy and sank; the voids are filled with closed-cell foam (about 3 g) so a leaking shell still floats (FLG-DDR-004 F1) | 61 % of buoyancy used <= 70 % of buoyancy used | Within known science | FLG-DDR-004 F1 (fix rule); model options_bc.py |
| C2 | C: the basin float (hollow shell, 56 mm OD) floats with its magnet at under 70 % of its volume submerged | Physics | Fluid mechanics | Archimedes: weight (shell 47.0 g, plus about 3 g of foam) = displaced water; solid ring first pass was 106.5 g against 97.4 g and sank | 48 % of buoyancy used <= 70 % of buoyancy used | Within known science | FLG-DDR-004 F1 (fix rule); model options_bc.py |
| C3 | C: a reed chain at 25 mm pitch reads the level to 25 mm steps (plus or minus 12.5 mm) | Mathematics | Quantisation | Resolution of a switch chain = pitch; the level is the highest closed reed, with one or two reeds closing at once, so the error is at most one pitch | True as stated. It exceeds the 10 mm street target of PR-002, so this is scored against the user requirements in FLG-OPT-001, not a failure of the science | Within known science |  |
| C4 | C: a ring magnet beside the sealed stem closes a glass reed switch 1.9 mm from the stem axis | Physics | Magnetism | Reed switches close at 10 to 30 ampere-turns of applied field; a sintered ring magnet at a few millimetres gives a field far above that; hysteresis spreads the closing height by a few mm | Plausible; the closing height and its spread need the reed's data sheet, assumed typical 10 to 30 AT | Plausible, to confirm at TRL 3 |  |
| C5 | C: the floats move freely on 16 mm stems in silty stormwater and at -20 C | Biology | Fouling | Silt and biofilm in the 0.9 mm radial gap between bore and stem can bind a float; ice binds it solid in a frozen tube | Plausible; the bottom cap drain holes empty the street pipe, the basin float is not protected from ice, to assess in OPT scoring | Plausible, to confirm at TRL 3 |  |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**.

## Assumptions

- Radar module accuracy 2 mm, 25 degree beam and range 20 m (Acconeer product page, as cited in FLG-PRB-001, 2026-09-25): accuracy and beam are assumed, there is no data sheet in the repo yet.
- Aluminium 6063-T6 class, yield 214 MPa, E = 69 GPa; band clamp preload 1,000 N and friction 0.30 (FieldNode assumption); pole wall 2.5 mm and f_u 360 MPa.
- Pressure transducer class 0.25 % of a 20 kPa full scale for option B; typical, not quoted.
- Reed switch operate range 10 to 30 ampere-turns for option C; typical, not quoted.
- Polypropylene 900 kg/m3 and sintered NdFeB 7,500 kg/m3 for the floats.

## Fields not relevant

- **Biology:** no living material; the only biological claims are fouling of the slots and floats (S21, C5).
- **Chemistry:** no reaction or dosing; the claims are corrosion and polymer service temperature (S19, S20) and vent condensation (B3).

## Concept options

- **A, radar and ultrasonic (current design):** within known science; S2, S3, S6, S10 to S12, S15, S17 to S19, S21 and S23 are plausible and wait for the radar and ranger data sheets, the weighed mass, the module immersion rating and a coating decision.
- **B, hydrostatic pressure:** within known science; the 8.7 mm street error (B2) is inside 10 mm only with the assumed transducer class, and the vent and freezing rows (B3, B4) are plausible.
- **C, float and reed chain:** within known science after fix F1; the 25 mm pitch (C3) is a requirement miss for PR-002, not a physics failure, and is scored in FLG-OPT-001.

## Fix made under the standing instruction

**F1, hollow floats (FLG-DDR-004).** The first model of option C used solid polypropylene ring floats with an 8 mm ring magnet. Archimedes' principle showed they sink: the street float weighs 44.4 g against 33.7 g of buoyancy, the basin float 106.5 g against 97.4 g (`stem_check.py` prints the record). The fix keeps the working principle: sealed hollow polypropylene shells with 1.6 mm walls and a 5 mm ring magnet, the street float widened from 38 to 42 mm. They then weigh 29.2 g and 47.0 g and ride at 61 % and 48 % of their buoyancy, so C1 and C2 close. The independent review added closed-cell foam in the voids so that a leaking shell still floats. The model, `cad/fidelity.json` and FLG-DEC-001 carry the change. A second fix, F2 (through-bolt class), came from the review (FLG-DDR-004).

## Independent review

A second agent (Claude, model claude-opus-5-5, run headless with no tools beyond reading the files and arithmetic) saw only this STEM check, the calculation note FLG-CAL-001, the product requirements FLG-PRS-001 and `sizing.py`, not the reasoning behind them. It was asked to refute the headline results and every "Within known science" verdict. It could not run `sizing.py` (the model is not in its folder) and recomputed from the stated inputs. Most results survived: the error budgets, airtime, energy, tube lag, arm stress, the speed-of-sound formula and the cost arithmetic. It found five things that changed a verdict or a requirement status, and ten smaller points.

**Changed a verdict or status, and what was done (fix rule, FLG-DDR-004):**

1. **S11, the through-bolt (refuted).** The couple model across the full pole was the wrong load path; the bolt bends as a cantilever through the spacer and resists 28 to 48 N m, not 922 N m. The factor of 37 was wrong. Fix F2: class A4-80 bolt, bending model in CAL H2b, factor 1.8 (1.3 for A4-70); S11 is now "Plausible, to confirm at TRL 3" and PR-015 is restated. Small poles remain thin: friction alone gives 0.97 on a 40 mm pole.
2. **S12 and PR-015, mass.** A 6 g margin on 4.994 kg is inside the accuracy of the estimate, and the 2.5 mm plate fallback saves only 45 g. PR-015 is now "At risk" (it was "Met on paper").
3. **PR-006, latency.** Held only to SF10; in event mode the 95th percentile is 123 s at SF11 and 201 s at SF12 (reproduced in CAL F4). PR-006 is limited to SF9 and SF10; new row S22.
4. **S2, street depth error.** It rested on the assumed 2 mm radar accuracy, which S3 calls plausible. S2 is now "Plausible, to confirm at TRL 3".
5. **C1 and C2, floats.** The sealed hollow shell moves the failure to leaks and pressure cycling of the sealed air. Fix F1 now fills the voids with closed-cell foam, so a leaking shell still floats; the model carries the foam as its own part. The rows stay within known science for buoyancy; sealing and creep are for the TRL 4 leak test.

**Smaller points, applied:** the brace used the Euler load where L/r = 37 makes it invalid (Johnson buckling and pin bearing now used: capacity 11.5 kN against 1.5 kN, S9); the wall-echo reasoning in S6 was wrong for slot edges and the cable loop (text corrected); the drain error if the ranger is plus or minus (1 cm + 0.3 % of range) and humidity in a saturated basin are noted in S5 and make the NTC mandatory; PVC brittleness at -20 C is noted in S20; I2C capacitance at 150 pF/m is now S23; the pole bow term (about 3 mm for 5 K across the pole) is noted in S2; stale text about the 150 mm band in CAL F was corrected.

**Not changed:** the float dead band (about 26 mm of water before a 42 mm float lifts) and the false-reading step rule against surges faster than 300 mm/min are logged for the design review; the sun-induced pole bow is not yet in the error budget. The reviewer also asked whether the 214 MPa yield is typical rather than minimum; with a 170 MPa minimum the arm still passes at a factor of 1.4.


## Sources

- Acconeer. "Products." <https://www.acconeer.com/products/>. Range 20 m, as cited in FLG-PRB-001 and first checked 2026-09-25; not reopened in this session.
- DFRobot. "A02YYUW waterproof ultrasonic sensor." <https://www.dfrobot.com/product-1935.html>. Checked 2026-09-25 (3 to 450 cm, plus or minus 1 cm, IP67).
- The Things Network. "Fair Use Policy explained." <https://www.thethingsnetwork.org/forum/t/fair-use-policy-explained/1300>. Checked 2026-10-31 (30 s/day).
- Legal Information Institute. "47 CFR 15.255." <https://www.law.cornell.edu/cfr/text/47/15.255>. Checked 2026-10-31.
- Archimedes' principle, hydrostatic pressure p = rho g h, Euler buckling, Coulomb friction, ideal-gas speed of sound and orifice flow: standard textbook relations.
- IEC 60529 (IP codes) and EU868 duty cycle rules are relied on from general knowledge and not reopened in this session (FLG-REG-001).
- FLG-CAL-001 (docs/04-calcs/01-sizing.md) and FLG-PRS-001 for the values the rows close against.
