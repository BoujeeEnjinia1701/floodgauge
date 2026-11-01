"""FloodGauge parametric model (build123d), kit 1.9 interface, detail level D3 for every option.

Run from the repo root:  python .kit/cad_check.py --export  (fidelity check and STEP per part and assembly)
                         python cad/src/model.py            (exports STL of the chosen option and prints the checks)
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
from pathlib import Path
import math
import sys

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
from flg_parts import fasten, orient, csk_cutter, snake_eye_nut, sleeve, ISO  # noqa: E402

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
    "loop_a": 100.0, "loop_b": 60.0, "loop_dx": 62.0, "loop_top": -100.0,  # drain cable 0.5 m slack loop (decided 2026-10-02): half width, half height, offset west of the tube axis, top height
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


# ------------------------------------------------------------------ components (kit 1.9)
EXPLODE = {"node": (-150, -500, 150), "panel": (-150, -500, 350), "street_head": (-250, -300, 350), "arm": (0, 0, 250),
           "drain_head": (-400, -500, 1650), "tube": (-400, -500, 1400), "cables": (250, -900, 0),
           "conduit": (300, -600, 600), "marker": (-300, -350, 0), "context": (0, 0, 0)}
GREEN = "#1F6B3A"       # PCB colour


def _vblock(p, xr, z):
    """V-block on the rear face xr of a plate, centred on y = 0 at height z (FieldNode pattern), with its
    two tapped M4 holes (drawn at the nominal 4 mm)."""
    b = _b3d()
    w, dpt, h = p["vblock"]
    blk = bx(xr, xr + dpt, -w / 2, w / 2, z - h / 2, z + h / 2)
    a = p["v_apex"]
    tri = b.Face(b.Wire.make_polygon([b.Vector(xr + a, 0, 0), b.Vector(xr + dpt + 1, dpt + 1 - a, 0),
                                      b.Vector(xr + dpt + 1, -(dpt + 1 - a), 0)], close=True))
    v = b.Pos(0, 0, z) * b.extrude(tri, h / 2 + 1, both=True)
    blk = cp.break_edges(blk - v, 0.5)
    for sy in (-18.0, 18.0):
        blk -= xcyl(xr + 6, sy, z, 2.0, 12.1)
    return blk


class _Out(list):
    """Part list with helpers that stamp the group, explode offset and legacy key on every part."""

    def add(self, key, name, shape, material, kind, bom, group, color=None):
        q = part(name, shape, material, kind=kind, bom=bom, group=group, explode=EXPLODE.get(group, (0, 0, 0)), color=color)
        q["key"] = key
        self.append(q)
        return q

    def fast(self, key, d, grip, origin, outward, group, bom, **kw):
        for q in fasten(d, grip, origin, outward, bom=bom, group=group, key=key, explode=EXPLODE.get(group, (0, 0, 0)), **kw):
            self.append(q)


def _fieldnode(p, D, o):
    """FieldNode core as built to FND-BLD-001, at envelope level but with real wall thickness: back plate, two V-blocks
    and two band clamps, hollow IP65 enclosure with lid, cell, board and connectors, panel bracket and 6 W panel.
    Faces the road (-X). Interior items are envelope placeholders sized from the FieldNode BOM, not FieldNode's own CAD."""
    b = _b3d()
    r = D["pole_r"]
    xr, xf = D["plate_rear_x"], D["plate_rear_x"] - p["fn_plate"][0]
    z0 = D["node_bot"]
    pt, pw, ph = p["fn_plate"]
    plate = cp.break_edges(bx(xf, xr, -pw / 2, pw / 2, z0 - p["fn_plate_drop"], z0 - p["fn_plate_drop"] + ph), 0.6)
    plate -= bx(xf - 1, xr + 1, -50, 50, z0 + 25, z0 + 175)            # window behind the box
    ys, (bw_, bt_) = p["fn_band_slot"], p["band"]
    for zc in p["fn_clamp_dz"]:
        plate -= bx(xf - 1, xr + 1, -ys - 1.5, -ys + 1.5, z0 + zc - 7.5, z0 + zc + 7.5)
        plate -= bx(xf - 1, xr + 1, ys - 1.5, ys + 1.5, z0 + zc - 7.5, z0 + zc + 7.5)
        for sy in (-18.0, 18.0):
            plate -= orient(csk_cutter(4, pt + 1), (xf, sy, z0 + zc), (-1, 0, 0))
    o.add("fn_plate", "FieldNode back plate", plate, "aluminium", "made", 1, "node")
    for zc in p["fn_clamp_dz"]:
        o.add("fn_vblocks", "FieldNode V-block", _vblock(p, xr, z0 + zc), "aluminium", "made", 1, "node")
        for sy in (-18.0, 18.0):
            o.fast("fn_screws", 4, pt, (xf, sy, z0 + zc), (-1, 0, 0), "node", 1, head="csk", nut=None, length=12)
    for zc in p["fn_clamp_dz"]:
        o.add("fn_bands", "FieldNode band clamp", band_loop(p["pole_x"], 0, r, [(xf - 0.01, ys + 1.5 - bt_ - 0.2, (-bt_, bt_)),
                                                                             (xf - 0.01, -ys - 1.5 + bt_ + 0.2, (-bt_, -bt_))],
                                                          z0 + zc, bw_, bt_), "stainless", "bought", 1, "node")
    ex, ey, ez = p["enc"]
    wl = 3.0                                                              # enclosure wall
    xb0 = xf - ex + 12                                                     # open (road) end of the body
    body = bx(xb0, xf, -ey / 2, ey / 2, z0, z0 + ez)
    body -= bx(xb0 - 1, xf - wl, -ey / 2 + wl, ey / 2 - wl, z0 + wl, z0 + ez - wl)
    bosses = []
    for sy in (-1, 1):
        for zz in (z0 + 9.0, z0 + ez - 9.0):
            bosses.append(xcyl(xb0 + 10, sy * (ey / 2 - 9.0), zz, 5.0, 20.0) - xcyl(xb0 + 10, sy * (ey / 2 - 9.0), zz, 2.0, 20.1))
    body = cp.break_edges(body, 1.0) + fuse(bosses)
    for yy in D["port_y"].values():                                     # holes for the connector stems
        body -= zcyl(D["port_x"], yy, z0 + 1.5, 6.0, wl + 2)
    for yy in (40.0, 8.0):
        body -= zcyl(xf - 27, yy, z0 + 1.5, 6.0, wl + 2)
    body -= zcyl(xf - 27, -24, z0 + 1.5, 4.0, wl + 2)
    body -= zcyl(D["port_x"], -30, z0 + 1.5, 4.0, wl + 2)
    o.add("fn_body", "FieldNode enclosure body (IP65, 3 mm wall)", body, "polycarbonate", "made", 1, "node")
    lid = bx(xf - ex, xf - ex + 12, -ey / 2, ey / 2, z0, z0 + ez)
    lid -= bx(xf - ex + 3, xf - ex + 13, -ey / 2 + wl, ey / 2 - wl, z0 + wl, z0 + ez - wl)
    lid = cp.break_edges(lid, 1.0)
    for sy in (-1, 1):
        for zz in (z0 + 9.0, z0 + ez - 9.0):
            lid -= xcyl(xf - ex + 1.5, sy * (ey / 2 - 9.0), zz, 2.25, 4.0)
    o.add("fn_lid", "FieldNode lid", lid, "polycarbonate", "made", 1, "node")
    for sy in (-1, 1):
        for zz in (z0 + 9.0, z0 + ez - 9.0):
            o.fast("fn_screws", 4, 3.0, (xf - ex, sy * (ey / 2 - 9.0), zz), (-1, 0, 0), "node", 1, head="button", nut=None, length=30)
    # connectors, glands and antenna
    for k_, yy in D["port_y"].items():
        con = zcyl(D["port_x"], yy, z0 - 10, 8.0, 20.0) + zcyl(D["port_x"], yy, z0 - 1.5, 11.0, 3.0) + zcyl(D["port_x"], yy, z0 + 4.5, 6.0, 9.0)
        con -= zcyl(D["port_x"], yy, z0 - 14, 5.5, 12.0)
        o.add("fn_ports", f"M12 5-pin panel connector, port {k_}", con, "brass", "bought", 1, "node")
    for yy in (40.0, 8.0, -24.0):
        g = zcyl(xf - 27, yy, z0 - 10, 8.0, 20.0) + zcyl(xf - 27, yy, z0 + 4.5, 4.0 if yy < 0 else 6.0, 9.0)
        g = cp.break_edges(g, 0.5)
        o.add("fn_ports", "Cable gland", g, "zinc_plated", "bought", 1, "node")
    whip = zcyl(D["port_x"], -30, z0 - 95, 5.0, 190.0)
    whip = cp.break_edges(whip, 2.0) + zcyl(D["port_x"], -30, z0 + 4.5, 4.0, 9.0)
    o.add("fn_ports", "LoRa antenna (rubber duck)", whip, "epdm", "bought", 1, "node")
    # inside the box: LiFePO4 32700 cell and the board on four standoffs
    cell = Pos(xf - wl - 18.5, 0, z0 + 28.0) * b.Rot(90, 0, 0) * b.Cylinder(16.0, 70.0)
    cell = cp.break_edges(cell, 0.8)
    o.add("fn_cell", "LiFePO4 cell, 6 Ah (32700)", cell, "aluminium", "bought", 1, "node")
    xpcb = xf - wl - 10.0
    pcb = cp.break_edges(bx(xpcb - 1.6, xpcb, -50, 50, z0 + 58, z0 + 168), 0.3)
    for sy in (-40.0, 40.0):
        for zz in (z0 + 66, z0 + 160):
            pcb -= xcyl(xpcb - 0.8, sy, zz, 1.7, 2.0)
    o.add("fn_pcb", "FieldNode board (MPPT, rails, STM32WL), 100 x 110 x 1.6", pcb, "hdpe_black", "bought", 1, "node", color=GREEN)
    for sy in (-40.0, 40.0):
        for zz in (z0 + 66, z0 + 160):
            so = xcyl(xf - wl - 4.0, sy, zz, 3.0, 8.0) - xcyl(xf - wl - 4.0, sy, zz, 1.5, 8.2)
            o.add("fn_pcb", "Board standoff M3 x 8", so, "brass", "bought", 1, "node")
            o.fast("fn_screws", 3, 0.0, (xpcb - 1.6, sy, zz), (-1, 0, 0), "node", 1, head="button", nut=None, length=10)
    # panel bracket: plate clips, two posts and two struts (aluminium flat bar), as one bent-and-bolted part
    fx = lambda fy: xr + fy + 42.0  # noqa: E731
    pcx, pcz = fx(-115.0), z0 + 385.0
    pts = {"post_foot": (fx(-63.0), z0 + 262.0), "post_head": (fx(-33.8), z0 + 420.4),
           "strut_foot": (fx(-62.0), z0 + 232.0), "strut_head": (fx(-164.0), z0 + 311.2)}
    bars = []
    for (a, c, yy) in (("post_foot", "post_head", 84.5), ("strut_foot", "strut_head", 78.5)):
        (xa, za), (xc, zc) = pts[a], pts[c]
        L = math.hypot(xc - xa, zc - za)
        ang = math.degrees(math.atan2(zc - za, xc - xa))
        for sy in (-1, 1):
            bars.append(b.Pos((xa + xc) / 2, sy * yy, (za + zc) / 2) * b.Rot(0, -ang, 0) * cp.break_edges(b.Box(L + 20, 3, 20), 0.6))
    clips = fuse([bx(xf - 30, xf, sy * 80, sy * 83, z0 + 218, z0 + 295) for sy in (-1, 1)]
                 + [bx(xf - 3, xf, sy * 53, sy * 83, z0 + 218, z0 + 295) for sy in (-1, 1)])
    bracket = fuse(bars) + clips
    o.add("fn_bracket", "FieldNode panel bracket (clips, posts, struts)", bracket, "aluminium", "made", 1, "panel")
    pw_, pl_, pth = p["panel"]
    frame = b.Box(pw_, pl_, pth) - b.Box(pw_ - 24, pl_ - 24, pth + 2)
    frame += b.Pos(0, 0, 3.0 - pth / 2) * (b.Box(pw_ - 24 + 0.01, pl_ - 24 + 0.01, 3.0) - b.Box(pw_ - 36, pl_ - 36, 4.0))
    frame = cp.break_edges(frame, 0.8)
    lam = cp.break_edges(b.Pos(0, 0, pth / 2 - 2.0) * b.Box(pw_ - 24, pl_ - 24, 4.0), 0.4)
    Tm = b.Pos(pcx, 0, pcz) * b.Rot(0, p["panel_tilt"], 0)
    o.add("fn_panel", "FieldNode 6 W panel frame", Tm * frame, "aluminium", "bought", 1, "panel")
    o.add("fn_panel", "FieldNode 6 W panel laminate", Tm * lam, "glass", "bought", 1, "panel", color="#1B2A5A")


