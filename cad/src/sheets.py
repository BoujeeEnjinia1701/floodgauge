"""FloodGauge general arrangement sheet FLG-DWG-001, Rev P2 (TRL 3, FLG-DDR-002 decisions applied).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/FLG-DWG-001.svg, .pdf and .png from the parametric model in cad/src/model.py
with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so they follow any parameter
change. The concept blueprint in media/ is FLG-DWG-010. PRELIMINARY, NOT FOR FABRICATION.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, INK, MUTED  # noqa: E402
from model import PARAMS as P, derived, build_parts, bands, site  # noqa: E402

DATE = "2026-09-25"
WORK = ROOT / "cad" / "drawings" / "_views"
SETUPS = {"front": ((0, -1, 0), (0, 0, 1)), "top": ((0, 0, 1), (0, 1, 0)), "right": ((1, 0, 0), (0, 0, 1)),
          "iso": ((1, -1, 0.8), (0, 0, 1))}


def project(shape, view, name, line_weight=0.35):
    """One hidden-line view of shape, edge by edge so that a degenerate edge is skipped. Returns the SVG path."""
    from build123d import ExportSVG, LineType, Unit
    WORK.mkdir(parents=True, exist_ok=True)
    bb = shape.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    (dx, dy, dz), up = SETUPS[view]
    visible, hidden = shape.project_to_viewport((c.X + dx * d, c.Y + dy * d, c.Z + dz * d), up, (c.X, c.Y, c.Z))
    ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
    ex.add_layer("Visible", line_color=0x111827)
    ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
    for layer, edges in (("Visible", visible), ("Hidden", hidden if view != "iso" else [])):
        for e in edges:
            try:
                ex.add_shape(e, layer=layer)
            except (AssertionError, ValueError, ZeroDivisionError):
                pass
    p = WORK / f"{name}.svg"
    ex.write(str(p))
    return p


def place(sheet, svg, x, y, k, label, sub):
    """Place a view at exact scale k with its top-left at (x, y); return mapping helpers."""
    vx, vy, vw, vh = _viewbox(Path(svg).read_text())
    sheet.add_svg(svg, x, y, scale=k, label=label, sublabel=sub)
    return vw * k, vh * k


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.1, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.1, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def line(x1, y1, x2, y2, w=0.35, color=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{w}"{d}/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 1.9, 400, INK, anchor)]


def main():
    from build123d import Box, Compound, Pos
    D = derived(P)
    K = build_parts()
    Bd = bands()
    S = site()
    kit = list(K.values()) + list(Bd.values())
    overall = Compound(children=kit + [S["pole"], S["basin"], S["grate"]])
    s = Sheet(project="FloodGauge", title="General arrangement", dwg_no="FLG-DWG-001", rev="P3",
              author="Amish Chadha", date=DATE, scale=1 / 50, theme="technical",
              material="Aluminium arm, PVC tube, bought-in heads per bom/bom.csv; existing street shown for context. "
                       "PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "DDR-002: lens 4.6 m, node 3.0 m, surface cable cover, anti-rotation bolt", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC")])
    L = []
    L.append(_t(16, 24, "PRELIMINARY, NOT FOR FABRICATION", 2.6, 600, "#B45309"))

    # ---------------- overall views at 1:50
    k = 1 / 50
    bb = overall.bounding_box()
    top = project(overall, "top", "o_top")
    front = project(overall, "front", "o_front")
    right = project(overall, "right", "o_right")
    x0, yt = 24.0, 34.0
    tw, th = place(s, top, x0, yt, k, "Top view", "Scale 1:50")
    yf = yt + th + 16
    fw, fh = place(s, front, x0, yf, k, "Front view", "Scale 1:50; looking along the street")
    xr = x0 + fw + 16
    rw, rh = place(s, right, xr, yf, k, "Right view", "Scale 1:50")
    X = lambda mx: x0 + (mx - bb.min.X) * k
    Z = lambda mz: yf + fh - (mz - bb.min.Z) * k
    # road and sidewalk surfaces
    L.append(line(X(bb.min.X) - 3, Z(0), X(0), Z(0), 0.35))
    L.append(line(X(0), Z(0), X(0), Z(P["curb_h"]), 0.35))
    L.append(line(X(0), Z(P["curb_h"]), X(bb.max.X) + 3, Z(P["curb_h"]), 0.35))
    L.append(_t(X(bb.min.X) - 3, Z(0) - 1, "ROAD, Z = 0 (DATUM)", 1.8, 600, MUTED))
    L.append(_t(X(bb.max.X) + 5, Z(P["curb_h"]) - 1, "SIDEWALK", 1.8, 600, MUTED, "start"))
    xd = X(bb.min.X) - 4
    L += [ext(X(D["head_x"]), Z(P["head_z"]), xd - 1, Z(P["head_z"]))]
    L += dim_v(xd, Z(P["head_z"]), Z(0), f"{P['head_z']:,.0f} lens to road")
    L += [ext(X(D["node_x"]), Z(P["node_z"]), xd - 7, Z(P["node_z"]))]
    L += dim_v(xd - 6, Z(P["node_z"]), Z(0), f"{P['node_z']:,.0f} node center")
    L += [ext(X(D["tube_x"]), Z(P["tube_top"]), xd - 1, Z(P["tube_top"]))]
    L += dim_v(xd, Z(0), Z(P["tube_top"]), f"{-P['tube_top']:.0f}")
    zt = D["overall_top"] + 250
    L += [ext(X(0), Z(P["curb_h"]), X(0), Z(zt) - 1), ext(X(D["head_x"]), Z(D["head_top"]), X(D["head_x"]), Z(zt) - 1)]
    L += dim_h(X(D["head_x"]), X(0), Z(zt), f"{P['head_offset']:.0f}")
    L += leader(X(0), Z(zt) + 2, X(0) + 3, Z(zt) - 4, "CURB FACE")
    # ---------------- Detail A: street head, arm and node, 1:10
    ka = 1 / 10
    stub = Pos(P["pole_x"], 0, P["arm_z"] - 200) * Box(P["pole_od"], P["pole_od"], 700) & S["pole"]
    detA = Compound(children=[K["street_head"], K["arm"], stub])
    bba = detA.bounding_box()
    fa = project(detA, "front", "a_front")
    xa, ya = 118.0, 36.0
    aw, ah = place(s, fa, xa, ya, ka, "Detail A: street head, arm and clamps", "Scale 1:10; front view")
    Xa = lambda mx: xa + (mx - bba.min.X) * ka
    Za = lambda mz: ya + ah - (mz - bba.min.Z) * ka
    L += [ext(Xa(D["arm_x0"]), Za(D["arm_top"]), Xa(D["arm_x0"]), Za(D["arm_top"] + 70)),
          ext(Xa(D["arm_x1"]), Za(D["arm_top"]), Xa(D["arm_x1"]), Za(D["arm_top"] + 70))]
    L += dim_h(Xa(D["arm_x0"]), Xa(D["arm_x1"]), Za(D["arm_top"] + 60), f"{D['arm_len']:.0f} arm")
    L += dim_h(Xa(D["head_x"]), Xa(P["pole_x"]), Za(D["arm_top"] + 25), f"{D['cantilever']:.0f} head to pole axis")
    zc2 = P["arm_z"] - P["clamp_dz"]
    xcl = Xa(bba.max.X) + 5
    L += [ext(Xa(P["pole_x"] + D["pole_r"] + 8), Za(P["arm_z"]), xcl + 1, Za(P["arm_z"])),
          ext(Xa(P["pole_x"] + D["pole_r"] + 8), Za(zc2), xcl + 1, Za(zc2))]
    L += dim_v(xcl, Za(P["arm_z"]), Za(zc2), f"{P['clamp_dz']:.0f} clamps", side=1)
    L += leader(Xa(D["head_x"]), Za(P["head_z"]), Xa(D["head_x"]) + 3, Za(P["head_z"]) + 18,
                f"2 RADAR HEAD D{P['head_d']:.0f}", "start")
    L += leader(Xa(P["pole_x"]), Za(zc2), Xa(P["pole_x"]) + 8, Za(zc2) + 8, "M8 THROUGH-BOLT, ANTI-ROTATION", "start")
    L += leader(Xa(-100), Za(P["arm_z"] - P["arm_sq"] / 2), Xa(-100) + 3, Za(P["arm_z"]) + 5,
                f"3 ARM {P['arm_sq']:.0f} x {P['arm_sq']:.0f} x {P['arm_wall']:.0f}", "start")
    L += leader(Xa(D["pole_face_x"] - P["brace_leg"] / 2), Za(P["arm_z"] - P["brace_leg"] / 2),
                Xa(D["pole_face_x"] - P["brace_leg"] / 2) - 12, Za(P["arm_z"] - P["brace_leg"] / 2) - 2,
                f"KNEE BRACE {P['brace_sq']:.0f} SQ, 45 DEG", "end")

    # ---------------- Section B: drain head and stilling tube, 1:20
    kb = 1 / 20
    half = site(basin_half=True)
    road_half = half["road"] & (Pos(-450, 0, -100) * Box(900, 4000, 400))
    detB = Compound(children=[K["drain_head"], K["tube"], half["basin"], half["grate"], road_half])
    bbb = detB.bounding_box()
    fb = project(detB, "front", "b_front")
    xb, yb = 124.0, 160.0
    bw, bh = place(s, fb, xb, yb, kb, "Section B: catch basin, drain head and tube", "Scale 1:20; basin cut on the street axis")
    Xb = lambda mx: xb + (mx - bbb.min.X) * kb
    Zb = lambda mz: yb + bh - (mz - bbb.min.Z) * kb
    xbd = Xb(bbb.max.X) + 5
    for i, (zz, txt) in enumerate(((P["tube_top"], f"{-P['tube_top']:.0f}"),
                                   (D["dh_top_level"], f"{-D['dh_top_level']:.0f}"),
                                   (D["tube_bot"], f"{-D['tube_bot']:,.0f} mouth"))):
        xx = xbd + 11 * i
        L += [ext(Xb(D["tube_x"]), Zb(zz), xx + 1, Zb(zz))]
        L += dim_v(xx, Zb(0), Zb(zz), txt, side=1)
    L.append(line(Xb(bbb.min.X) - 3, Zb(0), xbd + 30, Zb(0), 0.18, MUTED, "1.5 1"))
    L.append(_t(Xb(bbb.min.X) - 3, Zb(0) - 0.8, "ROAD Z = 0", 1.6, 600, MUTED, "start"))
    zm = (P["tube_top"] + D["tube_bot"]) / 2
    L += leader(Xb(D["tube_x"] - P["tube_od"] / 2), Zb(zm), Xb(D["tube_x"]) - 8, Zb(zm),
                f"5 TUBE {P['tube_od']:.0f} OD x {D['tube_len']:.0f}", "end")
    L += leader(Xb(D["tube_x"] - P["drain_head_d"] / 2), Zb(P["tube_top"] + 45), Xb(D["tube_x"]) - 8, Zb(P["tube_top"] - 60),
                "4 DRAIN HEAD", "end")
    L.append(_t(Xb(D["tube_x"]) - 5, Zb(-1050) + 1, "WATER ENTERS VIA SLOTS", 1.6, 400, MUTED, "end"))

    s._layers += L
    iso = project(Compound(children=kit + [S["pole"]]), "iso", "iso")
    s.add_svg(iso, 276, 32, 140, 100, label="Isometric view", sublabel="Kit on the existing pole; not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Datum: road surface at the gauge point, Z = 0; curb {P['curb_h']:.0f}",
        f"Radar lens {P['head_z']:,.0f} above road, {P['head_offset']:.0f} past curb face",
        f"Street depth 0 to 600: range {D['range_dry']:,.0f} to {D['range_600']:,.0f}",
        f"FieldNode 150 x 90 x 200 on {P['pole_od']:.0f} pole, center {P['node_z']:,.0f}",
        f"Arm {P['arm_sq']:.0f} sq x {D['arm_len']:.0f}; band clamps {P['clamp_dz']:.0f} apart",
        f"Tube {P['tube_od']:.0f} OD, ID {D['tube_id']:.0f}, {D['tube_len']:.0f} long, 40 slots 5 x 50",
        f"Drain reading {-D['dh_top_level']:.0f} to {-(P['basin_floor'] + 50):,.0f} below road; probe {-D['probe_level']:.0f}",
        f"Pilot cable route: steel cover {D['cover_len']:,.0f} long, curb and sidewalk anchors; riser guard",
        "Marker bands 150 to 300 amber, 300 to 450 red",
        f"Lens height {P['head_band'][0]:,.0f} to {P['head_band'][1]:,.0f} per site, clearance rule (FLG-CAL-001 A7)",
    ], x=276, y=150, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "FLG-DWG-001")
    shutil.rmtree(WORK, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png; overall 1:50, detail A 1:10, section B 1:20")


if __name__ == "__main__":
    main()
