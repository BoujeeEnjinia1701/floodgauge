---
doc_id: FLG-PLN-001
title: FloodGauge project plan
project: FloodGauge
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: Initial draft for the kit 1.9.1 upgrade
---

# FloodGauge project plan

FloodGauge is at stage P3 (constructable design, TRL 3, with detailed CAD for three concept options). The next gate is Amish's choice between option A and option B (FLG-OPT-001, FLG-DDR-004); P4 to P6 stay on hold while the portfolio stage cap is P3. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and users | Design lead | PRB, URS | Done at v0.6 and v0.1; co-design sessions not held |
| STEM check | Design lead | STM, stem_check.py | Done; independent review recorded |
| Concept options | Design lead | OPT, DDR-004, options picture | Done; choice awaits Amish; options picture rendered by the coordinator |
| Requirements | Design lead | PRS, RTM | Done; PR-001 to PR-019 |
| Calculations | Design lead | CAL, sizing.py | Done at v0.7 |
| CAD | Design lead | model.py for A, B and C, STEP, STL, drawings | Done at D3 |
| Build plan | Design lead | BLD, pictures | Done for option A (paper only) |
| Regulation, feasibility, risk, market | Design lead | REG, FEA, RSK, MKT | Done at v0.1; items "to assess" open |
| Pilot partner | Project lead | A host city or county agency | Not started |
| Prototype build and test | Builder | Hardware, TST | On hold (TRL 4, not started) |

## Resources needed

Table 2. Resources. Estimates are for planning only; no purchase is planned at TRL 3.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Pilot partner liaison | Site, permits (REG G9, G10) | 2 to 4 weeks part-time | To assess |
| Radar module data sheet and quote | Close STM S3, R-1 | 1 day | 0 |
| Parts for one prototype | Option chosen by Amish | 1 build, 2 to 3 days | 205.50 for option A (BOM, indicative) |
| Metal brake and workshop time | Hat covers, brackets | 1 day | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 | STEM check, concept options, REG, FEA, PLN | Reached 2026-10-31 |
| P1 | URS, PRS, RSK, MKT | Reached 2026-10-31 |
| P2 | RTM, CAL | Reached 2026-10-31 |
| P3 | BLD, DEC, constructable design, detailed CAD for every option, design FMEA | Reached 2026-10-31 |
| P4 | Prototype built and tested (TST) | On hold (stage cap) |
| P5 | Relevant-environment test | On hold |
| P6 | Released precis v1.0, drawings at a lettered revision | On hold |

## Next steps and decision requested

Decision requested from Amish: pick option A or option B, or ask for the hybrid of FLG-DDR-004 option 3 (radar over the street plus a hung pressure transducer in the basin). The recommended next step after that is to read the radar module data sheet, approach the pilot partner, and then plan the TRL 4 build for the chosen option when the portfolio cap allows.

## References

Sources for every cited fact are in FLG-REG-001 and FLG-MKT-001 and the problem statement FLG-PRB-001.