def _stand_off(o, p, tx, ty, zz, od, face_x, bom, group):
    """Stand-off pipe clamp: a stainless band with a tapped boss round a pipe of outside diameter od (axis at tx, ty),
    an M8 stud into the concrete face at x = face_x (the face looks toward -X), a 40 mm wall plate with washer and
    nut, and a lock nut on the boss."""
    pct, pcw = p["pclamp"]
    wd, wt = p["wall_plate"]
    x_ring = tx + od / 2 + pct
    ring = zcyl(tx, ty, zz, od / 2 + pct, pcw) - zcyl(tx, ty, zz, od / 2, pcw + 2)
    ring += bx(x_ring - 1, x_ring + 8, ty - 7, ty + 7, zz - 7, zz + 7) - xcyl(x_ring + 4, ty, zz, 4.0, 10)
    o.add("pclamps", "Stand-off pipe clamp band with tapped boss", cp.break_edges(ring, 0.4), "stainless", "bought", bom, group)
    plate = cp.break_edges(xcyl(face_x - wt / 2, ty, zz, wd / 2, wt) - xcyl(face_x - wt / 2, ty, zz, 4.25, wt + 2), 0.5)
    o.add("pclamps", "Wall plate (stainless, 40 dia x 5)", plate, "stainless", "bought", bom, group).update(key="pclamp_plates")
    x0, x1 = x_ring + 2.0, face_x + 50.0
    o.add("pclamps", "M8 stand-off stud and wall anchor", cp.break_edges(xcyl((x0 + x1) / 2, ty, zz, 4.0, x1 - x0), 0.4), "stainless", "bought", bom, group)
    o.add("pclamps", "M8 lock nut (boss)", orient(cp.hex_nut(8), (x_ring + 8, ty, zz), (1, 0, 0)), "stainless", "fastener", bom, group)
    o.add("pclamps", "M8 washer (wall plate)", orient(cp.washer(8), (face_x - wt, ty, zz), (-1, 0, 0)), "stainless", "fastener", bom, group)
    o.add("pclamps", "M8 hex nut (wall plate)", orient(cp.hex_nut(8), (face_x - wt - 1.6, ty, zz), (-1, 0, 0)), "stainless", "fastener", bom, group)


