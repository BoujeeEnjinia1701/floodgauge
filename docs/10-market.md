---
doc_id: FLG-MKT-001
title: FloodGauge market and viability
project: FloodGauge
doc_type: Market and viability
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

# FloodGauge market and viability

City and county drainage and emergency teams, and community flood groups, would use a FloodGauge to see street-level water; the closest benchmark is a published sensor design that costs under USD 200 but carries a non-commercial licence, which leaves room for an openly licensed design. Prices and benchmarks are cited with the date they were checked. Method: STANDARDS section 23. No market survey has been done; every figure below is either cited or marked "to assess".

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| City and county flood and drainage agencies | Pilot city with grated curb inlets and an existing gauge or alert programme, such as a county flood control district (FLG-DEC-001) | FloodNet, New York: ultrasonic street sensor, repository states a sensor cost below USD 200 per unit (floodnet-nyc/flood-sensor README, as cited in FLG-PRB-001 on 2026-09-25); commercial gauges: to assess | 205.50 for option A FloodGauge-specific parts, 344.50 with the FieldNode core (BOM; indicative); option B about 191 and option C about 171 FloodGauge-specific (FLG-OPT-001 estimates, not priced from a supplier) | Street and basin level from one node, so a blocked grate is told from a backed-up drain; open data |
| Community groups, schools and universities | Neighbourhood associations and researchers in flood-prone cities | Ultrasonic ranger module DFRobot A02YYUW at USD 15.90 (DFRobot product page, checked 2026-09-25); radar module price: to assess | 205.50 and up, as above | Local evidence for drainage upgrades; teaching kit |
| Low- and middle-income cities | Cities where river gauges are far from flooded streets (UNDRR and WMO 2024: 108 countries report multi-hazard early warning systems) | No benchmark found yet: to assess | 205.50 (hypothetical; the target is USD 160) | Low-cost local warning that supplements official systems |

## Open route

Who would build it: municipal workshops, university labs, makerspaces and flood groups with a metal brake and basic tools. How it spreads: the open files, the build plan (FLG-BLD-001), and a pilot with a county flood agency; the FieldNode core is shared with other Design Molecule repos. What keeps it open: CERN-OHL-S-2.0 for the hardware (strong reciprocity) and MIT for the software, the opposite of FloodNet's non-commercial licence (CC BY-NC-SA 4.0 on its designs, per its repository).

## Viability

The unit cost is above the USD 160 target but of the same order as the one published benchmark. Viability rests on the pilot partner and on the radar module price, neither of which is confirmed. Willingness to pay by a city is to assess; no quote or tender has been seen.

## Sources

- Rentschler, Salhab and Jafino. 2022. "Flood exposure and poverty in 188 countries." <https://www.nature.com/articles/s41467-022-30727-4>. As cited in FLG-PRB-001.
- UNDRR and WMO. 2024. "Global status of multi-hazard early warning systems." <https://www.undrr.org/reports/global-status-MHEWS-2024>. As cited in FLG-PRB-001.
- FloodNet. "Methodology" and "About." <https://www.floodnet.nyc/methodology>, <https://www.floodnet.nyc/about>. As cited in FLG-PRB-001, first checked 2026-09-25; not reopened in this session.
- floodnet-nyc. "flood-sensor." <https://github.com/floodnet-nyc/flood-sensor>. Cost and licence as cited in FLG-PRB-001, first checked 2026-09-25; not reopened in this session.
- DFRobot. "A02YYUW waterproof ultrasonic sensor." <https://www.dfrobot.com/product-1935.html>. USD 15.90, checked 2026-09-25 (bom/bom.csv, item 4).
