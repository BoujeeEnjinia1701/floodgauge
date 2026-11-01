---
doc_id: FLG-RSK-001
title: FloodGauge risk register and hazard analysis
project: FloodGauge
doc_type: Risk register
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: Initial draft for the kit 1.9.1 upgrade; project risks, preliminary hazard analysis and first-pass design FMEA of option A with notes for B and C
---

# FloodGauge risk register and hazard analysis

Top risks: the radar module is unverified, the drain head seal is only IP67, and the pilot city has not been approached. The main hazards are an arm falling onto a road and work at height beside traffic; both are controlled by the through-bolt and a traffic plan. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection is scored 1 (certain to be caught) to 10 (not caught) in the FMEA. The scores are first-pass judgements by the design lead for review with a partner; they are not measured.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-1 | Radar module data sheet does not support the 2 mm accuracy or the lens beam | Accuracy and beam width are assumed (CAL Table 1) | Street depth error above 10 mm (PR-002) or a false curb echo | 3 | 4 | Design lead | Read the data sheet before buying; if it fails, use option B's pressure transducer |
| R-2 | Pilot city refuses an arm over the gutter or an attachment on the pole | No road authority has been approached | Option A cannot be installed; stand pipe options B or C needed | 3 | 5 | Pilot partner | Ask early; FLG-OPT-001 carries B as the fallback |
| R-3 | Drain head loses its seal in a long flood | Transducer face keeps the stock IP67 seal (PR-009) | Basin reading lost during the event that matters most | 3 | 4 | Design lead | Ask the maker for a rating; consider option B's sealed stainless transducer for the basin |
| R-4 | Mass on the pole exceeds 5 kg | Margin is 0.01 kg on model volumes (PR-015) | Pole owner rejects the load | 3 | 3 | Design lead | Weigh at TRL 4; 2.5 mm bracket plate is the named fix |
| R-5 | Airtime exceeds network rules at slow spreading factors | SF10 and slower (PR-007) | Network operator limits or blocks the gateway | 3 | 3 | Network operator | Private or city gateway for event reporting (FLG-DEC-001) |
| R-6 | Cost stays above the USD 160 target | Radar and arm are USD 90 of USD 205.50 | Fewer gauges per budget | 4 | 2 | Design lead | Quote the radar; value-engineering list in DEC |
| R-7 | Tampering or theft at the sidewalk | Fixings within reach (PR-018) | Gauge removed or damaged | 3 | 3 | Pole owner | Security fixings are in the design; option A keeps the arm out of reach |
| R-8 | A fixed 60 GHz radar is not covered by the module's radio certificate | G1 and G2 are to assess | Cannot be used legally in the pilot country | 2 | 5 | Design lead | Check the certificate scope before the pilot |
| R-9 | Pilot partner never agrees to host a gauge | No partner is agreed (PRB open questions) | Design stays on paper | 3 | 4 | Project lead | Approach a county flood control district (FLG-DEC-001) |

## Preliminary hazard analysis

