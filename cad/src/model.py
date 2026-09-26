"""FloodGauge parametric model (build123d), TRL 3 (FLG-DDR-002 decisions applied).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
  floodgauge-assembly   kit parts 1 to 8 as installed (no street context)
  floodgauge-pole-kit   FieldNode core, street radar head, arm and clamps, depth marker (items 1 to 3, 8)
  floodgauge-drain-kit  drain head and stilling tube (items 4 and 5)
  floodgauge-site       existing street, catch basin, grate and pole (context only, not in the BOM)

FLG-DDR-002 (2026-09-25): lens at 4.6 m for a curb lane with tall vehicles (R1 band 2.5 to 5.0 m, set per
site); pilot cable route at the surface under a bolted steel cover (conduit kept for permanent sites);
M8 anti-rotation through-bolt at the upper clamp.

Massing-plus detail: main dimensions and interfaces are correct for concept review; fabrication
detail (slots, threads, fixings, seals) is not modeled. PRELIMINARY, NOT FOR FABRICATION.
The same PARAMS feed docs/04-calcs/sizing.py (FLG-CAL-001), the drawing FLG-DWG-001
(cad/src/sheets.py) and the concept media (cad/src/concept_media.py).

Coordinates in mm. The street runs along Y. X runs across the street: road at X < 0, curb face at
X = 0, sidewalk at X > 0. The road surface at the gauge point is Z = 0 (the depth datum).
FieldNode dimensions follow the FieldNode repo (FND-CAL-001 and its cad/src/model.py PARAMS):
enclosure 150 x 90 x 200 mm, panel 290 x 200 mm, mass 2.41 kg, cost $126.00.
"""
from pathlib import Path
import math

PARAMS = {
    # existing street (context, not in the BOM)
    "curb_h": 150.0, "slab": 200.0, "strip": 1500.0, "road_w": 1300.0, "walk_w": 1300.0,
    "pole_x": 450.0, "pole_od": 60.0, "pole_h": 4900.0,          # street pole, height above the sidewalk
    "grate": (-500.0, -100.0, 600.0, 40.0),                        # x0, x1, length along Y, thickness
    "basin": (-750.0, -50.0, 900.0), "basin_floor": -1300.0, "basin_wall": 100.0,
    "outlet_z": -1050.0, "outlet_bore": 300.0,                     # outlet pipe center and bore
    # 1 FieldNode core (from the FieldNode repo)
    "enc": (90.0, 150.0, 200.0),                                   # depth (X), width (Y), height (Z)
    "node_z": 3000.0,                                              # enclosure center above the road
    "back_plate": (12.0, 110.0, 240.0),
    "panel": (200.0, 290.0, 17.0), "panel_tilt": 25.0,             # tilted toward the road
    "fieldnode_mass": 2.41, "fieldnode_cost": 126.00,
    # 2 street radar head
    "head_offset": 250.0,          # head axis past the curb face, over the gutter
    "head_z": 4600.0,              # underside of the lens above the road (range to the dry road); DDR-002: clears a 4.3 m vehicle plus 0.3 m
    "head_band": (2500.0, 5000.0), # R1 mounting band, height set per site to the road authority's clearance rule
    "head_d": 76.0, "head_h": 90.0, "lens_d": 60.0, "lens_t": 6.0,
    # 3 sensor arm and clamps
    "arm_sq": 40.0, "arm_wall": 2.0, "arm_z": 4710.0,
    "clamp_dz": 400.0, "clamp_w": 50.0, "clamp_t": 8.0,
    "brace_sq": 25.0, "brace_wall": 2.0, "brace_leg": 400.0,
    "saddle": (70.0, 50.0, 40.0),
    "bolt_d": 8.0, "bolt_l": 110.0,  # M8 stainless anti-rotation through-bolt, upper clamp and pole (DDR-002)
    # 4 drain head and 5 stilling tube
    "tube_od": 75.0, "tube_wall": 3.0, "tube_inset": 90.0,         # tube axis from the basin wall (road side of curb)
    "tube_top": -300.0, "tube_bot_gap": 60.0,                       # top below the road; bottom above the basin floor
    "slot": (5.0, 50.0), "slots_per_row": 4, "slot_rows": 10,       # slot width, length (modeled in CAL only)
    "drain_head_d": 104.0, "drain_head_h": 90.0,
    "us_blind": 30.0,              # ultrasonic blind zone below the transducer face (A02YYUW, 3 cm)
    "probe_drop": 10.0,            # wet probe tips below the head face
    "bracket_z": (-380.0, -1010.0),
    # 6 cables, 7 surface cable cover (pilot route, DDR-002); conduit route kept for permanent sites
    "cable_d": 10.0, "cover_y": 250.0,  # cover line along the street, beside the grate end
    "cover_angle": (50.0, 5.0),    # steel angle leg and thickness over the gutter strip and curb face
    "cover_walk": (120.0, 12.0),   # low beveled steel cover across the sidewalk, width and height
    "riser_rise": 400.0,           # riser guard height above the sidewalk
    "guard": (40.0, 70.0, 300.0),
    # 8 depth marker plate
    "marker": (3.0, 90.0, 450.0), "bands": (150.0, 300.0, 450.0),  # amber from 150, red from 300 to 450 mm above road
}

