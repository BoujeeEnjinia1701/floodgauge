---
doc_id: FLG-REG-001
title: FloodGauge regulatory and standards register
project: FloodGauge
doc_type: Regulatory register
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

# FloodGauge regulatory and standards register

Which standards and regulations touch FloodGauge, where, and what is needed. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Method: STANDARDS section 23. Verdict: the radio and public-space items decide whether a pilot can start; no standard here has been tested against the design, and every claim of conformity waits for the module certificates and a local review.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | 47 CFR 15.255, operation within 57 to 71 GHz | United States | Unlicensed intentional radiators in the 60 GHz band, including radar | The 60 GHz street radar head of option A; the module maker's certification would be relied on, and its use as a fixed outdoor radar must be checked | Design lead | To assess |
| G2 | ETSI EN 305 550 series, radiodetermination equipment 40 to 246 GHz, under the Radio Equipment Directive 2014/53/EU | European Union | Short-range radar in the 40 to 246 GHz range | Same radar head in the EU; scope for a fixed outdoor level radar is not confirmed | Design lead | To assess |
| G3 | ETSI EN 300 220 (short range devices, 25 to 1,000 MHz), EU868 1 % duty cycle | European Union | LoRaWAN uplink timing and power | FieldNode radio; the event-mode interval keeps the sub-band duty cycle at or below 1 % (FLG-CAL-001 E1); owned by FieldNode | FieldNode owner | Met by design (CAL), certificate in the FieldNode repo |
| G4 | The Things Network fair use policy, 30 s uplink airtime per day | Network rule | Airtime on the community network | Normal mode uses 23.7 s/day at SF9 (PR-007) | Design lead | Applies; at risk at SF10 and slower |
| G5 | 47 CFR Part 15.247 (902 to 928 MHz) | United States | Unlicensed spread-spectrum radio | FieldNode LoRaWAN radio at US pilot sites; the module's grant is relied on | FieldNode owner | To assess |
| G6 | IEC 60529 ingress protection codes (IP67, IP68) | International | Dust and water ingress ratings | Drain head and street head; PR-009 asks IP68 at 2 m for 72 h and the transducer face is IP67 only | Design lead | At risk (CAL K1); immersion test at TRL 4 |
| G7 | Regulation (EU) 2016/679 (GDPR) | European Union | Personal data | Levels, status and battery only; no camera or microphone (PR-011); the device holds no personal data | Design lead | Does not apply as designed |
| G8 | Directive 2011/65/EU (RoHS) and Directive 2012/19/EU (WEEE) | European Union | Hazardous substances and end-of-life of electronics | Would apply if units are sold in the EU; not for a self-built pilot | Design lead | Certification needed later |
| G9 | Local road authority permission for a pole attachment, an arm over the gutter and anchors in the curb and sidewalk | Pilot city | Right to attach and to work in the public way | Arm at 4.6 m over the gutter (option A), stand pipe on the curb face (options B and C), eight anchors | Pilot partner | To assess |
| G10 | Local vehicle height limit and clearance rule for arms over the roadway | Pilot city | Minimum clearance above the road | The lens at 4.6 m clears a 4.3 m vehicle plus 0.3 m (CAL A7); the limit is typically 4.0 to 4.3 m and must be confirmed locally | Pilot partner | To assess |
| G11 | Local rules on work at a catch basin or storm drain and on confined spaces | Pilot city | Entry and work in drains | The design never enters the basin: work is from the surface with the grate lifted (PR-012) | Pilot partner | Met by design; permit to assess |
| G12 | UN 38.3 transport tests for lithium cells | International | Shipping the LiFePO4 cell | The cell is part of FieldNode; shipping a built unit is not planned at TRL 3 | FieldNode owner | Certification needed later |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

Checked 2026-10-31 unless stated.

- Legal Information Institute. "47 CFR 15.255, Operation within the band 57 to 71 GHz." <https://www.law.cornell.edu/cfr/text/47/15.255>.
- ETSI. "EN 305 550-1, Short Range Devices (SRD), radio equipment to be used in the 40 GHz to 246 GHz frequency range, part 1." <https://www.etsi.org/deliver/etsi_EN/305500_305599/30555001/01.01.01_60/en_30555001v010101p.pdf>.
- The Things Network. "Fair Use Policy explained." <https://www.thethingsnetwork.org/forum/t/fair-use-policy-explained/1300>.
- The Radio Equipment Directive 2014/53/EU, ETSI EN 300 220, 47 CFR 15.247, IEC 60529, Regulation (EU) 2016/679, Directives 2011/65/EU and 2012/19/EU and UN 38.3 are named from general knowledge and were not opened in this session; each needs its text read before any claim (hence "to assess").
- The shared FieldNode standards (radio certification, battery) are researched once in the FieldNode repo and relied on here.
