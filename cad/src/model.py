"""FloodGauge parametric model (build123d), TRL 3, constructable design (FLG-DDR-003).

Run from the repo root:  python cad/src/model.py            (exports and prints the checks)
                         python cad/src/model.py --check    (constructability checks only)
Exports STEP and STL into cad/step and cad/stl:
  floodgauge-assembly   kit parts 1 to 8 as installed, with the FieldNode core (no street context)
  floodgauge-pole-kit   FieldNode core, street radar head, arm and pole bracket, depth marker (items 1 to 3, 8)
  floodgauge-drain-kit  drain head, stilling tube and its pipe clamps (items 4 and 5)
  floodgauge-site       existing street, catch basin, grate and pole (context only, not in the BOM)

Decisions applied: FLG-DDR-001 and FLG-DDR-002 (lens 4.6 m, surface cable route for pilots,
M8 anti-rotation through-bolt). Revised 2026-10-01 under Amish's 2026-09-30 instruction to make the
design physically buildable (FLG-DDR-003, "Design for construction"):
  the arm no longer passes through the pole: it is bolted between two angle cleats on an aluminium
  pole bracket plate that sits on the pole on two V-blocks (the FieldNode pattern) and two band clamps;
  the knee brace is pinned in two folded clips, one under the arm and one on the bracket plate;
  the M8 through-bolt passes across the street through the bracket plate, a spacer and the pole;
  the radar head hangs from a head plate under the arm with a side cable gland (no saddle overlap);
  the drain head carries a 75 mm socket that slides over the stilling tube; the tube hangs on two
  stand-off pipe clamps instead of brackets set into the basin wall;
  the drain cable leaves the basin through a grate opening (the 5 mm gap at the grate frame cannot
  pass a cable) under three bolted hat-section covers (gutter, curb face, sidewalk), into a riser
  guard that is strapped to the pole beside the depth marker;
  the FieldNode core is its constructable design (FND-BLD-001) on its own V-blocks and band clamps;
  the depth marker plate is 2 mm and starts 15 mm above the sidewalk so the cover passes under it.
Main dimensions and interfaces only; tolerances are TRL 4 work.

The same PARAMS feed docs/04-calcs/sizing.py (FLG-CAL-001), the drawing FLG-DWG-001
(cad/src/sheets.py), the concept media (cad/src/concept_media.py) and the build plan pictures
(cad/src/build_plan_media.py).

Coordinates in mm. The street runs along Y. X runs across the street: road at X < 0, curb face at
X = 0, sidewalk at X > 0. The road surface at the gauge point is Z = 0 (the depth datum).
FieldNode dimensions follow the FieldNode repo (FND-BLD-001 and its cad/src/model.py PARAMS):
enclosure 150 x 90 x 200 mm, back plate 180 x 320 x 3 mm, panel 290 x 200 mm at 40 degrees,
mass 2.45 kg, cost $139.00.
"""
from dataclasses import dataclass
from pathlib import Path
import math
import sys

PARAMS = {
    # existing street (context, not in the BOM)
    "curb_h": 150.0, "slab": 200.0, "strip": 1500.0, "road_w": 1300.0, "walk_w": 1300.0,
    "pole_x": 450.0, "pole_od": 60.0, "pole_h": 4900.0,          # street pole, height above the sidewalk
    "grate": (-500.0, -100.0, 600.0, 40.0),                        # x0, x1, length along Y, thickness
    "basin": (-750.0, -50.0, 900.0), "basin_floor": -1300.0, "basin_wall": 100.0,
    "outlet_z": -1050.0, "outlet_bore": 300.0,                     # outlet pipe center and bore
    # 1 FieldNode core (constructable design, FND-BLD-001), facing the road
    "enc": (90.0, 150.0, 200.0),                                   # depth (X), width (Y), height (Z)
    "node_z": 3400.0,                                              # enclosure center above the road (FLG-DDR-003: was 3000, raised so the street cable fits 3 m)
    "fn_plate": (3.0, 180.0, 320.0), "fn_plate_drop": 40.0,        # FieldNode back plate t, w, h; bottom below the box
    "fn_clamp_dz": (-20.0, 230.0),                                 # FieldNode band clamps above the box bottom
    "fn_band_slot": 51.0,
    "panel": (200.0, 290.0, 17.0), "panel_tilt": 40.0,             # FieldNode 6 W panel on its own bracket
    "fieldnode_mass": 2.45, "fieldnode_cost": 139.00,
    "back_plate": (3.0, 180.0, 320.0),                             # kept for product_model.py
    # 2 street radar head: bought IP67 round housing, PTFE lens disc under it, side cable gland
    "head_offset": 250.0,          # head axis past the curb face, over the gutter
    "head_z": 4600.0,              # underside of the lens above the road (range to the dry road); DDR-002: clears a 4.3 m vehicle plus 0.3 m
    "head_band": (2500.0, 5000.0), # R1 mounting band, height set per site to the road authority's clearance rule
    "head_d": 76.0, "head_h": 90.0, "lens_d": 60.0, "lens_t": 6.0, "lens_window": 46.0,
    "gland": (20.0, 15.0),         # M12 cable gland on the housing side facing the pole: diameter, length
    "head_plate": (140.0, 70.0, 3.0),   # aluminium head plate under the arm: length (X), width (Y), thickness
    "head_bolt_dx": 55.0,          # head plate bolts each side of the head axis, through the arm
    # 3 sensor arm, knee brace and pole bracket
    "arm_sq": 40.0, "arm_wall": 1.6, "arm_tip": 70.0,              # arm tube; tube end beyond the head axis
    "clamp_dz": 400.0,                                             # band clamps 400 mm apart (concept)
    "band": (12.0, 0.8), "band_slot": (40.0, 3.0, 15.0),           # band width, thickness; slot centre y, width, height
    "bplate": (3.0, 100.0), "bplate_margin": 25.0,                 # bracket plate thickness, width; beyond each band
    "bplate_window": (60.0, 90.0),                                 # two lightening windows, width x height
    "vblock": (60.0, 33.0, 20.0), "v_apex": 7.8,                   # FieldNode V-block; V apex from the plate
    "angle": (30.0, 3.0), "cleat_len": 60.0,                       # arm cleats, 30 x 30 x 3 angle
    "brace_sq": 25.0, "brace_wall": 1.6,
    "clip": (3.0, 25.5, 50.0, 32.0),                               # brace clip strip t, inside width, length, ear depth
    "clip_pin": 22.0,                                              # brace pin below or in front of the clip base
    "foot_z": 4415.0,                                              # brace foot pin height above the road
    "spacer_d": 12.0,
    "bolt_d": 8.0, "bolt_l": 100.0,  # M8 stainless anti-rotation through-bolt, across the street through bracket plate and pole
    # kept for product_model.py (appearance model, concept geometry)
    "arm_z": 4713.0, "clamp_w": 50.0, "clamp_t": 8.0, "brace_leg": 253.0, "saddle": (70.0, 50.0, 40.0),
    # 4 drain head and 5 stilling tube
    "tube_od": 75.0, "tube_wall": 3.0, "tube_inset": 90.0,         # tube axis from the basin wall (road side of curb)
    "tube_top": -300.0, "tube_bot_gap": 60.0,                       # top (transducer face) below the road; bottom above the basin floor
    "slot": (5.0, 50.0), "slots_per_row": 4, "slot_rows": 10, "slot_pitch": 85.0, "slot_first": 55.0,
    "drain_head_d": 104.0, "drain_head_h": 90.0,
    "socket": (83.0, 40.0),        # 75 mm PVC socket under the head: outside diameter, length
    "us_blind": 30.0,              # ultrasonic blind zone below the transducer face (A02YYUW, 3 cm)
    "probe_drop": 10.0,            # wet probe tips below the head face
    "bracket_z": (-380.0, -1010.0),
    "pclamp": (3.0, 25.0),         # stand-off pipe clamp band thickness and width
    "wall_plate": (40.0, 5.0),
    # 6 cables
    "cable_d": 10.0,
    # 7 surface cable cover (pilot route, DDR-002): three hat-section covers and a riser guard
    "cover_y": 80.0,               # cover centre line along the street, over the grate opening nearest the curb
    "hat": (84.0, 16.0, 2.0),      # hat section overall width, height, sheet thickness
    "gutter_x0": -185.0,           # road end of the gutter cover, resting on the grate border
    "cable_exit_x": -165.0,        # where the drain cable comes up through the grate opening
    "riser_rise": 300.0,           # riser guard height above the sidewalk
    "guard": (40.0, 65.0, 2.0),    # riser guard U channel: width (X), depth (Y), sheet thickness
    "cover_angle": (50.0, 5.0), "cover_walk": (84.0, 16.0),        # kept for product_model.py
    # 8 depth marker plate
    "marker": (2.0, 90.0, 435.0), "marker_z0": 165.0,             # thickness, width, height; bottom above the road
    "marker_bands_z": (220.0, 420.0),                              # band clamps round the pole, marker and guard
    "bands": (150.0, 300.0, 450.0),  # amber from 150, red from 300 to 450 mm above road (amber visible from the plate bottom)
}

