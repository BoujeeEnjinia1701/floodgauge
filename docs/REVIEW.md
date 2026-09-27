# Review note: FloodGauge

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (FLG-PRB-001 v0.2): problem in numbers with cited sources, the two ways streets flood (drain backing up and blocked inlet), users, operating context, constraints, prior work (FloodNet, low-cost ultrasonic and 60 GHz radar modules), out of scope, open questions; co-design checklist kept.
- `docs/03-requirements.md` (FLG-REQ-001 v0.2): 17 measurable requirements (R1 to R17) with targets, verification method and status at TRL 2, plus assumptions and a list of requirements not met.
- `docs/02-concept.md` (FLG-PRC-001 v0.2): how it works, numbered components, first-order numbers with assumptions, design choices with options, safety section, open questions.
- `cad/src/concept_media.py`: massing model of a street strip (road, gutter, curb, sidewalk), catch basin with outlet and illustrative water level, existing sign pole, and the kit parts numbered 1 to 8. The scene uses a manually placed 1.75 m person on the sidewalk as a context part, because the kit's automatic scale figure would stand on the basin floor. A custom exploded view shows the kit parts only, so the street and basin do not hide them.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `cutaway.png` (section across the street through the inlet), `exploded.png` with BOM callouts, `flow.png` (data flow from water surface to alert), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 10 lines with indicative USD prices; items 1 to 8 match the exploded view. `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; Concept rationale, Burning platform, Where it could be used (6 industries, 6 countries or regions) and What sparked the idea expanded with cited sources; Key components and Safety updated to match the concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Street depth range | 0 to 600 mm with the head about 2.95 m above the road | R1 met |
| Street depth error, radar | temperature effect negligible; module accuracy unverified | R2 met on paper |
| Street depth error, ultrasonic | about ±100 mm uncompensated, about ±15 mm compensated | R2 not met |
| Drain level error | about ±15 mm | R4 met on paper |
| Sensor load | about 1.2 mW at 60 s sampling, about 7 mW at 10 s | R8 met (FieldNode allowance about 115 mW) |
| Uplink airtime | about 24 s/day normal; about 15 s per event hour | R7 partly met |
| Alert latency | about 70 s typical, about 110 s worst case | R6 met on paper, thin margin |
| Mass on the pole | about 3.1 kg | R15 met |
| Parts cost | about $271 including the $126 FieldNode; about $145 FloodGauge-specific | **R16 not met** |

Requirements not met or at risk:

- **R16 cost not met:** about $271 against the $150 in `project.yaml`.
- **R9 submersion not met** by the stock IP67 ultrasonic module; a potted head is proposed but unproven.
- **R7 not met on The Things Network** for events longer than about 24 min at 1 min reporting (fair use 30 s/day).
- **R12 installation at risk:** the conduit from basin to pole needs coring and trenching.
- **R10 false alerts unverified:** parked vehicles or people under the street head must be rejected by plausibility logic.

### Proposed, awaiting Amish (status updated 2026-09-25: see FLG-DDR-002)

1. **Budget.** Options: (a) cost FieldNode in its own repo and hold FloodGauge-specific parts to $150 (about $145 now); (b) raise `budget_usd` to $300; (c) cut to a street-only ultrasonic variant (about $188, still over $150, and misses R2). Recommendation: (a), with R16 reworded as "FloodGauge-specific parts $150 or less; FieldNode costed separately". `project.yaml` is unchanged. **Decided by Amish, 2026-09-25: go with recommendation.**
2. **Two heads on one node** (street and drain) versus street only or drain only. Recommendation: both. **Decided by Amish, 2026-09-25: go with recommendation.**
3. **Street head sensing:** 60 GHz radar versus ultrasonic. Recommendation: radar, with ultrasonic documented as the lower-cost variant. **Decided by Amish, 2026-09-25: go with recommendation.**
4. **Drain head:** ultrasonic in a slotted stilling tube with a wet probe, versus radar. Recommendation: ultrasonic in a tube. **Decided by Amish, 2026-09-25: go with recommendation.**
5. **Arm over the gutter** versus a head over the sidewalk. Recommendation: over the gutter at 2.95 m or higher, subject to the road authority's clearance rules. **Decided by Amish, 2026-09-25: go with recommendation.**
6. **Alert bands** at 150 mm and 300 mm of water above the road, from NWS guidance, plus a drain-full alert. Recommendation: defaults, to be set locally with the partner city. **Decided by Amish, 2026-09-25: go with recommendation.**
7. **Network:** private or city LoRaWAN gateway (TwinKit) for event reporting, TTN for pilots only. Recommendation: private gateway. **Decided by Amish, 2026-09-25: go with recommendation.**
8. **Pilot partner and city** for co-design and a first site. No recommendation; still Proposed, awaiting Amish.
9. `project.yaml` pitch and problem: no change proposed; the numbers found support them. **Decided by Amish, 2026-09-25: go with recommendation.**

