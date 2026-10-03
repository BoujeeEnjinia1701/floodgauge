"""FloodGauge prototype build plan pictures (FLG-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...] [only=NAME]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component laid out, numbered in build order
    cad/drawings/FLG-DWG-101 to 116        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import gc
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, derived, build_components, site, bx, fuse, cable  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
_ALL = build_components(P)
C = {k: v for k, v in _ALL.items() if not k.startswith("_")}
RUNS = _ALL["_runs"]
ST = site(P)
SH = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731

COL = {"bplate": "#A8A29E", "vblocks": "#57534E", "bands": "#9CA3AF", "cleats": "#1D4ED8", "clips": "#7C3AED",
       "arm": "#D4A017", "brace": "#B45309", "head_plate": "#64748B", "head": "#0F766E", "lens": "#F5F5F4",
       "spacer": "#DC2626", "bolt": "#111827", "fn": "#D1D5DB", "panel": "#1E3A8A", "marker": "#F9FAFB",
       "guard": "#6B7280", "covers": "#7C3AED", "tube": "#F59E0B", "drain": "#C2410C", "pclamps": "#374151",
       "cable": "#111827", "tie": "#F59E0B", "pole": "#9CA3AF"}

xr, xf = D["plate_rear_x"], D["plate_front_x"]
px, r = P["pole_x"], D["pole_r"]
az = D["arm_z"]
(xt, zt), (xft, zft) = D["pin_top"], D["pin_foot"]
zlo, zhi = D["bplate_z"]
cy = P["cover_y"]
tx = D["tube_x"]


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    return shape & bx(x0, x1, y0, y1, z0, z1)


def pole_seg(z0, z1):
    return win(ST["pole"], px - 40, px + 40, -40, 40, z0, z1)


def flat(shape, origin, x_dir, z_dir):
    import build123d as b
    return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_local_coords(shape)


def to_origin(shape):
    import build123d as b
    c = shape.bounding_box().center()
    return b.Pos(-c.X, -c.Y, -c.Z) * shape


def moved(shape, target):
    import build123d as b
    c = shape.bounding_box().center()
    return (target[0] - c.X, target[1] - c.Y, target[2] - c.Z)


# ----------------------------------------------------------------- named components, in build order
def made():
    fn = SH("fn_plate", "fn_vblocks", "fn_bands", "fn_body", "fn_lid", "fn_bracket", "fn_panel")
    return [
        ("bplate", "Pole bracket plate", C["bplate"].shape, COL["bplate"]),
        ("vblocks", "V-blocks (2)", C["vblocks"].shape, COL["vblocks"]),
        ("cleats", "Arm cleats (2)", C["cleats"].shape, COL["cleats"]),
        ("clips", "Brace clips (2)", SH("top_clip", "foot_clip"), COL["clips"]),
        ("arm", "Sensor arm", C["arm"].shape, COL["arm"]),
        ("brace", "Knee brace", C["brace"].shape, COL["brace"]),
        ("head_plate", "Head plate", C["head_plate"].shape, COL["head_plate"]),
        ("head", "Street radar head (housing and lens)", SH("head_housing", "lens"), COL["head"]),
        ("spacer", "Through-bolt spacer", C["spacer"].shape, COL["spacer"]),
        ("marker", "Depth marker plate", C["marker"].shape, "#E5E7EB"),
        ("guard", "Riser guard", C["guard"].shape, COL["guard"]),
        ("tube", "Stilling tube", C["tube"].shape, COL["tube"]),
        ("drain", "Drain head", C["drain_head"].shape, COL["drain"]),
        ("gutter", "Gutter cover", C["gutter_cover"].shape, COL["covers"]),
        ("curb", "Curb cover", C["curb_cover"].shape, "#6D28D9"),
        ("walk", "Sidewalk cover", C["walk_cover"].shape, "#8B5CF6"),
        ("fn", "FieldNode core (built to FND-BLD-001)", fn, COL["fn"]),
        ("bands", "Bracket band clamps (2)", C["bands"].shape, COL["bands"]),
        ("tbolt", "M8 through-bolt", C["through_bolt"].shape, COL["bolt"]),
        ("mbands", "Marker band clamps (2)", C["marker_bands"].shape, "#4B5563"),
        ("pclamps", "Stand-off pipe clamps (2)", C["pclamps"].shape, COL["pclamps"]),
    ]


# ----------------------------------------------------------------- overview
def overview():
    import build123d as b
    M = made()
    # a compact layout seen from the road side: pole kit across the top, sidewalk parts in the
    # middle, drain kit and the bought parts below. Positions are display only.
    pos = {"bplate": (0, 0, 1450), "vblocks": (200, 0, 1680), "cleats": (200, 0, 1500), "clips": (200, 0, 1330),
           "arm": (820, 0, 1700), "brace": (760, 0, 1420), "head_plate": (1330, 0, 1700), "head": (1330, 0, 1480),
           "spacer": (330, 0, 1700), "marker": (0, 0, 850), "guard": (200, 0, 850), "tube": (800, 0, 520),
           "drain": (1400, 0, 560), "gutter": (500, 0, 1050), "curb": (750, 0, 1000), "walk": (650, 0, 820),
           "fn": (-480, 0, 1150), "bands": (330, 0, 1520), "tbolt": (330, 0, 1330), "mbands": (200, 0, 560),
           "pclamps": (1400, 0, 800)}
    one = {"vblocks": C["vblocks"].shape & bx(xr - 1, xr + 40, -40, 40, D["band_z"][0] - 15, D["band_z"][0] + 15),
           "clips": C["foot_clip"].shape,
           "bands": C["bands"].shape & bx(0, 600, -100, 100, D["band_z"][0] - 10, D["band_z"][0] + 10),
           "mbands": C["marker_bands"].shape & bx(0, 600, -100, 200, P["marker_bands_z"][0] - 10, P["marker_bands_z"][0] + 10),
           "pclamps": C["pclamps"].shape & bx(-300, 0, -100, 100, P["bracket_z"][0] - 20, P["bracket_z"][0] + 20),
           "cleats": C["cleats"].shape}
    parts = []
    for k, name, sh, col in M:
        sh = one.get(k, sh)
        if k in ("marker", "bplate"):
            sh = b.Rot(0, 0, 65) * sh       # turn the flat plates so their faces show
        if k == "tube":
            sh = b.Rot(0, 90, 0) * sh       # lay the tube down
        parts.append(part(name, sh, col, moved(sh, pos[k])))
    return bv.overview(parts, OUT / "overview.png", "FloodGauge prototype: every component, laid out in build order",
                       subtitle="Numbered in build order (1 to 16 made here, 17 to 21 bought or built to the FieldNode plan); one of each pair shown. "
                                "Cables and small fixings not shown",
                       elev=14, azim=-75, size=(12, 8), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    base = dict(project="FloodGauge", date=DATE)
    out = []
    zb1, zb0 = D["band_z"]
    up = lambda z: z - zlo  # noqa: E731   height up the bracket plate from its bottom edge
    ctx_pole = pole_seg(zlo - 60, zhi + 60)
    bracket_ctx = [part("pole", ctx_pole, COL["pole"]), part("arm", C["arm"].shape & bx(0, 420, -30, 30, az - 30, az + 30), COL["arm"])]

    def sheet(key, prt, neigh, dwg, title, material, notes, **kw):
        if only and key not in only:
            return
        out.append(bv.component_sheet(prt, neigh, dwg_no=dwg, title=title, material=material, notes=notes, **kw, **base))
        gc.collect()

    wz = sorted(((D["bolt_z"] + P["foot_z"] + 25) / 2, (D["bolt_z"] + az - 30) / 2))
    ww, wh = P["bplate_window"]
    sheet("bplate", Part("Pole bracket plate", C["bplate"].shape, COL["bplate"]),
          bracket_ctx + [part("V-blocks", C["vblocks"].shape, COL["vblocks"]), part("cleats", C["cleats"].shape, COL["cleats"]),
                         part("clip", C["foot_clip"].shape, COL["clips"])],
          "FLG-DWG-101", "FloodGauge pole bracket plate: making sketch", "Aluminium sheet 3 mm, 5052 or 6061 class",
          [f"Blank 100 x {D['bplate_h']:.0f} mm, 3 mm aluminium. Front view is the face toward the road.",
           "Heights up from the bottom edge; sideways from the centre line.",
           f"Band slots 3 x 15 mm at 40 mm each side, centred {up(zb0):.0f} and {up(zb1):.0f} mm up:",
           "  chain drill 3 mm and file square. The band clamps pass through these.",
           f"V-block screws 4.5 mm at 18 mm each side, {up(zb0):.0f} and {up(zb1):.0f} mm up; countersink",
           "  from the front so the M4 heads sit flush under the band.",
           f"Brace clip bolts 6.6 mm on the centre line, {up(P['foot_z'] - 17):.0f} and {up(P['foot_z'] + 17):.0f} mm up.",
           f"Through-bolt hole 8.5 mm on the centre line, {up(D['bolt_z']):.0f} mm up.",
           f"Arm cleat bolts 6.6 mm at 38 mm each side, {up(az - 18):.0f} and {up(az + 18):.0f} mm up.",
           f"Two windows {ww:.0f} x {wh:.0f} mm, centred {up(wz[0]):.0f} and {up(wz[1]):.0f} mm up (saves weight):",
           "  drill 10 mm in the corners, cut between with a jigsaw, file straight.",
           "Deburr every hole and edge; round the corners to about 2 mm.",
           "Check: lay the V-blocks, cleats and clip on it; every hole lines up."],
          view_shape=flat(C["bplate"].shape, (xr, 0, zlo), (0, 1, 0), (0, 0, 1)), inset_view=(20, -40))

    vb = C["vblocks"].shape & bx(xr - 1, xr + 40, -40, 40, zb1 - 15, zb1 + 15)
    sheet("vblocks", Part("V-block", vb, COL["vblocks"]),
          [part("plate", win(C["bplate"].shape, xf - 1, xr + 1, -60, 60, zb1 - 60, zb1 + 60), COL["bplate"]),
           part("pole", pole_seg(zb1 - 80, zb1 + 80), COL["pole"]),
           part("band", win(C["bands"].shape, 300, 500, -80, 80, zb1 - 20, zb1 + 20), COL["bands"])],
          "FLG-DWG-102", "FloodGauge V-block (make 2): making sketch", "Aluminium flat bar 60 x 40 mm, 6082 or 6061",
          ["Make two; the same block as FieldNode's (FND-DWG-102). Saw a 20 mm",
           "  slice off 60 x 40 mm bar; saw and file to 60 wide x 33 deep x 20 tall.",
           "  The flat back goes on the bracket plate.",
           "Scribe a 90 degree V on both 60 x 33 faces with a 45 degree square:",
           "  50.4 mm wide at the front face, point 7.8 mm from the back face.",
           "Saw just inside the lines, file to them; keep the V faces flat.",
           "Break the V's front edges 0.5 mm so they cannot score the pole.",
           "Drill 3.3 mm 14 deep and tap M4 12 deep in the back face, at 18 mm",
           "  each side of centre, half way up (10 mm).",
           f"Fit: two M4 countersunk screws from the front of the plate. The {P['pole_od']:.0f} mm",
           f"  pole touches both V faces {D['v_contact']:.0f} mm from the plate; 40 to 71 mm poles seat.",
           "Check: on a 60 mm tube the block must not rock."],
          view_shape=to_origin(vb), inset_view=(30, -130))

    cl = C["cleats"].shape & bx(xf - 40, xf + 1, 0, 60, az - 40, az + 40)
    sheet("cleats", Part("Arm cleat", cl, COL["cleats"]),
          [part("plate", win(C["bplate"].shape, xf - 1, xr + 1, -60, 60, az - 70, az + 70), COL["bplate"]),
           part("arm", win(C["arm"].shape, 250, 400, -30, 30, az - 30, az + 30), COL["arm"]),
           part("other cleat", C["cleats"].shape & bx(xf - 40, xf + 1, -60, 0, az - 40, az + 40), COL["cleats"])],
          "FLG-DWG-103", "FloodGauge arm cleat (make 2, a left and a right): making sketch", "Aluminium equal angle 30 x 30 x 3 mm",
          [f"Cut two {P['cleat_len']:.0f} mm lengths of 30 x 30 x 3 angle; square and deburr the ends.",
           "Plate leg (goes flat on the bracket plate): two 6.6 mm holes, 12 mm",
           "  in from its free edge, 12 and 48 mm up from the bottom end.",
           "Arm leg (lies along the arm's side): two 6.6 mm holes, 15 mm out from",
           "  the face that sits on the plate, 20 and 40 mm up from the bottom end.",
           "Left and right cleats are mirror images: drill them clamped as a pair.",
           f"Fit: plate legs flat on the plate front, {az - P['cleat_len'] / 2 - zlo:.0f} to {az + P['cleat_len'] / 2 - zlo:.0f} mm up it, arm legs",
           "  40 mm apart; two M6 bolts each through the plate (nuts behind);",
           "  the arm slides between the arm legs and two M6 bolts with crush",
           "  sleeves pass through cleat, arm and cleat.",
           "Check: both cleats square to the plate, arm legs parallel, 40 mm apart."],
          view_shape=to_origin(cl), inset_view=(20, -125))

    ct, ci, clen, ce = P["clip"]
    sheet("clips", Part("Brace clip", C["foot_clip"].shape, COL["clips"]),
          [part("plate", win(C["bplate"].shape, xf - 1, xr + 1, -60, 60, zft - 70, zft + 70), COL["bplate"]),
           part("brace", win(C["brace"].shape, xft - 80, xf, -20, 20, zft - 20, zft + 80), COL["brace"])],
          "FLG-DWG-104", "FloodGauge brace clip (make 2): making sketch", "Aluminium strip 3 mm x 50 mm, 5052 class",
          [f"Make two the same. Cut a 50 x 90 mm blank from 3 mm strip.",
           f"Fold it to a U: base {ci + 2 * ct:.1f} mm wide outside, inside gap {ci} mm,",
           f"  ears {ce:.0f} mm deep from the outside of the base. Fold in a vice over",
           "  a 25 mm steel block so the gap comes out right.",
           "Base: two 6.6 mm holes on the centre line, 17 mm each side of the middle.",
           f"Ears: one 6.6 mm hole through both, at mid-length, {P['clip_pin'] + ct:.0f} mm out from",
           "  the outside of the base. Drill both ears in one pass after folding.",
           "Fit: one clip under the arm, base up, ears hanging down (two M6 bolts",
           "  up through the arm, crush sleeves, nuts on top). The other on the",
           "  bracket plate, ears forward (two M6 bolts, nuts behind the plate).",
           "  The brace end sits between the ears on one M6 pin with a sleeve.",
           "Check: a 25 mm square tube slides between the ears without play."],
          view_shape=to_origin(C["foot_clip"].shape), inset_view=(20, -125))

    hdx = P["head_bolt_dx"]
    x1 = D["arm_x1"]
    sheet("arm", Part("Sensor arm", C["arm"].shape, COL["arm"]),
          [part("cleats", C["cleats"].shape, COL["cleats"]), part("head plate", C["head_plate"].shape, COL["head_plate"]),
           part("head", SH("head_housing", "lens"), COL["head"]), part("brace", C["brace"].shape, COL["brace"]),
           part("clips", SH("top_clip", "foot_clip"), COL["clips"]), part("plate", C["bplate"].shape, COL["bplate"])],
          "FLG-DWG-105", "FloodGauge sensor arm: making sketch", "Aluminium square tube 40 x 40 x 1.6 mm, 6063-T6",
          [f"Cut {D['arm_len']:.0f} mm of 40 x 40 x 1.6 tube; square and deburr both ends.",
           "Measure from the pole end (the end that goes between the cleats).",
           "Cleat bolts: two 6.6 mm holes across the side faces, 13 mm from the pole",
           "  end, 10 mm above and below the centre line. Drill through both sides.",
           f"Brace clip bolts: two 6.6 mm holes down through top and bottom, on the",
           f"  centre line, {x1 - (xt + 17):.0f} and {x1 - (xt - 17):.0f} mm from the pole end.",
           f"Head plate bolts: two 6.6 mm holes down through top and bottom, on the",
           f"  centre line, {x1 - (D['head_x'] + hdx):.0f} and {x1 - (D['head_x'] - hdx):.0f} mm from the pole end.",
           "Use a drill stand so every hole goes square through both walls.",
           "Fit a 6 mm aluminium crush sleeve inside at every bolt so the tube",
           "  walls are not squeezed in; push a plastic cap into the road end.",
           f"The radar head axis is {D['cantilever']:.0f} mm from the pole axis.",
           "Check: lay it on the bench; the hole rows line up along the centre."],
          view_shape=to_origin(C["arm"].shape), inset_view=(18, -60))

    L = D["brace_pins"]
    import math
    u = (-1 / math.sqrt(2), 0, 1 / math.sqrt(2))
    sheet("brace", Part("Knee brace", C["brace"].shape, COL["brace"]),
          [part("arm", C["arm"].shape, COL["arm"]), part("clips", SH("top_clip", "foot_clip"), COL["clips"]),
           part("plate", C["bplate"].shape, COL["bplate"])],
          "FLG-DWG-106", "FloodGauge knee brace: making sketch", "Aluminium square tube 25 x 25 x 1.6 mm, 6063-T6",
          [f"Cut {L + 24:.0f} mm of 25 x 25 x 1.6 tube; cut both ends square, deburr.",
           f"Drill a 6.6 mm hole across through both walls 12 mm from each end:",
           f"  the two holes are {L:.1f} mm apart. Drill with the tube flat in a vice.",
           "Fit a 6 mm aluminium crush sleeve (21.8 mm long) at each hole.",
           "Fit: the brace runs at 45 degrees from the clip on the bracket plate",
           f"  up to the clip under the arm ({D['brace_leg']:.0f} mm up and {D['brace_leg']:.0f} mm out),",
           "  on one M6 pin at each end. It holds the arm level and takes the",
           "  load of anything hanging on the head.",
           "Check: hole centres within 0.5 mm; with the arm level, both pins",
           "  slide in by hand."],
          view_shape=flat(C["brace"].shape, ((xt + xft) / 2, 0, (zt + zft) / 2), u, (0, 1, 0)), inset_view=(15, -70))

    hl, hw, ht = P["head_plate"]
    sheet("head_plate", Part("Head plate", C["head_plate"].shape, COL["head_plate"]),
          [part("arm", win(C["arm"].shape, D["head_x"] - 100, D["head_x"] + 120, -30, 30, az - 30, az + 30), COL["arm"]),
           part("head", SH("head_housing", "lens"), COL["head"])],
          "FLG-DWG-107", "FloodGauge head plate: making sketch", "Aluminium sheet 3 mm, 5052 or 6061 class",
          [f"Cut {hl:.0f} x {hw:.0f} mm from 3 mm sheet; round the corners, deburr.",
           f"Two 6.6 mm holes on the long centre line, {hdx:.0f} mm each side of the middle",
           "  (they line up with the head plate holes in the arm).",
           "Four 4.5 mm holes, countersunk on the top face, 18 mm each side of the",
           "  middle along the plate and 27 mm each side across it.",
           "  Check the radar housing's lid bosses before drilling and move these",
           "  four holes to suit the housing you buy.",
           "Fit: under the arm, long side along it, centred on the head axis;",
           "  two M6 bolts up through plate and arm, crush sleeves, nuts on top.",
           "  The housing hangs below on four M4 countersunk screws.",
           "Check: plate flat; the housing sits square under it."],
          view_shape=to_origin(C["head_plate"].shape), inset_view=(-25, -60))

    sheet("head", Part("Street radar head", SH("head_housing", "lens"), COL["head"]),
          [part("plate", C["head_plate"].shape, COL["head_plate"]),
           part("arm", win(C["arm"].shape, D["head_x"] - 100, D["head_x"] + 120, -30, 30, az - 30, az + 30), COL["arm"])],
          "FLG-DWG-108", "FloodGauge street radar head: making sketch", "Bought IP67 round housing 76 mm; PTFE disc 60 x 6 mm",
          [f"Housing: a round IP67 box about {P['head_d']:.0f} mm across and {P['head_h'] - P['lens_t']:.0f} mm tall, with",
           "  a base that can be drilled and four lid bosses on top.",
           f"Drill a {P['lens_window']:.0f} mm window in the centre of the base (hole saw, slow).",
           f"Lens: a {P['lens_d']:.0f} x {P['lens_t']:.0f} mm PTFE disc (cut from rod or bought). Bed it on",
           "  neutral-cure silicone over the window outside the base and hold it",
           "  with three M3 stainless screws on a 53 mm circle.",
           "Drill an M12 gland hole in the side, half way up, facing the pole.",
           "Mount the radar module on its carrier on four standoffs inside the",
           "  base, its antenna face centred over the window.",
           "Fit: the housing top screws to the head plate (four M4 countersunk).",
           f"  The underside of the lens is the datum: {P['head_z']:,.0f} mm above the road.",
           "Check: lens flat and square to the housing; gland seals on a 10 mm cable."],
          view_shape=to_origin(SH("head_housing", "lens")), inset_view=(-20, -60))

    sheet("spacer", Part("Through-bolt spacer", C["spacer"].shape, COL["spacer"]),
          [part("plate", win(C["bplate"].shape, xf - 1, xr + 1, -50, 50, D["bolt_z"] - 50, D["bolt_z"] + 50), COL["bplate"]),
           part("pole", pole_seg(D["bolt_z"] - 80, D["bolt_z"] + 80), COL["pole"]),
           part("bolt", C["through_bolt"].shape, COL["bolt"])],
          "FLG-DWG-109", "FloodGauge through-bolt spacer: making sketch", "Aluminium tube 12 mm OD, 8.5 mm bore",
          [f"Cut {D['spacer_len']:.1f} mm of 12 mm aluminium tube (8.5 mm bore, or drill",
           "  the bore out to 8.5 mm). Face both ends square.",
           "It fills the gap between the back of the bracket plate and the pole",
           "  at the through-bolt, so tightening the bolt does not bend the plate.",
           "File the pole end to a shallow curve if it rocks on the pole.",
           "Fit: on the M8 through-bolt between the plate and the pole.",
           f"Check: length {D['spacer_len']:.1f} mm, within 0.5 mm; on a 60 mm pole the plate",
           "  stays flat when the bolt is tight."],
          view_shape=to_origin(C["spacer"].shape), inset_view=(45, -90))

    mt, mw, mh = P["marker"]
    m0 = P["marker_z0"]
    sheet("marker", Part("Depth marker plate", C["marker"].shape, "#E5E7EB"),
          [part("pole", win(ST["pole"], px - 40, px + 40, -40, 40, 150, 700), COL["pole"]),
           part("guard", C["guard"].shape, COL["guard"]), part("bands", C["marker_bands"].shape, COL["bands"])],
          "FLG-DWG-110", "FloodGauge depth marker plate: making sketch", "Aluminium sheet 2 mm with reflective film",
          [f"Cut {mw:.0f} x {mh:.0f} mm from 2 mm aluminium; round the corners, deburr.",
           f"The bottom edge sits {m0:.0f} mm above the road ({m0 - P['curb_h']:.0f} mm above the sidewalk), so",
           "  the sidewalk cover passes under it. Heights below are from the road.",
           f"Amber reflective film from the bottom edge up to 300 mm above the road",
           f"  ({300 - m0:.0f} mm up the plate). Red film from 300 to 450 mm above the road",
           f"  ({300 - m0:.0f} to {450 - m0:.0f} mm up the plate). Leave the top {m0 + mh - 450:.0f} mm plain for a label.",
           "Mark a black line at 150 mm and 300 mm above the road (the alert",
           "  depths) and number them.",
           "No holes: two band clamps go round the pole, across the plate's face",
           f"  and round the riser guard, at {P['marker_bands_z'][0]:.0f} and {P['marker_bands_z'][1]:.0f} mm above the road.",
           "Check: film edges straight and level when the plate is held plumb."],
          view_shape=flat(C["marker"].shape, (D["pole_face_x"], 0, m0), (0, 1, 0), (0, 0, 1)), inset_view=(20, -150))

    gw, gd, gt = P["guard"]
    sheet("guard", Part("Riser guard", C["guard"].shape, COL["guard"]),
          [part("pole", win(ST["pole"], px - 40, px + 40, -40, 40, 150, 700), COL["pole"]),
           part("marker", C["marker"].shape, "#E5E7EB"), part("cover", C["walk_cover"].shape & bx(300, 440, 0, 200, 140, 200), COL["covers"])],
          "FLG-DWG-111", "FloodGauge riser guard: making sketch", "Galvanized steel sheet 2 mm",
          [f"Cut a blank {P['riser_rise']:.0f} x {2 * gd + gw - 4 * gt:.0f} mm from 2 mm galvanized sheet.",
           f"Fold to a U: back {gw:.0f} mm wide outside, two sides {gd:.0f} mm deep.",
           "  Fold in a sheet folder or over a hardwood block in the vice.",
           "Cut a 20 x 20 mm notch at the foot of the side that faces the road,",
           "  against the back: the cable comes out of the sidewalk cover here.",
           "File every edge smooth; paint the cut edges with zinc paint.",
           "Fit: open side against the pole, the free edges of both sides bearing",
           f"  on the pole; it stands on the sidewalk beside the pole, {P['riser_rise']:.0f} mm tall.",
           "  The two marker band clamps go round it and hold it (pin-Torx security screws).",
           "Check: the free edges touch the pole along their whole length."],
          view_shape=to_origin(C["guard"].shape), inset_view=(30, -30))

    sheet("tube", Part("Stilling tube", C["tube"].shape, COL["tube"]),
          [part("drain head", C["drain_head"].shape, COL["drain"]), part("clamps", C["pclamps"].shape, COL["pclamps"]),
           part("basin", win(ST["basin"], -200, 60, 0, 460, -1400, -150), COL["pole"])],
          "FLG-DWG-112", "FloodGauge stilling tube: making sketch", "PVC pressure or drain pipe 75 mm OD, 3 mm wall",
          [f"Cut {D['tube_len']:.0f} mm of 75 mm PVC pipe; square and deburr both ends.",
           f"Slots 5 x 50 mm: ten rows, four slots a row at 90 degrees apart. Row",
           f"  centres {P['slot_first']:.0f} mm from the bottom end, then every {P['slot_pitch']:.0f} mm.",
           "  Turn the slots 45 degrees off the line to the basin wall (where the",
           "  clamp rods are). Cut with a hand saw and file, or a router.",
           "Two 3.5 mm pilot holes 20 mm below the top end, one each side, for",
           "  the screws that hold the drain head socket.",
           "Mark the clamp positions: 80 and 710 mm below the top end.",
           f"Fit: hangs in the basin {P['tube_inset']:.0f} mm from the curb-side wall on two",
           f"  stand-off pipe clamps; top end {-P['tube_top']:.0f} mm below the road; the open",
           f"  bottom end {P['tube_bot_gap']:.0f} mm above the basin floor.",
           "Check: a 50 mm ball dropped in falls straight out of the bottom."],
          view_shape=to_origin(C["tube"].shape), inset_view=(15, -60))

    so, sl = P["socket"]
    sheet("drain", Part("Drain head", C["drain_head"].shape, COL["drain"]),
          [part("tube", win(C["tube"].shape, tx - 50, tx + 50, -50, 50, -500, -290), COL["tube"]),
           part("clamp", win(C["pclamps"].shape, tx - 50, -40, -50, 50, -400, -350), COL["pclamps"])],
          "FLG-DWG-113", "FloodGauge drain head: making sketch", "PVC cap 104 mm, 75 mm PVC socket, potting compound",
          [f"Body: a sealed PVC cap about {P['drain_head_d']:.0f} mm across and {P['drain_head_h']:.0f} mm tall.",
           f"Socket: a 75 mm PVC socket coupling cut to {sl:.0f} mm, solvent-welded under",
           "  the body, centred. The tube top slides into it up to the body.",
           "Inside: the ultrasonic ranger, transducer face down and flush with",
           "  the inside of the socket; the 10 k NTC beside it; two stainless wet",
           f"  probe pins {P['probe_drop']:.0f} mm below the face, 36 mm apart; a cable gland on top.",
           "Pot the electronics, keeping the transducer face and the probe tips",
           "  clear of potting compound.",
           f"Fit: push over the tube top; two stainless screws through the socket",
           "  into the tube's pilot holes. Undo them to lift the head for cleaning.",
           f"Transducer face {-P['tube_top']:.0f} mm below the road.",
           "Check: the socket slides fully onto a tube offcut; probe tips clean."],
          view_shape=to_origin(C["drain_head"].shape), inset_view=(20, -60))

    W, H, t = P["hat"]
    hat_notes = ["Hat section: from 2 mm galvanized strip 84 mm wide, folded to two",
                 "  22 mm flanges, two 45 degree sides and a 16 mm wide top, 16 mm high",
                 "  overall. Fold in a sheet folder; cut lengths with a grinder.",
                 "Paint the cut ends with zinc paint; file all edges smooth."]
    sheet("gutter", Part("Gutter cover", C["gutter_cover"].shape, COL["covers"]),
          [part("curb cover", C["curb_cover"].shape, "#6D28D9"),
           part("grate", win(ST["grate"], -260, -100, -40, 200, -40, 0), "#374151"),
           part("road", win(ST["road"], -260, 0, -40, 200, -60, 0), COL["pole"])],
          "FLG-DWG-114", "FloodGauge gutter cover: making sketch", "Galvanized steel strip 2 mm",
          hat_notes + [f"Cut {-P['gutter_x0'] - 4 + 30:.0f} mm of hat section. At one end cut away the top and",
                       "  sides for 42 mm, leaving the two flanges; fold the flanges up",
                       f"  90 degrees 30 mm from their ends to make the tabs ({-P['gutter_x0'] - H:.0f} mm of raised part).",
                       "Drill a 9 mm hole in each tab, 18 mm up, 32 mm from the centre line.",
                       "Fit: lies across the gutter strip and 80 mm onto the grate's border,",
                       "  over the cable. The tabs go over the curb cover's flanges and",
                       "  share its two lower anchors (security nuts). Nothing is fixed to the road.",
                       "Check: lies flat with no rocking."],
          view_shape=to_origin(C["gutter_cover"].shape), inset_view=(30, -45))

    sheet("curb", Part("Curb cover", C["curb_cover"].shape, "#6D28D9"),
          [part("gutter cover", C["gutter_cover"].shape, COL["covers"]), part("sidewalk cover", C["walk_cover"].shape & bx(-10, 120, 0, 200, 100, 200), "#8B5CF6"),
           part("curb", win(ST["walk"], 0, 120, -40, 200, -60, 150), COL["pole"])],
          "FLG-DWG-115", "FloodGauge curb cover: making sketch", "Galvanized steel strip 2 mm",
          hat_notes + [f"Length {P['curb_h'] + H:.0f} mm of hat section. Cut both flanges off the top 16 mm",
                       "  (only the raised part rises above the sidewalk).",
                       "Cut a 20 x 16 mm notch in the raised face at the bottom end for",
                       "  the cable coming out of the gutter cover.",
                       "Four 9 mm holes in the flanges, 32 mm from the centre line, 18 and",
                       "  139 mm up from the bottom end.",
                       "Fit: flanges flat on the curb face, standing on the road; four M8",
                       "  masonry anchors, snake-eye security nuts, through it and the tabs.",
                       "Check: the top of the raised part is 16 mm above the sidewalk."],
          view_shape=to_origin(C["curb_cover"].shape), inset_view=(25, -150))

    sheet("walk", Part("Sidewalk cover", C["walk_cover"].shape, "#8B5CF6"),
          [part("curb cover", C["curb_cover"].shape, "#6D28D9"), part("guard", C["guard"].shape, COL["guard"]),
           part("pole", win(ST["pole"], px - 40, px + 40, -40, 40, 150, 500), COL["pole"]),
           part("walk", win(ST["walk"], 0, 520, -40, 200, 100, 150), "#E7E5E4")],
          "FLG-DWG-116", "FloodGauge sidewalk cover: making sketch", "Galvanized steel strip 2 mm",
          hat_notes + [f"Cut {px - P['guard'][0] / 2 - 1 + 26:.0f} mm of hat section. At one end cut away the top and",
                       "  sides for 26 mm, leaving the two flanges; fold the flanges down",
                       f"  90 degrees 22 mm from their ends to make the tabs ({px - P['guard'][0] / 2 - 1:.0f} mm raised).",
                       "Four 9 mm holes in the flanges, 32 mm from the centre line, 110 and",
                       "  330 mm from the curb end; a 9 mm hole in each tab, 11 mm down.",
                       "Grind a 45 degree bevel on the flange edges so it is not a trip edge.",
                       "Fit: across the sidewalk from the curb edge to 1 mm short of the",
                       "  riser guard; four M8 anchors, security nuts; tabs share the curb",
                       "  cover's upper anchors. Paint it yellow or fit hazard tape.",
                       "Check: no edge stands more than 2 mm off the sidewalk."],
          view_shape=to_origin(C["walk_cover"].shape), inset_view=(30, -45))
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    import build123d as b
    out = []
    zb1, zb0 = D["band_z"]

    def jn(n, parts, title, sub, **kw):
        if only and n not in only:
            return
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", title, subtitle=sub, size=(8, 6), **kw))
        gc.collect()

    box_ = (xf - 20, px + 45, -70, 70, zb1 - 8, zb1 + 4)
    jn(1, [part("Pole", win(ST["pole"], *box_), COL["pole"]),
           part("Bracket plate", win(C["bplate"].shape, *box_), COL["bplate"]),
           part("V-block", win(C["vblocks"].shape, *box_), COL["vblocks"]),
           part("Band clamp, through the plate slots", win(C["bands"].shape, *box_), COL["bands"])],
       "Joint 1: V-block, pole and band clamp at the bracket plate",
       "Cut level with the upper band, seen from above. The pole bears on both V faces; the band pulls it in",
       elev=80, azim=-90)
    box_ = (xf - 45, xr + 12, -60, 60, az - 40, az + 40)
    jn(2, [part("Bracket plate", win(C["bplate"].shape, *box_), COL["bplate"]),
           part("Arm cleats", win(C["cleats"].shape, *box_), COL["cleats"]),
           part("Sensor arm", win(C["arm"].shape, *box_), COL["arm"]),
           part("M6 bolts and crush sleeves", win(C["fixings"].shape, *box_), COL["bolt"])],
       "Joint 2: arm between the cleats on the bracket plate",
       "Seen from the road side and above. Two M6 bolts through cleat, arm and cleat; two through each cleat and the plate",
       elev=25, azim=-130)
    box_ = (xt - 45, xt + 45, -40, 40, zt - 40, D["arm_top"] + 10)
    jn(3, [part("Sensor arm", win(C["arm"].shape, *box_), COL["arm"]),
           part("Brace clip under the arm", win(C["top_clip"].shape, *box_), COL["clips"]),
           part("Knee brace", win(C["brace"].shape, *box_), COL["brace"]),
           part("M6 pin and bolts", win(SH("pins", "fixings"), *box_), COL["bolt"])],
       "Joint 3: top of the knee brace in its clip under the arm",
       "Cut through the middle of the arm. The brace end sits between the ears on one M6 pin",
       cut="+Y", elev=12, azim=-80)
    box_ = (xft - 60, px + 45, -45, 45, zft - 40, D["bolt_z"] + 30)
    jn(4, [part("Pole", win(ST["pole"], *box_), COL["pole"]),
           part("Bracket plate", win(C["bplate"].shape, *box_), COL["bplate"]),
           part("Brace clip on the plate", win(C["foot_clip"].shape, *box_), COL["clips"]),
           part("Knee brace", win(C["brace"].shape, *box_), COL["brace"]),
           part("Spacer", win(C["spacer"].shape, *box_), COL["spacer"]),
           part("M8 through-bolt", win(C["through_bolt"].shape, *box_), COL["bolt"]),
           part("M6 brace pin", win(C["pins"].shape, *box_), "#374151")],
       "Joint 4: foot of the knee brace and the anti-rotation through-bolt",
       "Cut on the centre line. The M8 bolt passes the plate, the spacer and both pole walls; nut behind the pole",
       cut="+Y", elev=10, azim=-80)
    hx = D["head_x"]
    box_ = (hx - 90, hx + 90, -50, 50, P["head_z"] - 5, D["arm_top"] + 10)
    jn(5, [part("Sensor arm", win(C["arm"].shape, *box_), COL["arm"]),
           part("Head plate", win(C["head_plate"].shape, *box_), COL["head_plate"]),
           part("Radar head housing and gland", win(C["head_housing"].shape, *box_), COL["head"]),
           part("PTFE lens", win(C["lens"].shape, *box_), "#E5E7EB"),
           part("M6 bolts through the arm", win(C["fixings"].shape, *box_), COL["bolt"])],
       "Joint 5: radar head on the head plate under the arm",
       "Seen from below and the road side. Plate bolted up through the arm; housing on four M4 screws",
       elev=-25, azim=-120)
    box_ = (tx - 60, P["basin"][1] + 5, 0.3, 60, -420, D["dh_top"] + 30)
    jn(6, [part("Basin wall", win(ST["basin"], *box_), COL["pole"]),
           part("Stilling tube", win(C["tube"].shape, *box_), COL["tube"]),
           part("Drain head and socket", win(C["drain_head"].shape, *box_), COL["drain"]),
           part("Stand-off pipe clamp", win(C["pclamps"].shape, *box_), COL["pclamps"])],
       "Joint 6: drain head socket on the tube, and the upper pipe clamp",
       "Cut on the tube axis. The tube top stops against the head; the clamp rod runs to a plate on the basin wall",
       elev=10, azim=-80)
    box_ = (-200, 90, cy, cy + 60, -60, 200)
    jn(7, [part("Street, cut (grate, gutter, curb, sidewalk)", win(ST["road"] + ST["walk"] + ST["grate"], *box_), "#9CA3AF"),
           part("Gutter cover", win(C["gutter_cover"].shape, *box_), COL["covers"]),
           part("Curb cover (anchored to the curb face)", win(SH("curb_cover", "anchors"), *box_), "#6D28D9"),
           part("Sidewalk cover", win(C["walk_cover"].shape, *box_), "#8B5CF6"),
           part("Drain cable", win(C["drain_cable"].shape, *box_), "#DC2626")],
       "Joint 7: the three covers at the curb, cut along the cable",
       "The cable rises through a grate opening, runs under the gutter cover, up the curb face and across the sidewalk",
       elev=18, azim=-55)
    box_ = (tx - 95, tx + 70, -125, 125, -260, -60)
    jn(9, [part("Stand-off pipe clamp", win(C["pclamps"].shape, *box_), COL["pclamps"]),
           part("Stilling tube", win(C["tube"].shape, *box_), COL["tube"]),
           part("Drain cable and 0.5 m slack loop", win(SH("slack_loop", "drain_cable"), *box_), "#DC2626"),
           part("Cable ties (2)", win(C["loop_tie"].shape, *box_), COL["tie"])],
       "Joint 9: slack loop tied to the upper pipe clamp",
       "Seen from above the basin, beside the tube. One tie holds the loop, one rings the clamp; the loop hangs clear of the tube slots",
       elev=35, azim=-60)
    zz = P["marker_bands_z"][0]
    box_ = (D["pole_face_x"] - 15, px + 45, -60, D["guard_y1"] + 10, zz - 8, zz + 4)
    jn(8, [part("Pole", win(ST["pole"], *box_), COL["pole"]),
           part("Depth marker plate", win(C["marker"].shape, *box_), "#E5E7EB"),
           part("Riser guard", win(C["guard"].shape, *box_), COL["guard"]),
           part("Band clamp", win(C["marker_bands"].shape, *box_), COL["bands"]),
           part("Drain cable inside the guard", win(C["drain_cable"].shape, *box_), "#DC2626")],
       "Joint 8: depth marker, riser guard and band clamp on the pole",
       "Cut level with the lower band, seen from above. One band holds the marker plate and the guard",
       elev=80, azim=-90)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    out = []

    def st(n, done, new, title, sub, **kw):
        if only and n not in only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
        gc.collect()

    def mv(name, shape, color, e):
        return part(name, shape, color, e)

    G = lambda name, *ks: part(name, SH(*ks), COL["bplate"])  # noqa: E731
    pl = part("Bracket plate", C["bplate"].shape, COL["bplate"])
    vbu = C["vblocks"].shape & bx(xr - 1, xr + 40, -40, 40, D["band_z"][0] - 15, D["band_z"][0] + 15)
    vbl = C["vblocks"].shape & bx(xr - 1, xr + 40, -40, 40, D["band_z"][1] - 15, D["band_z"][1] + 15)
    st(1, [pl], [mv("Upper V-block", vbu, COL["vblocks"], (90, 0, 0)), mv("Lower V-block", vbl, COL["vblocks"], (90, 0, 0))],
       "V-blocks onto the bracket plate", "Two M4 countersunk screws each, from the front of the plate, threadlocker. Seen from the pole side",
       elev=20, azim=40)
    st(2, [pl, part("V-blocks", C["vblocks"].shape, COL["vblocks"])],
       [mv("Arm cleats (2)", C["cleats"].shape, COL["cleats"], (-70, 0, 0)),
        mv("Brace clip (foot)", C["foot_clip"].shape, COL["clips"], (-70, 0, 0))],
       "cleats and foot clip onto the plate", "Two M6 bolts each through the plate, nyloc nuts behind; cleat legs square to the plate",
       elev=20, azim=-130, label_done=False)
    arm = part("Sensor arm", C["arm"].shape, COL["arm"])
    st(3, [arm], [mv("Head plate", C["head_plate"].shape, COL["head_plate"], (0, 0, -80)),
                  mv("Brace clip (top)", C["top_clip"].shape, COL["clips"], (0, 0, -80))],
       "head plate and top clip under the arm", "Arm upside down on the bench is easiest; M6 bolts up through the arm with crush sleeves, nuts on top",
       elev=-25, azim=-60)
    st(4, [arm, part("Head plate", C["head_plate"].shape, COL["head_plate"])],
       [mv("Street radar head", SH("head_housing", "lens"), COL["head"], (0, 0, -120))],
       "radar head onto the head plate", "Four M4 countersunk screws into the lid bosses; gland facing along the arm toward the pole end",
       elev=-20, azim=-60, label_done=False)
    plate_set = [pl, part("V-blocks and cleats", SH("vblocks", "cleats", "foot_clip"), COL["bplate"])]
    arm_set = part("Arm with head", SH("arm", "head_plate", "top_clip", "head_housing", "lens"), COL["arm"])
    st(5, plate_set, [mv("Arm with head", arm_set.shape, COL["arm"], (-200, 0, 0))],
       "arm between the cleats", "Two M6 bolts with crush sleeves through cleat, arm and cleat; arm square to the plate",
       elev=20, azim=-60, label_done=False)
    st(6, plate_set + [part("Arm", arm_set.shape, COL["bplate"])],
       [mv("Knee brace", C["brace"].shape, COL["brace"], (-60, -120, -60))],
       "knee brace into its clips", "One M6 pin with a sleeve at each end; check the arm is level, then tighten all bracket bolts",
       elev=15, azim=-60, label_done=False)
    z0n = D["node_bot"]
    fn = SH("fn_plate", "fn_vblocks", "fn_bands", "fn_body", "fn_lid", "fn_bracket", "fn_panel")
    st(7, [], [mv("FieldNode core, built to FND-BLD-001", fn, "#D1D5DB", (-200, 0, 0))],
       "FieldNode onto the pole", f"Its two band clamps round the pole, box bottom {z0n / 1000:.1f} m above the road, facing the road. From a platform",
       context=[part("Pole", pole_seg(z0n - 300, z0n + 700), COL["pole"])], elev=15, azim=-60)
    bracket = SH("bplate", "vblocks", "cleats", "foot_clip", "top_clip", "arm", "brace", "head_plate", "head_housing", "lens", "fixings", "pins")
    st(8, [], [mv("Arm and bracket, assembled", bracket, COL["arm"], (-250, 0, 0)),
               mv("Band clamps (2)", C["bands"].shape, COL["bands"], (0, 0, 0))],
       "arm and bracket onto the pole", "Lift the assembled arm from a platform; band clamps round the pole, through the slots, across the plate",
       context=[part("Pole", pole_seg(zlo - 250, zhi + 150), COL["pole"])], elev=15, azim=-60)
    armset = part("Arm and bracket", SH("bplate", "vblocks", "cleats", "foot_clip", "top_clip", "arm", "brace", "head_plate", "head_housing", "lens", "bands"), COL["bplate"])
    st(9, [armset], [mv("M8 through-bolt", C["through_bolt"].shape, COL["bolt"], (-120, 0, 0)),
                     mv("Spacer", C["spacer"].shape, COL["spacer"], (0, 0, 80))],
       "anti-rotation through-bolt", "Drill 8.5 mm through the pole via the plate hole (owner's permission); bolt, spacer, washer, nyloc nut behind",
       context=[part("Pole", pole_seg(zlo - 100, zhi + 100), COL["pole"])], elev=12, azim=-55, label_done=False)
    street = cable(RUNS["street"], P["cable_d"])
    st(10, [part("FieldNode", fn, COL["bplate"]), armset],
       [mv("Street head cable, 3 m", street, "#DC2626", (0, -150, 0))],
       "street cable to FieldNode port A", "Along the arm side, down the pole outside the band clamps, to port A; UV ties every 300 mm, drip loops",
       context=[part("Pole", pole_seg(z0n - 300, zhi + 100), COL["pole"])], elev=12, azim=-35, label_done=True)
    base = [part("Pole", win(ST["pole"], px - 40, px + 40, -40, 40, 150, 800), COL["bplate"])]
    walkctx = part("Sidewalk", win(ST["walk"], 250, 650, -150, 250, 100, 150), "#E5E7EB")
    st(11, base, [mv("Depth marker plate", C["marker"].shape, "#F9FAFB", (-120, 0, 0)),
                  mv("Riser guard", C["guard"].shape, COL["guard"], (0, 120, 0)),
                  mv("Band clamps (2)", C["marker_bands"].shape, COL["bands"], (0, 0, 0))],
       "depth marker and riser guard onto the pole", f"Marker bottom {P['marker_z0']:.0f} mm above the road; guard on the sidewalk, open side on the pole; two bands round all three, security screws",
       context=[walkctx], elev=20, azim=-50, label_done=False)
    basin = part("Catch basin (cut)", win(ST["basin"], -900, 60, 0, 500, -1450, -200), "#E5E7EB")
    st(12, [], [mv("Stand-off pipe clamps (2)", C["pclamps"].shape, COL["pclamps"], (-120, 0, 0)),
                mv("Stilling tube", C["tube"].shape, COL["tube"], (0, 0, 500))],
       "pipe clamps and stilling tube into the basin", "From the surface with the grate off: anchor the clamp plates to the wall, lower the tube in, close the clamps",
       context=[basin], elev=15, azim=-70)
    st(13, [part("Stilling tube and clamps", SH("tube", "pclamps"), COL["bplate"])],
       [mv("Drain head", C["drain_head"].shape, COL["drain"], (0, 0, 180)),
        mv("Slack loop and ties", SH("slack_loop", "loop_tie"), "#DC2626", (0, 0, 0))],
       "drain head onto the tube", "Push the socket over the tube top; two stainless screws into the pilot holes. Then form the 0.5 m loop and tie it to the clamp",
       context=[basin], elev=15, azim=-70, label_done=False)
    box_ = (-260, 520, -60, 220, -260, 520)
    surf = [part("Riser guard and marker", win(SH("guard", "marker"), *box_), COL["bplate"])]
    ctx = [part("Street", win(ST["road"] + ST["walk"] + ST["grate"], *box_), "#E5E7EB")]
    st(14, surf, [mv("Drain cable", win(C["drain_cable"].shape, *box_), "#DC2626", (0, 0, 0)),
                  mv("Gutter cover", C["gutter_cover"].shape, COL["covers"], (0, 0, 90)),
                  mv("Curb cover", C["curb_cover"].shape, "#6D28D9", (-90, 0, 0)),
                  mv("Sidewalk cover", C["walk_cover"].shape, "#8B5CF6", (0, 0, 90))],
       "drain cable and the three covers", "Cable up through a grate opening, along the curb and sidewalk into the guard; covers on eight M8 anchors with security nuts",
       context=ctx, elev=28, azim=-125, label_done=False)
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("only=")]
    only = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("only=")]
    only = [int(o) if o.isdigit() else o for o in (only[0].split(",") if only else [])] or None
    what = args or ["overview", "sheets", "joints", "steps"]
    fns = {"overview": lambda o: overview(), "sheets": sheets, "joints": joints, "steps": steps}
    for w in what:
        print(w, "->", fns[w](only))
