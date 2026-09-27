"""FloodGauge product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the FieldNode core with a filleted IP65 enclosure, a lid
with a parting line, a clear window over the board and the LiFePO4 cell, lid screws, a teal name
plate, a lit status light and two M12 sensor ports; the 6 W panel with its frame, cell grid and
mounting blade; the 60 GHz street radar head with a filleted housing, a parting groove, a teal band,
the PTFE lens, the radar module board and a side cable gland; the aluminium sensor arm with end caps,
band clamps, knee brace and the M8 anti-rotation through-bolt; the sensor cables with cable ties and
M12 plugs; the depth marker plate with its amber and red bands; the surface cable cover and riser
guard; and the drain head (ultrasonic transducer, wet probe pins, NTC) on its slotted stilling tube.
Context is a compact street corner: a pole section, curb and sidewalk, concrete gutter, cast iron
grate, asphalt and a shallow sheet of ponding stormwater under the radar head.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every part size, the head offset past the curb, the arm, clamp spacing, brace and through-bolt, the
node's place on the road side of the pole, the marker plate and the cable cover come from PARAMS,
derived() and build_parts() in model.py. Axes as model.py: X across the street (road at X < 0, curb
face at X = 0), Y along the street, road surface at the gauge point Z = 0.
For a compact product render the pole kit is drawn lower than installed (RENDER_LENS_Z, RENDER_NODE_Z
below): the lens is 1.3 m above the road instead of 4.6 m and the node center 0.74 m instead of 3.0 m.
The drain head and stilling tube are at their model.py positions inside the catch basin; they are in
the "accessory" group, so they appear in the exploded view but not in the hero. See docs/REVIEW.md,
session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Polygon, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, derived, bands

TITLE = "FloodGauge: street and drain water level sensor"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 24, "az": -140,
     "note": "Product render from the road side and above (about 24 deg elevation), looking toward the curb; "
             "radar head on its arm over the gutter and grate, solar-powered node on the pole with its board "
             "and cell behind a clear window. Pole kit drawn lower than installed (lens 4.6 m above the road)"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 22, "az": -130,
     "note": "Exploded view from the road side and above (about 22 deg elevation): node enclosure, lid and "
             "window, board, LiFePO4 cell and solar panel; radar head housing, module board and lens; arm, "
             "clamps and through-bolt; depth marker; drain head, ultrasonic transducer and stilling tube (left)"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 14, "az": -150,
     "note": "Detail from the road side, slightly above (about 14 deg elevation), without the street: "
             "radar head and arm (top), node and panel (middle), depth marker and cable cover (bottom)"},
]

# Render layout (not the installed layout); see the module docstring.
RENDER_LENS_Z = 1300.0     # underside of the lens above the road (installed: PARAMS["head_z"], 4600 mm)
RENDER_NODE_Z = 740.0      # FieldNode enclosure center above the road (installed: PARAMS["node_z"], 3000 mm)
POLE_TOP_ABOVE_ARM = 170.0  # the context pole section ends this far above the arm top
PATCH = (-760.0, 620.0, 380.0, 150.0)   # street patch: x0, x1, half length along Y, slab depth

# Colours (restrained product palette; kit accent)
C_SHELL = "#E7E9EB"
C_SHELL2 = "#CDD2D7"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_WINDOW = "#DCEBF5"
C_METAL = "#B8BEC6"
C_STEEL = "#A3AAB1"
C_ALU = "#C4CAD0"
C_GALV = "#9EA5AB"
C_PCB = "#166534"
C_CHIP = "#111827"
C_CELL = "#2F5D8A"
C_SOLAR = "#1B2A44"
C_LED_G = "#22C55E"
C_LABEL = "#F4F4F2"
C_PTFE = "#F1F0EA"
C_PVC = "#8E979D"
C_AMBER = "#E5A11B"
C_RED = "#C0352B"
C_POLE = "#A2A8AE"
C_CONCRETE = "#CFCBC3"
C_GUTTER = "#BDB8AF"
C_ASPHALT = "#5E6266"
C_IRON = "#34373A"
C_VOID = "#1D2023"
C_WATER = "#8DB6C2"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _span(x0, x1, y0, y1, z0, z1):
    return _box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _pipe(points, r):
    """Round cable or tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _minx(s):
    return s.faces().sort_by(Axis.X)[0].edges()


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_y(x, y, z, af, h):
    return Pos(x, y + h / 2, z) * Rot(90, 0, 0) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_x(x, y, z, af, h):
    return Pos(x - h / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=h)