### Safety concerns

- Work beside live traffic and at height on poles near overhead lines.
- Catch basins are confined spaces with possible toxic or oxygen-poor air and fast-rising water; the design is installed from the surface only. Heavy grates are a crush hazard. Stormwater is a biological and chemical hazard.
- LiFePO4 cell in FieldNode (about 19 Wh): fusing and the 0 to 45 °C charge window.
- Over-reliance: a silent or failed gauge can hide a flood. The alert service must flag missing reports, and FloodGauge must be presented as a supplement to official warnings.
- An arm over the gutter can be struck by tall vehicles if mounted too low.

### Problems and notes

- The kit's automatic scale figure is placed at the lowest point of the model (here the basin floor), so the person is passed as a context part instead. The hero note therefore reads "Grey: Person, 1.75 m (scale) for scale", and the blueprint isometric sublabel reads "grey is for scale".
- Radar module accuracy, current and price could not be verified from a data sheet in this session; the estimates are marked as assumptions.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 5. If approved, run `/advance-trl3` to check the error budgets, latency and airtime by calculation, confirm the radar module data, and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (FLG-DDR-001 v0.1, status proposed): nine items adopted as recommended for TRL 3, open for Amish's review (D1 to D9), and one left open (O1, pilot partner and city).
- `docs/04-calcs/01-sizing.md` (FLG-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: range and geometry, street and drain error budgets, stilling tube hydraulics, energy, airtime, alert latency (simulated), false readings, arm and clamp loads, mass, cables and ports, submersion, installation time and cost, with a status for every requirement. The script imports the model, reads the BOM and `project.yaml`, prints every number the note quotes with a tag, and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model (FieldNode core and panel, radar head, arm with brace and band clamps, drain head, slotted stilling tube with brackets, cables, conduit and riser guard, depth marker with bands) plus the existing street, basin and pole as context. Exports `cad/step/` and `cad/stl/` for `floodgauge-assembly`, `floodgauge-pole-kit`, `floodgauge-drain-kit` and `floodgauge-site`.
- `cad/src/sheets.py` and `cad/drawings/FLG-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1 (overall views 1:50, Detail A 1:10, Section B 1:20), marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". FLG-DWG-001 was free because the concept blueprint is FLG-DWG-010.
- `bom/bom.csv` (10 lines, all priced with a supplier or supplier type) and `bom/bom-notes.md`: $145.50 FloodGauge-specific against the $150 budget; $271.50 with FieldNode.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked; temporary `_views` folders deleted.
- FLG-PRB-001, FLG-PRC-001 and FLG-REQ-001 revised to v0.3; `README.md` (TRL badge and line, budget line, links, components, key numbers, safety) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

Design changes found necessary by the calculations, within the adopted choices: an NTC in the drain head for speed-of-sound compensation (+$0.50), a recorded dry-road background for the radar because its beam lights the curb, and the FieldNode lowered from 2.5 m to 2.35 m so that its panel clears the knee brace.

### Requirement status (FLG-CAL-001, Table 4)

2 not met, 3 at risk, 1 not verifiable at TRL 3, 8 met on paper, 3 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R3 Drain level range | **Not met** | Continuous only to 330 mm below the road; the top 290 mm below the grate has the wet probe alone (TRL 2 said met by design) |
| R12 Installation | **Not met** | 90 min for surface work alone; the conduit needs coring and trenching |
| R7 Airtime | At risk | 23.7 s/day at SF9; event reporting breaks 1 % at SF11 and SF12; TTN allows about 27 min of events at SF9 |
| R9 Submersion | At risk | 0.90 m over the head at 600 mm street depth; transducer face only IP67 |
| R14 Environment | At risk | Inherits FieldNode's interior heat finding; drain module rated -15 to 60 °C |
| R10 False readings | Not verifiable at TRL 3 | Rules defined; the curb echo would read 139 mm if not rejected |
| R1, R2, R4, R6, R8, R13, R15, R16 | Met on paper | 2.95 to 2.35 m range; ±6.3 mm radar (module accuracy assumed); ±11.0 mm drain; 82 s at the 95th percentile, 110 s worst; 68 days autonomy; ±5 mm datum; 4.62 kg; $145.50 |
| R5, R11, R17 | Met by design | |

Key numbers: 85.1 mJ per sampling cycle; 9.3 % of the FieldNode 100 mW allowance with event sampling all day; tube lag under 5 mm at 50 mm/s; arm twist factor 1.45 in a 35 m/s gust; 50 kg hanging on the head stresses the arm to 36 MPa.

### Decisions recorded (FLG-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review, and since then Decided by Amish, 2026-09-25: go with recommendation (FLG-DDR-002): D1 FieldNode costed in its own repo, R16 restated to "FloodGauge-specific parts $150 or less; FieldNode costed separately" (`budget_usd` unchanged at $150; no new figure was recommended); D2 two heads on one node; D3 radar street head, ultrasonic as the lower-cost variant; D4 ultrasonic drain head in a slotted stilling tube with a wet probe; D5 arm over the gutter at 2.95 m or higher, subject to clearance rules; D6 alert bands 150 mm and 300 mm plus drain-full, set locally with the partner city; D7 private or city gateway for event reporting, TTN for pilots only; D8 levels only, no imaging; D9 no change to pitch or problem, so `project.yaml` and `README.md` keep the existing wording.

### Still awaiting Amish

1. **O1, pilot partner and city** for co-design and a first site. No preference stated; no recommendation made.
2. **New, R3 wording.** Recommendation: restate R3 as "continuous reading from 50 mm above the basin floor to 330 mm below the road, plus a drain-full signal above that". **Decided by Amish, 2026-09-25: go with recommendation.** Applied (DDR-002 N1).
3. **New, head height and R1.** At 2.95 m the head is inside a 4.0 to 4.3 m vehicle envelope at the curb. Options: (a) widen the R1 mounting band to 2.5 to 5.0 m and set the height per site to the road authority's clearance rule (about 4.6 m where trucks use the curb lane); (b) keep 2.95 m only where the curb lane carries no tall vehicles. Recommendation: (a). **Decided by Amish, 2026-09-25: go with recommendation.** Applied (DDR-002 N2).
4. **New, R12 cable route.** Options: (a) conduit as now (civil work); (b) surface route out at the grate frame and along the curb face under a bolted steel cover; (c) a second FieldNode for the drain head. Recommendation: (b) for pilots, (a) at permanent sites installed with road works. **Decided by Amish, 2026-09-25: go with recommendation.** Applied (DDR-002 N3).
5. **New, arm anti-rotation.** Friction alone gives a twist factor of 1.45. Recommendation: add a through-bolt or pinned clamp as a design detail. **Decided by Amish, 2026-09-25: go with recommendation.** Applied as a through-bolt (DDR-002 N4).
6. **Suggestion only, not in the repo:** a first alert band below 150 mm, since in a fast flood the 150 mm alert arrives at about 190 to 250 mm; a matter for the partner city under D6. **Decided by Amish, 2026-09-25: go with recommendation.** Applied as a configurable band, depth set with the partner city (DDR-002 N5).

### Cross-repo consistency

- FieldNode (FND REVIEW, TRL 3): FloodGauge uses its 15.36 Wh usable, 4.0 mWh/day core, 246.8 ms SF9 airtime, 2.41 kg, $126.00 and two M12 ports with one switched rail each (street head at 3.3 V on port A, drain head at 5 V on port B, which uses the analog pin for the wet probe). FloodGauge's worst load (9.3 mW) fits the 100 mW allowance FieldNode recommends, so FieldNode's allowance proposal does not affect this repo. The pin assignment is still FieldNode O2. No conflict.
- FieldNode's R3 (interior heat) and R2 findings carry into FloodGauge R14 as at risk. FieldNode's proposed sun shield would add 0.15 kg, taking FloodGauge to 4.77 kg against 5.0 kg; still within R15.
- FieldNode mass rose from 1.7 kg (TRL 2 estimate used here) to 2.41 kg; FloodGauge's mass figure is updated accordingly.
- TwinKit (TWK REVIEW, TRL 3): the 4.7 s worst forwarding latency and the 1 % uplink loss target are used in the latency budget. TwinKit's R1 loss is marginal at SF9 with 50 nodes at 5 min; FloodGauge's 1 min event reporting adds load during storms, when every gauge in a city reports at once. Worth a check in TwinKit when a pilot size is known; noted here, TwinKit not edited.
- No other shared component (CellGuard, MotionCore, ThermaCart, CalRig) is used.

### Safety concerns

- Vehicle strike: an arm at 2.95 m over the gutter can be hit by trucks, buses or mirrors at the curb. Mount to the road authority's clearance height.
- Arm rotation in high wind (factor 1.45) could swing the head over the traffic lane; add an anti-rotation stop.
- Catch basins are confined spaces with possible toxic or oxygen-poor air and fast-rising water; installation is from the surface, but drilling anchors through the grate opening still needs care. Heavy grates are a crush hazard. Stormwater is a biological and chemical hazard.
- Work beside live traffic and at height near overhead lines.
- FieldNode LiFePO4 cell (about 19 Wh): fusing, protection and the 0 to 45 °C charge window, as in FieldNode.
- Over-reliance: a silent gauge can hide a flood; the alert service flags gauges silent for 30 min, and FloodGauge supplements official warnings.

### Gaps and notes

- Citations: no citations were flagged as unchecked in the TRL 2 note. WebFetch confirmed the A02YYUW figures on the DFRobot page (±1 cm, 60°, 8 mA or less, 100 ms, -15 to 60 °C, IP67, $15.90). The Acconeer products page confirmed only the 20 m range and module size; the XM125 product page returned 404 and a distributor page returned an unrelated part, so the radar's accuracy, current, beam width and price remain assumptions and are marked so.
- The kit's cutaway cuts at the mean Y of the parts and keeps the far half; with the scene rotated 180° about Z (as at TRL 2) it shows the section through the inlet and the tube, so no shift was needed.
- In `media/exploded.png`, callout 2 partly covers the small radar head.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. `firmware/` and `electronics/` hold only placeholders. No test, build or firmware material was created.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on D1 to D9, on O1 and on the new items 2 to 5 above. For the record only, TRL 4 would need: a bench build of both heads on a FieldNode; a lab test report (TST, `environment: lab`) covering radar depth accuracy over a water tank with a curb step in the beam, ultrasonic level accuracy in a slotted tube over temperature, immersion of the drain head, sampling energy and the end-to-end alert latency through a gateway; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (FLG-DDR-002 v0.1). Items without a recommendation stay "Proposed, awaiting Amish".

### Decisions applied and what changed

- **D1 to D9** (FLG-DDR-001, now v0.2): status wording only. `budget_usd` stays $150, the recommended figure; the pitch and problem are unchanged (D9).
- **N1, R3 restated** to "continuous reading from 50 mm above the basin floor to 330 mm below the road, plus a drain-full signal above that". R3: not met to met on paper.
- **N2, head height:** R1 band 2.5 to 3.5 m to 2.5 to 5.0 m, set per site. Reference lens 2.95 m to 4.6 m (clears a 4.3 m vehicle plus 0.3 m); existing pole in the model 3.3 m to 4.9 m above the sidewalk. Knock-on change: FieldNode center 2.35 m to 3.0 m and street cable 2 m to 3 m, because a 5 m I2C cable would reach about 550 pF against 400 pF (now 350 pF). Radar depth error ±6.3 mm to ±6.5 mm (pole expansion over the taller height).
- **N3, cable route:** conduit (coring and trenching) to a surface route for pilots under 0.76 m of bolted steel cover, anchored to the curb and sidewalk only. BOM line 7 $8.00 to $14.00. Installation 90 min plus civil work to 120 min with none.
- **N4, anti-rotation:** M8 A4 through-bolt at the lower clamp. Twist factor 1.45 to 37. BOM line 3 $18.00 to $20.00.
- **N5, first alert band below 150 mm:** supported by the alert service, depth set with the partner city (no figure chosen).
- **Totals:** FloodGauge-specific parts $145.50 to $153.50; complete gauge $271.50 to $279.50. Mass on the pole 4.62 kg to 4.74 kg.
- **Files:** `cad/src/model.py` (STEP and STL re-exported), `cad/src/sheets.py` and FLG-DWG-001 Rev P1 to P2, `cad/src/concept_media.py` and all of `media/` re-rendered (hero, blueprint and exploded checked; `_views` folders removed), `docs/04-calcs/sizing.py` and FLG-CAL-001 v0.1 to v0.2, FLG-REQ-001 v0.3 to v0.4, FLG-PRC-001 v0.3 to v0.4, `bom/bom.csv`, `bom/bom-notes.md`, `project.yaml` (evidence list), `README.md` (key components, numbers, safety; "What sparked the idea" rewritten around the September 2021 Ida flooding in New York City). PDFs rebuilt; superseded PDFs removed from `docs/pdf/`.

### Requirement status (FLG-CAL-001 v0.2)

2 not met, 3 at risk, 1 not verifiable at TRL 3, 8 met on paper, 3 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R12 Installation | **Not met** | 120 min on the surface route, no civil work (target 90 min) |
| R16 Cost | **Not met** | $153.50 FloodGauge-specific against $150 |
| R7 Airtime | At risk | Unchanged: 23.7 s/day at SF9; event reporting breaks 1 % at SF11 and SF12 |
| R9 Submersion | At risk | Unchanged: transducer face only IP67 |
| R14 Environment | At risk | Unchanged: FieldNode heat; drain module rated -15 to 60 °C |
| R10 False readings | Not verifiable at TRL 3 | Curb echo would read 143 mm if not rejected |
| R1, R2, R3, R4, R6, R8, R13, R15 | Met on paper | Lens 4.6 m, 1.9 to 5.0 m over the band; ±6.5 mm; restated R3; ±11.0 mm; 82 s at 95 %; 68 days; ±5 mm; 4.74 kg |
| R5, R11, R17 | Met by design | |

### Still awaiting Amish

1. **O1, pilot partner and city.** No recommendation. The depth of the N5 band waits on it.
2. **New, R16 over budget by $3.50.** Options: (a) raise `budget_usd` to $160; (b) hold $150 and cost the surface cover as site installation material, like the conduit it replaces; (c) hold $150 and find savings in the radar housing once a data sheet and quote exist. Recommendation: (b), since the cable route depends on the site and the conduit was already outside the total. Not applied; `budget_usd` stays $150. **Decided by Amish, 2026-09-26: `budget_usd` $160 (option (a)); see "Session 2026-09-26: budget approved".**
3. **New, R12 at 120 min.** Options: (a) relax R12 to 120 min for the pilot route; (b) keep 90 min and prefabricate the cover and bracket set to cut site time (unproven). Recommendation: (a). Not applied.

### Cross-repo actions (other repos not edited)

- **FieldNode:** FloodGauge now mounts the core at 3.0 m (was 2.35 m) and relies on FND-CAL-001's $126.00 and 2.41 kg under D1; the port pin assignment (FieldNode O2) and the sun shield (0.15 kg, would give 4.89 kg on the pole, still under 5.0 kg) remain FieldNode's to settle.
- **TwinKit:** check gateway loss at SF9 when every gauge in a city reports every minute in a storm, once a pilot size is known (carried from the TRL 3 session).

### Safety

- The arm at 4.7 m needs a mobile elevating platform and clearance from overhead lines; drilling the pole for the through-bolt needs the asset owner's permission.
- The surface cable cover crosses the sidewalk: low, beveled, anchored and marked to avoid a trip hazard.
- Confined space, traffic, stormwater and LiFePO4 notes from the earlier sessions stand.

### Gaps and notes

- Callouts 2 and 4 in `media/exploded.png` sit over the small radar and drain heads, which are small at the scale needed for a 4.9 m pole.
- Radar module accuracy, current and price are still assumptions; the cover and bolt prices are indicative.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No build, test, purchasing, PCB or firmware work was done.

## Session 2026-09-26: budget approved

Amish wrote, in chat on 2026-09-26: "i approve all the budget items." The open R16 budget item (O2) is decided: budget set to $160 to cover the priced BOM (FLG-DDR-002 v0.2).

- `project.yaml` `budget_usd` $150 to $160; README budget and cost lines updated.
- R16 target $150 to $160; status **not met to met on paper** ($153.50 FloodGauge-specific, $6.50 under; $279.50 with the FieldNode core, which stays costed in its own repo).
- Requirement counts (FLG-CAL-001 v0.3): 1 not met (R12), 3 at risk, 1 not verifiable, 9 met on paper, 3 met by design.
- Documents: FLG-PRB-001 v0.4, FLG-PRC-001 v0.5, FLG-REQ-001 v0.5, FLG-CAL-001 v0.3 (`sizing.py` target now read from `budget_usd`; `results.csv` regenerated), FLG-DDR-002 v0.2; `bom/bom-notes.md`; PDFs rebuilt. No media shows the budget, so none was regenerated.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was added

`cad/src/product_model.py` exposes `product_parts()` (68 parts: 42 shell, 9 internal, 10 accessory, 7 context), `TITLE` and `RENDER_VIEWS` (hero, exploded and a detail view of the pole kit without the street). It reuses PARAMS, derived() and bands() from `cad/src/model.py`; every part size, the head offset past the curb face, the arm length, the clamp spacing, the knee brace, the M8 through-bolt, the node's place on the road side of the pole, the marker plate and bands, the cable cover and riser guard, and the drain head and stilling tube positions are as model.py. It adds:

- FieldNode core (item 1): filleted enclosure with side ribs and a lid parting line, a lid with a clear window over the board and the LiFePO4 cell, four lid screws, a teal name plate, a lit green status light, two M12 sensor ports and a vent plug on the underside, back plate and pole straps; inside, the MPPT and LoRaWAN board with its radio shield can and flex antenna, and the 6 Ah cell in a holder.
- 6 W panel: aluminium frame, dark cells under glass with grid lines, and a mounting blade, in the model.py pose (25° toward the road).
- Street radar head (item 2): filleted housing with a parting groove, a teal band and a label, a side M12 cable gland, the PTFE lens in a retaining ring, and the radar module on its carrier board.
- Sensor arm (item 3): aluminium tube with end caps, head saddle and screws, two band clamps with bolted ears, the knee brace, and the M8 through-bolt with its nyloc nut and washer.
- Sensor cables (item 6): the street cable from the head gland along the arm and down the pole, the drain cable from the riser guard to the node, M12 plugs and cable ties.
- Depth marker plate (item 8) with amber and red bands, tick marks and rivets; surface cable cover (item 7) as a ridged angle over the gutter strip, a plate up the curb face and a beveled cover across the sidewalk, with the riser guard and masonry anchors.
- Drain head (item 4): cap with a teal band and top gland, potted base, ultrasonic transducer, wet probe pins and NTC bead; stilling tube (item 5) with its 40 slots (10 rows of 4) and two wall brackets.
- Context (not in the BOM): a compact street patch with asphalt, a concrete gutter strip, the cast iron grate over a dark basin throat, the curb and sidewalk, a thin sheet of ponding stormwater (illustrative), and a section of the existing pole.

`README.md` now shows `media/render-hero.png` and links `media/render-exploded.png`; the orchestrator produces both files.

### Differences from model.py (Proposed, awaiting Amish)

1. **Render layout of the pole kit.** Installed, the lens is 4.6 m above the road and the node center 3.0 m, so a true-scale render would show a tall bare pole with small devices. The appearance model draws the arm, clamps and head 3.3 m lower (lens 1.3 m above the road) and the node 2.26 m lower (center 0.74 m), just under the lower clamp; the pole section is cut off 170 mm above the arm. All sizes and horizontal offsets are unchanged, and the marker plate, cable cover and riser guard stay at their true heights. Proposed, awaiting Amish. Recommendation: keep this as a render-only layout with the hero caption saying the kit is drawn lower than installed (the view note does); the installed heights stay as in model.py and FLG-DWG-001. Option: render the true heights, accepting a small device in a tall frame.
2. **Drain kit only in the exploded view.** The drain head and stilling tube sit inside the catch basin, 0.3 to 1.24 m below the road, so they are in the "accessory" group: the exploded view lifts them beside the pole kit, and the hero and detail views leave them out. Proposed, awaiting Amish. Recommendation: accept, and consider a later cutaway render through the basin if the drain side needs a product image of its own.
3. **Cable routes.** model.py draws the cables as straight boxes (street cable vertical through the saddle and arm; drain cable up the pole behind it). The appearance model routes the street cable from a side gland on the head along the arm's side and down the pole beside the clamps to the node's M12 port, and the drain cable from the top of the riser guard to the other port. Cable lengths are not recomputed. Proposed, awaiting Amish. Recommendation: adopt the side gland on the head (it keeps the cable out of the saddle and gives a drip loop) and check the 3 m street cable length against the new route at the next calc revision.
4. **Appearance details not in the BOM text.** The clear window in the node lid, the name plate and status light, the panel mounting blade, the cable ties, the marker ticks and rivets, and the ridged angle profile of the cable cover are appearance choices; the FieldNode enclosure and panel follow the FieldNode repo and are not redefined here. Proposed, awaiting Amish. Recommendation: treat them as render detail only; if a clear-lid node is wanted, raise it in the FieldNode repo.

### Status

This is an appearance model only: no tolerances, no fabrication detail, nothing past TRL 3. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold. model.py, the BOM and the other documents were not edited.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.
