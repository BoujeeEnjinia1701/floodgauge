"""FloodGauge product appearance model (build123d), TRL 3, on the constructable design (FLG-DDR-003).

Finished-product look for photoreal renders. Every steel, aluminium and plastic part that is also in the
constructable design (pole bracket plate on its V-blocks and band clamps, arm cleats, sensor arm, knee brace
in its clips, head plate, radar head housing and lens, through-bolt and spacer, FieldNode enclosure, lid,
back plate, panel bracket and 40 degree panel, depth marker and its band clamps, riser guard, three
hat-section covers, anchors, stilling tube, pipe clamps, drain head, drain cable slack loop and its ties)
is taken from build_components() in model.py, so its size and place cannot drift from the model. This file
adds only paint, accent bands, the clear lid window, name plate, status light, the depth bands, the
cable runs and the street context (asphalt, gutter, curb, sidewalk, grate, pole, ponding water).
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X across the street (road at X < 0, curb face at X = 0), Y along the street, road
surface at the gauge point Z = 0.
Render-only layout (not the installed layout): the pole kit is drawn lower than installed so the product fits
the frame. The arm kit (bracket, arm, head) is lowered by RENDER_ARM_DROP so the lens is 1.3 m above the road
instead of 4.6 m, and the FieldNode core with its panel is lowered by RENDER_NODE_DROP so its center is 0.5 m
instead of 3.4 m. The drain head, stilling tube and slack loop stay at their model positions inside the catch
basin; they are in the "accessory" group, so they appear in the exploded view but not in the hero.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Polygon, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, derived, bands, build_components, cable

TITLE = "FloodGauge: street and drain water level sensor"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 24, "az": -140,
     "note": "Product render from the road side and above (about 24 deg elevation), looking toward the curb; "
             "radar head on its arm over the gutter and grate, solar-powered node on the pole under its 40 deg panel, "
             "cable covers and riser guard at the curb. Pole kit drawn lower than installed (lens 1.3 m instead of "
             "4.6 m above the road, node 0.5 m instead of 3.4 m)"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 22, "az": -130,
     "note": "Exploded view from the road side and above (about 22 deg elevation): node enclosure, lid and "
             "window, back plate, panel bracket and solar panel; radar head housing and lens; bracket plate, cleats, arm, "
             "brace, clips and through-bolt; depth marker and band clamps; drain head, stilling tube and slack loop (left)"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 14, "az": -150,
     "note": "Detail from the road side, slightly above (about 14 deg elevation), without the street: "
             "radar head and arm bracket (top), node and 40 deg panel (middle), depth marker and cable covers (bottom)"},
]

# Render layout (not the installed layout); see the module docstring.
RENDER_LENS_Z = 1300.0     # underside of the lens above the road (installed: PARAMS["head_z"], 4600 mm)
RENDER_ARM_DROP = PARAMS["head_z"] - RENDER_LENS_Z   # the arm kit is drawn this far below installed (3300 mm)
RENDER_NODE_DROP = 2900.0  # the FieldNode core and panel are drawn this far below installed (center 3400 to 500 mm)
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
    Cm = build_components(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    def mdl(key, name, color, material, group, explode, dz=0.0):
        """A part of the constructable design, taken from model.py and only moved for the render layout."""
        c = Cm[key]
        sh = Pos(0, 0, dz) * c.shape if dz else c.shape
        add(name, sh, color, material, c.bom, group, explode)

    zsh = lambda z: z - (RENDER_ARM_DROP if z >= 4000.0 else (RENDER_NODE_DROP if z >= 1000.0 else 0.0))  # noqa: E731
    dA, dN = -RENDER_ARM_DROP, -RENDER_NODE_DROP
    px, pr = P["pole_x"], D["pole_r"]
    pf = D["pole_face_x"]
    hx = D["head_x"]
    cs = P["curb_h"]
    cy = P["cover_y"]
    al, at = P["cover_angle"]
    az = P["arm_z"] + dA
    arm_top = az + P["arm_sq"] / 2

    # ------------------------------------------------------------ 1 FieldNode core (from the model) and render detail
    nx = D["node_x"]
    ex, ey, ez = P["enc"]
    nbot = D["node_bot"] + dN
    nz = nbot + ez / 2
    x0 = nx - ex / 2                                # front face of the lid
    mdl("fn_body", "Node enclosure body", C_SHELL, "plastic", "shell", (0, 0, 0), dN)
    mdl("fn_lid", "Node lid", C_SHELL2, "plastic", "shell", (-240, 0, 0), dN)
    wy, wz0, wz1 = 55.0, nz - 22.0, nz + 82.0
    pane = _span(x0 - 1.0, x0 + 1.0, -wy, wy, wz0, wz1)
    add("Node clear lid window (render detail)", pane, C_WINDOW, "clear", 1, "shell", (-290, 0, 0))
    plate = _span(x0 - 0.8, x0, -45, 45, nbot + 42, nbot + 56)
    add("Node name plate (render detail)", plate, C_ACCENT, "painted", 1, "shell", (-290, 0, 0))
    led = (Pos(x0 - 1.6, 0, nbot + 24) * Sphere(3.2)) & _span(x0 - 6, x0 - 0.5, -5, 5, nbot + 19, nbot + 29)
    add("Status light, green (render detail)", led, C_LED_G, "emissive", 1, "shell", (-290, 0, 0))
    mdl("fn_plate", "Node back plate", C_METAL, "metal", "shell", (0, 0, 0), dN)
    mdl("fn_vblocks", "Node V-blocks", C_STEEL, "metal", "shell", (0, 0, 0), dN)
    mdl("fn_bands", "Node band clamps", C_STEEL, "metal", "shell", (0, 0, 0), dN)
    mdl("fn_bracket", "Node panel bracket", C_METAL, "metal", "shell", (-60, 0, 60), dN)
    mdl("fn_panel", "Solar panel, 40 deg tilt", C_SOLAR, "screen", "shell", (-150, 0, 120), dN)

    # ------------------------------------------------------------ 2 street radar head
    hd, hh, lt = P["head_d"], P["head_h"], P["lens_t"]
    hr = hd / 2
    hz = RENDER_LENS_Z
    mdl("head_housing", "Radar head housing and gland", C_SHELL, "plastic", "shell", (0, 0, -110), dA)
    mdl("lens", "PTFE lens", C_PTFE, "plastic", "shell", (0, 0, -230), dA)
    band = _zcyl(hx, 0, hz + lt + 50, hr + 0.4, 6.0) - _zcyl(hx, 0, hz + lt + 50, hr - 1, 8)
    add("Radar head accent band (render detail)", band, C_ACCENT, "painted", 2, "shell", (0, 0, -110))
    mdl("head_screws", "Head housing screws", C_STEEL, "metal", "shell", (0, 0, -60), dA)

    # ------------------------------------------------------------ 3 pole bracket, arm, brace, bolt
    mdl("bplate", "Pole bracket plate", C_ALU, "metal", "shell", (0, 0, 0), dA)
    mdl("vblocks", "Bracket V-blocks", C_ALU, "metal", "shell", (60, 0, 0), dA)
    mdl("bands", "Bracket band clamps", C_STEEL, "metal", "shell", (60, 0, 0), dA)
    mdl("cleats", "Arm cleats", C_ALU, "metal", "shell", (-70, 0, 0), dA)
    mdl("top_clip", "Brace clip under the arm", C_ALU, "metal", "shell", (0, 0, -60), dA)
    mdl("foot_clip", "Brace clip on the plate", C_ALU, "metal", "shell", (-70, 0, 0), dA)
    mdl("arm", "Sensor arm (aluminium tube)", C_ALU, "metal", "shell", (0, 0, 0), dA)
    mdl("brace", "Knee brace", C_ALU, "metal", "shell", (-60, -120, -60), dA)
    mdl("head_plate", "Head plate", C_ALU, "metal", "shell", (0, 0, -60), dA)
    mdl("spacer", "Through-bolt spacer", C_ALU, "metal", "shell", (0, 0, 80), dA)
    mdl("through_bolt", "M8 anti-rotation through-bolt", C_METAL, "metal", "shell", (-120, 0, 0), dA)
    mdl("fixings", "Bracket bolts, nuts and sleeves", C_STEEL, "metal", "shell", (0, 0, 40), dA)
    mdl("pins", "Brace pins and sleeves", C_STEEL, "metal", "shell", (0, 0, 40), dA)

    # ------------------------------------------------------------ 6 sensor cables (render runs) and slack loop
    runs = Cm["_runs"]
    cr = P["cable_d"]
    street = cable([(x, y, zsh(z)) for x, y, z in runs["street"]], cr)
    add("Street head cable", street, C_BLACK, "rubber", 6, "shell", (0, 0, 0))
    dr = runs["drain"]
    k0 = next(i for i, p_ in enumerate(dr) if p_[2] >= 0.0)
    surf = cable([(x, y, zsh(z)) for x, y, z in dr[k0 - 1:]], cr)
    add("Drain head cable above ground", surf, C_BLACK, "rubber", 6, "shell", (0, 0, 0))
    basin_run = cable(dr[:k0 + 1], cr)
    add("Drain head cable in the basin", basin_run, C_BLACK, "rubber", 6, "accessory", (-520, 0, 1150))
    mdl("slack_loop", "Drain cable 0.5 m slack loop", C_BLACK, "rubber", "accessory", (-520, 0, 1150))
    mdl("loop_tie", "Slack loop cable ties", C_AMBER, "plastic", "accessory", (-520, 0, 1150))

    # ------------------------------------------------------------ 8 depth marker, bands and band clamps
    mdl("marker", "Depth marker plate", C_LABEL, "painted", "shell", (-90, 0, 0))
    B = bands(P)
    add("Depth band, amber (150 to 300 mm)", B["amber"], C_AMBER, "painted", 8, "shell", (-90, 0, 0))
    add("Depth band, red (300 to 450 mm)", B["red"], C_RED, "painted", 8, "shell", (-90, 0, 0))
    mdl("marker_bands", "Marker and guard band clamps", C_STEEL, "metal", "shell", (-40, 0, 0))

    # ------------------------------------------------------------ 7 surface cable covers and riser guard
    mdl("gutter_cover", "Gutter cover (galvanized steel)", C_GALV, "metal", "shell", (0, 0, 90))
    mdl("curb_cover", "Curb cover (galvanized steel)", C_GALV, "metal", "shell", (-90, 0, 0))
    mdl("walk_cover", "Sidewalk cover (galvanized steel)", C_GALV, "metal", "shell", (0, 0, 90))
    mdl("guard", "Riser guard", C_GALV, "metal", "shell", (0, 120, 0))
    mdl("anchors", "Masonry anchors with security nuts", C_STEEL, "metal", "shell", (0, 0, 40))

    # ------------------------------------------------------------ 4 drain head and 5 stilling tube
    DX, DZ = -520.0, 1150.0                        # exploded: drain kit lifted beside the pole kit
    mdl("drain_head", "Drain head (potted cap, socket, probe pins)", C_DARK, "plastic", "accessory", (DX, 0, DZ + 220))
    tx, tt = D["tube_x"], P["tube_top"]
    dd = P["drain_head_d"]
    dband = _zcyl(tx, 0, tt + 52, dd / 2 + 0.4, 6.0) - _zcyl(tx, 0, tt + 52, dd / 2 - 1, 8)
    add("Drain head accent band (render detail)", dband, C_ACCENT, "painted", 4, "accessory", (DX, 0, DZ + 220))
    mdl("tube", "Stilling tube (slotted PVC)", C_PVC, "plastic", "accessory", (DX, 0, DZ))
    mdl("pclamps", "Stand-off pipe clamps", C_STEEL, "metal", "accessory", (DX, 0, DZ))

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
