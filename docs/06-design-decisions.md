---
doc_id: FLG-DEC-001
title: FloodGauge design decisions register
project: FloodGauge
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from REVIEW.md, FLG-DDR-001 to FLG-DDR-003 and the build plan work
---

# FloodGauge design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, all Proposed, awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction changes (P1 to P11) | Accept; accept with changes; return to the concept | Accept | Every component and step of the build plan | FLG-DDR-003 |
| 2 | Node height 3.4 m (was 3.0 m), so the street cable fits the 3 m I2C limit along its real route | Keep 3.4 m; keep 3.0 m with an I2C bus extender and a 4 m cable | Keep 3.4 m | FieldNode position on the pole (step 7); cable lengths | FLG-DDR-003, P6 |
| 3 | R15 mass margin is 0.01 kg on estimated masses (4.99 kg against 5.0 kg) | Accept and weigh the prototype at TRL 4; lighten further now (for example a 2.5 mm bracket plate) | Accept and weigh at TRL 4 | Bracket plate thickness | FLG-DDR-003, A1 |
| 4 | Lifting the grate with the drain cable threaded through a grate opening | Undo the gutter cover's two anchor nuts and lift the grate with a 0.5 m slack loop in the basin; add an inline M12 joint at the riser guard foot | First option for the pilot; review after the first cleaning visit | Drain cable slack; maintenance | FLG-DDR-003, A2 |
| 5 | R12 installation takes 120 min against 90 min on the surface route | Relax R12 to 120 min for the pilot route; keep 90 min and prefabricate the cover and bracket set | Relax R12 to 120 min for the pilot route | None (installation time only) | REVIEW.md, 2026-09-25, item 3; FLG-DDR-002, O3 |
| 6 | Pilot partner and city for co-design and a first site; depth of the first alert band below 150 mm | Not yet identified | None made | Site pole, curb lane traffic, lens height within 2.5 to 5.0 m | FLG-DDR-001, O1; FLG-DDR-002, N5 |
| 7 | Render layout of the pole kit drawn 3.3 m lower than installed | Keep as a render-only layout with a caption; render true heights | Keep, with the caption | Photoreal renders only | REVIEW.md, 2026-09-26, item 1 |
| 8 | Drain kit shown only in the exploded render | Accept; add a cutaway render through the basin | Accept | Photoreal renders only | REVIEW.md, 2026-09-26, item 2 |
| 9 | Side gland on the radar head and the street cable route | Adopt (now in the model, FLG-DDR-003 P5) | Adopt | Radar head housing (section 3.8 of the build plan) | REVIEW.md, 2026-09-26, item 3 |
| 10 | Appearance details not in the BOM (clear lid window, name plate, status light, cover ridges) | Render detail only; raise a clear-lid node in the FieldNode repo | Render detail only | None | REVIEW.md, 2026-09-26, item 4 |
| 11 | Alert governance: who receives alerts, who acts, how residents opt in and out | To be set with the partner city | None made | Alert service only | FLG-PRC-001, open questions |
| 12 | Theft and vandalism protection with the node at 3.4 m and the marker and guard at street level | Tamper-resistant screw heads; leave as designed for the pilot | None made | Fixings on the marker bands and covers | FLG-PRC-001, open questions |

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

Value-engineering target: USD 160 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 190.50 for the FloodGauge-specific parts (USD 30.50 over the target); USD 329.50 with the USD 139.00 FieldNode core, which is costed in its own repo.

Main cost drivers: the street radar head (USD 55.00), the sensor arm and pole bracket (USD 35.00), the surface covers and riser guard (USD 26.00) and the drain head (USD 24.50).

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
| 2026-10-01 | Design for construction, P1 to P11 | Made under Amish's 2026-09-30 instruction to make the design physically buildable ("fix the design assumptions to match and be physically feasible"); open for his review (open decision 1) | FLG-DDR-003 |