def option_a(p=PARAMS):
    """Option A, the current design: radar over the gutter, ultrasonic in a stilling tube."""
    b = _b3d()
    D = derived(p)
    o = _Out()
    px, r = p["pole_x"], D["pole_r"]
    xr, xf = D["plate_rear_x"], D["plate_front_x"]
    bw_, bt_ = p["band"]
    hx = D["head_x"]
    az = D["arm_z"]
    hw = p["arm_sq"] / 2
    ct, ci, clen, ce = p["clip"]
    (xt, zt), (xft, zft) = D["pin_top"], D["pin_foot"]
    pt, pw = p["bplate"]

    _fieldnode(p, D, o)

    # ---------------- 3 pole bracket plate, V-blocks, band clamps
    z_lo, z_hi = D["bplate_z"]
    plate = cp.break_edges(bx(xf, xr, -pw / 2, pw / 2, z_lo, z_hi), 0.6)
    ys, sw, sh = p["band_slot"]
    for zb in D["band_z"]:
        for sy in (-1, 1):
            plate -= bx(xf - 1, xr + 1, sy * ys - sw / 2, sy * ys + sw / 2, zb - sh / 2, zb + sh / 2)
        for sy in (-18.0, 18.0):
            plate -= orient(csk_cutter(4, pt + 1), (xf, sy, zb), (-1, 0, 0))
    ww, wh = p["bplate_window"]
    wz = (D["bolt_z"] + p["foot_z"] + 25) / 2, (D["bolt_z"] + D["arm_z"] - 30) / 2
    for zc in wz:
        plate -= bx(xf - 1, xr + 1, -ww / 2, ww / 2, zc - wh / 2, zc + wh / 2)
    for sy in (-1, 1):
        for dz in (-18.0, 18.0):
            plate -= xcyl(xr - pt / 2, sy * 38.0, az + dz, 3.3, pt + 2)
    for dz in (-17.0, 17.0):
        plate -= xcyl(xr - pt / 2, 0, p["foot_z"] + dz, 3.3, pt + 2)
    plate -= xcyl(xr - pt / 2, 0, D["bolt_z"], 4.5, pt + 2)
    o.add("bplate", "Pole bracket plate", plate, "aluminium", "made", 3, "arm")
    for zb in D["band_z"]:
        o.add("vblocks", "V-block", _vblock(p, xr, zb), "aluminium", "made", 3, "arm")
        for sy in (-18.0, 18.0):
            o.fast("fixings", 4, pt, (xf, sy, zb), (-1, 0, 0), "arm", 3, head="csk", nut=None, length=12)
    for zb in D["band_z"]:
        o.add("bands", "Band clamp", band_loop(px, 0, r, [(xf - 0.01, ys + sw / 2 - bt_ - 0.2, (-bt_, bt_)),
                                                          (xf - 0.01, -ys - sw / 2 + bt_ + 0.2, (-bt_, -bt_))], zb, bw_, bt_),
              "stainless", "bought", 3, "arm")
    # ---------------- arm cleats (30 x 30 x 3 angle) and their bolts
    a_, at = p["angle"]
    cl = p["cleat_len"]
    for sy in (-1, 1):
        y0 = sy * hw
        c = (bx(xf - at, xf, y0, y0 + sy * a_, az - cl / 2, az + cl / 2) + bx(xf - a_, xf, y0, y0 + sy * at, az - cl / 2, az + cl / 2))
        c = cp.break_edges(c, 0.5)
        for dz in (-18.0, 18.0):
            c -= xcyl(xf - at / 2, sy * 38.0, az + dz, 3.3, at + 2)
        for dz in (-10.0, 10.0):
            c -= ycyl(xf - 15.0, sy * (hw + at / 2), az + dz, 3.3, at + 2)
        o.add("cleats", "Arm cleat (angle 30 x 30 x 3)", c, "aluminium", "made", 3, "arm")
    for sy in (-1, 1):
        for dz in (-18.0, 18.0):
            o.fast("fixings", 6, at + pt, (sy * 38.0 * 0 + xf - at, sy * 38.0, az + dz), (-1, 0, 0), "arm", 3)
    for dz in (-10.0, 10.0):
        o.fast("fixings", 6, 2 * at + p["arm_sq"], (xf - 15.0, -(hw + at), az + dz), (0, -1, 0), "arm", 3)
    # ---------------- brace clips
    top_clip = (bx(xt - clen / 2, xt + clen / 2, -ci / 2 - ct, ci / 2 + ct, D["arm_bot"] - ct, D["arm_bot"])
                + bx(xt - clen / 2, xt + clen / 2, ci / 2, ci / 2 + ct, D["arm_bot"] - ce, D["arm_bot"])
                + bx(xt - clen / 2, xt + clen / 2, -ci / 2 - ct, -ci / 2, D["arm_bot"] - ce, D["arm_bot"]))
    foot_clip = (bx(xf - ct, xf, -ci / 2 - ct, ci / 2 + ct, zft - clen / 2, zft + clen / 2)
                 + bx(xf - ce, xf, ci / 2, ci / 2 + ct, zft - clen / 2, zft + clen / 2)
                 + bx(xf - ce, xf, -ci / 2 - ct, -ci / 2, zft - clen / 2, zft + clen / 2))
    top_clip = cp.break_edges(top_clip, 0.5) - ycyl(xt, 0, zt, 3.3, ci + 2 * ct + 2)
    foot_clip = cp.break_edges(foot_clip, 0.5) - ycyl(xft, 0, zft, 3.3, ci + 2 * ct + 2)
    for dx in (-17.0, 17.0):
        top_clip -= zcyl(xt + dx, 0, D["arm_bot"] - ct / 2, 3.3, ct + 2)
        foot_clip -= xcyl(xf - ct / 2, 0, zft + dx, 3.3, ct + 2)
    o.add("top_clip", "Brace clip under the arm", top_clip, "aluminium", "made", 3, "arm")
    o.add("foot_clip", "Brace clip on the bracket plate", foot_clip, "aluminium", "made", 3, "arm")
    for dx in (-17.0, 17.0):
        o.fast("fixings", 6, ct + p["arm_sq"], (xt + dx, 0, D["arm_bot"] - ct), (0, 0, -1), "arm", 3, head="button")
        o.fast("fixings", 6, ct + pt, (xf - ct, 0, zft + dx), (-1, 0, 0), "arm", 3, head="button")
    # ---------------- arm tube (40 x 40 x 1.6 SHS) with crush sleeves
    arm = Pos(D["arm_x0"], 0, az) * Rot(0, 90, 0) * cp.shs(p["arm_sq"], p["arm_wall"], D["arm_x1"] - D["arm_x0"])
    for dz in (-10.0, 10.0):
        arm -= ycyl(xf - 15.0, 0, az + dz, 3.3, p["arm_sq"] + 2)
    arm_holes = (xt - 17.0, xt + 17.0, hx - p["head_bolt_dx"], hx + p["head_bolt_dx"])
    for x_ in arm_holes:
        arm -= zcyl(x_, 0, az, 3.3, p["arm_sq"] + 2)
    o.add("arm", "Sensor arm (SHS 40 x 40 x 1.6)", arm, "aluminium", "made", 3, "arm")
    sl_in = p["arm_sq"] - 2 * p["arm_wall"]
    for dz in (-10.0, 10.0):
        o.add("fixings", "Crush sleeve (arm, cross bolt)", Pos(xf - 15.0, 0, az + dz) * Rot(90, 0, 0) * sleeve(10.0, 6.4, sl_in), "aluminium", "made", 3, "arm")
    for x_ in arm_holes:
        o.add("fixings", "Crush sleeve (arm, vertical bolt)", Pos(x_, 0, az) * sleeve(10.0, 6.4, sl_in), "aluminium", "made", 3, "arm")
    # ---------------- knee brace (25 x 25 x 1.6 SHS) pinned in the clips
    bs, bwall = p["brace_sq"], p["brace_wall"]
    Lb = D["brace_pins"]
    over = 12.0
    mid = ((xt + xft) / 2, (zt + zft) / 2)
    brace = Pos(mid[0], 0, mid[1]) * Rot(0, -45, 0) * Pos(0, 0, -(Lb + 2 * over) / 2) * cp.shs(bs, bwall, Lb + 2 * over)
    for (xx, zz) in ((xt, zt), (xft, zft)):
        brace -= ycyl(xx, 0, zz, 3.3, bs + 2)
    o.add("brace", "Knee brace (SHS 25 x 25 x 1.6)", brace, "aluminium", "made", 3, "arm")
    for (xx, zz) in ((xt, zt), (xft, zft)):
        o.fast("pins", 6, ci + 2 * ct, (xx, -(ci / 2 + ct), zz), (0, -1, 0), "arm", 3)
        o.add("pins", "Crush sleeve (brace)", Pos(xx, 0, zz) * Rot(90, 0, 0) * sleeve(9.0, 6.4, bs - 2 * bwall), "aluminium", "made", 3, "arm")
    # ---------------- through-bolt across the street with its spacer
    zb = D["bolt_z"]
    spacer = Pos(xr, 0, zb) * Rot(0, 90, 0) * cp.round_tube(p["spacer_d"], (p["spacer_d"] - 8.5) / 2, D["spacer_len"])
    o.add("spacer", "Through-bolt spacer", spacer, "aluminium", "made", 3, "arm")
    o.fast("through_bolt", 8, D["pole_back_x"] - xf, (xf, 0, zb), (-1, 0, 0), "arm", 3, wash_head=True, wash_nut=True, length=100)
    # ---------------- head plate
    hl_, hw_, ht_ = p["head_plate"]
    hplate = cp.break_edges(bx(hx - hl_ / 2, hx + hl_ / 2, -hw_ / 2, hw_ / 2, D["head_top"], D["arm_bot"]), 0.6)
    for dx in (-p["head_bolt_dx"], p["head_bolt_dx"]):
        hplate -= zcyl(hx + dx, 0, D["head_top"] + ht_ / 2, 3.3, ht_ + 2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            hplate -= zcyl(hx + sx * 18, sy * 27, D["head_top"] + ht_ / 2, 2.25, ht_ + 2)
    o.add("head_plate", "Head plate", hplate, "aluminium", "made", 3, "arm")
    for dx in (-p["head_bolt_dx"], p["head_bolt_dx"]):
        o.fast("fixings", 6, ht_ + p["arm_sq"], (hx + dx, 0, D["head_top"]), (0, 0, -1), "arm", 3, head="button")

    # ---------------- 2 street radar head: housing can, lid, radar module on its carrier, lens, screws, gland
    hz = p["head_z"]
    hd, hh, lt = p["head_d"], p["head_h"], p["lens_t"]
    can_z0, can_z1 = hz + lt, D["head_top"] - 10.0                          # can floor underside to the lid underside
    can = zcyl(hx, 0, (can_z0 + can_z1) / 2, hd / 2, can_z1 - can_z0)
    can -= zcyl(hx, 0, (can_z0 + 5.0 + can_z1 + 1) / 2, hd / 2 - 3.0, can_z1 - can_z0 - 5.0 + 1)
    can -= zcyl(hx, 0, can_z0 + 2.5, p["lens_window"] / 2, 5.2)
    for k_ in range(3):
        a_k = math.radians(90 + 120 * k_)
        can -= zcyl(hx + 26 * math.cos(a_k), 26 * math.sin(a_k), can_z0 + 2.5, 1.5, 5.2)
    posts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            posts.append(zcyl(hx + sx * 20, sy * 20, can_z0 + 5.0 + 3.0 - 0.01, 3.0, 6.02) - zcyl(hx + sx * 20, sy * 20, can_z0 + 5.0 + 3.0, 1.5, 6.1))
    can = cp.break_edges(can, 0.8) + fuse(posts)
    gd, gl = p["gland"]
    zg = hz + lt + 5.0 + (can_z1 - can_z0 - 5.0) / 2
    can -= xcyl(hx + hd / 2 - 1.5, 0, zg, 6.0, 3.4)
    o.add("head_housing", "Radar head housing can (IP67)", can, "hdpe_black", "bought", 2, "street_head")
    lid = zcyl(hx, 0, can_z1 + 5.0, hd / 2, 10.0)
    lid = cp.break_edges(lid, 0.8)
    for sx in (-1, 1):
        for sy in (-1, 1):
            lid -= zcyl(hx + sx * 18, sy * 27, D["head_top"] - 5, 2.0, 10.02)
    o.add("head_housing", "Radar head housing lid with tapped bosses", lid, "hdpe_black", "bought", 2, "street_head")
    carrier = cp.break_edges(bx(hx - 25, hx + 25, -25, 25, can_z0 + 11.0, can_z0 + 12.6), 0.3)
    for sx in (-1, 1):
        for sy in (-1, 1):
            carrier -= zcyl(hx + sx * 20, sy * 20, can_z0 + 11.8, 1.4, 2.0)
    o.add("head_housing", "Radar carrier board 50 x 50 x 1.6", carrier, "hdpe_black", "bought", 2, "street_head", color=GREEN)
    mod = cp.break_edges(bx(hx - 9.3, hx + 9.3, -7.5, 7.5, can_z0 + 7.3, can_z0 + 11.0), 0.4)
    o.add("head_housing", "60 GHz radar module (XM125 class), 18.6 x 15", mod, "aluminium", "bought", 2, "street_head")
    for sx in (-1, 1):
        for sy in (-1, 1):
            o.fast("head_housing", 3, 1.6, (hx + sx * 20, sy * 20, can_z0 + 12.6), (0, 0, 1), "street_head", 2, head="button", nut=None, length=6)
    g = xcyl(hx + hd / 2 + gl / 2, 0, zg, gd / 2, gl) + xcyl(hx + hd / 2 - 1.5, 0, zg, 6.0, 3.2)
    g = cp.break_edges(g, 0.5)
    o.add("head_housing", "M12 cable gland (street head)", g, "zinc_plated", "bought", 2, "street_head")
    lens = cp.break_edges(zcyl(hx, 0, hz + lt / 2, p["lens_d"] / 2, lt), 0.6)
    for k_ in range(3):
        a_k = math.radians(90 + 120 * k_)
        lens -= orient(csk_cutter(3, lt + 1), (hx + 26 * math.cos(a_k), 26 * math.sin(a_k), hz), (0, 0, -1))
    o.add("lens", "PTFE lens disc 60 x 6", lens, "hdpe_natural", "made", 2, "street_head")
    for k_ in range(3):
        a_k = math.radians(90 + 120 * k_)
        o.fast("head_screws", 3, lt, (hx + 26 * math.cos(a_k), 26 * math.sin(a_k), hz), (0, 0, -1), "street_head", 2, head="csk", nut=None, length=10)
    for sx in (-1, 1):
        for sy in (-1, 1):
            o.fast("head_screws", 4, ht_, (hx + sx * 18, sy * 27, D["arm_bot"]), (0, 0, 1), "street_head", 2, head="button", nut=None, length=14)

    # ---------------- 8 depth marker plate, films and band clamps
    mt, mw, mh = p["marker"]
    mz0 = p["marker_z0"]
    marker = cp.break_edges(bx(D["pole_face_x"] - mt, D["pole_face_x"], -mw / 2, mw / 2, mz0, mz0 + mh), 0.4)
    o.add("marker", "Depth marker plate", marker, "aluminium", "made", 8, "marker")
    bd = bands(p)
    gw, gdp, gt = p["guard"]
    y0, y1 = D["guard_y0"], D["guard_y1"]
    mclamps = [band_loop(px, 0, r, [(D["pole_face_x"] - mt, mw / 2, (-bt_, bt_)), (D["pole_face_x"] - mt, -mw / 2, (-bt_, -bt_)),
                                                                          (D["pole_face_x"], mw / 2, (0, bt_)), (D["pole_face_x"], -mw / 2, (0, -bt_)),
                                                                          (px - gw / 2, y1, (-bt_, bt_)), (px + gw / 2, y1, (bt_, bt_))], zz, bw_, bt_) for zz in p["marker_bands_z"]]
    clamp_cut = fuse(mclamps)
    o.add("marker_film", "Marker film, amber 150 to 300", cp.break_edges(bd["amber"], 0.3) - clamp_cut, "safety_yellow", "made", 8, "marker")
    o.add("marker_film", "Marker film, red 300 to 450", cp.break_edges(bd["red"], 0.3) - clamp_cut, "safety_red", "made", 8, "marker")
    for cl_ in mclamps:
        o.add("marker_bands", "Marker and guard band clamp", cl_, "stainless", "bought", 8, "marker")

    # ---------------- 7 riser guard, three hat covers and eight security anchors
    zg0, zg1 = p["curb_h"], D["riser_top"]
    cy = p["cover_y"]
    guard = (bx(px - gw / 2, px - gw / 2 + gt, y0, y1, zg0, zg1) + bx(px + gw / 2 - gt, px + gw / 2, y0, y1, zg0, zg1)
             + bx(px - gw / 2, px + gw / 2, y1 - gt, y1, zg0, zg1))
    guard -= bx(px - gw / 2 - 1, px - gw / 2 + gt + 1, cy - 11, y1 + 1, zg0 - 1, zg0 + 20)
    o.add("guard", "Riser guard (U channel 40 x 65 x 2)", cp.break_edges(guard, 0.5), "galvanised", "made", 7, "conduit")
    W, H, t = p["hat"]
    gx0 = p["gutter_x0"]
    gut = hat((gx0, cy, 0), (0, 1, 0), (1, 0, 0), -H - gx0)
    gut += fuse([bx(-H, -4, cy + s * 21, cy + s * (W / 2), 0, t) for s in (-1, 1)])
    gut += fuse([bx(-4, -2, cy + s * 22, cy + s * (W / 2), 0, 30) for s in (-1, 1)])
    for s in (-1, 1):
        gut -= xcyl(-3, cy + s * 32, 18, 4.5, 4)
    o.add("gutter_cover", "Gutter cover (hat section)", cp.break_edges(gut, 0.5), "galvanised", "made", 7, "conduit")
    curb = hat((0, cy, 0), (0, 1, 0), (0, 0, 1), p["curb_h"] + H)
    curb -= fuse([bx(-3, 1, cy + s * 20.5, cy + s * (W / 2 + 1), p["curb_h"], p["curb_h"] + H + 1) for s in (-1, 1)])
    curb -= bx(-H - 1, -H + t + 1, cy - 10, cy + 10, -1, H)
    for s in (-1, 1):
        for zz in (18.0, 139.0):
            curb -= xcyl(-1, cy + s * 32, zz, 4.5, 4)
    o.add("curb_cover", "Curb cover (hat section)", cp.break_edges(curb, 0.5), "galvanised", "made", 7, "conduit")
    xw1 = px - gw / 2 - 1.0
    walk = hat((0, cy, p["curb_h"]), (0, 1, 0), (1, 0, 0), xw1)
    walk += fuse([bx(-4, 0, cy + s * 22, cy + s * (W / 2), p["curb_h"], p["curb_h"] + t) for s in (-1, 1)])
    walk += fuse([bx(-4, -2, cy + s * 22, cy + s * (W / 2), p["curb_h"] - 22, p["curb_h"] + t) for s in (-1, 1)])
    for s in (-1, 1):
        walk -= xcyl(-3, cy + s * 32, 139.0, 4.5, 4)
        for xx in (110.0, 330.0):
            walk -= zcyl(xx, cy + s * 32, p["curb_h"] + t / 2, 4.5, t + 2)
    o.add("walk_cover", "Sidewalk cover (hat section)", cp.break_edges(walk, 0.5), "galvanised", "made", 7, "conduit")
    for s in (-1, 1):
        for zz in (18.0, 139.0):
            _anchor(o, (0.0, cy + s * 32, zz), (-1, 0, 0), 4.0)
        for xx in (110.0, 330.0):
            _anchor(o, (xx, cy + s * 32, p["curb_h"]), (0, 0, 1), t)

    # ---------------- 5 stilling tube and its two stand-off pipe clamps
    tx = D["tube_x"]
    tube = Pos(tx, 0, D["tube_bot"]) * cp.round_tube(p["tube_od"], p["tube_wall"], D["tube_len"])
    sw_, sl_ = p["slot"]
    for k in range(p["slot_rows"]):
        zc = D["tube_bot"] + p["slot_first"] + k * p["slot_pitch"]
        for j in range(p["slots_per_row"]):
            a = 45.0 + 90.0 * j
            tube -= b.Pos(tx, 0, zc) * b.Rot(0, 0, a) * b.Pos(p["tube_od"] / 2, 0, 0) * b.Box(10, sw_, sl_)
    for sy in (-1, 1):
        tube -= ycyl(tx, sy * (p["tube_od"] / 2 - 1.5), p["tube_top"] - 20, 2.0, 6)
    o.add("tube", "Stilling tube (PVC 75 OD x 3, 40 slots)", tube, "pe_tank_white", "made", 5, "tube")
    bx1 = p["basin"][1]
    for zz in p["bracket_z"]:
        _stand_off(o, p, tx, 0.0, zz, p["tube_od"], bx1, 5, "tube")

    # ---------------- 4 drain head
    so, sl = p["socket"]
    tt = p["tube_top"]
    dh_r, dh_h = p["drain_head_d"] / 2, p["drain_head_h"]
    cap = zcyl(tx, 0, tt + dh_h / 2, dh_r, dh_h) - zcyl(tx, 0, tt + 4.0 + (dh_h - 7.0) / 2, dh_r - 3.0, dh_h - 7.0)
    cap -= zcyl(tx, 0, tt + 2.0, 9.5, 4.2)
    for sx in (-1, 1):
        cap -= zcyl(tx + sx * 18, 0, tt + 2.0, 1.5, 4.2)
    cap -= zcyl(tx, 0, tt + dh_h - 1.5, 6.0, 3.2)
    o.add("drain_head", "Drain head cap (sealed, 104 dia)", cp.break_edges(cap, 1.0), "hdpe_black", "made", 4, "drain_head")
    xdc = zcyl(tx, 0, tt + 16.5, 9.0, 33.0)
    pot = zcyl(tx, 0, tt + 5.2 + 25.0, dh_r - 4.2, 50.0) - xdc - zcyl(tx, 0, tt + 40.0 + 25.0, 6.0, 50.0)
    for sx in (-1, 1):
        pot -= zcyl(tx + sx * 18, 0, tt + 5.0, 1.5, 30.0)
    o.add("drain_head", "Potting compound", pot, "matte_black", "made", 4, "drain_head")
    o.add("drain_head", "Ultrasonic ranger A02YYUW (transducer 18 dia)", cp.break_edges(xdc, 0.8), "aluminium", "bought", 4, "drain_head")
    sock = zcyl(tx, 0, tt - sl / 2, so / 2, sl) - zcyl(tx, 0, tt - sl / 2, p["tube_od"] / 2, sl + 2)
    for sy in (-1, 1):
        sock -= ycyl(tx, sy * 39.5, tt - 20, 2.2, 4.4)
    o.add("drain_head", "PVC socket coupling 75 mm", cp.break_edges(sock, 0.6), "pe_tank_white", "bought", 4, "drain_head")
    for sy in (-1, 1):
        o.fast("drain_head", 4, 4.0, (tx, sy * 41.5, tt - 20), (0, sy, 0), "drain_head", 4, head="button", nut=None, length=12)
    for sx in (-1, 1):
        o.add("drain_head", "Wet probe electrode (stainless 3 dia x 30)", cp.break_edges(zcyl(tx + sx * 18, 0, tt + 5.0, 1.5, 30.0), 0.3),
              "stainless", "bought", 4, "drain_head")
    dg = cp.break_edges(zcyl(tx, 0, tt + dh_h + 7.5, gd / 2, 15) + zcyl(tx, 0, tt + dh_h - 1.5, 6.0, 3.0), 0.5)
    o.add("drain_head", "M12 cable gland (drain head)", dg, "zinc_plated", "bought", 4, "drain_head")

    _cables(o, p, D, gd, gl, hx, hw, az, zg, px, r, tx, cy)
    # ---------------- existing street (context, not in the BOM)
    for k, shp, mat in _site_parts(p):
        q = part(f"{k} (site)", shp, mat, kind="context", group="context")
        q["key"] = "site_" + k
        o.append(q)
    return list(o)

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


def site_compound(p=PARAMS):
    from build123d import Compound
    s = site(p)
    return Compound(children=[s[k] for k in ("road", "walk", "basin", "grate", "pole")])



def _anchor(o, origin, outward, stack):
    """M8 masonry stud with washer and security (snake-eye) nut, embedded 50 mm in the concrete face at `origin`
    (outward points out of the concrete); `stack` is the thickness of sheet clamped against the face."""
    emb, w_h, n_h = 50.0, ISO[8][4], 7.0
    top = stack + w_h + n_h + 2.0
    stud = cp.break_edges(Pos(0, 0, (top - emb) / 2) * _b3d().Cylinder(4.0, top + emb), 0.4)
    for nm, shp, mat, kd in (("Masonry stud anchor M8 x 105", stud, "stainless", "bought"),
                             ("M8 washer (ISO 7089)", Pos(0, 0, stack) * cp.washer(8), "stainless", "fastener"),
                             ("M8 security (snake-eye) nut", Pos(0, 0, stack + w_h) * snake_eye_nut(8), "stainless", "fastener")):
        q = part(nm, orient(shp, origin, outward), mat, kind=kd, bom=7, group="conduit", explode=EXPLODE["conduit"])
        q["key"] = "anchors"
        o.append(q)


_RUNS = {}


def _cables(o, p, D, gd, gl, hx, hw, az, zg, px, r, tx, cy):
    b = _b3d()
    c = p["cable_d"]
    xg = hx + p["head_d"] / 2 + gl
    ya = -hw - 2 - c / 2
    xs = 340.0
    zr = D["band_z"][1] - 60.0
    z0 = D["node_bot"]
    zs, zd = z0 - 140.0, z0 - 100.0
    zend = z0 - 45.0                                                  # cable enters the plug moulding here
    street = [(xg, 0, zg), (xg + 25, 0, zg), (xg + 25, ya, zg), (xg + 25, ya, az), (xs, ya, az), (xs, ya, zr),
              (xs, -47.0, zr), (px, -47.0, zr), (px, -47.0, zs), (370.0, -47.0, zs), (370.0, D["port_y"]["A"], zs),
              (D["port_x"], D["port_y"]["A"], zs), (D["port_x"], D["port_y"]["A"], zend)]
    zc_ = 7.0
    zw = p["curb_h"] + 7.0
    xcab = -8.0
    drain = [(tx, 0, D["dh_top"] + 15), (tx, 0, -100), (p["cable_exit_x"], 0, -100), (p["cable_exit_x"], cy, -100),
             (p["cable_exit_x"], cy, zc_), (xcab, cy, zc_), (xcab, cy, zw), (px, cy, zw), (px, cy, D["riser_top"] + 60),
             (px, r + 8.0, D["riser_top"] + 110), (px, r + 8.0, zd), (D["port_x"], r + 8.0, zd), (D["port_x"], D["port_y"]["B"], zd),
             (D["port_x"], D["port_y"]["B"], zend)]
    la, lb, ltop, ldx = p["loop_a"], p["loop_b"], p["loop_top"], p["loop_dx"]
    lx = tx - ldx
    lc = ltop - lb
    circ = [(lx, la * math.sin(2 * math.pi * k / 24), lc + lb * math.cos(2 * math.pi * k / 24)) for k in range(25)]
    o.add("slack_loop", "Drain cable slack loop (0.5 m)", cable([(tx, 0, ltop), (lx, 0, ltop)] + circ, c), "epdm", "bought", 6, "cables")
    zr_ = p["bracket_z"][0]
    ztie = lc - lb
    rc = p["tube_od"] / 2 + p["pclamp"][0]
    zt2 = zr_ + 14.0                                                   # tie ring on the pipe above the clamp band
    strap = zcyl(lx, 0, (ztie + zt2) / 2, 1.5, abs(ztie - zt2)) + xcyl((lx + tx - p["tube_od"] / 2) / 2, 0, zt2, 1.5, abs(lx - (tx - p["tube_od"] / 2))) \
        + (ycyl(lx, 0, ztie, c / 2 + 1.5, 5) - ycyl(lx, 0, ztie, c / 2, 6)) + (zcyl(tx, 0, zt2, p["tube_od"] / 2 + 3, 3) - zcyl(tx, 0, zt2, p["tube_od"] / 2, 4))
    o.add("loop_tie", "Slack loop cable ties (2)", strap, "matte_black", "fastener", 10, "cables")
    o.add("street_cable", "Street head cable, 3 m", cable(street, c), "epdm", "bought", 6, "cables")
    o.add("drain_cable", "Drain head cable, 5 m", cable(drain, c), "epdm", "bought", 6, "cables")
    for k_, yy in D["port_y"].items():
        xp = D["port_x"]
        plug = zcyl(xp, yy, z0 - 32.5, 8.0, 25.0) + zcyl(xp, yy, z0 - 15.0, 4.5, 10.0)
        ring = zcyl(xp, yy, z0 - 23.0, 9.5, 30.0) - zcyl(xp, yy, z0 - 23.0, 8.5, 31.0)
        o.add("plugs", f"M12 5-pin cable plug, port {k_}", cp.break_edges(plug, 0.6), "epdm", "bought", 6, "cables")
        o.add("plugs", f"M12 coupling ring, port {k_}", cp.break_edges(ring, 0.5), "brass", "bought", 6, "cables")
    _RUNS.clear()
    _RUNS.update(street=street, drain=drain)


def _site_parts(p):
    s = site(p)
    return [("Road slab and gutter", s["road"], "matte_black"), ("Curb and sidewalk", s["walk"], "concrete"),
            ("Catch basin and outlet pipe", s["basin"], "concrete"), ("Grate", s["grate"], "mild_steel"),
            ("Street pole 60 mm", s["pole"], "galvanised"), ("Pole-top sign", s["sign"], "aluminium")]


# ------------------------------------------------------------------ options B and C live in options_bc.py
OPTIONS = {"A": "Radar over the gutter, ultrasonic in a stilling tube",
           "B": "Hydrostatic pressure transducers",
           "C": "Float and reed-switch chain"}
PRINCIPLES = {
    "A": "A 60 GHz radar head on an arm over the gutter times the echo from the street, and an ultrasonic ranger in a slotted stilling tube times the echo from the basin water; neither touches the water.",
    "B": "A vented submersible pressure transducer at the foot of a perforated stand pipe on the curb face, and a second hung in the basin tube, read the water head as pressure (p = rho g h); both sit in the water.",
    "C": "A magnet in a float rises on a sealed guide tube and closes a reed switch on a 25 mm pitched chain, so the level is read as the highest closed switch; one tube on the curb face and one in the basin.",
}
CHOSEN = "A"
OPTION_VIEWS = {"A": {"el": 18, "az": -58, "scale": "person", "keep_context": True, "ground_z": 0},
                "B": {"el": 18, "az": -58, "scale": "person", "keep_context": True, "ground_z": 0},
                "C": {"el": 18, "az": -58, "scale": "person", "keep_context": True, "ground_z": 0}}
ALLOWED_CONTACTS = [("panel bracket", "6 W panel"), ("Slack loop cable ties", "Drain cable slack loop"), ("Slack loop cable ties", "Drain head cable"),
                    ("Drain cable slack loop", "Drain head cable"), ("Drain cable slack loop", "Drain unit cable"), ("Slack loop cable ties", "Drain unit cable"), ("Crush sleeve", "Sensor arm"), ("Crush sleeve", "SHS"), ("Crush sleeve", "Knee brace"),
                    ("M12 coupling ring", "M12 5-pin panel connector")]


def components(option=CHOSEN):
    """Kit 1.9 interface: the list of cad_parts.part() dicts for one concept option."""
    if option == "A":
        return option_a()
    import options_bc
    return options_bc.option(option, sys.modules[__name__])


# ------------------------------------------------------------------ legacy views of the chosen option, built from components()
class _Comp:
    def __init__(self, name, shape, bom, kind, group):
        self.name, self.shape, self.bom, self.kind, self.group = name, shape, bom, kind, group


def keyed(p=PARAMS):
    """The chosen option grouped by legacy component key: {key: _Comp with the fused shape}. The drawing, the concept
    media, the build plan pictures and the calculation note read this, so they always draw the kit 1.9 model."""
    out = {}
    for q in option_a(p):
        if q["kind"] == "context":
            continue
        for k in {q["key"], {"pclamp_plates": "pclamps", "marker_film": "marker"}.get(q["key"], q["key"])}:
            if k in out:
                out[k].shape = out[k].shape + q["shape"]
            else:
                out[k] = _Comp(q["name"], q["shape"], q["bom"], q["kind"], q["group"])
    out["_runs"] = dict(_RUNS)
    return out


def build_components(p=PARAMS):
    return keyed(p)


def build_parts(p=PARAMS):
    """{group: fused solid} of the kit parts (groups are the BOM keys of the old model)."""
    C = {k: v for k, v in keyed(p).items() if not k.startswith("_")}
    out = {}
    for k, c in C.items():
        out[c.group] = c.shape if c.group not in out else out[c.group] + c.shape
    return out


MASS_KEYS = ("bplate", "vblocks", "bands", "cleats", "top_clip", "foot_clip", "arm", "brace", "spacer", "through_bolt", "fixings", "pins",
             "head_plate", "head_screws", "marker", "guard", "marker_bands", "gutter_cover", "curb_cover", "walk_cover")


def masses(p=PARAMS):
    """Mass (kg) of the made aluminium and steel components, from the volume of each part and its material density."""
    m = {}
    for q in option_a(p):
        if q.get("key") in MASS_KEYS and q["kind"] != "context":
            m[q["key"]] = m.get(q["key"], 0.0) + cp.mass_kg(q)
    return m


def cable_runs(p=PARAMS):
    """Cable centre-line lengths (mm) from the model, for the calculation note."""
    option_a(p)
    return {k: cable_length(v) for k, v in _RUNS.items()}


def assembly(p=PARAMS, with_site=False):
    from build123d import Compound
    shapes = [q["shape"] for q in option_a(p) if q["kind"] != "context" or with_site and q["key"] in ("site_Street pole 60 mm",)]
    return Compound(children=shapes)


def pole_kit(p=PARAMS):
    from build123d import Compound
    return Compound(children=[q["shape"] for q in option_a(p) if q["kind"] != "context" and q["group"] in ("node", "panel", "street_head", "arm", "marker")])


def drain_kit(p=PARAMS):
    from build123d import Compound
    return Compound(children=[q["shape"] for q in option_a(p) if q["kind"] != "context" and q["group"] in ("drain_head", "tube")])



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
        ok = v < 5.0 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
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
    chk("Pipe clamp wall plates on the basin wall", S("pclamp_plates"), basin, "touch")
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
    # drain cable slack loop (0.5 m) tied to the stilling tube clamp
    chk("Slack loop clear of the stilling tube and its slots", S("slack_loop"), S("tube"), 10.0)
    chk("Slack loop clear of the drain head", S("slack_loop"), S("drain_head"), 5.0)
    chk("Slack loop clear of the basin wall", S("slack_loop"), basin, 10.0)
    chk("Slack loop clear of the pipe clamps", S("slack_loop"), S("pclamps"), 10.0)
    chk("Slack loop clear of the road slab and grate", S("slack_loop"), road + grate, 5.0)
    joined = lambda desc, a, b_: rows.append((desc, _vol(a, b_), a.distance_to(b_), "touch", a.distance_to(b_) < 0.05))  # noqa: E731
    joined("Slack loop joined to the drain cable", S("slack_loop"), S("drain_cable"))
    joined("Loop tie round the slack loop", S("loop_tie"), S("slack_loop"))
    joined("Loop tie on the upper pipe clamp", S("loop_tie"), S("pclamps"))
    chk("Loop tie ring round the stilling tube above the clamp band", S("loop_tie"), S("tube"), "touch")
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
    from build123d import export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "stl").mkdir(exist_ok=True)
    D = derived()
    outs = {"floodgauge-assembly": assembly(), "floodgauge-pole-kit": pole_kit(),
            "floodgauge-drain-kit": drain_kit(), "floodgauge-site": site_compound()}
    for name, shape in outs.items():
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.15, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    for opt in OPTIONS:
        ps = [q for q in components(opt) if q["kind"] != "context"]
        print(f"option {opt}: {len(ps)} parts, {sum(cp.mass_kg(q) for q in ps):.2f} kg")
    print(f"head {PARAMS['head_offset']:.0f} mm past the curb face, lens {PARAMS['head_z']:.0f} mm above the road; "
          f"arm {D['arm_len']:.0f} mm at {D['arm_z']:.0f}; bracket plate {D['bplate_h']:.0f} mm tall; brace pins {D['brace_pins']:.1f} mm apart; "
          f"tube {D['tube_len']:.0f} mm long, ID {D['tube_id']:.0f} mm")
    for k, v in cable_runs().items():
        print(f"cable run {k}: {v:.0f} mm")
    for k, v in masses().items():
        print(f"mass {k}: {v:.3f} kg")
    print_checks()
