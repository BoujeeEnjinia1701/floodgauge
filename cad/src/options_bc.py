"""FloodGauge concept options B and C at detail level D3 (FLG-OPT-001, STANDARDS sections 21 and 24).

Option B: hydrostatic pressure. A vented submersible pressure transducer at the foot of a perforated stand pipe on
the curb face reads the street water, and a second one hangs in the stilling tube in the basin.
Option C: float and reed chain. A magnet in a float rides a sealed stem inside the same pipe and tube and closes a
reed switch on a 25 mm chain; the level is the highest closed switch.

Both share option A's FieldNode core, depth marker, riser guard, covers, anchors, plugs, basin stilling tube and its
two stand-off clamps; the pole bracket, arm and radar head are not needed, so the through-bolt and pole bracket
are absent. `option(key, model)` returns the part list, built on the module `model`.
"""
from __future__ import annotations

import math

from build123d import Pos, Rot
import cad_parts as cp
from cad_parts import part
from flg_parts import orient, fasten

PX = -70.0            # street stand pipe axis, mm from the curb face (road side)
PIPE_OD, PIPE_T = 50.0, 2.4
PIPE_Z0, PIPE_Z1 = 4.0, 650.0
CABLE_D = 7.0         # vented transducer cable, mm
CLAMP_Z = (110.0, 520.0)
WIN_Z = 60.0          # height at which the street cable runs along the curb face


def _keep_from_a(M, p):
    keep = ("node", "panel", "marker", "conduit")
    out = []
    for q in M.option_a(p):
        if q["kind"] == "context" or q["group"] in keep:
            out.append(q)
        elif q["key"] in ("tube", "pclamps", "pclamp_plates", "plugs"):
            out.append(q)
        elif q["group"] == "drain_head" and (q["name"].startswith("PVC socket") or q["name"].startswith("M4x12 button")):
            out.append(q)
    return out


def _notch_curb_cover(parts, M, p):
    """Cut a window in the +Y ramp of the curb cover for the street cable (z about 60)."""
    cy = p["cover_y"]
    cut = M.bx(-17.0, -1.0, cy - 5.0, cy + 26.0, WIN_Z - 8.0, WIN_Z + 8.0)
    for q in parts:
        if q["name"].startswith("Curb cover"):
            q["shape"] = q["shape"] - cut
    return parts


def _street_pipe(o, M, p, opt, py):
    z = PIPE_Z1 - 30
    pipe = Pos(PX, py, PIPE_Z0) * cp.round_tube(PIPE_OD, PIPE_T, PIPE_Z1 - PIPE_Z0)
    for k in range(9):
        zc = 50.0 + k * 70.0
        for j in range(4):
            pipe -= Pos(PX, py, zc) * Rot(0, 0, 45 + 90 * j) * Pos(PIPE_OD / 2, 0, 0) * M._b3d().Box(10, 5, 40)
    pipe -= M.ycyl(PX, py + PIPE_OD / 2, 620.0, 4.5, 6.0)
    o.add("street_unit", "Street stand pipe (PVC 50 OD x 2.4, 36 slots)", pipe, "pe_tank_white", "made", None, "street_head")
    bot = cp.break_edges(M.zcyl(PX, py, 12.0, 28.0, 24.0), 0.8) - M.zcyl(PX, py, 14.0, PIPE_OD / 2, 20.2)
    for j in range(4):
        a = math.radians(45 + 90 * j)
        bot -= M.zcyl(PX + 12 * math.cos(a), py + 12 * math.sin(a), 2.0, 3.0, 4.4)
    if opt == "C":
        bot -= M.zcyl(PX, py, 2.0, 2.8, 4.4)
    o.add("street_unit", "Stand pipe bottom cap (drain holes)", bot, "pe_tank_white", "bought", None, "street_head")
    top = cp.break_edges(M.zcyl(PX, py, 642.0, 28.0, 24.0), 0.8) - M.zcyl(PX, py, 640.0, PIPE_OD / 2, 20.2) - M.zcyl(PX, py, 652.0, 1.5, 4.4)
    o.add("street_unit", "Stand pipe top cap (vent hole)", top, "pe_tank_white", "bought", None, "street_head")
    gm = M.ycyl(PX, py + PIPE_OD / 2 + 0.5, 620.0, 4.5, 4.0) - M.ycyl(PX, py + PIPE_OD / 2 + 0.5, 620.0, 3.7, 5.0)
    o.add("street_unit", "Rubber cable grommet", cp.break_edges(gm, 0.3), "epdm", "bought", None, "street_head")
    for zz in CLAMP_Z:
        M._stand_off(o, p, PX, py, zz, PIPE_OD, 0.0, None, "street_head")