BOM = {"node": (1, "FieldNode core"), "panel": (1, "FieldNode 6 W panel"),
       "street_head": (2, "Street radar head"), "arm": (3, "Sensor arm and pole clamps"),
       "drain_head": (4, "Drain head"), "tube": (5, "Stilling tube"),
       "cables": (6, "Sensor cables"), "conduit": (7, "Surface cable cover and riser guard"),
       "marker": (8, "Depth marker plate")}


def derived(p=PARAMS):
    """Dimensions quoted by the calc note and the drawing, computed from PARAMS."""
    d = {}
    d["pole_r"] = p["pole_od"] / 2
    d["head_x"] = -p["head_offset"]
    d["pole_face_x"] = p["pole_x"] - d["pole_r"]                  # road side face of the pole
    d["arm_x0"] = d["head_x"] - p["saddle"][0] / 2                 # free end of the arm
    d["arm_x1"] = p["pole_x"] + d["pole_r"] + 40.0                 # arm end behind the pole
    d["arm_len"] = d["arm_x1"] - d["arm_x0"]
    d["cantilever"] = p["pole_x"] - d["head_x"]                    # pole axis to head axis
    d["brace_len"] = math.hypot(p["brace_leg"], p["brace_leg"]) - 60.0
    d["arm_top"] = p["arm_z"] + p["arm_sq"] / 2
    d["head_top"] = p["head_z"] + p["head_h"]
    d["range_dry"] = p["head_z"]                                   # mm, lens to dry road
    d["range_600"] = p["head_z"] - 600.0
    bx0, bx1, by = p["basin"]
    d["tube_x"] = bx1 - p["tube_inset"]
    d["tube_id"] = p["tube_od"] - 2 * p["tube_wall"]
    d["tube_bot"] = p["basin_floor"] + p["tube_bot_gap"]
    d["tube_len"] = p["tube_top"] - d["tube_bot"]
    d["dh_face"] = p["tube_top"]                                   # drain head transducer face
    d["dh_top_level"] = p["tube_top"] - p["us_blind"]              # highest level the ultrasonic reads
    d["probe_level"] = p["tube_top"] - p["probe_drop"]             # wet probe trips
    d["grate_under"] = -p["grate"][3]
    d["outlet_invert"] = p["outlet_z"] - p["outlet_bore"] / 2
    d["dh_range_max"] = p["tube_top"] - (p["basin_floor"] + 50.0)  # face to the lowest level R3 asks for
    d["node_x"] = d["pole_face_x"] - p["back_plate"][0] - p["enc"][0] / 2
    d["node_bot"] = p["node_z"] - p["enc"][2] / 2
    d["node_top"] = p["node_z"] + p["enc"][2] / 2
    d["riser_x"] = p["pole_x"] + 60.0
    d["riser_top"] = p["curb_h"] + p["riser_rise"]
    d["walk_top"] = p["curb_h"]
    d["overall_top"] = max(d["arm_top"], d["head_top"])
    d["head_clear_min"] = p["head_band"][0]
    # cable runs (mm), street head: along the arm, down to the node; drain head (surface route, DDR-002):
    # up from the head to the grate frame, across the gutter strip, up the curb face, across the sidewalk
    # under the cover to the riser guard, then up the pole to the node
    d["cable_street"] = (d["cantilever"] - d["pole_r"]) + (p["arm_z"] - p["node_z"])
    d["cable_drain"] = ((0.0 - p["tube_top"]) + (0.0 - d["tube_x"]) + p["cover_y"] + p["curb_h"]
                        + d["riser_x"] + (d["riser_top"] - p["curb_h"]) + (d["node_bot"] - d["riser_top"]))
    d["cover_len"] = (0.0 - p["grate"][1]) + p["curb_h"] + d["riser_x"]   # gutter strip, curb face, sidewalk
    return d


