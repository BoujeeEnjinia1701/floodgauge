---
doc_id: FLG-DDR-002
title: FloodGauge recommendations accepted
project: FloodGauge
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($160)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "O1 and O3 decided by Amish on 2026-10-02 (FLG-DEC-001, items 5 and 6)"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below with a recommendation is "Decided by Amish, 2026-09-25: go with recommendation". Items without a recommendation stayed "Proposed, awaiting Amish" at this record; O1 and O3 were decided by Amish on 2026-10-02 (FLG-DEC-001, items 6 and 5): "i approve your recommendations for all 555 open decisions."

## Context

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." At that point this repo had nine items adopted for TRL 3 work pending his review (FLG-DDR-001, D1 to D9), one open item with no recommendation (O1), and five further items raised by the TRL 3 calculations in `docs/REVIEW.md` (session 2026-09-25, TRL 3, "Still awaiting Amish", items 2 to 6). Where a recommendation offered several options, the recommended option is the decision. TRL 4 remains on hold by Amish's instruction, and nothing here goes past TRL 3.

## Options considered

The options for each item are those in `docs/REVIEW.md` (both 2026-09-25 sessions), FLG-DDR-001 and FLG-CAL-001 v0.1.

## Decision

*Table 1. Items from FLG-DDR-001, now decided.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Budget | FieldNode costed in its own repo; FloodGauge-specific parts $150 or less | `budget_usd` stays $150 (the recommended figure); R16 wording as in FLG-REQ-001 v0.3 |
| D2 | Heads | Street and drain heads on one node | None beyond the status wording |
| D3 | Street sensing | 60 GHz radar; ultrasonic as the lower-cost variant | None beyond the status wording |
| D4 | Drain head | Ultrasonic in a slotted stilling tube with a wet probe | None beyond the status wording |
| D5 | Head position | Arm over the gutter, height to the clearance rule | Height now set under N2 below |
| D6 | Alert bands | 150 mm and 300 mm plus drain-full, set with the partner city | First band below 150 mm added under N5 |
| D7 | Network | Private or city gateway for events; TTN for pilots only | None beyond the status wording |
| D8 | Privacy | Levels only | None beyond the status wording |
| D9 | Pitch and problem | No change | `project.yaml` and `README.md` keep the existing wording |

All nine: Decided by Amish, 2026-09-25: go with recommendation.

*Table 2. Items raised at TRL 3, now decided.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| N1 | R3 wording | Restate R3 as "continuous reading from 50 mm above the basin floor to 330 mm below the road, plus a drain-full signal above that" | FLG-REQ-001 v0.4; R3 not met to met on paper |
| N2 | Head height and R1 | Option (a): widen the R1 band to 2.5 to 5.0 m and set the height per site to the road authority's clearance rule, about 4.6 m where trucks use the curb lane | R1 target in FLG-REQ-001 v0.4; lens 2.95 m to 4.6 m and pole 3.3 m to 4.9 m in `cad/src/model.py`; FieldNode center 2.35 m to 3.0 m and street cable 2 m to 3 m to keep the I2C bus under 400 pF (350 pF); FLG-DWG-001 Rev P1 to P2 |
| N3 | R12 cable route | Option (b) for pilots: out at the grate frame and along the curb face under a bolted steel cover; option (a), the conduit, at permanent sites laid with road works | BOM line 7 conduit ($8.00) to surface cable cover ($14.00); model item 7 redrawn; installation with no civil work, 120 min; R12 still not met on time |
| N4 | Arm anti-rotation | Add a through-bolt or pinned clamp; the through-bolt is used | M8 A4 through-bolt at the lower clamp in the model and BOM line 3 ($18.00 to $20.00); twist factor 1.45 to 37 |
| N5 | First alert band below 150 mm | The alert service supports a first band below 150 mm; its depth is set with the partner city under D6 | FLG-PRC-001 v0.4 and FLG-REQ-001 v0.4 text; no depth chosen, because none was recommended |

All five: Decided by Amish, 2026-09-25: go with recommendation.

*Table 3. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Pilot partner and city for co-design and a first site. No preference stated and no recommendation made. The depth of the N5 band waits on this. | Decided by Amish, 2026-10-02 (FLG-DEC-001, item 6): a city or county flood agency with street flooding at grated curb inlets and an existing gauge or alert programme; first candidate type to approach, a county flood control district such as the Harris County Flood Control District; first alert band 100 mm unless the partner's practice says otherwise. Nothing is agreed. |
| O2 | R16 over budget after N3 and N4: $153.50 against $150 (new, raised by FLG-CAL-001 v0.2) | Decided by Amish, 2026-09-26: `budget_usd` $160 (see below) |
| O3 | R12 installation 120 min against 90 min on the surface route (new) | Decided by Amish, 2026-10-02 (FLG-DEC-001, item 5): R12 relaxed to 120 min for the pilot surface route; 90 min stays the target for permanent sites on the conduit route. |

## Consequences

- FLG-REQ-001 v0.4, FLG-PRC-001 v0.4, FLG-CAL-001 v0.2 and FLG-DDR-001 v0.2 carry the new wording and numbers. FLG-DWG-001 is at Rev P2. The STEP, STL and media files are regenerated from the model.
- Requirement status: 2 not met (R12, R16), 3 at risk (R7, R9, R14), 1 not verifiable at TRL 3 (R10), 8 met on paper, 3 met by design. R3 moves from not met to met on paper; R16 moves from met on paper to not met.
- Cost: FloodGauge-specific parts $145.50 to $153.50; complete gauge $271.50 to $279.50. `budget_usd` stays $150.
- Mass on the pole 4.62 kg to 4.74 kg; still under 5.0 kg.
- A site now needs a pole about 4.9 m tall above the sidewalk where tall vehicles use the curb lane, and a mobile elevating platform to fit the arm.
- Cross-repo actions are listed in `docs/REVIEW.md`; no other repo was edited.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building, testing or purchasing.

## Budget approved, 2026-09-26

On 2026-09-26 Amish wrote, in chat: "i approve all the budget items."

- Budget set to $160 to cover the priced BOM: decided by Amish, 2026-09-26. This settles O2. FloodGauge-specific parts are $153.50 (lines 2 to 10; the $126.00 FieldNode core stays costed in its own repo under D1), so R16 moves from not met to met on paper with a $6.50 margin.
- Requirement status: 1 not met (R12), 3 at risk, 1 not verifiable at TRL 3, 9 met on paper, 3 met by design.
- Files changed: `project.yaml` (`budget_usd` 150 to 160); FLG-REQ-001 v0.5; FLG-CAL-001 v0.3, `docs/04-calcs/sizing.py` (target read from `budget_usd`) and `results.csv`; FLG-PRB-001 v0.5 and FLG-PRC-001 v0.5 (budget figure); `README.md`; `bom/bom-notes.md`; `docs/REVIEW.md`.
