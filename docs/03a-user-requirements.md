---
doc_id: FLG-URS-001
title: FloodGauge user requirements
project: FloodGauge
doc_type: User requirements
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: Initial draft, written for the kit 1.9.1 upgrade from the users and stakeholders in FLG-PRB-001 Table 1 and the constraints in FLG-PRB-001
---

# FloodGauge user requirements

What the people who would use, install, pay for or live near a FloodGauge need, written from their side. The product requirements that meet these needs are in FLG-PRS-001 (`03-requirements.md`) and the links are in the traceability matrix (`03b-traceability.md`). Method: STANDARDS section 22. The needs are drawn from the users listed in FLG-PRB-001 (drainage crews, emergency managers, residents, community groups, planners and researchers) plus the road authority and network operator who give permission for the site; no interviews have been held yet, so the priorities are proposals to confirm with a pilot partner (FLG-PRB-001, user research and co-design).

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Depth of water on the street | I can read how deep the water is on my street, from dry to 600 mm, so I know whether to close the road or stay out | High | Emergency managers; residents (PRB Users and context) |
| UR-002 | Performance | Tell a blocked inlet from a backed-up drain | I can tell whether the water on the street comes from a blocked grate or from a drain that is full below, so the crew goes to the right place | High | Drainage and public works crews (PRB Users and context) |
| UR-003 | Performance | Readings accurate enough to trust | A reading is close enough to the true depth that an alert at 150 mm or 300 mm is not early or late by a visible amount | High | Emergency managers (PRB Users and context) |
| UR-004 | Performance | A warning while there is still time | An alert reaches me within a couple of minutes of the water crossing a set depth | High | Emergency managers; residents (PRB The problem in numbers) |
| UR-005 | Performance | Faster readings when it matters | The gauge reads more often when water is rising and saves effort when the street is dry | Medium | Emergency managers (PRB Users and context) |
| UR-006 | Environment and durability | Works through the storm | The gauge keeps working in a storm with no mains power at the pole and no sun for days | High | Drainage crews; emergency managers (PRB Operating context) |
| UR-007 | Environment and durability | Survives weather and submersion | The part in the drain survives being under stormwater with silt, and the part on the pole survives sun, frost, rain and road spray | High | Drainage crews (PRB Operating context) |
| UR-008 | Deployment and assembly | Installed by a small crew from the surface | Two people can fit it in a short visit without drilling the road or entering the catch basin | High | Drainage crews; road authority (PRB Constraints) |
| UR-009 | Deployment and assembly | Fits an existing pole and clears traffic | It fits the pole already there, adds little load, and nothing hangs where a tall vehicle can hit it | High | Road authority; pole owner (PRB Operating context) |
| UR-010 | Safety | Safe for the public and the crew | Nobody can be cut, tripped or hit by the gauge, its cover or its cable, and the crew lifts nothing heavy | High | Residents; drainage crews (PRB Constraints) |
| UR-011 | Performance | No false alarms | A passing truck, a person under the arm or a leaf on the grate does not raise an alert | Medium | Emergency managers; residents (PRB Users and context) |
| UR-012 | Regulatory | Privacy | The gauge records levels only and nothing that identifies a person | High | Residents; city privacy officer (PRB Constraints) |
| UR-013 | Regulatory | Radio that follows the network rules | The gauge does not break the airtime limits of the radio band or of the community network it uses | Medium | Network operator (PRB Operating context) |
| UR-014 | Maintenance | Readings traceable to the road level | Each reading refers to the road surface at the gauge, and I can check it again each year | Medium | Planners and researchers (PRB Users and context) |
| UR-015 | Regulatory | Open data | Levels are published in an open, documented format that I can use without a licence fee | Medium | Community groups; planners and researchers (PRB Users and context) |
| UR-016 | Cost | A cost a city or community can afford | The parts cost is low enough to deploy many gauges, within the project's value-engineering target | Medium | Funders; pilot city (PRB Constraints) |
| UR-017 | Maintenance | Resists theft and tampering | Casual vandalism or theft takes more than a pocket tool | Medium | Pole owner; drainage crews (PRB Operating context) |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