BOM = {"node": (1, "FieldNode core"), "panel": (1, "FieldNode 6 W panel"),
       "street_head": (2, "Street radar head"), "arm": (3, "Sensor arm, knee brace and pole bracket"),
       "drain_head": (4, "Drain head"), "tube": (5, "Stilling tube and pipe clamps"),
       "cables": (6, "Sensor cables"), "conduit": (7, "Surface cable covers and riser guard"),
       "marker": (8, "Depth marker plate")}

RHO_AL, RHO_STEEL = 2.70e-6, 7.85e-6   # kg/mm3


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str          # "made", "bought", "fixing" or "sub-assembly"
    group: str         # key in BOM (build_parts groups components by it)
    rho: float = 0.0   # density for the mass estimate (0: not estimated from volume)


def derived(p=PARAMS):
    """Dimensions quoted by the calc note, the drawings and the build plan, computed from PARAMS."""
    d = {}
    r = p["pole_od"] / 2
    d["pole_r"] = r
    d["head_x"] = -p["head_offset"]
    d["pole_face_x"] = p["pole_x"] - r                            # road side face of the pole
    d["pole_back_x"] = p["pole_x"] + r
    # V-block seat: pole axis this far behind the rear face of a plate on two V-blocks
    d["v_axis"] = p["v_apex"] + r * math.sqrt(2)
    d["plate_rear_x"] = p["pole_x"] - d["v_axis"]                 # bracket plate and FieldNode plate rear face
    d["plate_front_x"] = d["plate_rear_x"] - p["bplate"][0]
    d["v_contact"] = p["v_apex"] + r / math.sqrt(2)               # pole touches the V faces this far from the plate
    d["head_top"] = p["head_z"] + p["head_h"]
    d["arm_bot"] = d["head_top"] + p["head_plate"][2]
    d["arm_z"] = d["arm_bot"] + p["arm_sq"] / 2
    d["arm_top"] = d["arm_z"] + p["arm_sq"] / 2
    d["arm_x0"] = d["head_x"] - p["arm_tip"]                       # free end of the arm
    d["arm_x1"] = d["plate_front_x"] - 2.0                         # 2 mm short of the bracket plate
    d["arm_len"] = d["arm_x1"] - d["arm_x0"]
    d["cantilever"] = p["pole_x"] - d["head_x"]                    # pole axis to head axis
    d["band_z"] = (d["arm_z"] + 50.0, d["arm_z"] + 50.0 - p["clamp_dz"])
    d["bplate_z"] = (d["band_z"][1] - p["bplate_margin"], d["band_z"][0] + p["bplate_margin"])
    d["bplate_h"] = d["bplate_z"][1] - d["bplate_z"][0]
    d["bolt_z"] = (d["band_z"][0] + d["band_z"][1]) / 2           # anti-rotation through-bolt
    d["spacer_len"] = d["v_axis"] - r                               # plate rear to the pole at the bolt
    # brace: pins in the two clips
    ct, cw, cl, ce = p["clip"]
    d["pin_top"] = (None, d["arm_bot"] - ct - p["clip_pin"])        # x set below
    d["pin_foot"] = (d["plate_front_x"] - ct - p["clip_pin"], p["foot_z"])
    dz = d["pin_top"][1] - p["foot_z"]
    d["pin_top"] = (d["pin_foot"][0] - dz, d["pin_top"][1])          # 45 degrees
    d["brace_pins"] = math.hypot(dz, dz)
    d["brace_leg"] = dz
    d["head_z"] = p["head_z"]
    d["range_dry"] = p["head_z"]                                   # mm, lens to dry road
    d["range_600"] = p["head_z"] - 600.0
    bx0, bx1, by = p["basin"]
    d["tube_x"] = bx1 - p["tube_inset"]
    d["tube_id"] = p["tube_od"] - 2 * p["tube_wall"]
    d["tube_bot"] = p["basin_floor"] + p["tube_bot_gap"]
    d["tube_len"] = p["tube_top"] - d["tube_bot"]
    d["dh_face"] = p["tube_top"]                                   # drain head transducer face (on the tube top)
    d["dh_top"] = p["tube_top"] + p["drain_head_h"]
    d["dh_top_level"] = p["tube_top"] - p["us_blind"]              # highest level the ultrasonic reads
    d["probe_level"] = p["tube_top"] - p["probe_drop"]             # wet probe trips
    d["grate_under"] = -p["grate"][3]
    d["outlet_invert"] = p["outlet_z"] - p["outlet_bore"] / 2
    d["dh_range_max"] = p["tube_top"] - (p["basin_floor"] + 50.0)  # face to the lowest level R3 asks for
    d["node_x"] = d["plate_front_x"] - p["enc"][0] / 2
    d["node_bot"] = p["node_z"] - p["enc"][2] / 2
    d["node_top"] = p["node_z"] + p["enc"][2] / 2
    d["walk_top"] = p["curb_h"]
    d["riser_x"] = p["pole_x"]
    d["riser_top"] = p["curb_h"] + p["riser_rise"]
    gw, gd, gt = p["guard"]
    d["guard_y0"] = math.sqrt(r ** 2 - (gw / 2 - gt) ** 2)       # flange edges bear on the pole here
    d["guard_y1"] = d["guard_y0"] + gd
    d["overall_top"] = d["bplate_z"][1]
    d["head_clear_min"] = p["head_band"][0]
    d["port_x"] = d["plate_front_x"] - 55.0                        # FieldNode sensor ports, front row
    d["port_y"] = {"A": 54.0, "B": 22.0}
    d["cover_len"] = (0.0 - p["gutter_x0"]) + p["curb_h"] + (p["pole_x"] - p["guard"][0] / 2 - 1.0)
    d["brace_len"] = d["brace_pins"] + 30.0
    d["arm_x1_concept"] = p["pole_x"] + r + 40.0
    return d


# ------------------------------------------------------------------ geometry helpers
def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def bx(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def zcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def ycyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Rot(90, 0, 0) * b.Cylinder(r, h)


def xcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, h)