def _street_cable_route(M, p, D, py):
    cy = p["cover_y"]
    yo = py + PIPE_OD / 2 + CABLE_D + 1.0
    zw = p["curb_h"] + 7.0
    r = D["pole_r"]
    z0 = D["node_bot"]
    return yo, [(-8.0, yo, WIN_Z), (-8.0, cy + 3.0, WIN_Z), (-8.0, cy + 3.0, zw), (p["pole_x"], cy + 3.0, zw),
                (p["pole_x"], cy + 3.0, D["riser_top"] + 72), (p["pole_x"], r + 16.0, D["riser_top"] + 122), (p["pole_x"], r + 16.0, z0 - 140.0),
                (D["port_x"], r + 16.0, z0 - 140.0), (D["port_x"], D["port_y"]["A"], z0 - 140.0), (D["port_x"], D["port_y"]["A"], z0 - 45.0)]


def option(opt, M):
    p = M.PARAMS
    D = M.derived(p)
    cy = p["cover_y"]
    py = cy + 130.0
    o = M._Out()
    for q in _notch_curb_cover(_keep_from_a(M, p), M, p):
        o.append(q)
    _street_pipe(o, M, p, opt, py)
    yo, tail = _street_cable_route(M, p, D, py)
    tx, tt = D["tube_x"], p["tube_top"]
    so = p["socket"][0]

    # ---- drain tube cap and gland (replaces the drain head)
    cap = M.zcyl(tx, 0, tt + 15.0, so / 2, 30.0) - M.zcyl(tx, 0, tt + 13.0, D["tube_id"] / 2, 26.2)
    cap -= M.zcyl(tx, 0, tt + 28.0, 8.0 if opt == "C" else 6.0, 4.4)
    cap -= M.zcyl(tx + 20, 0, tt + 28.0, 1.2, 4.4)
    o.add("drain_unit", "Tube end cap 83 mm with gland hole", cp.break_edges(cap, 0.8), "pe_tank_white", "bought", None, "drain_head")
    if opt == "B":
        g = M.zcyl(tx, 0, tt + 37.5, 9.0, 15.0) - M.zcyl(tx, 0, tt + 37.5, CABLE_D / 2 + 0.2, 16.0) + M.zcyl(tx, 0, tt + 28.0, 6.0, 4.0) - M.zcyl(tx, 0, tt + 28.0, CABLE_D / 2 + 0.2, 5.0)
        o.add("drain_unit", "M12 cable gland (drain unit)", cp.break_edges(g, 0.5), "zinc_plated", "bought", None, "drain_head")
        z_top = -1115.0
        o.add("drain_unit", "Hung pressure transducer 22 dia x 120 (316L)", cp.break_edges(M.zcyl(tx, 0, z_top - 60.0, 11.0, 120.0), 1.0), "stainless", "bought", None, "drain_head")
        o.add("drain_unit", "Transducer nose cone and cable weight", cp.break_edges(M.zcyl(tx, 0, z_top - 125.0, 11.5, 10.0), 1.5), "brass", "bought", None, "drain_head")
        start = [(tx, 0, z_top), (tx, 0, tt + 46.0)]
    else:
        _stem(o, M, tx, 0.0, z_bot=-1230.0, z_top=tt + 30.0, travel=(-1210.0, -340.0), float_od=56.0, float_z=-800.0,
              reed_from=-1205.0, reed_to=-335.0, group="drain_head", plug_top=True, tag="drain unit")
        g = M.zcyl(tx, 0, tt + 38.0, 12.0, 16.0) - M.zcyl(tx, 0, tt + 38.0, CABLE_D / 2 + 0.2, 17.0)
        o.add("drain_unit", "M12 cable gland (stem head)", cp.break_edges(g, 0.5), "zinc_plated", "bought", None, "drain_head")
        start = [(tx, 0, tt + 46.0)]
    # ---- street unit internals
    if opt == "B":
        o.add("street_unit", "Pressure transducer 19 dia x 90 (316L, vented cable)", Pos(PX, py, 5.0) * cp.round_bar(19.0, 90.0, 1.0),
              "stainless", "bought", None, "street_head")
        street_in = [(PX, py, 95.0), (PX, py, 620.0), (PX, yo, 620.0), (PX, yo, WIN_Z)]
    else:
        _stem(o, M, PX, py, z_bot=PIPE_Z0, z_top=636.0, travel=(18.0, 608.0), float_od=42.0, float_z=320.0, reed_from=22.0, reed_to=618.0,
              group="street_head", plug_top=False, tag="street unit", screw_from_below=True)
        street_in = [(PX, py, 636.0), (PX, py, 640.0), (PX, py + 12.0, 640.0), (PX, py + 12.0, 620.0), (PX, yo, 620.0), (PX, yo, WIN_Z)]
    street = street_in + tail
    zc_ = 7.0
    zw = p["curb_h"] + 7.0
    r = D["pole_r"]
    z0 = D["node_bot"]
    drain = start + [(tx, 0, -100.0), (p["cable_exit_x"], 0, -100.0), (p["cable_exit_x"], cy - 5.0, -100.0), (p["cable_exit_x"], cy - 5.0, zc_),
                     (-8.0, cy - 5.0, zc_), (-8.0, cy - 5.0, zw), (p["pole_x"], cy - 5.0, zw), (p["pole_x"], cy - 5.0, D["riser_top"] + 60),
                     (p["pole_x"], r + 8.0, D["riser_top"] + 110), (p["pole_x"], r + 8.0, z0 - 100.0), (D["port_x"], r + 8.0, z0 - 100.0),
                     (D["port_x"], D["port_y"]["B"], z0 - 100.0), (D["port_x"], D["port_y"]["B"], z0 - 45.0)]
    # slack loop and ties as in option A, 7 mm cable
    la, lb, ltop, ldx = p["loop_a"], p["loop_b"], p["loop_top"], p["loop_dx"]
    lx = tx - ldx
    lc = ltop - lb
    circ = [(lx, la * math.sin(2 * math.pi * k / 24), lc + lb * math.cos(2 * math.pi * k / 24)) for k in range(25)]
    c = CABLE_D
    o.add("slack_loop", "Drain cable slack loop (0.5 m)", M.cable([(tx, 0, ltop), (lx, 0, ltop)] + circ, c), "epdm", "bought", None, "cables")
    zr_ = p["bracket_z"][0]
    ztie = lc - lb
    zt2 = zr_ + 14.0
    rt = p["tube_od"] / 2
    strap = M.zcyl(lx, 0, (ztie + zt2) / 2, 1.5, abs(ztie - zt2)) + M.xcyl((lx + tx - rt) / 2, 0, zt2, 1.5, abs(lx - (tx - rt))) \
        + (M.ycyl(lx, 0, ztie, c / 2 + 1.5, 5) - M.ycyl(lx, 0, ztie, c / 2, 6)) + (M.zcyl(tx, 0, zt2, rt + 3, 3) - M.zcyl(tx, 0, zt2, rt, 4))
    o.add("loop_tie", "Slack loop cable ties (2)", strap, "matte_black", "fastener", None, "cables")
    o.add("street_cable", "Street unit cable, vented 7 mm", M.cable(street, c), "epdm", "bought", None, "cables")
    o.add("drain_cable", "Drain unit cable, vented 7 mm", M.cable(drain, c), "epdm", "bought", None, "cables")
    return list(o)


