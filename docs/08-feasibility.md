---
doc_id: FLG-FEA-001
title: FloodGauge feasibility assessment
project: FloodGauge
doc_type: Feasibility assessment
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

# FloodGauge feasibility assessment

Overall verdict: a FloodGauge is feasible as a garage-built pilot at TRL 3 for the physics, parts and assembly, with the radar module data sheet, the drain head seal and road-authority permission as the three things that could stop it. Method: STANDARDS section 23. Ratings describe the recommended pair of options (A or B, FLG-OPT-001); option C is feasible but misses the accuracy target.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Every claim checked is within known science or plausible (15 within, 17 plausible, none fails); the detail model of all three options passes the D3 fidelity check; the only requirements not met on paper are over target on cost and at risk on airtime, immersion and heat | High | Radar accuracy and echo logic rest on an unverified data sheet (STM S3); the 4.994 kg mass margin is 0.1 % and the through-bolt twist factor is 1.8, not 37 (STM S11) | STM, CAL-001, cad/fidelity.json |
| Materials | Aluminium 6063 arm, galvanised steel covers, stainless fasteners, PVC tube; all stock sections | High | Galvanic contact of stainless with aluminium and zinc in road salt (STM S19) | BOM, STM |
| Manufacturing and assembly | A two-person crew can make and fit the kit with hand tools; the build plan sequences 10 steps in 120 min on site | Medium | Bent hat covers, V-blocks and cleats need a bench and a brake; the arm is lifted from a platform | BLD-001, CAL-001 L1 |
| Power and controls | 9.3 mW worst-case sensor load against a 100 mW allowance; 47 days at -20 C without sun | High | FieldNode interior heat above the cell's 45 C charge limit (PR-014 at risk) | CAL-001 D, FieldNode FND-CAL-001 |
| Supply of parts | Radar module, ultrasonic ranger, stainless fasteners and sections from catalogue suppliers | Medium | Radar module and housing prices are unverified (BOM item 2, USD 55.00 indicative); pressure transducer prices for option B are estimates | BOM, OPT |
| Regulation and permission | A fixed outdoor 60 GHz radar and an arm over a road need a certificate and a permit | Medium | G1, G2, G9 and G10 are all "to assess" | REG |
| Cost | USD 205.50 for FloodGauge-specific parts, USD 45.50 over the USD 160 target; option B estimated about USD 191 and option C about USD 171 | Medium | The target is a value-engineering control, not a limit | BOM, PR-016, OPT |

Ratings: High, Medium, Low.