def hexprism(axis, x, y, z, af, h):
    b = _b3d()
    s = b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), h / 2, both=True)
    rot = {"z": b.Rot(0, 0, 0), "y": b.Rot(90, 0, 0), "x": b.Rot(0, 90, 0)}[axis]
    return b.Pos(x, y, z) * rot * s


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def bolt(axis, a, b_, c1, c2, d=6.0, head=10.0):
    """Hex bolt and nyloc nut along an axis clamping the stack from coordinate a to b_ (a < b_);
    c1, c2 are the other two coordinates (y, z for 'x'; x, z for 'y'; x, y for 'z')."""
    hl, nl = 0.6 * d, 0.9 * d
    if axis == "x":
        P = lambda u: (u, c1, c2)  # noqa: E731
        cyl = xcyl
    elif axis == "y":
        P = lambda u: (c1, u, c2)  # noqa: E731
        cyl = ycyl
    else:
        P = lambda u: (c1, c2, u)  # noqa: E731
        cyl = zcyl
    return (hexprism(axis, *P(a - hl / 2), head, hl) + cyl(*P((a + b_) / 2), d / 2 - 0.3, b_ - a)
            + hexprism(axis, *P(b_ + nl / 2), head, nl) + cyl(*P(b_ + nl + 1), d / 2 - 0.3, 2))