def _stem(o, M, x, y, z_bot, z_top, travel, float_od, float_z, reed_from, reed_to, group, plug_top, tag, screw_from_below=False):
    """Option C: a sealed 16 mm stem with a reed chain on a strip, a float with a ring magnet, and two stop collars."""
    b = M._b3d()
    zb = lambda *a: M.zcyl(x, y, *a)  # noqa: E731
    stem = zb((z_bot + z_top) / 2, 8.0, z_top - z_bot) - zb((z_bot + z_top) / 2, 6.0, z_top - z_bot + 1)
    o.add("float_unit", f"Sealed stem 16 OD x 2 ({tag})", cp.break_edges(stem, 0.4), "hdpe_natural", "bought", None, group)
    plug = zb(z_bot + 6.0, 6.0, 12.0)
    if screw_from_below:
        plug -= zb(z_bot + 6.0, 2.5, 13.0)
    o.add("float_unit", f"Stem bottom plug ({tag})", cp.break_edges(plug, 0.4), "hdpe_natural", "bought", None, group)
    if screw_from_below:
        o.fast("float_unit", 5, 4.0, (x, y, 0.0), (0, 0, -1), group, None, head="button", nut=None, length=14)
    ptop = zb(z_top - 6.0, 6.0, 12.0) - zb(z_top - 6.0, CABLE_D / 2 + 0.2, 13.0)
    o.add("float_unit", f"Stem top plug with cable passage ({tag})", cp.break_edges(ptop, 0.4), "hdpe_natural", "bought", None, group)
    # reed chain strip: 8 x 1.6 PCB with a reed every 25 mm
    n = int((reed_to - reed_from) // 25.0) + 1
    zc = (reed_from + reed_to) / 2
    pcb = cp.break_edges(M.bx(x - 4.0, x + 4.0, y - 0.8, y + 0.8, reed_from - 3.0, reed_to + 3.0), 0.3)
    o.add("float_unit", f"Reed chain strip, {n} reeds at 25 mm ({tag})", pcb, "hdpe_black", "bought", None, group, color="#1F6B3A")
    reeds = M.fuse([M.zcyl(x, y + 0.8 + 1.1, reed_from + 25.0 * k, 1.1, 10.0) for k in range(n)])
    o.add("float_unit", f"Reed switches (glass, 2.2 x 10) ({tag})", reeds, "glass", "bought", None, group)
    # float: a sealed hollow shell (1.6 mm walls, two annular voids above and below the magnet pocket) filled with closed-cell foam, with a ring magnet.
    # The first pass was a solid ring; FLG-STM-001 S22 showed it sinks (43.7 g against 34.9 g of buoyancy), so the shell is hollow
    big = float_od > 50
    fh = 45.0 if big else 44.0
    wt, rp, hp = 1.6, (13.5 if big else 12.5), 7.0
    fl = zb(float_z, float_od / 2, fh) - zb(float_z, 8.9, fh + 1) - zb(float_z, rp, hp)
    seg = (fh - hp) / 2 - 2 * wt
    foam = None
    for sgn in (1, -1):
        zv = float_z + sgn * (hp / 2 + wt + seg / 2)
        void = zb(zv, float_od / 2 - wt, seg) - zb(zv, 8.9 + wt, seg)
        fl -= void
        foam = void if foam is None else foam + void
    o.add("float_unit", f"Float, sealed hollow polypropylene shell {float_od:.0f} OD ({tag})", cp.break_edges(fl, 1.0), "hdpe_natural", "made", None, group)
    # closed-cell foam fills both voids (STM review, FLG-DDR-004 F1): a leaking shell still floats and the sealed air no longer cycles in pressure
    o.add("float_unit", f"Closed-cell foam core ({tag})", foam, "insulated_white", "bought", None, group)
    mag = zb(float_z, rp - 0.1, 5.0) - zb(float_z, 8.9, 6.0)
    o.add("float_unit", f"Ring magnet ({tag})", cp.break_edges(mag, 0.4), "mild_steel", "bought", None, group)
    for zz in travel:
        col = zb(zz, 12.0, 8.0) - zb(zz, 8.0, 9.0)
        o.add("float_unit", f"Stop collar ({tag})", cp.break_edges(col, 0.5), "stainless", "bought", None, group)
