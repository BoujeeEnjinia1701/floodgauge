---
doc_id: FLG-DDR-003
title: FloodGauge design for construction
project: FloodGauge
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish on 2026-10-02 (Tables 1 to 3); record stays Draft"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 and Table 2 were made under Amish's 2026-09-30 instruction to make the design physically buildable. Nothing here changes what FloodGauge does, its pitch or its safety case. Accepted by Amish on 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 and A2), recorded in the design decisions register (FLG-DEC-001, items 1 to 4). The record stays Draft.

## Context

On 2026-09-30 Amish asked for every repo's build plan to show how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of FLG-DDR-002 showed what FloodGauge does, but checking it with build123d (overlap volumes and gaps between parts) found parts that pass through each other, parts with no fixing and a cable route that cannot be laid. The changes below keep what the gauge does: the same two heads, the same lens height of 4.6 m and 250 mm past the curb face, the same stilling tube, drain head height and reading range, the same surface cable route for pilots and the same anti-rotation through-bolt, alert bands and data path.

Every change is in `cad/src/model.py`, which now runs 110 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must not touch are apart by at least the stated clearance. All 110 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept (measured on the model) | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The 40 mm square arm ran straight through the 60 mm pole (15,515 mm³ of overlap) and 40 mm past its far side; the upper clamp ring overlapped the arm (5,174 mm³); the two clamps were plain rings 0.5 mm off the pole with no way to tighten them. | A pole bracket: an aluminium plate 3 x 100 x 450 mm on two V-blocks (the FieldNode V-block, 60 x 33 x 20 mm with a 90° V), held by two 12 mm stainless band clamps 400 mm apart that pass round the pole, through slots in the plate and across its front. The arm stops 2 mm short of the plate and is held between two 30 x 30 x 3 mm angle cleats: two M6 bolts through each cleat and the plate, two M6 bolts with crush sleeves through cleat, arm and cleat. The arm is now 715 mm long (was 805 mm). | The FieldNode V-block and band pattern is already in the lab's build plans, seats poles of 40 to 71 mm and needs no welding. The band spacing of the concept (400 mm) is kept. |
| P2 | The knee brace touched the arm with 663 mm³ of overlap at its top and stopped 6.7 mm short of the lower clamp: it had no fixing at either end. | A 25 x 25 x 1.6 mm tube, 382 mm long, pinned at each end by one M6 bolt and sleeve between the ears of a folded clip: one clip under the arm (two M6 bolts up through the arm), one on the bracket plate (two M6 bolts through the plate). The pins are 358 mm apart at 45°. | Two identical clips folded from 3 mm strip. A pinned brace carries only push and pull, which is what the calculation assumes. |
| P3 | The M8 anti-rotation through-bolt ran along the street through the lower band clamp and the pole. A worm-drive band has no material that can take a bolt. | The M8 bolt runs across the street, through the bracket plate, a 20.2 mm aluminium spacer and both walls of the pole, half way between the bands, with a nyloc nut behind the pole. It is now M8 x 100 mm (was M8 x 110 mm). | The bolt still pins the bracket to the pole; the couple across the pole and the twist factor of 37 are unchanged [H2b]. The spacer stops the plate bending when the bolt is tightened. |
| P4 | The head saddle (a 70 x 50 x 40 mm block under the arm) sat inside the top 40 mm of the radar housing (125,252 mm³ of overlap). | A 140 x 70 x 3 mm head plate bolted under the arm (two M6 bolts up through the arm); the housing hangs from it on four M4 countersunk screws into its lid bosses. The arm centre rises 3 mm, to 4,713 mm, so that the lens stays at 4,600 mm. | The lens height is the depth datum and must not move. |
| P5 | The street cable left the top of the head straight up through the arm wall (800 mm³ of overlap). | An M12 gland on the side of the housing facing the pole. The cable runs along the side of the arm, drops beside the bracket plate, runs down the pole outside the band clamps and goes to port A under the FieldNode box, tied every 300 mm. | The side gland was already proposed in the appearance model (REVIEW, 2026-09-26, item 3). |
| P6 | FieldNode was drawn as a box on a 12 mm plate in line contact with the pole with no fixing, and its panel floated 35 mm above it with no bracket. | FieldNode is its constructable design (FND-BLD-001): a 3 mm back plate on two V-blocks and two band clamps, the box on lugs, and the 6 W panel on its own bracket at 40° (the concept drew 25°). It faces the road. The node centre rises from 3.0 m to 3.4 m above the road. | Measured along the real route (along the arm, down the pole outside the bands and up to port A on the underside of the box), the street cable at 3.0 m needed 3.04 m, 3.34 m with drip loops, more than the 3 m cable that keeps the I2C bus under 400 pF. At 3.4 m the run is 2.64 m, 2.94 m with loops [J1]. The 5 m drain cable still fits (4.83 m with loops) [J2]. |
| P7 | The drain cable was drawn leaving the basin "at the grate frame". The grate sits 5 mm from its frame, too narrow for a 10 mm cable, and the drawn cable passed through 4,712 mm³ of the road slab. | The cable comes up through the grate opening nearest the curb, 165 mm from the curb face and 80 mm along the street from the inlet centre, inside the gutter cover. | No drilling of the road, the grate or its frame, as the surface route intends. |
| P8 | The surface cover was an angle drawn as flat boxes with no fixing; the riser guard stood on the sidewalk 250 mm along the street from the pole (160 mm from it), and the drain cable went up the far side of the pole 233 mm from the guard, unconnected. | Three hat-section covers bent from 2 mm galvanized strip, 84 mm wide and 16 mm high: a gutter cover lying across the gutter strip and onto the grate border, with two tabs up the curb face; a curb cover on the curb face with four M8 masonry anchors; a sidewalk cover with four anchors and two tabs down the curb face that share the curb cover's upper anchors. The riser guard is a 40 x 65 x 2 mm steel U channel, 300 mm tall, standing on the sidewalk with its open side on the pole, and the cable runs inside it and on up the pole to port B. | One section shape for all three covers. Anchors stay in the curb and sidewalk only (FLG-DDR-002). The guard is held by the marker's two band clamps, so it needs no anchor. |
| P9 | The two stilling tube brackets were set 10 mm into the basin wall (24,000 mm³ of overlap). | Two bought stainless stand-off pipe clamps for 75 mm pipe, each with an M8 rod to a wall plate and one wall anchor, 80 and 710 mm below the tube top. | Bought, adjustable, fitted from the surface with the grate off, as FLG-CAL-001 L1 already allowed for. |
| P10 | The drain head sat on the tube top with no fixing. | A 75 mm PVC socket coupling, 40 mm long, solvent-welded under the head; the tube top slides into it up to the head, and two stainless screws hold it. | The head lifts off for cleaning after two screws. The transducer face stays 300 mm below the road. |
| P11 | The depth marker plate stood flat on the round pole with no fixing; the new sidewalk cover would have run under its bottom edge. | A 2 mm plate (was 3 mm), 90 x 435 mm, with its bottom edge 165 mm above the road (15 mm above the sidewalk), held by two band clamps round the pole, the plate and the riser guard. The amber band shows from the bottom edge to 300 mm. | The sidewalk cover passes under the plate; the plate and the guard share two clamps. The thinner plate helps hold the mass requirement. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Arm wall 2.0 to 1.6 mm, brace wall 2.0 to 1.6 mm, two 60 x 90 mm windows in the bracket plate. Mass on the pole 4.99 kg (was 4.74 kg), 0.01 kg under R15's 5.0 kg [I2]. The riser guard and the covers (2.00 kg) stand on the sidewalk and are not carried by the pole. | The bracket, clips, cleats, bolts and the FieldNode's constructable design (2.45 kg, was 2.41 kg) added mass. In the 50 kg misuse case the 1.6 mm arm is stressed to 60 MPa (factor 3.6) and the brace carries 1,504 N against a buckling load of 73,043 N [H3]. |
| Loads | Arm pull at the cleats in the misuse case 1,063 N against 2,000 N band capacity (factor 1.9) [H4]; M6 joints and pins at least 11 times the load [H5]. | New load path through the bracket. |
| Cost | BOM lines 3, 4, 5, 7 and 8 repriced; line 1 follows FieldNode's constructable design ($139.00). FloodGauge-specific parts $190.50 (was $153.50) against the value-engineering target of $160: $30.50 over the target. Complete gauge $329.50 [M1]. | Parts added for construction. |
| Drawing | FLG-DWG-001 Rev P4; making sketches FLG-DWG-101 to 116 added. | Follows the model. |
| Documents | FLG-CAL-001 v0.4, FLG-REQ-001 v0.6, FLG-PRC-001 v0.6. R16 is now reported against the value-engineering target. No other requirement changes status. | Follows the model. |
| Unchanged | Lens height and offset, depth error budget, drain reading range and error, tube hydraulics, energy, airtime, latency, false-reading rules, twist factor, installation time (120 min, R12 still not met). | |

