---
doc_id: FLG-DEC-001
title: FloodGauge design decisions register
project: FloodGauge
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from REVIEW.md, FLG-DDR-001 to FLG-DDR-003 and the build plan work
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for all twelve open decisions on 2026-10-02 (FLG-DDR-003 accepted); moved to decisions made"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Value engineering restated with the priced tamper-resistant fixings (USD 205.50, USD 45.50 over the target)"
---

# FloodGauge design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Radar module data sheet: accuracy, current, beam width with the lens, price and 60 GHz certification for fixed outdoor use in the pilot country | The depth error, energy and false-reading figures assume them | FLG-CAL-001, Table 1 |
| 2 | The radar housing's lid boss pattern and a base that can take a 46 mm window | Sets the four M4 holes in the head plate and the lens fixing | FLG-DDR-003, P4 |
| 3 | The ranger's transducer face seal (IP67 only) and potting compatibility | R9 is at risk on the face seal | FLG-REQ-001, R9 |
| 4 | Band clamps that close on a 60 mm pole with the V-block and plate inside (about 330 to 380 mm round for the bracket and FieldNode, about 450 mm for the marker), and the torque that gives 1,000 N of preload | The twist and pull figures assume 1,000 N per band | FLG-CAL-001, H2 and H4 |
| 5 | The site pole's wall thickness (2.5 mm assumed) and the owner's permission to drill it | Bearing strength of the through-bolt | FLG-CAL-001, H2b |
| 6 | A grate opening within 70 mm of the grate's curb edge on the chosen cover line, and the curb height (150 mm assumed) | The cable comes up through that opening; the curb cover length follows the curb | FLG-DDR-003, P7 and P8 |
| 7 | The 75 mm socket coupling fits the chosen pipe, and the stand-off pipe clamps reach 90 mm from the wall | Sets the drain head fit and the tube position | FLG-DDR-003, P9 and P10 |
| 8 | Outdoor cable mass and diameter (0.07 kg/m, 10 mm assumed) | Mass margin and the fit inside the 16 mm covers | FLG-CAL-001, I1 |

## Value engineering

Value-engineering target: USD 160 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 205.50 for the FloodGauge-specific parts (USD 45.50 over the target); USD 344.50 with the USD 139.00 FieldNode core, which is costed in its own repo.

Main cost drivers: the street radar head (USD 55.00), the sensor arm and pole bracket (USD 35.00), the surface covers and riser guard (USD 32.00) and the drain head (USD 24.50).

Savings worth trying:

- Quote the radar module and a housing with the lens window already moulded; the USD 55.00 is unverified and is the largest line.
- Cut the bracket plate, cleats, clips and head plate from one sheet and one angle offcut, and buy band clamps and M6 fixings in packs shared with FieldNode builds.
- Make the riser guard and covers from one 2 mm galvanized strip length, or use a bought steel cable protector for the sidewalk run.
- Use the conduit route (about USD 8 plus civil work, not in this total) at sites where road works are planned anyway.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: FieldNode costed in its own repo; street and drain heads on one node; radar street head with ultrasonic as the lower-cost variant; ultrasonic drain head in a slotted stilling tube with a wet probe; arm over the gutter; 150 and 300 mm alert bands plus drain-full; private or city gateway for events; levels only; pitch and problem unchanged | Amish: "i accept all your recommendations, go with them across all repos." | FLG-DDR-001, FLG-DDR-002 |
| 2026-09-25 | TRL 3 items N1 to N5: R3 restated; lens set per site within 2.5 to 5.0 m (4.6 m reference); surface cable route for pilots with conduit at permanent sites; M8 anti-rotation through-bolt; a first alert band below 150 mm supported | Amish, same instruction | FLG-DDR-002 |
| 2026-09-26 | `budget_usd` set to USD 160 | Amish: "i approve all the budget items." | FLG-DDR-002 |
| 2026-10-01 | Budgets are value-engineering targets, not limits; cost is reported over or under the target | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | STANDARDS section 18 |
| 2026-10-01 | Design for construction, P1 to P11 | Made under Amish's 2026-09-30 instruction to make the design physically buildable ("fix the design assumptions to match and be physically feasible"); accepted on 2026-10-02 (below) | FLG-DDR-003 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P11 of FLG-DDR-003 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | FLG-DDR-003 |
| 2026-10-02 | Node kept at 3.4 m, so the street cable fits the 3 m I2C limit along its real route | Amish: "i approve your recommendations for all 555 open decisions." | FLG-DDR-003, P6 |
| 2026-10-02 | R15 mass margin of 0.01 kg accepted; the prototype is weighed at TRL 4, and a 2.5 mm bracket plate is the named fix if the weighed mass is over 5.0 kg | Amish: "i approve your recommendations for all 555 open decisions." | FLG-DDR-003, A1 |
| 2026-10-02 | Grate lifting for the pilot: undo the gutter cover's two anchor nuts and lift the grate with the cable threaded and a 0.5 m slack loop in the basin, the loop tied to the stilling tube clamp so it cannot catch debris; reviewed after the first cleaning visit | Amish: "i approve your recommendations for all 555 open decisions." | FLG-DDR-003, A2 |
| 2026-10-02 | R12 relaxed to 120 min for the pilot surface route; 90 min stays the target for permanent sites built on the conduit route with road works | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-25, item 3; FLG-DDR-002, O3 |
| 2026-10-02 | Pilot partner: a city or county flood agency with a known street-flooding problem at grated curb inlets and an existing gauge or alert programme. First candidate type to approach: a county flood control district such as the Harris County Flood Control District in Houston. First alert band at 100 mm unless the partner's own practice says otherwise | Amish: "i approve your recommendations for all 555 open decisions." | FLG-DDR-001, O1; FLG-DDR-002, N5 |
| 2026-10-02 | Render-only layout of the pole kit kept, with the caption; the caption's heights are updated to the 3.4 m node when the renders are redone | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 1 |
| 2026-10-02 | Drain kit shown in the exploded render only; a basin cutaway render only if the drain head is shown as a product on its own | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 2 |
| 2026-10-02 | Side gland on the radar head and the street cable route closed as adopted with item 1 (FLG-DDR-003, P5) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 3; FLG-DDR-003, P5 |
| 2026-10-02 | Clear lid window, name plate, status light and cover ridges are render detail only; no clear-lid node is raised with FieldNode | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 4 |
| 2026-10-02 | Alert governance: the partner city's emergency management office owns the alerts. FloodGauge publishes levels and band crossings only, the city decides who acts, and residents opt in and out through the city's existing alert channel, so the project holds no resident contact data | Amish: "i approve your recommendations for all 555 open decisions." | FLG-PRC-001, open questions |
| 2026-10-02 | Tamper-resistant screw heads and nuts on everything within reach of the sidewalk (marker bands, covers, riser guard and anchors) for the pilot; the node stays at 3.4 m as designed | Amish: "i approve your recommendations for all 555 open decisions." | FLG-PRC-001, open questions |