def _tube_sq(size, wall, length):
    from build123d import Box
    return Box(length, size, size) - Box(length + 2, size - 2 * wall, size - 2 * wall)


def build_parts(p=PARAMS):
    """Return {key: solid} for the kit parts (keys in BOM)."""
    from build123d import Box, Cylinder, Pos, Rot
    D = derived(p)
    px, pr = p["pole_x"], D["pole_r"]
    parts = {}

    # 1 FieldNode core: enclosure on a back plate on the road side of the pole, panel above as a hood
    ex, ey, ez = p["enc"]
    bt, bw, bh = p["back_plate"]
    node = Pos(D["node_x"], 0, p["node_z"]) * Box(ex, ey, ez)
    node += Pos(D["pole_face_x"] - bt / 2, 0, p["node_z"]) * Box(bt, bw, bh)
    parts["node"] = node
    pw, pl, pt = p["panel"]
    parts["panel"] = (Pos(D["node_x"] - 30, 0, D["node_top"] + 55) * Rot(0, -p["panel_tilt"], 0)
                      * Box(pw, pl, pt))

    # 2 street radar head: housing and lens face, lens underside at head_z
    hx = D["head_x"]
    head = Pos(hx, 0, p["head_z"] + p["lens_t"] + p["head_h"] / 2 - p["lens_t"]) * Cylinder(p["head_d"] / 2, p["head_h"] - p["lens_t"])
    head += Pos(hx, 0, p["head_z"] + p["lens_t"] / 2) * Cylinder(p["lens_d"] / 2, p["lens_t"])
    parts["street_head"] = head

    # 3 arm: square tube, head saddle, two band clamps on the pole, knee brace
    arm = Pos((D["arm_x0"] + D["arm_x1"]) / 2, 0, p["arm_z"]) * _tube_sq(p["arm_sq"], p["arm_wall"], D["arm_len"])
    sx, sy, sz = p["saddle"]
    arm += Pos(hx, 0, p["arm_z"] - p["arm_sq"] / 2 - sz / 2) * Box(sx, sy, sz)
    for z in (p["arm_z"], p["arm_z"] - p["clamp_dz"]):
        arm += Pos(px, 0, z) * (Cylinder(pr + p["clamp_t"], p["clamp_w"]) - Cylinder(pr + 0.5, p["clamp_w"] + 2))
    L = p["brace_leg"]
    arm += (Pos(D["pole_face_x"] - L / 2, 0, p["arm_z"] - L / 2) * Rot(0, -45, 0)
            * Box(p["brace_sq"], p["brace_sq"], D["brace_len"]))
    # M8 anti-rotation through-bolt through the lower clamp band and the pole, axis along the street (DDR-002)
    arm += Pos(px, 0, p["arm_z"] - p["clamp_dz"]) * Rot(90, 0, 0) * Cylinder(p["bolt_d"] / 2, p["bolt_l"])
    parts["arm"] = arm

    # 4 drain head on top of 5 the stilling tube
    tx = D["tube_x"]
    parts["drain_head"] = Pos(tx, 0, p["tube_top"] + p["drain_head_h"] / 2) * Cylinder(p["drain_head_d"] / 2, p["drain_head_h"])
    tube = Pos(tx, 0, (p["tube_top"] + D["tube_bot"]) / 2) * (
        Cylinder(p["tube_od"] / 2, D["tube_len"]) - Cylinder(D["tube_id"] / 2, D["tube_len"] + 2))
    bx1 = p["basin"][1]
    for z in p["bracket_z"]:
        tube += (Pos((tx + bx1) / 2 + 5, 0, z) * Box(bx1 - tx + 10, 30, 40)
                 - Pos(tx, 0, z) * Cylinder(p["tube_od"] / 2 + 0.5, 42))
    parts["tube"] = tube

    # 6 cables (street: along the arm and down to the node; drain: up the pole from the riser)
    c = p["cable_d"]
    xa = D["pole_face_x"] - 20
    cab = Pos((xa + hx) / 2, 0, D["arm_top"] + c / 2 + 3) * Box(xa - hx, c, c)
    cab += Pos(xa, 0, (D["arm_top"] + 8 + D["node_top"]) / 2) * Box(c, c, D["arm_top"] + 8 - D["node_top"])
    cab += Pos(hx, 0, (D["arm_top"] + 8 + D["head_top"]) / 2) * Box(c, c, D["arm_top"] + 8 - D["head_top"])
    xb = px + pr + 8
    cab += Pos(xb, 0, (D["riser_top"] + D["node_bot"]) / 2) * Box(c, c, D["node_bot"] - D["riser_top"])
    parts["cables"] = cab

    # 7 surface cable cover (pilot route, DDR-002): the cable leaves the basin at the grate frame, runs under a
    # steel angle across the gutter strip and up the curb face (anchored to the curb only, no road drilling),
    # under a low beveled steel cover across the sidewalk, and up a riser guard beside the pole
    cy, xr = p["cover_y"], D["riser_x"]
    al, at = p["cover_angle"]
    cw, ch = p["cover_walk"]
    gx1 = p["grate"][1]
    cov = Pos(gx1 / 2, cy, at / 2) * Box(-gx1, al, at)                                    # over the gutter strip
    cov += Pos(-at / 2, cy, p["curb_h"] / 2) * Box(at, al, p["curb_h"])                  # up the curb face
    cov += Pos(xr / 2, cy, p["curb_h"] + ch / 2) * Box(xr, cw, ch)                       # across the sidewalk
    gx, gy, gz = p["guard"]
    cov += Pos(xr, cy, p["curb_h"] + gz / 2) * (Box(gx, gy, gz) - Box(gx - 6, gy - 6, gz + 2))
    cov += Pos(tx, 0, (p["tube_top"] + p["drain_head_h"] - 60) / 2) * Cylinder(5, -(p["tube_top"] + p["drain_head_h"] + 60))  # flexible tail
    cov += Pos(tx, cy / 2, -60) * Rot(90, 0, 0) * Cylinder(5, cy)
    cov += Pos((tx + gx1) / 2, cy, -60) * Rot(0, 90, 0) * Cylinder(5, gx1 - tx)
    cov += Pos(gx1 + 5, cy, -30) * Cylinder(5, 60)                                         # out at the grate frame
    parts["conduit"] = cov

    # 8 depth marker plate on the road side of the pole, from the sidewalk up
    mt, mw, mh = p["marker"]
    parts["marker"] = Pos(D["pole_face_x"] - mt / 2, 0, p["curb_h"] + mh / 2) * Box(mt, mw, mh)
    return parts