def _screw_x(x, y, z, r=3.2, h=1.4):
    """Pan head screw facing -X with a slot."""
    s = _xcyl(x, y, z, r, h)
    s = _fillet_try(s, _minx(s), [0.6, 0.3])
    return s - _box(x - h / 2, y, z, 1.0, r * 1.2, 0.8)


def product_parts(P=PARAMS):
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    dz_arm = P["head_z"] - RENDER_LENS_Z          # arm and head drawn this far below installed
    hz = RENDER_LENS_Z                            # lens underside
    az = P["arm_z"] - dz_arm                      # arm axis
    arm_top = az + P["arm_sq"] / 2
    px, pr = P["pole_x"], D["pole_r"]
    pf = D["pole_face_x"]
    hx = D["head_x"]
    cs = P["curb_h"]

    # ------------------------------------------------------------ 1 FieldNode core
    ex, ey, ez = P["enc"]
    nx, nz = D["node_x"], RENDER_NODE_Z
    x0, x1 = nx - ex / 2, nx + ex / 2              # front (road) face, back face
    nbot, ntop = nz - ez / 2, nz + ez / 2
    lid_t = 12.0
    xp = x0 + lid_t                                # parting plane
    outer = _box(nx, 0, nz, ex, ey, ez)
    outer = _fillet_try(outer, _edges_par(outer, Axis.X), [10.0, 8.0, 5.0])
    outer = _fillet_try(outer, _minx(outer), [3.0, 2.0, 1.0])
    outer = _fillet_try(outer, outer.faces().sort_by(Axis.X)[-1].edges(), [2.0, 1.0])
    body = outer & _span(xp + 0.4, x1 + 1, -ey, ey, nbot - 1, ntop + 1)
    body -= _span(xp - 1, x1 - 3, -ey / 2 + 3, ey / 2 - 3, nbot + 3, ntop - 3)
    for dz in (-60, -30, 0, 30, 60):               # side grip ribs (texture)
        for sy in (-1, 1):
            body -= _box(nx + 10, sy * ey / 2, nz + dz, 50, 1.6, 2.0)
    add("Node enclosure body", body, C_SHELL, "plastic", 1, "shell", (0, 0, 0))

    lid = outer & _span(x0 - 1, xp - 0.4, -ey, ey, nbot - 1, ntop + 1)
    lid -= _span(x0 + 3, xp, -ey / 2 + 3, ey / 2 - 3, nbot + 3, ntop - 3)
    wy, wz0, wz1 = 55.0, nz - 22.0, nz + 82.0      # window opening in the lid
    lid -= _span(x0 - 2, x0 + 4, -wy, wy, wz0, wz1)
    EL = (-240, 0, 0)
    add("Node lid", lid, C_SHELL2, "plastic", 1, "shell", EL)
    pane = _span(x0 + 3, x0 + 5, -wy - 4, wy + 4, wz0 - 4, wz1 + 4)
    add("Node clear window", pane, C_WINDOW, "clear", 1, "shell", EL)
    scr = _union([_screw_x(x0 - 0.6, sy * (ey / 2 - 10), nz + sz * (ez / 2 - 10))
                  for sy in (-1, 1) for sz in (-1, 1)])
    add("Node lid screws", scr, C_METAL, "metal", 10, "shell", (-290, 0, 0))
    plate = _span(x0 - 0.4, x0, -45, 45, nbot + 42, nbot + 56)
    add("Node name plate", plate, C_ACCENT, "painted", 1, "shell", EL)
    ink = (_span(x0 - 0.7, x0 - 0.4, -38, 8, nbot + 47, nbot + 51)
           + _span(x0 - 0.7, x0 - 0.4, 14, 38, nbot + 48, nbot + 50))
    add("Node name plate print", ink, C_LABEL, "paper", 1, "shell", EL)
    ledh = _xcyl(x0 - 0.8, 0, nbot + 24, 5.0, 1.6)
    add("Status light bezel", ledh, C_BLACK, "plastic", 1, "shell", EL)
    led = (Pos(x0 - 1.6, 0, nbot + 24) * Sphere(3.2)) & _span(x0 - 6, x0 - 1.2, -5, 5, nbot + 19, nbot + 29)
    add("Status light, green (lit)", led, C_LED_G, "emissive", 1, "shell", EL)

    # back plate and pole straps (node side of item 1)
    bt, bw, bh = P["back_plate"]
    bp = _span(pf - bt, pf, -bw / 2, bw / 2, nz - bh / 2, nz + bh / 2)
    bp = _fillet_try(bp, _edges_par(bp, Axis.X), [6.0, 4.0])
    add("Node back plate", bp, C_METAL, "metal", 1, "shell", (0, 0, 0))
    straps = _union([_zcyl(px, 0, nz + s * 85, pr + 1.5, 14) - _zcyl(px, 0, nz + s * 85, pr + 0.2, 16)
                     for s in (-1, 1)])
    add("Node pole straps", straps, C_STEEL, "metal", 1, "shell", (0, 0, 0))

    # board and cell behind the window (internal)
    pcb = _span(x1 - 12, x1 - 10.4, -ey / 2 + 8, ey / 2 - 8, nbot + 10, ntop - 10)
    add("Node board (MPPT and LoRaWAN)", pcb, C_PCB, "plastic", 1, "internal", (-120, 0, 0))
    comps = (_span(x1 - 16, x1 - 12, -50, -14, nz + 30, nz + 64)                  # radio module
             + _span(x1 - 18, x1 - 12, 20, 44, nz - 30, nz - 6)                   # MPPT inductor
             + _span(x1 - 17, x1 - 12, -50, 50, nbot + 14, nbot + 24)             # sensor port header
             + _span(x1 - 15, x1 - 12, 22, 40, nz + 40, nz + 58))                 # controller
    add("Node board components", comps, C_CHIP, "plastic", 1, "internal", (-120, 0, 0))
    shield = _span(x1 - 16.6, x1 - 16, -48, -16, nz + 32, nz + 62)
    add("Radio module shield can", shield, C_METAL, "metal", 1, "internal", (-120, 0, 0))
    ant = _span(x1 - 13, x1 - 12, -60, -20, ntop - 22, ntop - 16)
    add("Radio antenna (flex)", ant, C_BLACK, "plastic", 1, "internal", (-120, 0, 0))
    cyz = nz + 34
    cell = _ycyl(nx + 2, 0, cyz, 16.0, 70.0)
    cell = _fillet_try(cell, cell.edges(), [2.0, 1.0])
    add("LiFePO4 cell, 6 Ah", cell, C_CELL, "plastic", 1, "internal", (-180, 0, 0))
    caps = _ycyl(nx + 2, 36, cyz, 7.0, 2.0) + _ycyl(nx + 2, -36, cyz, 7.0, 2.0)
    add("Cell terminals", caps, C_METAL, "metal", 1, "internal", (-180, 0, 0))
    holder = _span(nx - 14, nx + 18, -42, 42, cyz - 20, cyz - 8) - _ycyl(nx + 2, 0, cyz, 16.5, 90)
    add("Cell holder", holder, C_BLACK, "plastic", 1, "internal", (-150, 0, 0))

    # M12 sensor ports on the underside
    ports = None
    for sy in (-1, 1):
        g = _hex_z(nx, sy * 35, nbot - 2.5, 17.0, 5.0) + _zcyl(nx, sy * 35, nbot - 10, 7.5, 10)
        ports = g if ports is None else ports + g
    add("M12 sensor ports", ports, C_METAL, "metal", 1, "shell", (0, 0, -60))
    vent = _zcyl(nx, 0, nbot - 3, 6.0, 6.0)
    vent = _fillet_try(vent, _bottom(vent), [1.5, 1.0])
    add("Pressure vent plug", vent, C_DARK, "plastic", 1, "shell", (0, 0, -60))

    # 6 W panel as a hood, same pose as model.py; frame, cells and a mounting blade
    pw, pl, pt = P["panel"]
    T = Pos(nx - 30, 0, ntop + 55) * Rot(0, -P["panel_tilt"], 0)
    frame = Box(pw, pl, pt)
    frame = _fillet_try(frame, _edges_par(frame, Axis.Z), [4.0, 2.0])
    frame -= Pos(0, 0, pt / 2) * Box(pw - 12, pl - 12, 5)
    frame -= Pos(0, 0, -pt / 2) * Box(pw - 16, pl - 16, 12)
    EP = (-150, 0, 120)
    add("Solar panel frame", T * frame, C_ALU, "metal", 1, "shell", EP)
    glass = Pos(0, 0, pt / 2 - 3.2) * Box(pw - 12, pl - 12, 1.6)
    add("Solar cells under glass", T * glass, C_SOLAR, "screen", 1, "shell", EP)
    grid = None
    for k in range(1, 4):
        g = Pos(-pw / 2 + 6 + k * (pw - 12) / 4, 0, pt / 2 - 2.3) * Box(0.8, pl - 16, 0.3)
        grid = g if grid is None else grid + g
    for k in range(1, 6):
        grid += Pos(0, -pl / 2 + 6 + k * (pl - 12) / 6, pt / 2 - 2.3) * Box(pw - 16, 0.8, 0.3)
    add("Solar cell grid lines", T * grid, C_METAL, "metal", 1, "shell", EP)
    blade = _span(nx - 22, nx + 22, -60, 60, ntop - 2, ntop + 110)
    blade -= T * (Pos(0, 0, 150 - pt / 2) * Box(600, 600, 300))
    blade = _fillet_try(blade, _edges_par(blade, Axis.X), [3.0, 1.5])
    add("Panel mounting blade", blade, C_METAL, "metal", 1, "shell", (-60, 0, 60))

    # ------------------------------------------------------------ 2 street radar head
    hd, hh, lt = P["head_d"], P["head_h"], P["lens_t"]
    hr = hd / 2
    EH = (0, 0, -110)
    housing = _zcyl(hx, 0, hz + lt + (hh - lt) / 2, hr, hh - lt)
    housing = _fillet_try(housing, _bottom(housing), [5.0, 3.0, 2.0])
    housing -= _zcyl(hx, 0, hz + lt + 34, hr + 2, 1.0) - _zcyl(hx, 0, hz + lt + 34, hr - 0.8, 2.0)
    add("Radar head housing", housing, C_SHELL, "plastic", 2, "shell", EH)
    band = _zcyl(hx, 0, hz + lt + 50, hr + 0.4, 6.0) - _zcyl(hx, 0, hz + lt + 50, hr - 1, 8)
    add("Radar head accent band", band, C_ACCENT, "painted", 2, "shell", EH)
    lab = (_zcyl(hx, 0, hz + lt + 20, hr + 0.3, 16.0) - _zcyl(hx, 0, hz + lt + 20, hr - 1, 18)) \
        & _span(hx - 30, hx + 30, -hr - 2, -hr + 12, hz, hz + 100)
    add("Radar head label", lab, C_LABEL, "paper", 2, "shell", EH)
    bez = _zcyl(hx, 0, hz + lt + 1.5, P["lens_d"] / 2 + 4, 3.0) - _zcyl(hx, 0, hz + lt + 1.5, P["lens_d"] / 2, 4)
    add("Lens retaining ring", bez, C_DARK, "plastic", 2, "shell", (0, 0, -170))
    lens = _zcyl(hx, 0, hz + lt / 2, P["lens_d"] / 2, lt)
    lens = _fillet_try(lens, _bottom(lens), [2.5, 1.5])
    add("PTFE lens", lens, C_PTFE, "plastic", 2, "shell", (0, 0, -230))
    rb = _zcyl(hx, 0, hz + lt + 12, 28.0, 1.6)
    add("Radar module carrier board", rb, C_PCB, "plastic", 2, "internal", (0, 0, -170))
    chip = _box(hx, 0, hz + lt + 9.5, 15, 15, 3.4)
    add("60 GHz radar module", chip, C_CHIP, "plastic", 2, "internal", (0, 0, -170))
    gz = hz + lt + 62
    gl = _hex_x(hx + hr + 1.5, 0, gz, 15.0, 5.0) + _xcyl(hx + hr + 8, 0, gz, 6.5, 9.0)
    gl = _fillet_try(gl, gl.faces().sort_by(Axis.X)[-1].edges(), [1.5, 1.0])
    add("Radar head cable gland", gl, C_DARK, "plastic", 2, "shell", (40, 0, -110))

    # ------------------------------------------------------------ 3 arm, saddle, clamps, brace, bolt
    a0, a1 = D["arm_x0"], D["arm_x1"]
    s = P["arm_sq"]
    tube = _span(a0, a1, -s / 2, s / 2, az - s / 2, az + s / 2)
    tube = _fillet_try(tube, _edges_par(tube, Axis.X), [3.0, 2.0])
    tube -= _span(a0 - 1, a1 + 1, -s / 2 + P["arm_wall"], s / 2 - P["arm_wall"],
                  az - s / 2 + P["arm_wall"], az + s / 2 - P["arm_wall"])
    add("Sensor arm (aluminium tube)", tube, C_ALU, "metal", 3, "shell", (0, 0, 0))
    caps = None
    for xe, sg in ((a0, -1), (a1, 1)):
        c = _span(xe, xe + sg * 4, -s / 2 - 0.5, s / 2 + 0.5, az - s / 2 - 0.5, az + s / 2 + 0.5)
        c = _fillet_try(c, _edges_par(c, Axis.X), [3.0, 2.0])
        c = _fillet_try(c, c.faces().sort_by(Axis.X)[0 if sg < 0 else -1].edges(), [1.2, 0.6])
        caps = c if caps is None else caps + c
    add("Arm end caps", caps, C_BLACK, "plastic", 3, "shell", (0, 0, 0))
    sx_, sy_, sz_ = P["saddle"]
    sad = _box(hx, 0, az - s / 2 - sz_ / 2, sx_, sy_, sz_)
    sad = _fillet_try(sad, _edges_par(sad, Axis.Z), [6.0, 4.0])
    sad = _fillet_try(sad, _bottom(sad), [2.0, 1.0])
    add("Head saddle", sad, C_METAL, "metal", 3, "shell", (0, 0, -40))
    sscr = _union([_zcyl(hx + dx, 0, az + s / 2 + 1.0, 3.6, 2.0) for dx in (-22, 22)])
    add("Saddle screws", sscr, C_STEEL, "metal", 10, "shell", (0, 0, 40))

    zc_lo = az - P["clamp_dz"]
    clamps = None
    for z in (az, zc_lo):
        ring = _zcyl(px, 0, z, pr + P["clamp_t"], P["clamp_w"]) - _zcyl(px, 0, z, pr + 0.5, P["clamp_w"] + 2)
        ring = _fillet_try(ring, _top(ring) + _bottom(ring), [1.5, 1.0])
        ears = (_span(px + pr + 4, px + pr + 22, -9, -2, z - 18, z + 18)
                + _span(px + pr + 4, px + pr + 22, 2, 9, z - 18, z + 18))
        clamps = ring + ears if clamps is None else clamps + ring + ears
    add("Pole band clamps", clamps, C_STEEL, "metal", 3, "shell", (0, 0, 0))
    cb = _union([_ycyl(px + pr + 15, 0, z + dz, 3.0, 30) + _hex_y(px + pr + 15, 13, z + dz, 10, 5)
                 + _hex_y(px + pr + 15, -13, z + dz, 10, 5)
                 for z in (az, zc_lo) for dz in (-9, 9)])
    add("Clamp bolts", cb, C_METAL, "metal", 10, "shell", (60, 0, 0))

    L = P["brace_leg"]
    brace = (Pos(pf - L / 2, 0, az - L / 2) * Rot(0, -45, 0)
             * Box(P["brace_sq"], P["brace_sq"], D["brace_len"]))
    brace = _fillet_try(brace, brace.edges().filter_by(lambda e: abs(e.length - D["brace_len"]) < 1.0),
                        [2.0, 1.0])
    add("Knee brace", brace, C_ALU, "metal", 3, "shell", (0, 0, 0))
    bl = P["bolt_l"]
    bolt = _ycyl(px, 0, zc_lo, P["bolt_d"] / 2, bl)
    bolt += _hex_y(px, -bl / 2 - 2.5, zc_lo, 13.0, 5.0)
    add("M8 anti-rotation through-bolt", bolt, C_METAL, "metal", 3, "shell", (0, -140, 0))
    nut = _hex_y(px, bl / 2 - 12, zc_lo, 13.0, 8.0) + _ycyl(px, bl / 2 - 17, zc_lo, 8.0, 1.6)
    nut = _fillet_try(nut, nut.edges().filter_by(Axis.Y, reverse=True), [0.6, 0.3])
    add("Nyloc nut and washer", nut, C_STEEL, "metal", 3, "shell", (0, 120, 0))

    # ------------------------------------------------------------ 6 sensor cables and M12 plugs
    cr = P["cable_d"] / 2
    yc, xc = -38.0, px - 22.0                     # street cable down the pole, clear of clamps and bolt
    street = _pipe([(hx + hr + 12, 0, gz), (hx + hr + 30, 0, gz - 6), (hx + hr + 48, 0, gz + 10),
                    (hx + hr + 70, -s / 2 - cr, az), (pf - 25, -s / 2 - cr, az),
                    (xc, yc, az - 30), (xc, yc, nbot - 30), (nx + 10, yc + 5, nbot - 30),
                    (nx, -35, nbot - 22)], cr)
    gx_, gy_, gh_ = P["guard"]
    xr, cy = D["riser_x"], P["cover_y"]
    drain = _pipe([(xr, cy, cs + gh_ - 10), (xr, cy, cs + gh_ + 40), (px + 30, 60, nbot - 50),
                   (nx + 10, 40, nbot - 30), (nx, 35, nbot - 22)], cr)
    add("Sensor cables", street + drain, C_BLACK, "rubber", 6, "shell", (0, 0, 0))
    plugs = None
    for sy in (-1, 1):
        pg = _zcyl(nx, sy * 35, nbot - 21, 8.5, 18)
        pg = _fillet_try(pg, _bottom(pg), [2.0, 1.0])
        pg += _zcyl(nx, sy * 35, nbot - 13, 9.5, 5.0)
        plugs = pg if plugs is None else plugs + pg
    add("M12 cable plugs", plugs, C_DARK, "rubber", 6, "shell", (0, 0, -120))
    ties = None
    for x in (hx + hr + 110, 60.0, 250.0):
        t = (_span(x - 2.5, x + 2.5, -s / 2 - 2 * cr - 1.5, s / 2 + 1.5, az - s / 2 - 1.5, az + s / 2 + 1.5)
             - _span(x - 3, x + 3, -s / 2 - 2 * cr - 0.2, s / 2 + 0.1, az - s / 2 - 0.1, az + s / 2 + 0.1))
        ties = t if ties is None else ties + t
    for z in (az - 150, az - 480, nz + 60):
        t = _zcyl(px, 0, z, 49.0, 5.0) - _zcyl(px, 0, z, 47.5, 7.0)
        t &= _span(px - 60, px + 60, -60, 0, z - 5, z + 5)
        ties += t
    add("Cable ties", ties, C_BLACK, "plastic", 10, "shell", (0, 0, 0))

    # ------------------------------------------------------------ 8 depth marker plate and bands
    mt, mw, mh = P["marker"]
    mk = _span(pf - mt, pf, -mw / 2, mw / 2, cs, cs + mh)
    mk = _fillet_try(mk, _edges_par(mk, Axis.X), [4.0, 2.0])
    add("Depth marker plate", mk, C_LABEL, "painted", 8, "shell", (-90, 0, 0))
    B = bands(P)
    add("Depth band, amber (150 to 300 mm)", B["amber"], C_AMBER, "painted", 8, "shell", (-90, 0, 0))
    add("Depth band, red (300 to 450 mm)", B["red"], C_RED, "painted", 8, "shell", (-90, 0, 0))
    a_, r_, top_ = P["bands"]
    ticks = _union([_span(pf - mt - 0.6, pf - mt, -mw / 2 + 6, -mw / 2 + (26 if k % 2 == 0 else 16),
                          z - 1.2, z + 1.2) for k, z in enumerate(range(int(top_) + 50, int(cs + mh) - 10, 25))])
    add("Depth marker ticks", ticks, C_DARK, "paper", 8, "shell", (-90, 0, 0))
    rivets = _union([_xcyl(pf - mt - 0.6, sy * (mw / 2 - 8), z, 3.0, 1.2)
                     for sy in (-1, 1) for z in (cs + 12, cs + mh - 12)])
    add("Marker plate rivets", rivets, C_METAL, "metal", 10, "shell", (-90, 0, 0))

    # ------------------------------------------------------------ 7 surface cable cover and riser guard
    al, at = P["cover_angle"]
    cw, ch = P["cover_walk"]
    gx1 = P["grate"][1]
    ang = Pos(0, cy, 0) * extrude(Plane.YZ * Polygon((-al / 2, 0), (al / 2, 0), (0, 12)), amount=-gx1)
    ang = Pos(gx1, 0, 0) * ang
    ang -= Pos(gx1 - 1, cy, 0) * extrude(Plane.YZ * Polygon((-al / 2 + at, 0), (al / 2 - at, 0),
                                                            (0, 12 - at * 1.4)), amount=-gx1 + 2)
    face = _span(-at, 0, cy - al / 2, cy + al / 2, 0, cs + 1)
    walk = Pos(0, cy, cs) * extrude(Plane.YZ * Polygon((-cw / 2, 0), (cw / 2, 0), (cw / 2 - 20, ch),
                                                       (-cw / 2 + 20, ch)), amount=xr - gx_ / 2)
    cover = ang + face + walk
    add("Surface cable cover (galvanized steel)", cover, C_GALV, "metal", 7, "shell", (0, 0, 0))
    guard = _span(xr - gx_ / 2, xr + gx_ / 2, cy - gy_ / 2, cy + gy_ / 2, cs, cs + gh_)
    guard = _fillet_try(guard, _edges_par(guard, Axis.Z), [3.0, 2.0])
    guard -= _span(xr - gx_ / 2 + 3, xr + gx_ / 2 - 3, cy - gy_ / 2 + 3, cy + gy_ / 2 - 3, cs + 3, cs + gh_ + 1)
    add("Riser guard", guard, C_GALV, "metal", 7, "shell", (0, 0, 0))
    anchors = _union([_zcyl(x, cy + dy, cs + ch - 1.0, 5.0, 2.4) for x in (60.0, 200.0, 340.0) for dy in (-45,)]
                     + [_xcyl(-at - 1.0, cy + dy, cs / 2, 4.5, 2.0) for dy in (-15, 15)]
                     + [_zcyl(-60.0, cy + dy, 6.0, 4.5, 2.4) for dy in (-18, 18)])
    add("Masonry anchors", anchors, C_STEEL, "metal", 7, "shell", (0, 0, 0))

    # ------------------------------------------------------------ 4 drain head and 5 stilling tube
    tx = D["tube_x"]
    tt = P["tube_top"]
    dd, dh = P["drain_head_d"], P["drain_head_h"]
    DX, DZ = -520.0, 1150.0                        # exploded: drain kit lifted beside the pole kit
    cap = _zcyl(tx, 0, tt + dh / 2 + 6, dd / 2, dh - 12)
    cap = _fillet_try(cap, _top(cap), [10.0, 6.0, 3.0])
    cap -= _zcyl(tx, 0, tt + 30, dd / 2 + 2, 1.0) - _zcyl(tx, 0, tt + 30, dd / 2 - 0.8, 2)
    add("Drain head cap", cap, C_DARK, "plastic", 4, "accessory", (DX, 0, DZ + 260))
    dband = _zcyl(tx, 0, tt + 52, dd / 2 + 0.4, 6.0) - _zcyl(tx, 0, tt + 52, dd / 2 - 1, 8)
    add("Drain head accent band", dband, C_ACCENT, "painted", 4, "accessory", (DX, 0, DZ + 260))
    dgl = _hex_z(tx, 0, tt + dh + 2.5, 15.0, 5.0) + _zcyl(tx, 0, tt + dh + 9, 6.5, 8)
    add("Drain head cable gland", dgl, C_BLACK, "plastic", 4, "accessory", (DX, 0, DZ + 300))
    skirt = _zcyl(tx, 0, tt + 6, dd / 2, 12) - _zcyl(tx, 0, tt + 6, 22, 14)
    add("Drain head potted base", skirt, C_BLACK, "plastic", 4, "accessory", (DX, 0, DZ + 200))
    xd = _zcyl(tx, 0, tt + 8, 20.0, 16)
    xd = _fillet_try(xd, _bottom(xd), [1.5, 1.0])
    add("Ultrasonic transducer (A02YYUW)", xd, C_CHIP, "plastic", 4, "accessory", (DX, 0, DZ + 150))
    xf = _zcyl(tx, 0, tt + 0.3, 16.0, 0.6)
    add("Transducer face", xf, "#3A3F46", "rubber", 4, "accessory", (DX, 0, DZ + 150))
    probes = _union([_zcyl(tx + sx * 27, 0, tt - P["probe_drop"] / 2 + 2, 1.6, P["probe_drop"] + 4)
                     + (Pos(tx + sx * 27, 0, tt - P["probe_drop"]) * Sphere(1.6)) for sx in (-1, 1)])
    add("Wet probe pins", probes, C_METAL, "metal", 4, "accessory", (DX, 0, DZ + 100))
    ntc = _zcyl(tx, 30, tt - 3, 2.2, 6) + Pos(tx, 30, tt - 6) * Sphere(2.2)
    add("NTC air temperature bead", ntc, C_CHIP, "plastic", 4, "accessory", (DX, 0, DZ + 100))

    tb = D["tube_bot"]
    tr, tid = P["tube_od"] / 2, D["tube_id"] / 2
    pipe = _zcyl(tx, 0, (tt + tb) / 2, tr, tt - tb) - _zcyl(tx, 0, (tt + tb) / 2, tid, tt - tb + 2)
    sw, sl = P["slot"]
    rows = P["slot_rows"]
    pitch = (tt - tb - 120) / (rows - 1)
    for k in range(rows):
        zs = tb + 60 + k * pitch
        for j in range(P["slots_per_row"]):
            ang_deg = 45 + 90 * j + (45 if k % 2 else 0)
            pipe -= Pos(tx, 0, zs) * Rot(0, 0, ang_deg) * Pos(tr, 0, 0) * Box(12, sw, sl)
    add("Stilling tube (slotted PVC)", pipe, C_PVC, "plastic", 5, "accessory", (DX, 0, DZ))
    bx1 = P["basin"][1]
    brk = None
    for z in P["bracket_z"]:
        b = _span(tx, bx1, -15, 15, z - 20, z + 20) - _zcyl(tx, 0, z, tr + 0.5, 42)
        b += _zcyl(tx, 0, z, tr + 3, 30) - _zcyl(tx, 0, z, tr + 0.5, 32)
        b = b + _span(bx1 - 3, bx1, -30, 30, z - 25, z + 25)
        brk = b if brk is None else brk + b
    add("Stilling tube wall brackets", brk, C_STEEL, "metal", 5, "accessory", (DX, 0, DZ))

    # ------------------------------------------------------------ context (not in the BOM)
    X0, X1, HY, SD = PATCH
    gx0, gx1_, gl_, gt = P["grate"]
    gutter_x0 = gx0 - 100
    asph = _span(X0, gutter_x0, -HY, HY, -SD, 0)
    add("Asphalt road", asph, C_ASPHALT, "clay", None, "context", (0, 0, 0))
    gut = _span(gutter_x0, 0, -HY, HY, -SD, 0) - _span(gx0, gx1_, -gl_ / 2, gl_ / 2, -SD - 1, 1)
    add("Concrete gutter strip", gut, C_GUTTER, "clay", None, "context", (0, 0, 0))
    walk_ = _span(0, X1, -HY, HY, -SD, cs)
    walk_ = _fillet_try(walk_, walk_.edges().filter_by(Axis.Y).filter_by(
        lambda e: abs(e.center().X) < 1 and e.center().Z > cs - 1), [12.0, 8.0, 4.0])
    for k in range(1, 3):
        walk_ -= _span(-1, X1 + 1, -HY + k * 300 - 1.5, -HY + k * 300 + 1.5, cs - 2, cs + 1)
    add("Curb and sidewalk", walk_, C_CONCRETE, "clay", None, "context", (0, 0, 0))
    throat = _span(gx0, gx1_, -gl_ / 2, gl_ / 2, -SD, gt * -1 - 2)
    add("Catch basin throat (in shadow)", throat, C_VOID, "clay", None, "context", (0, 0, 0))
    grate = _span(gx0 + 5, gx1_ - 5, -gl_ / 2 + 5, gl_ / 2 - 5, -gt, 0)
    for k in range(7):
        grate -= _box((gx0 + gx1_) / 2, -240 + k * 80, -gt / 2, 300, 40, gt + 10)
    add("Cast iron grate", grate, C_IRON, "metal", None, "context", (0, 0, 0))
    water = _span(X0 + 20, -0.2, -HY + 20, HY - 20, 0.2, 28.0)
    water = _fillet_try(water, [e for e in _edges_par(water, Axis.Z) if e.center().X < -100], [120.0, 60.0, 20.0])
    water -= _span(gx1_ - 2, 1, cy - al / 2 - 2, cy + al / 2 + 2, -1, 20)
    add("Ponding stormwater (illustrative)", water, C_WATER, "clear", None, "context", (0, 0, 0))
    ptop = arm_top + POLE_TOP_ABOVE_ARM
    pole = _zcyl(px, 0, (cs + ptop) / 2, pr, ptop - cs)
    pole += Pos(px, 0, ptop) * Sphere(pr) & _span(px - pr, px + pr, -pr, pr, ptop - 1, ptop + pr)
    add("Street pole section (existing)", pole, C_POLE, "painted", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
