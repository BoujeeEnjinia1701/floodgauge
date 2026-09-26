---
doc_id: FLG-DDR-001
title: FloodGauge TRL 2 review decisions
project: FloodGauge
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 work, open for Amish's review, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations in items D1 to D9 are adopted for TRL 3 work pending Amish's review; item O1 remains "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis FLG-PRC-001 v0.2 listed seven key design choices, all marked proposed. On 2026-09-25 Amish asked for this batch of Design Molecule repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 work, open for his review. The item without a recommendation stays open. Nothing here is recorded as decided or approved by Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in FLG-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3 work.*

| # | Item | Adopted recommendation | Status |
| --- | --- | --- | --- |
| D1 | Budget (review item 1) | Option (a): cost the FieldNode core in the FieldNode repo and hold FloodGauge-specific parts to $150. R16 is restated as "FloodGauge-specific parts $150 or less; FieldNode costed separately". `budget_usd` stays $150; no new budget figure was recommended | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D2 | Heads (review item 2, precis choice 1) | Two heads on one node: street and drain; street head only is the fallback where no cable route to the basin exists | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D3 | Street head sensing (review item 3, precis choice 2) | 60 GHz pulsed coherent radar; an ultrasonic street head is documented as the lower-cost variant | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D4 | Drain head (review item 4, precis choice 3) | Waterproof ultrasonic ranger in a slotted 75 mm stilling tube, with a two-electrode wet probe as a second signal | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D5 | Head position (review item 5, precis choice 4) | Arm over the gutter with the head at 2.95 m or higher, subject to the road authority's clearance rules | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D6 | Alert bands (review item 6, precis choice 5) | 150 mm and 300 mm of water above the road, from NWS guidance, plus a drain-full alert from the wet probe; defaults to be set locally with the partner city | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D7 | Network (review item 7, precis choice 6) | Private or city LoRaWAN gateway (TwinKit or the city network) for event reporting; The Things Network for pilots only | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D8 | Privacy (precis choice 7) | Levels only; no camera, no microphone, no imaging | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D9 | Pitch and problem (review item 9) | No change was recommended; the pitch and problem lines in `project.yaml` and `README.md` are unchanged | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Pilot partner and city for co-design and a first site (review item 8). No preference stated and no recommendation made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: only the TRL fields and the evidence list change. `budget_usd` stays $150, and the pitch and problem are unchanged (D9).
- FLG-PRB-001, FLG-PRC-001 and FLG-REQ-001 are revised to v0.3. The design choices in the precis are no longer described as "proposed"; they are adopted for TRL 3 work pending Amish's review.
- Requirement R16 is restated to match D1: it now covers FloodGauge-specific parts only, with the FieldNode core costed in its own repo ($126.00, FND-CAL-001). No other target changes in this record.
- `bom/bom.csv` keeps the FieldNode core as line 1 for the complete-gauge total, marked as costed in the FieldNode repo and excluded from the R16 total.
- The TRL 3 calculations (FLG-CAL-001) found problems that need Amish's decision: R3 is not met above 330 mm below the road, R12 is not met because of the conduit, the 2.95 m head height is inside a tall vehicle envelope, and the arm's twist margin on two band clamps is 1.45. The proposals for these are in `docs/REVIEW.md` and are not decided by this record.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