def bands(p=PARAMS):
    """Amber and red bands on the marker plate (colored faces of item 8)."""
    from build123d import Box, Pos
    D = derived(p)
    a, r, top = p["bands"]
    x = D["pole_face_x"] - p["marker"][0] - 2
    mw = p["marker"][1] + 2
    return {"amber": Pos(x, 0, (a + r) / 2) * Box(4, mw, r - a),
            "red": Pos(x, 0, (r + top) / 2) * Box(4, mw, top - r)}


def site(p=PARAMS, basin_half=False):
    """Existing street, catch basin, grate, stormwater (illustrative) and pole. Not in the BOM.
    basin_half keeps only the +Y half of the basin and slab (for a section view)."""
    from build123d import Box, Cylinder, Pos, Rot
    D = derived(p)
    S, cs = p["slab"], p["curb_h"]
    gx0, gx1, gl, gt = p["grate"]
    road = Pos(-p["road_w"] / 2, 0, -S / 2) * Box(p["road_w"], p["strip"], S)
    road -= Pos((gx0 + gx1) / 2, 0, -S / 2) * Box(gx1 - gx0, gl, S + 2)
    walk = Pos(p["walk_w"] / 2, 0, (cs - S) / 2) * Box(p["walk_w"], p["strip"], cs + S)
    bx0, bx1, by = p["basin"]
    w, fl = p["basin_wall"], p["basin_floor"]
    ox0, ox1 = bx0 - w, bx1 + w
    outer = Pos((ox0 + ox1) / 2, 0, (fl - w - S) / 2) * Box(ox1 - ox0, by + 2 * w, -(fl - w) - S)
    inner = Pos((bx0 + bx1) / 2, 0, (fl - S) / 2 + 1) * Box(bx1 - bx0, by, -fl - S + 2)
    oz, ob = p["outlet_z"], p["outlet_bore"]
    basin = outer - inner - Pos(ox0 - 350, 0, oz) * Rot(0, 90, 0) * Cylinder(ob / 2, 800)
    basin += Pos(ox0 - 350, 0, oz) * Rot(0, 90, 0) * (Cylinder(ob / 2 + 20, 700) - Cylinder(ob / 2, 702))
    grate = Pos((gx0 + gx1) / 2, 0, -gt / 2) * Box(gx1 - gx0 - 10, gl - 10, gt)
    for k in range(7):
        grate -= Pos((gx0 + gx1) / 2, -240 + k * 80, -gt / 2) * Box(300, 40, gt + 10)
    water = Pos((bx0 + bx1) / 2, 0, (fl - 800.0) / 2) * Box(bx1 - bx0 - 2, by - 2, -800.0 - fl - 2)
    pole = Pos(p["pole_x"], 0, cs + p["pole_h"] / 2) * Cylinder(D["pole_r"], p["pole_h"])
    pole += Pos(p["pole_x"], 0, cs + p["pole_h"] - 120) * Box(20, 760, 200)
    out = {"road": road, "walk": walk, "basin": basin, "grate": grate, "water": water, "pole": pole}
    if basin_half:
        keep = Pos(0, 5000, 0) * Box(20000, 10000, 20000)
        out = {k: (v & keep) for k, v in out.items()}
    return out


