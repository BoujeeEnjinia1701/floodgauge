---
doc_id: FLG-DDR-004
title: FloodGauge concept options and the STEM-check fix
project: FloodGauge
doc_type: Design decision record
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: Initial record for the kit 1.9.1 upgrade; concept selection proposed to Amish; float-shell fix made under the standing instruction of 2026-10-23
---

# 0004: Concept options and the STEM-check fix

- **Date:** 2026-10-31
- **Status:** Draft. Part 1 (the concept choice) is **Proposed, awaiting Amish**. Part 2 (F1, the float shell in option C) was decided under Amish's standing instruction of 2026-10-23, because it fixes a failed STEM-check detail and keeps option C's working principle.

## Context

The kit 1.9.1 upgrade asks every repo to compare at least two concept options with different working principles, to check the physics of each claim (FLG-STM-001), and to model every option to the same detail (D3 at stage P3). The current design (radar over the gutter plus an ultrasonic ranger in a stilling tube, FLG-DDR-001 to FLG-DDR-003) is option A and is not changed by this record. Options B and C were added to give the choice some range: B reads the water by its pressure and C reads it with a float and reed switches. FLG-OPT-001 scores the three options against the 17 user requirements in FLG-URS-001.

## Part 1. Concept choice (Proposed, awaiting Amish)

| Option | Working principle | Weighted score (max 220) | Share of maximum |
| --- | --- | --- | --- |
| A | 60 GHz radar over the gutter and an ultrasonic ranger in a stilling tube; no contact with the water | 163 | 74.1 % |
| B | Vented submersible pressure transducers, one in a stand pipe on the curb face and one in the basin tube (p = rho g h) | 174 | 79.1 % |
| C | Float with a ring magnet closing reed switches on a 25 mm chain, in the same pipe and tube | 160 | 72.7 % |

B leads A by 6.7 %, which is inside the 10 % band in STANDARDS section 21, so **no pick is made and both A and B go to Amish**. Option C scores last and does not meet the 10 mm street accuracy target (PR-002) at a 25 mm switch pitch, so it is dropped unless a 15 mm pitch is accepted. Nothing in this record changes option A, which stays the design the repo describes until Amish decides.

Options considered for Amish:

1. **Keep A.** No contact with the water, nothing in the road except an arm 4.6 m up, tamper-resistant by height. Costs $205.50 (over the target by $45.50), needs an arm lifted onto the pole, and its accuracy rests on a radar module whose data sheet is not yet checked.
2. **Switch to B.** Fewer parts and no arm, accuracy set by a transducer class, no air-temperature error. Puts a 50 mm stand pipe in the gutter edge within reach of the public, relies on a vented cable staying dry, and its cost is an estimate until a transducer is quoted (about $191 on the estimate in FLG-OPT-001).
3. **Keep A and graft B's idea.** Use a hung pressure transducer in the basin tube (B's best feature) in place of the ultrasonic ranger and its temperature correction, keeping the radar over the street. This changes the scope of option A, so it is also Amish's decision.

Recommendation: because the margin is inside 10 %, both A and B go to Amish with option 3 as the idea worth testing at TRL 4. Nothing here is decided until Amish says so.

## Part 2. Fix F1: hollow floats in option C (decided under the standing instruction)

**Problem.** The first model of option C had solid polypropylene ring floats with a ring magnet. The STEM check (FLG-STM-001, C1 and C2) showed they sink: the street float weighs 44.4 g against 33.7 g of buoyancy at full submersion, and the basin float 106.5 g against 97.4 g.

**Options weighed.** A bigger solid float (needs a bore wider than the pipe allows), a foam-filled float (absorbs water, hard to mould), a smaller magnet only (saves 6 g, not enough), a sealed hollow shell with 1.6 mm walls (rotationally moulded or welded halves).

