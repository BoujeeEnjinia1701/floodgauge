"""FloodGauge product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is (kit 1.9, detail level D3): the FieldNode
enclosure, lid, back plate, panel and bracket, the radar head with its housing, lens, boss screws and gland, the
pole bracket plate with V-blocks, band clamps, cleats, arm, knee brace and clips, the anti-rotation through-bolt,
the marker plate and its band clamps, the three hat covers, riser guard and anchors, the drain head, stilling
tube and pipe clamps, the cables and plugs, and every bolt, nut, washer and screw. Nothing is redrawn and the
pole kit is shown at its installed height (lens 4.6 m, node 3.4 m above the road).

Only the site is added, as context parts: the road slab and gutter, curb and sidewalk, catch basin, grate and the
street pole from components(), with the pole carried 100 mm into the sidewalk so it does not stand on the
ground, and a 1.75 m mannequin standing on the sidewalk. The hero is rendered by .kit/photoreal.py as an outdoor
scene, ground level at model z = 0 (the road surface), concrete ground (RENDER_VIEWS "args").
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the kit above ground), "drain" (drain head, tube, clamps and the slack loop in the catch basin),
"pole" (the street pole, shown with the product), "context" (site and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Cylinder, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "FloodGauge: street and drain water level sensor"

_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=38,-120", "--lens=35"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "pole", "context"], "explode": False, "el": 12, "az": -140, "args": _SITE,
     "note": "Site render from the road side, looking toward the curb and a little above (about 12 deg elevation): the "
             "60 GHz radar head on its braced arm 4.6 m over the gutter and grate, the solar-powered node on the pole under its "
             "40 deg panel, the depth marker, riser guard and cable covers at the curb, and a 1.75 m person on the "
             "sidewalk for scale. Installed heights, concept option A"},
    {"name": "studio", "groups": ["shell", "pole"], "explode": False, "el": 20, "az": -140,
     "note": "Studio render from the road side and above (about 20 deg elevation): node and panel, radar head on its "
             "braced arm with the pole bracket, band clamps and through-bolt, depth marker with its bands and the riser guard, "
             "on a 60 mm pole section, at installed height"},
    {"name": "exploded", "groups": ["shell", "drain"], "explode": True, "el": 22, "az": -130,
     "note": "Exploded view from the road side and above (about 22 deg elevation): node, lid and panel; radar head; "
             "bracket plate, cleats, arm, brace and through-bolt; depth marker and band clamps; cable covers and riser guard; "
             "drain head, stilling tube, clamps and slack loop pulled out below"},
]


def site():
    """Site context: the street from components() with every part reaching below ground (z = 0 is the road
    surface) and a mannequin on the sidewalk. Pole and sign are named '(site)' so camera framing ignores them."""
    P = M.PARAMS
    out = []
    for q in M.components(M.CHOSEN):
        if q["kind"] != "context":
            continue
        q = dict(q)
        if q["name"].startswith("Street pole"):
            # carry the pole 100 mm into the sidewalk (its base is at curb height) so it is planted, not standing on the ground
            q["shape"] = q["shape"] + Pos(P["pole_x"], 0, (P["curb_h"] - 100.0) / 2) * Cylinder(P["pole_od"] / 2, P["curb_h"] + 100.0)
            q["group"] = "pole"
        out.append(q)
    try:
        import context_parts
        man = Pos(P["pole_x"] + 330.0, -650.0, P["curb_h"]) * Rot(0, 0, -90) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            continue
        q = dict(p)
        q["bom_group"] = p["group"]
        q["group"] = "drain" if p["group"] in ("drain_head", "tube") else "shell"
        out.append(q)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "shell" for p in ps), "shell,", sum(p["group"] == "drain" for p in ps), "drain,",
          sum(p["group"] in ("context", "pole") for p in ps), "context")