def cable(points, d):
    """A flexible cable along straight runs between points, with a sphere at each bend."""
    b = _b3d()
    out = None
    for (p0, p1) in zip(points[:-1], points[1:]):
        v = [p1[i] - p0[i] for i in range(3)]
        L = math.sqrt(sum(c * c for c in v))
        if L < 1e-6:
            continue
        pl = b.Plane(origin=p0, z_dir=tuple(c / L for c in v))
        seg = pl * b.Cylinder(d / 2, L, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
        out = seg if out is None else out + seg
    for pt in points[1:-1]:
        out += b.Pos(*pt) * b.Sphere(d / 2)
    return out


def cable_length(points):
    return sum(math.dist(a, c) for a, c in zip(points[:-1], points[1:]))


def _hull(pts):
    pts = sorted(set(pts))
    def cross(o, a, c):
        return (a[0] - o[0]) * (c[1] - o[1]) - (a[1] - o[1]) * (c[0] - o[0])
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def band_loop(cx, cy, r, extra, z, width, t):
    """A stainless band clamp: the convex loop round a pole (centre cx, cy, radius r) and the extra
    corner points (x, y) it is pulled across, t thick, width tall, centred at height z."""
    b = _b3d()

    def ring(rr, ex):
        rr = rr / math.cos(math.pi / 180)
        pts = [(cx + rr * math.cos(a), cy + rr * math.sin(a)) for a in [i * math.pi / 90 for i in range(180)]]
        return _hull([(round(x, 4), round(y, 4)) for x, y in pts + ex])

    inner = ring(r, [(x, y) for x, y, _ in extra])
    outer = ring(r + t, [(x + ox, y + oy) for x, y, (ox, oy) in extra])
    fo = b.Face(b.Wire.make_polygon([b.Vector(x, y, 0) for x, y in outer], close=True))
    fi = b.Face(b.Wire.make_polygon([b.Vector(x, y, 0) for x, y in inner], close=True))
    return b.Pos(0, 0, z) * b.extrude(fo - fi, width / 2, both=True)


def hat(origin, w_dir, l_dir, length, p=PARAMS):
    """Hat-section cover bent from steel strip: flanges flat on the surface, raised beveled centre
    over the cable. origin is the centre of the flat underside at one end; w_dir across the cover,
    l_dir along it; the raised side faces w_dir x l_dir... built so that h points away from the surface."""
    b = _b3d()
    W, H, t = p["hat"]
    hw = W / 2
    prof = [(-hw, 0), (-20, 0), (-8, H - t), (8, H - t), (20, 0), (hw, 0), (hw, t), (21.2, t), (9.2, H), (-9.2, H),
            (-21.2, t), (-hw, t)]
    pl = b.Plane(origin=origin, x_dir=w_dir, z_dir=l_dir)
    face = b.Face(b.Wire.make_polygon([b.Vector(x, y, 0) for x, y in prof], close=True))
    return b.extrude(pl * face, length)


# ------------------------------------------------------------------ components
def _vblock(p, xr, z):
    """FieldNode V-block on the rear face xr of a plate, centred on y = 0 at height z."""
    b = _b3d()
    w, dpt, h = p["vblock"]
    blk = bx(xr, xr + dpt, -w / 2, w / 2, z - h / 2, z + h / 2)
    a = p["v_apex"]
    tri = b.Face(b.Wire.make_polygon([b.Vector(xr + a, 0, 0), b.Vector(xr + dpt + 1, dpt + 1 - a, 0),
                                      b.Vector(xr + dpt + 1, -(dpt + 1 - a), 0)], close=True))
    v = b.Pos(0, 0, z) * b.extrude(tri, h / 2 + 1, both=True)
    blk = blk - v
    for sy in (-18.0, 18.0):  # tapped M4 holes from the plate side
        blk -= xcyl(xr + 6, sy, z, 1.65, 12.1)
    return blk


def _fieldnode(p, D, C, add):
    """FieldNode core as built to FND-BLD-001, simplified to its envelope: back plate, V-blocks,
    band clamps, enclosure and lid, ports and glands, panel bracket and panel. Faces the road (-X)."""
    b = _b3d()
    r = D["pole_r"]
    xr, xf = D["plate_rear_x"], D["plate_rear_x"] - p["fn_plate"][0]
    z0 = D["node_bot"]
    pt, pw, ph = p["fn_plate"]
    plate = bx(xf, xr, -pw / 2, pw / 2, z0 - p["fn_plate_drop"], z0 - p["fn_plate_drop"] + ph)
    plate -= bx(xf - 1, xr + 1, -50, 50, z0 + 25, z0 + 175)            # FieldNode window behind the box
    ys, (bw_, bt_) = p["fn_band_slot"], p["band"]
    for zc in p["fn_clamp_dz"]:
        plate -= bx(xf - 1, xr + 1, -ys - 1.5, -ys + 1.5, z0 + zc - 7.5, z0 + zc + 7.5)
        plate -= bx(xf - 1, xr + 1, ys - 1.5, ys + 1.5, z0 + zc - 7.5, z0 + zc + 7.5)
    vb = fuse([_vblock(p, xr, z0 + zc) for zc in p["fn_clamp_dz"]])
    bands = fuse([band_loop(p["pole_x"], 0, r, [(xf - 0.01, ys + 1.5 - bt_ - 0.2, (-bt_, bt_)), (xf - 0.01, -ys - 1.5 + bt_ + 0.2, (-bt_, -bt_))],
                            z0 + zc, bw_, bt_) for zc in p["fn_clamp_dz"]])
    ex, ey, ez = p["enc"]
    body = bx(xf - ex + 12, xf, -ey / 2, ey / 2, z0, z0 + ez)
    lid = bx(xf - ex, xf - ex + 12, -ey / 2, ey / 2, z0, z0 + ez)
    ports = fuse([zcyl(D["port_x"], y, z0 - 10, 8, 20) + zcyl(D["port_x"], y, z0 - 1.5, 11, 3) for y in D["port_y"].values()])
    glands = fuse([zcyl(xf - 27, y, z0 - 10, 8, 20) for y in (40.0, 8.0)]) + zcyl(xf - 27, -24, z0 - 5, 6, 10)
    whip = zcyl(D["port_x"], -30, z0 - 95, 5, 190)
    # panel bracket (FieldNode plate clips, posts, struts, panel clips), simplified to bars
    fx = lambda fy: xr + fy + 42.0  # noqa: E731  FieldNode frame (rear face at y = -42) to FloodGauge x
    t = math.radians(p["panel_tilt"])
    pcx, pcz = fx(-115.0), z0 + 385.0
    pts = {"post_foot": (fx(-63.0), z0 + 262.0), "post_head": (fx(-33.8), z0 + 420.4),
           "strut_foot": (fx(-62.0), z0 + 232.0), "strut_head": (fx(-164.0), z0 + 311.2)}
    bars = []
    for (a, c, yy) in (("post_foot", "post_head", 84.5), ("strut_foot", "strut_head", 78.5)):
        (xa, za), (xc, zc) = pts[a], pts[c]
        L = math.hypot(xc - xa, zc - za)
        ang = math.degrees(math.atan2(zc - za, xc - xa))
        for sy in (-1, 1):
            bars.append(b.Pos((xa + xc) / 2, sy * yy, (za + zc) / 2) * b.Rot(0, -ang, 0) * b.Box(L + 20, 3, 20))
    clips = fuse([bx(xf - 30, xf, sy * 80, sy * 83, z0 + 218, z0 + 295) for sy in (-1, 1)]
                 + [bx(xf - 3, xf, sy * 53, sy * 83, z0 + 218, z0 + 295) for sy in (-1, 1)])
    pw_, pl_, pth = p["panel"]
    panel = b.Pos(pcx, 0, pcz) * b.Rot(0, p["panel_tilt"], 0) * b.Box(pw_, pl_, pth)
    add("fn_plate", "FieldNode back plate", plate, 1, "sub-assembly", "node")
    add("fn_vblocks", "FieldNode V-blocks", vb, 1, "sub-assembly", "node")
    add("fn_bands", "FieldNode band clamps", bands, 1, "sub-assembly", "node")
    add("fn_body", "FieldNode enclosure", body + ports + glands + whip, 1, "sub-assembly", "node")
    add("fn_lid", "FieldNode lid", lid, 1, "sub-assembly", "node")
    add("fn_bracket", "FieldNode panel bracket", fuse(bars) + clips, 1, "sub-assembly", "node")
    add("fn_panel", "FieldNode 6 W panel", panel, 1, "sub-assembly", "panel")


def build_components(p=PARAMS):
    """Every component as a Comp, keyed by a short name, in build order within each group."""
    b = _b3d()
    D = derived(p)
    C = {}

    def add(key, name, shape, bom, kind, group, rho=0.0):
        C[key] = Comp(name, shape, bom, kind, group, rho)

    px, r = p["pole_x"], D["pole_r"]
    xr, xf = D["plate_rear_x"], D["plate_front_x"]
    bw_, bt_ = p["band"]

    # ---------------- 1 FieldNode core
    _fieldnode(p, D, C, add)

    # ---------------- 3 pole bracket: plate, V-blocks, bands, cleats, clips, spacer, through-bolt
    pt, pw = p["bplate"]
    z_lo, z_hi = D["bplate_z"]
    plate = bx(xf, xr, -pw / 2, pw / 2, z_lo, z_hi)
    ys, sw, sh = p["band_slot"]
    for zb in D["band_z"]:
        for sy in (-1, 1):
            plate -= bx(xf - 1, xr + 1, sy * ys - sw / 2, sy * ys + sw / 2, zb - sh / 2, zb + sh / 2)
        for sy in (-18.0, 18.0):
            plate -= xcyl(xr - pt / 2, sy, zb, 2.25, pt + 2)
    ww, wh = p["bplate_window"]
    wz = (D["bolt_z"] + p["foot_z"] + 25) / 2, (D["bolt_z"] + D["arm_z"] - 30) / 2
    for zc in wz:
        plate -= bx(xf - 1, xr + 1, -ww / 2, ww / 2, zc - wh / 2, zc + wh / 2)
    for sy in (-1, 1):                                            # arm cleat bolts
        for dz in (-18.0, 18.0):
            plate -= xcyl(xr - pt / 2, sy * 38.0, D["arm_z"] + dz, 3.3, pt + 2)
    for dz in (-17.0, 17.0):                                      # foot clip bolts
        plate -= xcyl(xr - pt / 2, 0, p["foot_z"] + dz, 3.3, pt + 2)
    plate -= xcyl(xr - pt / 2, 0, D["bolt_z"], 4.25, pt + 2)       # through-bolt
    add("bplate", "Pole bracket plate", plate, 3, "made", "arm", RHO_AL)
    add("vblocks", "V-blocks (2)", fuse([_vblock(p, xr, zb) for zb in D["band_z"]]), 3, "made", "arm", RHO_AL)
    add("bands", "Band clamps (2)", fuse([band_loop(px, 0, r, [(xf - 0.01, ys + sw / 2 - bt_ - 0.2, (-bt_, bt_)), (xf - 0.01, -ys - sw / 2 + bt_ + 0.2, (-bt_, -bt_))],
                                                   zb, bw_, bt_) for zb in D["band_z"]]), 3, "bought", "arm", RHO_STEEL)
    vscrews = fuse([xcyl(xf + 6, sy, zb, 2.0, 12) + xcyl(xf + 1.2, sy, zb, 4.0, 2.4) for zb in D["band_z"] for sy in (-18.0, 18.0)])
    # arm cleats: 30 x 30 x 3 angle; one leg on the plate front, the other along the arm side
    a_, at = p["angle"]
    az, cl = D["arm_z"], p["cleat_len"]
    hw = p["arm_sq"] / 2
    cleats = []
    for sy in (-1, 1):
        y0 = sy * hw
        cleats.append(bx(xf - at, xf, y0, y0 + sy * a_, az - cl / 2, az + cl / 2)
                      + bx(xf - a_, xf, y0, y0 + sy * at, az - cl / 2, az + cl / 2))
    cleats = fuse(cleats)
    for sy in (-1, 1):
        for dz in (-18.0, 18.0):
            cleats -= xcyl(xf - at / 2, sy * 38.0, az + dz, 3.3, at + 2)
        for dz in (-10.0, 10.0):
            cleats -= ycyl(xf - 15.0, sy * (hw + at / 2), az + dz, 3.3, at + 2)
    add("cleats", "Arm cleats (2)", cleats, 3, "made", "arm", RHO_AL)
    cleat_bolts = fuse([bolt("x", xf - at, xr, sy * 38.0, az + dz) for sy in (-1, 1) for dz in (-18.0, 18.0)])
    arm_cleat_bolts = fuse([bolt("y", -hw - at, hw + at, xf - 15.0, az + dz) for dz in (-10.0, 10.0)])
    # brace clips: U folded from 3 mm strip, base on the arm underside (top clip) or on the plate (foot clip)
    ct, ci, clen, ce = p["clip"]
    (xt, zt), (xft, zft) = D["pin_top"], D["pin_foot"]
    top_clip = (bx(xt - clen / 2, xt + clen / 2, -ci / 2 - ct, ci / 2 + ct, D["arm_bot"] - ct, D["arm_bot"])
                + bx(xt - clen / 2, xt + clen / 2, ci / 2, ci / 2 + ct, D["arm_bot"] - ce, D["arm_bot"])
                + bx(xt - clen / 2, xt + clen / 2, -ci / 2 - ct, -ci / 2, D["arm_bot"] - ce, D["arm_bot"]))
    foot_clip = (bx(xf - ct, xf, -ci / 2 - ct, ci / 2 + ct, zft - clen / 2, zft + clen / 2)
                 + bx(xf - ce, xf, ci / 2, ci / 2 + ct, zft - clen / 2, zft + clen / 2)
                 + bx(xf - ce, xf, -ci / 2 - ct, -ci / 2, zft - clen / 2, zft + clen / 2))
    top_clip -= ycyl(xt, 0, zt, 3.3, ci + 2 * ct + 2)
    foot_clip -= ycyl(xft, 0, zft, 3.3, ci + 2 * ct + 2)
    for dx in (-17.0, 17.0):
        top_clip -= zcyl(xt + dx, 0, D["arm_bot"] - ct / 2, 3.3, ct + 2)
        foot_clip -= xcyl(xf - ct / 2, 0, zft + dx, 3.3, ct + 2)
    add("top_clip", "Brace clip under the arm", top_clip, 3, "made", "arm", RHO_AL)
    add("foot_clip", "Brace clip on the bracket plate", foot_clip, 3, "made", "arm", RHO_AL)
    # clip fixings: button-head screws from inside the clip; nyloc nuts on the arm top (with crush sleeves) or behind the plate
    clip_bolts = fuse([zcyl(xt + dx, 0, D["arm_bot"] - ct - 1.65, 5.5, 3.3) + zcyl(xt + dx, 0, D["arm_z"], 2.7, p["arm_sq"] + 2 * ct)
                       + hexprism("z", xt + dx, 0, D["arm_top"] + 2.7, 10, 5.4) for dx in (-17.0, 17.0)]
                      + [xcyl(xf - ct - 1.65, 0, zft + dx, 5.5, 3.3) + xcyl(xr - pt / 2 - ct / 2, 0, zft + dx, 2.7, pt + ct + 4)
                         + hexprism("x", xr + 2.7, 0, zft + dx, 10, 5.4) for dx in (-17.0, 17.0)])
    # crush sleeves inside the arm at every through-bolt
    sleeves = fuse([ycyl(xf - 15.0, 0, az + dz, 5.0, p["arm_sq"] - 2 * p["arm_wall"]) - ycyl(xf - 15.0, 0, az + dz, 3.2, p["arm_sq"])
                    for dz in (-10.0, 10.0)]
                   + [zcyl(x_, 0, az, 5.0, p["arm_sq"] - 2 * p["arm_wall"]) - zcyl(x_, 0, az, 3.2, p["arm_sq"])
                      for x_ in (xt - 17.0, xt + 17.0, D["head_x"] - p["head_bolt_dx"], D["head_x"] + p["head_bolt_dx"])])
    # arm
    arm = bx(D["arm_x0"], D["arm_x1"], -hw, hw, D["arm_bot"], D["arm_top"])
    arm -= bx(D["arm_x0"] - 1, D["arm_x1"] + 1, -hw + p["arm_wall"], hw - p["arm_wall"], D["arm_bot"] + p["arm_wall"], D["arm_top"] - p["arm_wall"])
    for dz in (-10.0, 10.0):
        arm -= ycyl(xf - 15.0, 0, az + dz, 3.3, p["arm_sq"] + 2)
    for x_ in (xt - 17.0, xt + 17.0, D["head_x"] - p["head_bolt_dx"], D["head_x"] + p["head_bolt_dx"]):
        arm -= zcyl(x_, 0, az, 3.3, p["arm_sq"] + 2)
    add("arm", "Sensor arm", arm, 3, "made", "arm", RHO_AL)
    # knee brace, 25 x 25 x 2 tube between the pins, ends cut square to fit inside the clip ears
    bs, bwall = p["brace_sq"], p["brace_wall"]
    L = D["brace_pins"]
    over = 12.0                                                  # tube end beyond each pin
    mid = ((xt + xft) / 2, (zt + zft) / 2)
    brace = b.Pos(mid[0], 0, mid[1]) * b.Rot(0, -45, 0) * (b.Box(bs, bs, L + 2 * over) - b.Box(bs - 2 * bwall, bs - 2 * bwall, L + 2 * over + 2))
    for (xx, zz) in ((xt, zt), (xft, zft)):
        brace -= ycyl(xx, 0, zz, 3.3, bs + 2)
    add("brace", "Knee brace", brace, 3, "made", "arm", RHO_AL)
    pins = fuse([bolt("y", -ci / 2 - ct, ci / 2 + ct, xx, zz) for (xx, zz) in ((xt, zt), (xft, zft))])
    pin_sleeves = fuse([ycyl(xx, 0, zz, 4.5, bs - 2 * bwall) - ycyl(xx, 0, zz, 3.2, bs) for (xx, zz) in ((xt, zt), (xft, zft))])
    # through-bolt across the street: bracket plate, spacer, both pole walls
    zb = D["bolt_z"]
    spacer = xcyl(xr + D["spacer_len"] / 2, 0, zb, p["spacer_d"] / 2, D["spacer_len"]) - xcyl(xr + D["spacer_len"] / 2, 0, zb, 4.25, D["spacer_len"] + 2)
    add("spacer", "Through-bolt spacer", spacer, 3, "made", "arm", RHO_AL)
    tbolt = (hexprism("x", xf - 2.65, 0, zb, 13, 5.3) + xcyl(xf + p["bolt_l"] / 2, 0, zb, 3.7, p["bolt_l"])
             + hexprism("x", D["pole_back_x"] + 1.6 + 3.4, 0, zb, 13, 6.8) + xcyl(D["pole_back_x"] + 0.8, 0, zb, 8, 1.6))
    add("through_bolt", "M8 anti-rotation through-bolt", tbolt, 3, "fixing", "arm", RHO_STEEL)
    # head plate under the arm
    hl_, hw_, ht_ = p["head_plate"]
    hx = D["head_x"]
    hplate = bx(hx - hl_ / 2, hx + hl_ / 2, -hw_ / 2, hw_ / 2, D["head_top"], D["arm_bot"])
    for dx in (-p["head_bolt_dx"], p["head_bolt_dx"]):
        hplate -= zcyl(hx + dx, 0, D["head_top"] + ht_ / 2, 3.3, ht_ + 2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            hplate -= zcyl(hx + sx * 18, sy * 27, D["head_top"] + ht_ / 2, 2.25, ht_ + 2)
    add("head_plate", "Head plate", hplate, 3, "made", "arm", RHO_AL)
    head_bolts = fuse([zcyl(hx + dx, 0, D["head_top"] - 1.65, 5.5, 3.3) + zcyl(hx + dx, 0, az, 2.7, p["arm_sq"] + ht_ + 2)
                       + hexprism("z", hx + dx, 0, D["arm_top"] + 2.7, 10, 5.4) for dx in (-p["head_bolt_dx"], p["head_bolt_dx"])])
    head_screws = fuse([zcyl(hx + sx * 18, sy * 27, D["arm_bot"] - 6, 1.9, 12) + zcyl(hx + sx * 18, sy * 27, D["arm_bot"] + 1.1, 4, 2.2)
                        for sx in (-1, 1) for sy in (-1, 1)])
    add("fixings", "Bracket bolts, nuts and sleeves", fuse([vscrews, cleat_bolts, arm_cleat_bolts, clip_bolts, sleeves, head_bolts]),
        3, "fixing", "arm", RHO_STEEL)
    add("pins", "Brace pins and sleeves", pins + pin_sleeves, 3, "fixing", "arm", RHO_STEEL)

    # ---------------- 2 street radar head
    hz = p["head_z"]
    housing = zcyl(hx, 0, hz + p["lens_t"] + (p["head_h"] - p["lens_t"]) / 2, p["head_d"] / 2, p["head_h"] - p["lens_t"])
    housing -= zcyl(hx, 0, hz + p["lens_t"] + 1.5, p["lens_window"] / 2, 3.2)
    lens = zcyl(hx, 0, hz + p["lens_t"] / 2, p["lens_d"] / 2, p["lens_t"])
    for sx in (-1, 1):
        for sy in (-1, 1):   # tapped holes in the housing's lid bosses for the M4 screws
            housing -= zcyl(hx + sx * 18, sy * 27, D["head_top"] - 5, 1.9, 10.02)
    gd, gl = p["gland"]
    zg = hz + p["lens_t"] + (p["head_h"] - p["lens_t"]) / 2
    gland = xcyl(hx + p["head_d"] / 2 + gl / 2, 0, zg, gd / 2, gl)
    add("head_housing", "Radar head housing", housing + gland, 2, "bought", "street_head")
    add("head_screws", "Head housing screws (4)", head_screws, 2, "fixing", "street_head", RHO_STEEL)
    add("lens", "PTFE lens disc", lens, 2, "made", "street_head")

    # ---------------- 8 depth marker plate (2 mm), on the road face of the pole
    mt, mw, mh = p["marker"]
    mz0 = p["marker_z0"]
    marker = bx(D["pole_face_x"] - mt, D["pole_face_x"], -mw / 2, mw / 2, mz0, mz0 + mh)
    add("marker", "Depth marker plate", marker, 8, "made", "marker", RHO_AL)

    # ---------------- 7 riser guard: U channel, open side on the pole, standing on the sidewalk
    gw, gdp, gt = p["guard"]
    y0, y1 = D["guard_y0"], D["guard_y1"]
    zg0, zg1 = p["curb_h"], D["riser_top"]
    guard = (bx(px - gw / 2, px - gw / 2 + gt, y0, y1, zg0, zg1) + bx(px + gw / 2 - gt, px + gw / 2, y0, y1, zg0, zg1)
             + bx(px - gw / 2, px + gw / 2, y1 - gt, y1, zg0, zg1))
    cy = p["cover_y"]
    guard -= bx(px - gw / 2 - 1, px - gw / 2 + gt + 1, cy - 11, y1 + 1, zg0 - 1, zg0 + 20)      # cable notch at the foot
    add("guard", "Riser guard", guard, 7, "made", "conduit", RHO_STEEL)
    mb = []
    for zz in p["marker_bands_z"]:
        mb.append(band_loop(px, 0, r, [(D["pole_face_x"] - mt, mw / 2, (-bt_, bt_)), (D["pole_face_x"] - mt, -mw / 2, (-bt_, -bt_)),
                                       (D["pole_face_x"], mw / 2, (0, bt_)), (D["pole_face_x"], -mw / 2, (0, -bt_)),
                                       (px - gw / 2, y1, (-bt_, bt_)), (px + gw / 2, y1, (bt_, bt_))], zz, bw_, bt_))
    add("marker_bands", "Marker and guard band clamps (2)", fuse(mb), 8, "bought", "marker", RHO_STEEL)

    # ---------------- 7 surface cable covers (hat sections) and their anchors
    W, H, t = p["hat"]
    gx0 = p["gutter_x0"]
    gut = hat((gx0, cy, 0), (0, 1, 0), (1, 0, 0), -H - gx0)                       # to the curb cover's face
    gut += fuse([bx(-H, -4, cy + s * 21, cy + s * (W / 2), 0, t) for s in (-1, 1)])  # flanges to the tabs
    gut += fuse([bx(-4, -2, cy + s * 22, cy + s * (W / 2), 0, 30) for s in (-1, 1)])  # tabs up the curb face
    for s in (-1, 1):
        gut -= xcyl(-3, cy + s * 32, 18, 4.5, 4)
    add("gutter_cover", "Gutter cover", gut, 7, "made", "conduit", RHO_STEEL)
    curb = hat((0, cy, 0), (0, 1, 0), (0, 0, 1), p["curb_h"] + H)
    curb -= fuse([bx(-3, 1, cy + s * 20.5, cy + s * (W / 2 + 1), p["curb_h"], p["curb_h"] + H + 1) for s in (-1, 1)])
    curb -= bx(-H - 1, -H + t + 1, cy - 10, cy + 10, -1, H)                         # cable notch at the foot
    for s in (-1, 1):
        for zz in (18.0, 139.0):
            curb -= xcyl(-1, cy + s * 32, zz, 4.5, 4)
    add("curb_cover", "Curb cover", curb, 7, "made", "conduit", RHO_STEEL)
    xw1 = px - gw / 2 - 1.0
    walk = hat((0, cy, p["curb_h"]), (0, 1, 0), (1, 0, 0), xw1)
    walk += fuse([bx(-4, 0, cy + s * 22, cy + s * (W / 2), p["curb_h"], p["curb_h"] + t) for s in (-1, 1)])
    walk += fuse([bx(-4, -2, cy + s * 22, cy + s * (W / 2), p["curb_h"] - 22, p["curb_h"] + t) for s in (-1, 1)])
    for s in (-1, 1):
        walk -= xcyl(-3, cy + s * 32, 139.0, 4.5, 4)
        for xx in (110.0, 330.0):
            walk -= zcyl(xx, cy + s * 32, p["curb_h"] + t / 2, 4.5, t + 2)
    add("walk_cover", "Sidewalk cover", walk, 7, "made", "conduit", RHO_STEEL)
    anchors = fuse([xcyl(-4 - (4 if zz > 100 else 2) - 3, cy + s * 32, zz, 6.5, 6) for s in (-1, 1) for zz in (18.0, 139.0)]
                   + [zcyl(xx, cy + s * 32, p["curb_h"] + t + 3, 6.5, 6) for s in (-1, 1) for xx in (110.0, 330.0)])
    add("anchors", "Masonry anchors and nuts (8)", anchors, 7, "fixing", "conduit")

    # ---------------- 5 stilling tube and its stand-off pipe clamps
    tx = D["tube_x"]
    tube = zcyl(tx, 0, (p["tube_top"] + D["tube_bot"]) / 2, p["tube_od"] / 2, D["tube_len"])
    tube -= zcyl(tx, 0, (p["tube_top"] + D["tube_bot"]) / 2, D["tube_id"] / 2, D["tube_len"] + 2)
    sw_, sl_ = p["slot"]
    for k in range(p["slot_rows"]):
        zc = D["tube_bot"] + p["slot_first"] + k * p["slot_pitch"]
        for j in range(p["slots_per_row"]):
            a = 45.0 + 90.0 * j
            tube -= b.Pos(tx, 0, zc) * b.Rot(0, 0, a) * b.Pos(p["tube_od"] / 2, 0, 0) * b.Box(10, sw_, sl_)
    for sy in (-1, 1):         # two pilot holes for the screws that hold the drain head socket
        tube -= ycyl(tx, sy * (p["tube_od"] / 2 - 1.5), p["tube_top"] - 20, 1.75, 6)
    add("tube", "Stilling tube", tube, 5, "made", "tube")
    bx1 = p["basin"][1]
    pct, pcw = p["pclamp"]
    wd, wt = p["wall_plate"]
    clamps = []
    for zz in p["bracket_z"]:
        ring = zcyl(tx, 0, zz, p["tube_od"] / 2 + pct, pcw) - zcyl(tx, 0, zz, p["tube_od"] / 2, pcw + 2)
        x_ring = tx + p["tube_od"] / 2 + pct
        rod = xcyl((x_ring + bx1 - wt) / 2, 0, zz, 4.0, bx1 - wt - x_ring + 0.02)
        boss = xcyl(x_ring + 4, 0, zz, 7, 8)
        wall_plate = xcyl(bx1 - wt / 2, 0, zz, wd / 2, wt)
        clamps.append(ring + rod + boss + wall_plate)
    add("pclamps", "Stand-off pipe clamps (2)", fuse(clamps), 5, "bought", "tube")

    # ---------------- 4 drain head with its 75 mm socket
    so, sl = p["socket"]
    tt = p["tube_top"]
    dh = zcyl(tx, 0, tt + p["drain_head_h"] / 2, p["drain_head_d"] / 2, p["drain_head_h"])
    dh += zcyl(tx, 0, D["dh_top"] + 7.5, gd / 2, 15)                                  # cable gland on top
    sock = zcyl(tx, 0, tt - sl / 2, so / 2, sl) - zcyl(tx, 0, tt - sl / 2, p["tube_od"] / 2, sl + 2)
    probes = fuse([zcyl(tx + sx * 18, 0, tt - p["probe_drop"] / 2, 1.5, p["probe_drop"]) for sx in (-1, 1)])
    add("drain_head", "Drain head", dh + sock + probes, 4, "made", "drain_head")

    # ---------------- 6 sensor cables (flexible, tied along their runs)
    c = p["cable_d"]
    xg = hx + p["head_d"] / 2 + gl
    ya = -hw - 2 - c / 2                    # along the arm's side
    xs = 340.0                              # where the street cable leaves the arm
    zr = D["band_z"][1] - 60.0
    xb = D["pole_back_x"] + c / 2 + 3
    zs, zd = D["node_bot"] - 140.0, D["node_bot"] - 100.0
    street = [(xg, 0, zg), (xg + 25, 0, zg), (xg + 25, ya, zg), (xg + 25, ya, az), (xs, ya, az), (xs, ya, zr),
              (xs, -47.0, zr), (px, -47.0, zr), (px, -47.0, zs), (370.0, -47.0, zs), (370.0, D["port_y"]["A"], zs), (D["port_x"], D["port_y"]["A"], zs),
              (D["port_x"], D["port_y"]["A"], D["node_bot"] - 20)]
    zc_ = 7.0
    zw = p["curb_h"] + 7.0
    xcab = -8.0
    drain = [(tx, 0, D["dh_top"] + 15), (tx, 0, -100), (p["cable_exit_x"], 0, -100), (p["cable_exit_x"], cy, -100),
             (p["cable_exit_x"], cy, zc_), (xcab, cy, zc_), (xcab, cy, zw), (px, cy, zw), (px, cy, D["riser_top"] + 60),
             (px, r + 8.0, D["riser_top"] + 110), (px, r + 8.0, zd), (D["port_x"], r + 8.0, zd), (D["port_x"], D["port_y"]["B"], zd),
             (D["port_x"], D["port_y"]["B"], D["node_bot"] - 20)]
    add("street_cable", "Street head cable, 3 m", cable(street, c), 6, "bought", "cables")
    add("drain_cable", "Drain head cable, 5 m", cable(drain, c), 6, "bought", "cables")
    C["_runs"] = {"street": street, "drain": drain}
    return C


def cable_runs(p=PARAMS):
    """Cable centre-line lengths (mm) from the model, for the calculation note."""
    C = build_components(p)
    return {k: cable_length(v) for k, v in C["_runs"].items()}


def build_parts(p=PARAMS):
    """Return {BOM key: solid} for the kit parts (keys in BOM), for the concept media and the drawing."""
    C = {k: v for k, v in build_components(p).items() if not k.startswith("_")}
    out = {}
    for k, c in C.items():
        out[c.group] = c.shape if c.group not in out else out[c.group] + c.shape
    return out


def bands(p=PARAMS):
    """Amber and red bands on the marker plate (coloured faces of item 8). Amber shows from the plate bottom."""
    D = derived(p)
    a, r_, top = p["bands"]
    a = max(a, p["marker_z0"])
    x = D["pole_face_x"] - p["marker"][0] - 0.5
    mw = p["marker"][1]
    return {"amber": box(x, 0, (a + r_) / 2, 1.0, mw, r_ - a),
            "red": box(x, 0, (r_ + top) / 2, 1.0, mw, top - r_)}


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
    pole -= Pos(p["pole_x"], 0, D["bolt_z"]) * Rot(0, 90, 0) * Cylinder(4.25, p["pole_od"] + 2)     # through-bolt hole
    sign = Pos(p["pole_x"], 0, cs + p["pole_h"] - 120) * Box(20, 760, 200)
    out = {"road": road, "walk": walk, "basin": basin, "grate": grate, "water": water, "pole": pole, "sign": sign}
    if basin_half:
        keep = Pos(0, 5000, 0) * Box(20000, 10000, 20000)
        out = {k: (v & keep) for k, v in out.items()}
    return out


def assembly(p=PARAMS, with_site=False):
    from build123d import Compound
    C = build_components(p)
    shapes = [c.shape for k, c in C.items() if not k.startswith("_")] + list(bands(p).values())
    if with_site:
        s = site(p)
        shapes += [s["pole"], s["basin"], s["grate"]]
    return Compound(children=shapes)


def pole_kit(p=PARAMS):
    from build123d import Compound
    C = build_components(p)
    return Compound(children=[c.shape for k, c in C.items() if not k.startswith("_") and c.group in ("node", "panel", "street_head", "arm", "marker")])


def drain_kit(p=PARAMS):
    from build123d import Compound
    C = build_components(p)
    return Compound(children=[C[k].shape for k in ("drain_head", "tube", "pclamps")])


def site_compound(p=PARAMS):
    from build123d import Compound
    s = site(p)
    return Compound(children=[s[k] for k in ("road", "walk", "basin", "grate", "pole")])


def masses(p=PARAMS):
    """Estimated mass (kg) of each made aluminium or steel component, from the model volume."""
    C = build_components(p)
    return {k: c.shape.volume * c.rho for k, c in C.items() if not k.startswith("_") and c.rho}


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch, and pairs that must stay apart by at least a clearance (mm). Returns
    rows of (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    st = site(p)
    S = lambda k: C[k].shape  # noqa: E731
    pole, grate, road, walk, basin, sign = st["pole"], st["grate"], st["road"], st["walk"], st["basin"], st["sign"]
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    # pole bracket
    chk("Bracket V-blocks on the bracket plate", S("vblocks"), S("bplate"), "touch")
    chk("Bracket V-blocks on the pole (both V faces)", S("vblocks"), pole, "touch")
    chk("Bracket band clamps on the pole", S("bands"), pole, "touch")
    chk("Bracket band clamps through the plate slots and across its front", S("bands"), S("bplate"), "touch")
    chk("Bracket band clamps clear of the V-blocks", S("bands"), S("vblocks"), 1.0)
    chk("Bracket plate clear of the pole", S("bplate"), pole, 15.0)
    chk("Arm cleats on the bracket plate", S("cleats"), S("bplate"), "touch")
    chk("Arm between the cleats", S("arm"), S("cleats"), "touch")
    chk("Arm end short of the bracket plate", S("arm"), S("bplate"), 1.5)
    chk("Arm clear of the pole", S("arm"), pole, 20.0)
    chk("Arm cleats clear of the band clamps", S("cleats"), S("bands"), 5.0)
    chk("Top brace clip under the arm", S("top_clip"), S("arm"), "touch")
    chk("Foot brace clip on the bracket plate", S("foot_clip"), S("bplate"), "touch")
    chk("Foot brace clip clear of the band clamps", S("foot_clip"), S("bands"), 5.0)
    chk("Knee brace clear of the top clip (inside its ears)", S("brace"), S("top_clip"), 0.2)
    chk("Knee brace clear of the foot clip (inside its ears)", S("brace"), S("foot_clip"), 0.2)
    chk("Knee brace clear of the arm", S("brace"), S("arm"), 1.0)
    chk("Knee brace clear of the bracket plate", S("brace"), S("bplate"), 1.0)
    chk("Spacer against the bracket plate", S("spacer"), S("bplate"), "touch")
    chk("Spacer against the pole", S("spacer"), pole, "touch")
    chk("Through-bolt clear of the band clamps", S("through_bolt"), S("bands"), 20.0)
    chk("Through-bolt clear of the V-blocks", S("through_bolt"), S("vblocks"), 20.0)
    chk("Bracket plate clear of the pole-top sign", S("bplate"), sign, 20.0)
    chk("Bracket fixings clear of the knee brace", S("fixings"), S("brace"), 0.5)
    chk("Bracket fixings under the band clamps (flush screw heads)", S("fixings"), S("bands"), 0.0)
    chk("Brace pins through the knee brace", S("pins"), S("brace"), "touch")
    chk("Brace pins through the clip ears", S("pins"), S("top_clip") + S("foot_clip"), "touch")
    chk("Bracket fixings clear of the pole", S("fixings"), pole, 1.0)
    chk("Through-bolt through the pole holes", S("through_bolt"), pole, 0.0)
    chk("Head bolts clear of the radar head housing", S("fixings"), S("head_housing"), 5.0)
    # head
    chk("Head plate under the arm", S("head_plate"), S("arm"), "touch")
    chk("Radar head housing under the head plate", S("head_housing"), S("head_plate"), "touch")
    chk("Lens disc on the housing", S("lens"), S("head_housing"), "touch")
    chk("Housing screws into the housing lid bosses", S("head_screws"), S("head_housing"), "touch")
    chk("Radar head clear of the knee brace", S("head_housing"), S("brace"), 100.0)
    # FieldNode
    chk("FieldNode V-blocks on the pole", S("fn_vblocks"), pole, "touch")
    chk("FieldNode V-blocks on its back plate", S("fn_vblocks"), S("fn_plate"), "touch")
    chk("FieldNode band clamps on the pole", S("fn_bands"), pole, "touch")
    chk("FieldNode band clamps through its plate slots", S("fn_bands"), S("fn_plate"), "touch")
    chk("FieldNode band clamps clear of its V-blocks", S("fn_bands"), S("fn_vblocks"), 1.0)
    chk("FieldNode enclosure on its back plate", S("fn_body"), S("fn_plate"), "touch")
    chk("FieldNode panel clear of the knee brace and bracket", S("fn_panel"), S("brace") + S("bplate") + S("foot_clip"), 300.0)
    # marker and guard
    chk("Marker plate on the pole", S("marker"), pole, "touch")
    chk("Marker plate clear of the sidewalk cover", S("marker"), S("walk_cover"), 0.5)
    chk("Marker band clamps on the pole", S("marker_bands"), pole, "touch")
    chk("Marker band clamps across the marker plate", S("marker_bands"), S("marker"), "touch")
    chk("Marker band clamps across the riser guard", S("marker_bands"), S("guard"), "touch")
    chk("Riser guard flange edges on the pole", S("guard"), pole, "touch")
    chk("Riser guard standing on the sidewalk", S("guard"), walk, "touch")
    chk("Riser guard clear of the marker plate", S("guard"), S("marker"), 5.0)
    chk("Riser guard clear of the sidewalk cover end", S("guard"), S("walk_cover"), 0.5)
    # covers
    chk("Gutter cover on the road and grate", S("gutter_cover"), road + grate, "touch")
    chk("Gutter cover tabs on the curb cover", S("gutter_cover"), S("curb_cover"), "touch")
    chk("Curb cover on the curb face", S("curb_cover"), walk, "touch")
    chk("Sidewalk cover on the sidewalk", S("walk_cover"), walk, "touch")
    chk("Sidewalk cover tabs on the curb cover", S("walk_cover"), S("curb_cover"), "touch")
    chk("Sidewalk cover clear of the pole", S("walk_cover"), pole, 5.0)
    chk("Gutter cover clear of the sidewalk cover", S("gutter_cover"), S("walk_cover"), 50.0)
    chk("Anchors clear of the cable", S("anchors"), S("drain_cable"), 5.0)
    # drain kit
    chk("Drain head socket over the tube top", S("drain_head"), S("tube"), "touch")
    chk("Pipe clamps round the tube", S("pclamps"), S("tube"), "touch")
    chk("Pipe clamp wall plates on the basin wall", S("pclamps"), basin, "touch")
    chk("Drain head clear of the road slab", S("drain_head"), road, 5.0)
    chk("Drain head clear of the basin wall", S("drain_head"), basin, 20.0)
    chk("Drain head clear of the grate", S("drain_head"), grate, 100.0)
    # cables
    for k, nm in (("street_cable", "Street cable"), ("drain_cable", "Drain cable")):
        for o in ("arm", "bplate", "brace", "cleats", "top_clip", "foot_clip", "head_plate", "vblocks", "bands", "through_bolt",
                  "fn_plate", "fn_lid", "fn_panel", "fn_bracket", "marker", "fixings"):
            chk(f"{nm} clear of the {C[o].name.lower()}", S(k), S(o), 1.0)
        chk(f"{nm} clear of the pole", S(k), pole, 1.0)
    chk("Street cable clear of the drain cable", S("street_cable"), S("drain_cable"), 2.0)
    chk("Drain cable clear of the road slab", S("drain_cable"), road, 1.0)
    chk("Drain cable through the grate opening", S("drain_cable"), grate, 2.0)
    chk("Drain cable inside the gutter cover", S("drain_cable"), S("gutter_cover"), 0.5)
    chk("Drain cable inside the curb cover", S("drain_cable"), S("curb_cover"), 0.5)
    chk("Drain cable inside the sidewalk cover", S("drain_cable"), S("walk_cover"), 0.5)
    chk("Drain cable inside the riser guard", S("drain_cable"), S("guard"), 0.5)
    chk("Drain cable on the sidewalk under its cover", S("drain_cable"), walk, 1.0)
    chk("Drain cable clear of the marker band clamps", S("drain_cable"), S("marker_bands"), 1.0)
    chk("Drain cable clear of the FieldNode band clamps", S("drain_cable"), S("fn_bands"), 1.0)
    chk("Street cable clear of the FieldNode band clamps", S("street_cable"), S("fn_bands"), 1.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:64s} overlap {v:9.3f} mm3  gap {gp:8.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    D = derived()
    outs = {"floodgauge-assembly": assembly(), "floodgauge-pole-kit": pole_kit(),
            "floodgauge-drain-kit": drain_kit(), "floodgauge-site": site_compound()}
    for name, shape in outs.items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"head {PARAMS['head_offset']:.0f} mm past the curb face, lens {PARAMS['head_z']:.0f} mm above the road; "
          f"arm {D['arm_len']:.0f} mm at {D['arm_z']:.0f}; bracket plate {D['bplate_h']:.0f} mm tall; brace pins {D['brace_pins']:.1f} mm apart; "
          f"tube {D['tube_len']:.0f} mm long, ID {D['tube_id']:.0f} mm")
    for k, v in cable_runs().items():
        print(f"cable run {k}: {v:.0f} mm")
    for k, v in masses().items():
        print(f"mass {k}: {v:.3f} kg")
    print_checks()