Table 2. Hazards. Severity is 1 (minor) to 5 (fatal); likelihood is 1 (remote) to 5 (frequent).

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H-1 | Arm or head falls onto the roadway | Clamp slip, bolt failure or vandalism | Strike to a person or vehicle | 5 | 2 | Through-bolt and two clamps, factor 37 against wind twist; 50 kg hang case passes (CAL H) | Low if the through-bolt is fitted |
| H-2 | Head or arm struck by a tall vehicle | Lens 4.6 m above a 4.3 m vehicle | Damage to the vehicle or the gauge | 3 | 2 | Lens set per site with 0.3 m margin (PR-001) | Low |
| H-3 | Person trips on the surface cable covers | Covers on the gutter and sidewalk are 16 mm high | Fall | 3 | 3 | Low hat section with ramped ends; edges broken (PR-019); marker plate | Medium; to review with the partner |
| H-4 | Cut from a sharp edge during installation or by a passer-by | Cut sheet metal and bolt ends | Laceration | 2 | 3 | Edges broken in the model; covers 2 mm folded; guards on bolt ends to assess | Low |
| H-5 | Fall or strike while lifting the arm to 4.6 m | Work at height beside traffic | Serious injury | 5 | 2 | Two-person crew with traffic protection, mobile platform (CAL L1); not tested at TRL 3 | Medium; training and traffic plan needed |
| H-6 | Gas, drowning or crush when lifting a grate or entering a basin | Confined space and heavy grate | Serious injury | 5 | 2 | No entry; grate lifted with a hook by two people (PR-012) | Low |
| H-7 | Lithium iron phosphate cell overheats in sun | Hot enclosure above the charge limit (FieldNode) | Fire or cell damage | 4 | 2 | Charger cut-out and the cell chemistry; FieldNode safety case | Medium; inherited from FieldNode |
| H-8 | Radio emission exposure | 60 GHz and 868 MHz low power | None expected at the power levels of certified modules | 1 | 1 | Certified modules; to assess (REG G1, G2) | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes of option A (rows F-1 to F-12) and of the new parts in options B and C (F-13, F-14). RPN = severity x occurrence x detection, each scored 1 to 10 here; a row with an RPN above 100 gets an action before TRL 4.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-1 | Radar head | Measure street range | No echo or false echo from the curb | Wrong or missing street depth | Rain on the PTFE lens; curb inside the beam | 4 | 4 | 5 | 80 | Record a dry-road background; reject the curb echo (CAL G2) |
| F-2 | Radar head housing | Keep water out | Seal leak at the lens or gland | Radar fails | Gasket creep, UV | 7 | 3 | 4 | 84 | Specify a sealed lid; check the housing rating |
| F-3 | Drain head ranger | Measure basin level | Echo from the tube wall or condensation | Reading error | 69 mm bore; fog on the face | 5 | 4 | 5 | 100 | Use first-echo logic and the NTC; test at TRL 4 |
| F-4 | Drain head seal | Survive submersion | Water reaches the transducer | Drain reading lost | IP67 face only (PR-009) | 7 | 4 | 6 | 168 | Ask for a rating; consider option B transducer |
| F-5 | Stilling tube slots | Pass water, damp waves | Slots clog with leaf litter | Level lags the basin | Biofilm and debris | 5 | 4 | 4 | 80 | Clean at each grate visit; the open area has margin (STM S21) |
| F-6 | Pole bracket and band clamps | Hold the arm | Slip or twist on the pole | Head moves, datum lost | Preload loss, vibration | 7 | 3 | 4 | 84 | Specify clamp torque for 1,000 N (DEC to confirm 4) |
| F-7 | M8 through-bolt | Stop twist | Shear or bearing failure in a thin pole wall | Arm swings round | 2.5 mm wall assumed (DEC item 5) | 8 | 2 | 5 | 80 | Confirm pole wall at each site (DEC to confirm 5) |
| F-8 | Arm tube | Carry the head | Fatigue crack at the cleats | Head falls | Wind buffeting, 1.6 mm wall | 9 | 2 | 5 | 90 | Fillet-free cleats; inspect yearly |
| F-9 | Drain cable | Carry data | Cable cut or crushed under the cover or by the grate | Drain reading lost | Grate seated on the cable | 6 | 4 | 4 | 96 | Slack loop tied to the tube clamp; route by the grate opening |
| F-10 | Surface covers | Protect the cable | Cover lifted or tripped on | Cable exposed; trip hazard | Anchor removed | 6 | 3 | 3 | 54 | Security nuts on anchors |
| F-11 | FieldNode (shared) | Power and radio | Cell does not charge in heat or cold | No data | Charge window 0 to 45 C | 6 | 4 | 5 | 120 | Inherited; see FieldNode risks |
| F-12 | Marker plate | Show depth by eye | Bands fade | Misread depth | UV on film | 3 | 5 | 3 | 45 | Use UV-stable film; yearly check |
| F-13 | Option B transducer | Measure pressure | Zero shifts with a wet vent | Constant depth error | Condensation in the vent tube (STM B3) | 6 | 4 | 6 | 144 | Desiccant or membrane; yearly zero check |
| F-14 | Option C float | Move with the water | Float binds or fills | Reading sticks | Silt, ice or a cracked shell (STM C5) | 6 | 4 | 5 | 120 | Hollow shell fix made (FLG-DDR-004 F1); stop collars |

## Safety

Work at height beside traffic, lifting a grate, a pole-mounted mass, a lithium iron phosphate cell and mains-free 12 V electronics are the hazards in this design. No mains voltage is present. The installation sequence is paper work only at TRL 3; no one has built or installed a unit.