*Table 3. Proposed, then accepted by Amish as recommended on 2026-10-02 (FLG-DEC-001, items 3 and 4).*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The R15 mass margin is now 0.01 kg on estimated masses. | (a) accept and weigh the prototype at TRL 4; (b) lighten further now, for example a 2.5 mm bracket plate. | (a). Accepted 2026-10-02, with the 2.5 mm bracket plate named as the fix if the weighed prototype is over 5.0 kg. |
| A2 | Lifting the grate for maintenance: the drain cable passes through a grate opening and the gutter cover rests on the grate border. | (a) undo the gutter cover's two anchor nuts and lift the grate with the cable still threaded, using a 0.5 m slack loop left in the basin; (b) add an inline M12 joint at the foot of the riser guard so the cable can be unplugged. | (a) for the pilot; decide after the first cleaning visit. Accepted 2026-10-02, with the slack loop tied to the stilling tube clamp so it cannot catch debris. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan FLG-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: 1 not met (R12), 3 at risk (R7, R9, R14), 1 not verifiable at TRL 3 (R10), 8 met on paper, 3 met by design; R16 is over the value-engineering target by $30.50 (FLG-CAL-001 v0.4). With R12 relaxed to 120 min for the pilot surface route on 2026-10-02 (FLG-DEC-001, item 5), R12 is met on paper and none is not met (FLG-CAL-001 v0.5).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept arm, saddle, cover and node height; they need updating on Amish's Mac.
- The FieldNode repo is not edited. FloodGauge uses its constructable design on a 60 mm pole, which needs band clamps of about 330 to 380 mm round instead of FieldNode's 230 to 280 mm.