**Fix.** A sealed hollow polypropylene shell with two annular voids above and below the magnet pocket, the voids filled with closed-cell foam (added after the independent review, which pointed out that a leaking empty shell would fill and sink with its magnet, and that sealed air would cycle in pressure with temperature), and a 5 mm ring magnet instead of an 8 mm one. The street float grows from 38 to 42 mm OD (the pipe bore is 45.2 mm, so 1.6 mm of radial clearance stays). The street float then weighs 29.2 g and rides at 61 % of its buoyancy; the basin float weighs 47.0 g and rides at 48 %. The model (`cad/src/options_bc.py`) and `cad/fidelity.json` carry the fix, and the rerun STEM check closes C1 and C2.

**Why decided here.** It fixes a detail, keeps the working principle (a magnet on a float closing a reed switch), and changes no scope or pitch, so it falls under the standing instruction of 2026-10-23.

## Part 2b. Fix F2: through-bolt class (decided under the standing instruction)

**Problem.** The independent review of the STEM check (FLG-STM-001) showed the first twist analysis of the M8 anti-rotation through-bolt used the wrong load path. The plate presses on the bolt sideways, 52 mm from the pole axis, through a 20.2 mm spacer, so the bolt bends as a short cantilever out of the pole wall; it does not act as a couple across the full 60 mm pole. Capacity is 33 N m with the A4-70 class and 45 N m with A4-80, not 922 N m, so the "twist factor 37" in FLG-CAL-001 H2b and FLG-PRS-001 PR-015 was wrong. Against the 24.8 N m wind twist the real factor is 1.8 with A4-80 (1.3 with A4-70); friction in the band clamps adds 1.45 on a 60 mm pole and only 0.97 on a 40 mm pole.

**Options weighed.** An M10 bolt (about 2 times the bending capacity, but about 0.03 kg more mass, which would put the pole over 5 kg, and a new hole and spacer size), a shorter spacer (needs a new plate position), a stronger class of the same bolt (no geometry change, no mass change).

**Fix.** Specify the M8 x 100 through-bolt in stainless class A4-80 (ISO 3506, proof stress 600 MPa) with the partial thread kept out of the cantilever. The bolt BOM line is changed in text only; its price is to confirm with a supplier. FLG-CAL-001 H2b is rewritten with the bending model, S11 is corrected and stays "Plausible, to confirm at TRL 3", and PR-015 now states a twist factor of 1.8 on the bolt. This keeps the working principle and the design dimensions. If Amish wants more margin on small poles, an M10 bolt or a second bolt is the next step, and that is his decision because it adds mass against the 5 kg limit.

## Part 2c. Other review findings applied (also under the standing instruction)

| Finding | Change |
| --- | --- |
| Mass margin 0.006 kg is inside the estimate's accuracy | PR-015 restated "At risk"; the weigh-in at TRL 4 and the 2.5 mm plate fallback (saves only 0.045 kg) stay as decided on 2026-10-02 |
| PR-006 holds only to SF10 | Status limited to SF9 and SF10 on a private gateway; SF11 and SF12 give 123 s and 201 s in event mode (FLG-CAL-001 F4) |
| S2 rests on an assumed radar accuracy | Verdict changed to Plausible |
| Euler buckling of the brace not valid at L/r 37 | Johnson buckling and pin bearing used; capacity 11.5 kN against 1.5 kN |
| Drain accuracy if the ranger's error is plus or minus (1 cm + 0.3 %) | Noted in S5; the NTC stays mandatory |

## Part 3. Model changes recorded

No design dimension of option A (`PARAMS`) changed. The kit 1.9 model draws every bolt, nut, washer and plug, so the two cable centre lines now end in the plug moulding 45 mm above the node base: the street cable run is 2,619 mm (was 2,641 mm) and the drain cable run 4,310 mm (was 4,335 mm), both still inside the 3 m and 5 m cables with their drip loops. FLG-CAL-001 sections J and I are updated to match.

## Consequences

- FLG-OPT-001 and the options picture show A, B and C side by side.
- `concept_chosen` stays unset in `project.yaml` until Amish decides.
- If Amish picks B, requirements PR-001, PR-009, PR-012, PR-015 and PR-018 change (no head, no arm, no through-bolt; a stand pipe instead), and the build plan is rewritten at the next session.
