# FloodGauge

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $150 USD · **Difficulty:** 2 of 5

A street and drain water level sensor using ultrasonic or radar ranging, warning residents and crews when drains back up or streets begin to flood.

![FloodGauge concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Concept rationale

Street-level readings give minutes of warning where river gauges give none. Streets flood in two ways: the drain fills and backs up through the grate, or the grate is blocked and water ponds above an empty drain. FloodGauge watches both from one pole. A radar head on a short arm over the gutter measures water depth on the street, and an ultrasonic head in a stilling tube inside the catch basin sees the drain filling first. The lab's FieldNode core supplies the enclosure, solar power and LoRaWAN radio, so this project adds only the heads, the mounting and the alert logic.

Keeping it open and garage-buildable lets a city, a university or a neighborhood group build, inspect and repair its own gauges and own its data. The parts are off the shelf or cut with hand tools, the designs are under CERN-OHL-S-2.0 and the software under MIT, and the gauge sends water levels only: no camera, no microphone.

## Burning platform

About 1.81 billion people, 23 % of the world's population, are directly exposed to 1-in-100-year floods, and 89 % of them live in low- and middle-income countries ([Rentschler, Salhab and Jafino, 2022](https://www.nature.com/articles/s41467-022-30727-4)). Only 108 countries, 55 % of the total, reported multi-hazard early warning systems in 2024, and countries with limited coverage had disaster mortality nearly six times higher than those with substantial coverage ([UNDRR and WMO, 2024](https://www.undrr.org/reports/global-status-MHEWS-2024)).

Depths that look harmless kill. The US National Weather Service warns that 150 mm (6 in) of fast-moving water can knock over an adult and 300 mm (12 in) can carry away most cars, and that over half of flood drownings happen when a vehicle is driven into flood water ([NWS](https://www.weather.gov/safety/flood-turn-around-dont-drown)). Those depths build up on a street in minutes, well before a river gauge downstream responds.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal drainage and public works | Find blocked or surcharging inlets during a storm and send crews to the right street |
| Emergency management | Street depth and rate of rise to close underpasses and warn basement residents |
| Road and transit operators | Flooding alerts at underpasses, bus stops and depot entrances |
| Property and campus management | Early warning for car parks, loading docks and basement entrances |
| Insurance and resilience planning | An open record of where and how often streets flood |
| Research and education | Open, repeatable urban hydrology data for universities and schools |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | Over half of flood drownings involve vehicles driven into water ([NWS](https://www.weather.gov/safety/flood-turn-around-dont-drown)); New York City's FloodNet reached 250 street sensors in 2024 ([FloodNet](https://www.floodnet.nyc/about)), showing demand for street-level data. |
| Netherlands | The highest share of population in flood zones worldwide, 58.7 % ([Rentschler et al., 2022](https://www.nature.com/articles/s41467-022-30727-4)); dense cities need drain-level data as well as dikes. |
| Germany and Belgium | The July 2021 floods caused more than 200 deaths after record rainfall ([Copernicus, 2021](https://climate.copernicus.eu/esotc/2021/flooding-july)). |
| India and China | Together about 785 million flood-exposed people, over one third of the global total ([Rentschler et al., 2022](https://www.nature.com/articles/s41467-022-30727-4)), many in fast-growing cities. |
| Vietnam | 46 % of the population lives in flood zones, the highest share among developing countries ([Rentschler et al., 2022](https://www.nature.com/articles/s41467-022-30727-4)). |
| Sub-Saharan Africa | 44 % of the 170 million people facing both high flood risk and extreme poverty live here ([Rentschler et al., 2022](https://www.nature.com/articles/s41467-022-30727-4)); low-cost open gauges suit city budgets. |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. The real-world trigger is community street flood sensing such as New York City's FloodNet, whose low-cost ultrasonic sensors on sign posts sample every minute ([FloodNet](https://www.floodnet.nyc/methodology)); its designs carry a non-commercial license ([floodnet-nyc/flood-sensor](https://github.com/floodnet-nyc/flood-sensor)), which leaves room for an openly licensed gauge that also looks inside the drain.

## Problem

Urban flash floods rise in minutes, and warnings rely on river gauges far from the streets that flood.

## Concept

A street and drain water level sensor using ultrasonic or radar ranging, warning residents and crews when drains back up or streets begin to flood.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- FieldNode core (enclosure, 6 W solar panel, LiFePO4 cell, LoRaWAN radio), shared with other lab projects
- Street head: 60 GHz radar on a short arm over the gutter (proposed)
- Drain head: waterproof ultrasonic ranger with wet probe, in a slotted stilling tube inside the catch basin (proposed)
- Conduit from basin to pole, depth marker plate with 150 mm and 300 mm bands
- Open alert service on a LoRaWAN gateway such as TwinKit

First-order estimates (to be checked at TRL 3): about 70 s typical alert latency, a few milliwatts of sensor load, about 3.1 kg on the pole and about $271 in parts including the $126 FieldNode core, above the $150 budget. See the [design precis](docs/02-concept.md) and [requirements](docs/03-requirements.md), including the requirements not yet met.

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Install only with traffic and confined space precautions. Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.
>
> Never enter a catch basin: it can hold toxic or oxygen-poor air and fast-rising water. Stormwater carries sewage and chemicals; wear gloves and eye protection. The FieldNode LiFePO4 cell must be fused and charged only between 0 and 45 °C.
>
> FloodGauge supplements official flood warnings and must never be the only warning people rely on.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (FLG-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `FLG-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
