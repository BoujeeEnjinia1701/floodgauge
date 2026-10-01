"""FloodGauge concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The street runs along Y. X runs across the street: road at X < 0,
curb face at X = 0, sidewalk at X > 0. Road surface at Z = 0, sidewalk top at Z = 150.
The existing street, catch basin and pole are grey with no BOM number; kit parts are colored.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Rot
from concept import Part, render_all, human_figure, _render

# Geometry comes from the parametric model (cad/src/model.py), so the media follow PARAMS.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import PARAMS as P, build_parts, bands, site  # noqa: E402

CURB_H = P["curb_h"]
GREY = "#B8BEC6"
CONCRETE = "#A8A29E"
ROAD = "#4B5563"

K = build_parts()
B = bands()
S = site()

parts = [
    Part("Existing road slab and gutter", S["road"], ROAD, None),
    Part("Existing curb and sidewalk", S["walk"], CONCRETE, None),
    Part("Existing catch basin and outlet pipe", S["basin"], "#9CA3AF", None),
    Part("Existing grate", S["grate"], "#374151", None),
    Part("Stormwater (illustrative level)", S["water"], "#3B82F6", None),
    Part("Existing street pole, 60 mm", S["pole"], GREY, None),
    Part("FieldNode core (enclosure, LiFePO4, LoRaWAN)", K["node"], "#E5E7EB", 1, (-150, -500, 150)),
    Part("FieldNode 6 W panel (part of item 1)", K["panel"], "#1E3A8A", None, (-150, -500, 350)),
    Part("Street radar head, 60 GHz", K["street_head"], "#0F766E", 2, (-250, -300, 350)),
    Part("Sensor arm and pole clamps", K["arm"], "#D4A017", 3, (0, 0, 250)),
    Part("Drain head, ultrasonic with wet probe", K["drain_head"], "#C2410C", 4, (-400, -500, 1650)),
    Part("Stilling tube, 75 mm slotted PVC", K["tube"], "#F59E0B", 5, (-400, -500, 1400)),
    Part("Sensor cables, M12", K["cables"], "#111827", 6, (250, -900, 0)),
    Part("Surface cable cover and riser guard", K["conduit"], "#7C3AED", 7, (300, -600, 600)),
    Part("Depth marker plate", K["marker"], "#F9FAFB", 8, (-300, -350, 0)),
    Part("Depth bands, 150 to 300 mm (amber)", B["amber"], "#F59E0B", None, (-300, -350, 0)),
    Part("Depth bands, 300 to 450 mm (red)", B["red"], "#DC2626", None, (-300, -350, 0)),
]

# Turn the scene 180 degrees about Z so the standard isometric camera looks from the road side,
# at the face of the node, the grate and the depth marker. Exploded offsets keep their Y (toward the camera).
for p in parts:
    p.shape = Rot(0, 0, 180) * p.shape
    p.explode = (-p.explode[0], p.explode[1], p.explode[2])

person = human_figure(1750.0, x=-1000.0, y=300.0, z=CURB_H)

if __name__ == "__main__":
    render_all(
        parts, project="FloodGauge", title="Street and drain level gauge concept", dwg_no="FLG-DWG-010",
        key_figures=[f"Street head: 60 GHz radar, lens {P['head_z'] / 1000:.1f} m above road (2.5 to 5.0 m per site)",
                     "Drain head: ultrasonic in 75 mm stilling tube",
                     "Alert bands: 150 mm and 300 mm of water",
                     "Alert latency 82 s (95 %), 110 s worst (estimate)",
                     "Parts $153.50 plus FieldNode $126 (indicative)"],
        scale_figure=False, context=[person],
        flow={"title": "data flow from water surface to alert (values are estimates)", "unit": "",
              "stages": [("Water surface", "street and drain"),
                         ("Two ranging heads", "60 s; 10 s in events"),
                         ("FieldNode", "level, rise rate, bands"),
                         ("LoRaWAN uplink", "about 0.25 s at SF9"),
                         ("Gateway and alerts", "TwinKit or city LNS"),
                         ("Crews and residents", "82 s at 95 %, estimate")]},
    )
    # Exploded view of the kit only: the existing street, basin and water are left out so that
    # no part is hidden by them; the existing pole stays as a grey reference.
    kit = [p for p in parts if p.bom is not None or p.name.startswith(("FieldNode 6 W", "Depth bands", "Existing street pole"))]
    _render(kit, Path("media/exploded.png"), offsets=True, labels=True, title="FloodGauge: exploded view",
            note="Existing street, catch basin and water not shown. Grey: existing street pole (not in kit).")
    import shutil
    for d in (Path("media/_views"), Path("media/_views_fig")):
        shutil.rmtree(d, ignore_errors=True)
