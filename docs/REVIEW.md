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

### Proposed, awaiting Amish

1. **Budget.** Options: (a) cost FieldNode in its own repo and hold FloodGauge-specific parts to $150 (about $145 now); (b) raise `budget_usd` to $300; (c) cut to a street-only ultrasonic variant (about $188, still over $150, and misses R2). Recommendation: (a), with R16 reworded as "FloodGauge-specific parts $150 or less; FieldNode costed separately". `project.yaml` is unchanged.
2. **Two heads on one node** (street and drain) versus street only or drain only. Recommendation: both.
3. **Street head sensing:** 60 GHz radar versus ultrasonic. Recommendation: radar, with ultrasonic documented as the lower-cost variant.
4. **Drain head:** ultrasonic in a slotted stilling tube with a wet probe, versus radar. Recommendation: ultrasonic in a tube.
5. **Arm over the gutter** versus a head over the sidewalk. Recommendation: over the gutter at 2.95 m or higher, subject to the road authority's clearance rules.
6. **Alert bands** at 150 mm and 300 mm of water above the road, from NWS guidance, plus a drain-full alert. Recommendation: defaults, to be set locally with the partner city.
7. **Network:** private or city LoRaWAN gateway (TwinKit) for event reporting, TTN for pilots only. Recommendation: private gateway.
8. **Pilot partner and city** for co-design and a first site.
9. `project.yaml` pitch and problem: no change proposed; the numbers found support them.

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
