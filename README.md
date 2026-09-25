# FloodGauge

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $150 USD · **Difficulty:** 2 of 5

A street and drain water level sensor using ultrasonic or radar ranging, warning residents and crews when drains back up or streets begin to flood.

## Concept rationale

Street-level readings give minutes of warning where river gauges give none.

## Burning platform

Flash floods in cities are increasing with heavier rainfall and more paved surfaces.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab.

## Problem

Urban flash floods rise in minutes, and warnings rely on river gauges far from the streets that flood.

## Concept

A street and drain water level sensor using ultrasonic or radar ranging, warning residents and crews when drains back up or streets begin to flood.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Ultrasonic or radar level sensor
- FieldNode core
- Mounting bracket over drain or channel
- Alert service

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Install only with traffic and confined space precautions. Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.

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
