---
doc_id: FLG-PRB-001
title: FloodGauge problem statement
project: FloodGauge
doc_type: Problem statement
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; budget treatment and design direction per FLG-DDR-001 (adopted for TRL 3 pending Amish's review); open questions updated from FLG-CAL-001
- version: "0.4"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($160)
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Open questions on the pilot partner and alert ownership answered by Amish's 2026-10-02 decisions"
---

# FloodGauge problem statement

Urban flash floods rise in minutes, and warnings rely on river gauges far from the streets that flood. The people most at risk, drivers entering an underpass, residents of basement homes and crews clearing blocked drains, need a reading from their own street, not from a river several kilometers away.

## The problem in numbers

- About 1.81 billion people, 23 % of the world's population, are directly exposed to 1-in-100-year floods, and 89 % of them live in low- and middle-income countries ([Rentschler, Salhab and Jafino, 2022](https://www.nature.com/articles/s41467-022-30727-4)).
- Shallow water is enough to kill. The US National Weather Service states that 150 mm (6 in) of fast-moving water can knock over an adult, 300 mm (12 in) of rushing water can carry away most cars, and over half of flood drownings happen when a vehicle is driven into flood water ([NWS](https://www.weather.gov/safety/flood-turn-around-dont-drown)).
- Only 108 countries, 55 % of the total, reported multi-hazard early warning systems in 2024, and countries with limited coverage had disaster mortality nearly six times that of countries with substantial coverage ([UNDRR and WMO, 2024](https://www.undrr.org/reports/global-status-MHEWS-2024)).

Street flooding has two common causes, and a useful gauge must see both:

1. **The drain backs up.** Rain exceeds pipe capacity, or the outfall is submerged, so water rises inside the catch basin and then out through the grate.
2. **The inlet is blocked.** Leaves, litter or sediment cover the grate, so water ponds in the gutter while the basin below stays nearly empty.

A sensor inside the basin sees the first case early and misses the second. A sensor over the gutter sees the second but only once water is already on the street. FloodGauge therefore uses one node with two ranging heads (FLG-DDR-001 D2, adopted for TRL 3 pending Amish's review; see FLG-PRC-001).

## Users and context

| User | Need | Setting |
| --- | --- | --- |
| Drainage and public works crews | Know which inlets are blocked or surcharging, in time to clear them or close a road | Municipal depots, on-call staff with phones |
| Emergency managers | Street-level depth and rate of rise to decide road closures and warnings | City or district emergency operations |
| Residents, especially of basement and ground-floor homes | A plain local warning when water on their street passes a set depth | Opt-in text message or public map |
| Community groups and schools | Open local data to argue for drainage upgrades and to learn | Neighborhood associations, universities |
| Planners and researchers | A record of where and how often streets flood | Open data portals |

Operating context (assumed, to be confirmed with partners):

- Mounted on an existing sign or light pole within about 1 m of a storm inlet, with the owner's permission.
- Outdoor, -20 to 50 °C air, direct sun, driving rain, road spray, vandalism and theft risk.
- No mains power at the pole; solar through FieldNode.
- LoRaWAN coverage from a city network, a community gateway such as TwinKit, or The Things Network.

## Constraints

- Garage-buildable prototype: FloodGauge-specific parts within the $160 USD budget in `project.yaml` (approved by Amish on 2026-09-26), with the shared FieldNode core ($126.00) costed in its own repo (FLG-DDR-001 D1, adopted for TRL 3 pending Amish's review). FLG-CAL-001 gives $153.50.
- Builds on the lab's FieldNode core for enclosure, power and radio, so FloodGauge designs only its sensing heads, mounting and alert logic.
- Levels only: no camera, no microphone, no images or audio leave the device.
- No drilling of the road surface; any work in the catch basin is done from the surface without entering it.
- Open licenses: CERN-OHL-S-2.0 for hardware, MIT for software.
- Not a replacement for official warnings. It supplements them.

## Prior work

- **FloodNet, New York City.** Researchers at New York University and the City University of New York run a street flood sensor network whose sensors use an ultrasonic range finder over the street, sample every minute and publish near real-time data ([FloodNet methodology](https://www.floodnet.nyc/methodology)). The project reached 250 sensors in 2024, and the NYC Department of Environmental Protection commissioned 500 ([FloodNet](https://www.floodnet.nyc/about)). Its build repository describes solar power, LoRaWAN, a sign-post mount and a sensor cost below $200 per unit, and its designs are published under CC BY-NC-SA 4.0 ([floodnet-nyc/flood-sensor](https://github.com/floodnet-nyc/flood-sensor)). FloodNet shows the approach works at city scale. Its non-commercial license means FloodGauge is an independent design, not a derivative.
- **Low-cost waterproof ultrasonic rangers.** Modules such as the DFRobot A02YYUW (3 to 450 cm, ±1 cm, IP67, 60° beam) cost about $16 ([DFRobot](https://www.dfrobot.com/product-1935.html)). Their wide beam and temperature sensitivity shape the design choices in FLG-PRC-001.
- **60 GHz pulsed coherent radar modules.** Acconeer's A121 sensor and XM125 module range up to 20 m in an 18.6 x 15 mm module ([Acconeer](https://www.acconeer.com/products/)). Radar ranging does not depend on air temperature, unlike ultrasound.

## Out of scope at this stage

- River, canal or coastal gauging.
- Flow or velocity measurement.
- Rainfall measurement and flood forecasting models.
- Automatic road barriers or pump control.

## Open questions

- [ ] Which alert depths do local crews and residents want? The default 150 mm and 300 mm bands follow NWS guidance but are not validated locally; in a fast flood the first alert arrives at about 190 to 250 mm (FLG-CAL-001).
- [x] Who owns the alert service and the duty to act on an alert? Decided by Amish, 2026-10-02: the partner city's emergency management office; FloodGauge publishes levels and band crossings only.
- [ ] Can a cable be run from the catch basin to the pole, or does the drain head need its own node?
- [ ] Is an arm over the gutter allowed by the road authority, and at what height? At 2.95 m it is inside the envelope of a 4 m truck at the curb (FLG-CAL-001).
- [x] Which pilot partner and city? Decided by Amish, 2026-10-02 (FLG-DDR-001 O1): a city or county flood agency with street flooding at grated curb inlets and an existing gauge or alert programme; the first candidate type to approach is a county flood control district such as the Harris County Flood Control District in Houston. Nothing is agreed.
- [ ] What does the pilot city's LoRaWAN coverage look like at street level near inlets?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