def assembly(p=PARAMS, with_site=False):
    from build123d import Compound
    parts = build_parts(p)
    shapes = list(parts.values()) + list(bands(p).values())
    if with_site:
        s = site(p)
        shapes += [s["pole"], s["basin"], s["grate"]]
    return Compound(children=shapes)


def pole_kit(p=PARAMS):
    from build123d import Compound
    b = build_parts(p)
    return Compound(children=[b[k] for k in ("node", "panel", "street_head", "arm", "marker")])


def drain_kit(p=PARAMS):
    from build123d import Compound
    b = build_parts(p)
    return Compound(children=[b["drain_head"], b["tube"]])


def site_compound(p=PARAMS):
    from build123d import Compound
    s = site(p)
    return Compound(children=[s[k] for k in ("road", "walk", "basin", "grate", "pole")])


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    D = derived()
    outs = {"floodgauge-assembly": assembly(), "floodgauge-pole-kit": pole_kit(),
            "floodgauge-drain-kit": drain_kit(), "floodgauge-site": site_compound()}
    for name, shape in outs.items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm, volume {shape.volume / 1e6:.3f} L")
    print(f"head {PARAMS['head_offset']:.0f} mm past the curb face, "
          f"lens {PARAMS['head_z']:.0f} mm above the road; arm {D['arm_len']:.0f} mm; "
          f"tube {D['tube_len']:.0f} mm long, ID {D['tube_id']:.0f} mm")
