"""FloodGauge concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The street runs along Y. X runs across the street: road at X < 0,
curb face at X = 0, sidewalk at X > 0. Road surface at Z = 0, sidewalk top at Z = 150.
The existing street, catch basin and pole are grey with no BOM number; kit parts are colored.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all, human_figure, _render

# ---------------- key dimensions (concept values) ----------------
CURB_H = 150.0            # curb reveal above road
SLAB = 200.0              # road and sidewalk slab thickness
STRIP = 1500.0            # length of street strip shown (along Y)
ROAD_W = 1300.0           # road width shown (X < 0)
WALK_W = 1300.0           # sidewalk width shown (X > 0)
POLE_X, POLE_R, POLE_H = 450.0, 30.0, 3300.0     # existing 60 mm sign pole, 450 mm back from the curb face
GRATE_X0, GRATE_X1, GRATE_Y = -500.0, -100.0, 600.0   # grate opening in the gutter
BASIN_X0, BASIN_X1, BASIN_Y = -750.0, -50.0, 900.0    # catch basin inner plan
BASIN_FLOOR = -1300.0     # basin inner floor below road
WALL = 100.0
WATER_Z = -800.0          # illustrative backed-up water level in the basin
HEAD_X = -250.0           # street radar head: 250 mm past the curb face, over the gutter
HEAD_Z = 2950.0           # underside of the street head (range to road about 2.95 m)
ARM_Z = 3060.0            # arm centerline

GREY = "#B8BEC6"
CONCRETE = "#A8A29E"
ROAD = "#4B5563"

# ---------------- existing street (no BOM number) ----------------
road = Pos(-ROAD_W / 2, 0, -SLAB / 2) * Box(ROAD_W, STRIP, SLAB)
road = road - Pos((GRATE_X0 + GRATE_X1) / 2, 0, -SLAB / 2) * Box(GRATE_X1 - GRATE_X0, GRATE_Y, SLAB + 2)
walk = Pos(WALK_W / 2, 0, (CURB_H - SLAB) / 2) * Box(WALK_W, STRIP, CURB_H + SLAB)

bx0, bx1 = BASIN_X0 - WALL, BASIN_X1 + WALL
basin_outer = Pos((bx0 + bx1) / 2, 0, (BASIN_FLOOR - WALL - SLAB) / 2) * Box(bx1 - bx0, BASIN_Y + 2 * WALL, -(BASIN_FLOOR - WALL) - SLAB)
basin_inner = Pos((BASIN_X0 + BASIN_X1) / 2, 0, (BASIN_FLOOR - SLAB) / 2 + 1) * Box(BASIN_X1 - BASIN_X0, BASIN_Y, -BASIN_FLOOR - SLAB + 2)
OUT_Z = -1050.0
outlet = Pos(bx0 - 350, 0, OUT_Z) * Rot(0, 90, 0) * (Cylinder(170, 700) - Cylinder(150, 702))
basin = basin_outer - basin_inner - Pos(bx0 - 350, 0, OUT_Z) * Rot(0, 90, 0) * Cylinder(150, 800)
basin = basin + outlet

grate = Pos((GRATE_X0 + GRATE_X1) / 2, 0, -20) * Box(GRATE_X1 - GRATE_X0 - 10, GRATE_Y - 10, 40)
for k in range(7):
    y = -240 + k * 80
    grate = grate - Pos((GRATE_X0 + GRATE_X1) / 2, y, -20) * Box(300, 40, 50)

water = Pos((BASIN_X0 + BASIN_X1) / 2, 0, (BASIN_FLOOR + WATER_Z) / 2) * Box(BASIN_X1 - BASIN_X0 - 2, BASIN_Y - 2, WATER_Z - BASIN_FLOOR - 2)

pole = Pos(POLE_X, 0, CURB_H + POLE_H / 2) * Cylinder(POLE_R, POLE_H)
sign = Pos(POLE_X, 0, CURB_H + POLE_H - 120) * Box(20, 760, 200)   # street name sign on the existing pole

# ---------------- kit parts ----------------
# 1 FieldNode core: IP65 enclosure about 200 x 150 x 90 mm on the pole, facing the road
NODE_Z = 2500.0
node = Pos(POLE_X - POLE_R - 45 - 12, 0, NODE_Z) * Box(90, 150, 200)
node = node + Pos(POLE_X - POLE_R - 6, 0, NODE_Z) * Box(12, 110, 240)      # back plate
# FieldNode 6 W panel as sun and rain hood (part of item 1)
panel = Pos(POLE_X - POLE_R - 80, 0, NODE_Z + 175) * Rot(0, -25, 0) * Box(200, 290, 18)

# 2 Street radar head under the arm tip
street_head = Pos(HEAD_X, 0, HEAD_Z + 45) * Cylinder(38, 90)
street_head = street_head + Pos(HEAD_X, 0, HEAD_Z + 3) * Cylinder(30, 6)   # PTFE lens face

# 3 Sensor arm, 40 mm square aluminium tube, with two pole clamps and a knee brace
arm_len = POLE_X + POLE_R + 40 - (HEAD_X - 60)
arm = Pos((POLE_X + POLE_R + 40 + HEAD_X - 60) / 2, 0, ARM_Z) * Box(arm_len, 40, 40)
arm = arm + Pos(HEAD_X, 0, HEAD_Z + 110) * Box(70, 50, 40)                 # head saddle
for z in (ARM_Z, ARM_Z - 400):
    arm = arm + Pos(POLE_X, 0, z) * (Cylinder(POLE_R + 8, 50) - Cylinder(POLE_R + 1, 52))
brace_len = (400 ** 2 + 400 ** 2) ** 0.5
arm = arm + Pos(POLE_X - POLE_R - 200, 0, ARM_Z - 200) * Rot(0, -45, 0) * Box(25, 25, brace_len - 60)

# 4 Drain head: ultrasonic ranger with wet probe in a potted housing, at the top of the stilling tube
TUBE_X = BASIN_X1 - 90.0
TUBE_TOP, TUBE_BOT = -300.0, BASIN_FLOOR + 60
drain_head = Pos(TUBE_X, 0, TUBE_TOP + 45) * Cylinder(52, 90)

# 5 Stilling tube, 75 mm slotted PVC, with two wall brackets
tube = Pos(TUBE_X, 0, (TUBE_TOP + TUBE_BOT) / 2) * (Cylinder(40, TUBE_TOP - TUBE_BOT) - Cylinder(35, TUBE_TOP - TUBE_BOT + 2))
for z in (TUBE_TOP - 80, TUBE_BOT + 250):
    tube = tube + (Pos(TUBE_X + 45, 0, z) * Box(90, 30, 40) - Pos(TUBE_X, 0, z) * Cylinder(40.5, 42))

# 6 Sensor cables with M12 connectors: street head along the arm; drain head up the pole from the conduit
c_arm = Pos((POLE_X - POLE_R - 20 + HEAD_X) / 2, 0, ARM_Z + 28) * Box(POLE_X - POLE_R - 20 - HEAD_X, 10, 10)
c_drop = Pos(POLE_X - POLE_R - 20, 0, (ARM_Z + 28 + NODE_Z + 100) / 2) * Box(10, 10, ARM_Z + 28 - NODE_Z - 100)
c_pole = Pos(POLE_X + POLE_R + 8, 0, (CURB_H + 250 + NODE_Z - 100) / 2) * Box(10, 10, NODE_Z - 100 - CURB_H - 250)
c_head = Pos(HEAD_X, 0, (ARM_Z + 28 + HEAD_Z + 90) / 2) * Box(10, 10, ARM_Z + 28 - HEAD_Z - 90)
cables = c_arm + c_drop + c_pole + c_head

# 7 Conduit, 25 mm, cored through the basin wall under the sidewalk to the back of the pole base, with a riser guard
CZ = -330.0
cond_h = Pos((BASIN_X1 - 20 + POLE_X + 60) / 2, 40, CZ) * Rot(0, 90, 0) * Cylinder(14, POLE_X + 60 - BASIN_X1 + 20)
cond_v = Pos(POLE_X + 60, 40, (CZ + CURB_H + 250) / 2) * Cylinder(14, CURB_H + 250 - CZ)
guard = Pos(POLE_X + POLE_R + 20, 20, CURB_H + 150) * Box(40, 70, 300)
conduit = cond_h + cond_v + guard + Pos(TUBE_X + 30, 40, CZ) * Rot(0, 90, 0) * Cylinder(8, BASIN_X1 - TUBE_X)

# 8 Depth marker plate on the pole: bands at 150 to 300 mm and 300 to 450 mm of water above the road
marker = Pos(POLE_X - POLE_R - 3, 0, CURB_H + 225) * Box(6, 90, 450)
band_amber = Pos(POLE_X - POLE_R - 7, 0, 225) * Box(4, 92, 150)
band_red = Pos(POLE_X - POLE_R - 7, 0, 375) * Box(4, 92, 150)

parts = [
    Part("Existing road slab and gutter", road, ROAD, None),
    Part("Existing curb and sidewalk", walk, CONCRETE, None),
    Part("Existing catch basin and outlet pipe", basin, "#9CA3AF", None),
    Part("Existing grate", grate, "#374151", None),
    Part("Stormwater (illustrative level)", water, "#3B82F6", None),
    Part("Existing sign pole, 60 mm", pole + sign, GREY, None),
    Part("FieldNode core (enclosure, LiFePO4, LoRaWAN)", node, "#E5E7EB", 1, (-150, -500, 150)),
    Part("FieldNode 6 W panel (part of item 1)", panel, "#1E3A8A", None, (-150, -500, 350)),
    Part("Street radar head, 60 GHz", street_head, "#0F766E", 2, (-250, -300, -350)),
    Part("Sensor arm and pole clamps", arm, "#D4A017", 3, (0, 0, 250)),
    Part("Drain head, ultrasonic with wet probe", drain_head, "#C2410C", 4, (-400, -500, 1650)),
    Part("Stilling tube, 75 mm slotted PVC", tube, "#F59E0B", 5, (-400, -500, 1400)),
    Part("Sensor cables, M12", cables, "#111827", 6, (250, -900, 0)),
    Part("Conduit and riser guard", conduit, "#7C3AED", 7, (300, -600, 600)),
    Part("Depth marker plate", marker, "#F9FAFB", 8, (-300, -350, 0)),
    Part("Depth bands, 150 to 300 mm (amber)", band_amber, "#F59E0B", None, (-300, -350, 0)),
    Part("Depth bands, 300 to 450 mm (red)", band_red, "#DC2626", None, (-300, -350, 0)),
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
        key_figures=["Street head: 60 GHz radar, about 2.95 m above road (proposed)",
                     "Drain head: ultrasonic in 75 mm stilling tube (proposed)",
                     "Alert bands: 150 mm and 300 mm of water (proposed)",
                     "Alert latency about 70 s, private gateway (estimate)",
                     "Parts about $271 incl. FieldNode $126 (indicative)"],
        scale_figure=False, context=[person],
        flow={"title": "data flow from water surface to alert (values are estimates or proposals)", "unit": "",
              "stages": [("Water surface", "street and drain"),
                         ("Two ranging heads", "every 60 s; 10 s rising"),
                         ("FieldNode", "level, rise rate, bands"),
                         ("LoRaWAN uplink", "about 0.25 s at SF9"),
                         ("Gateway and alerts", "TwinKit or city LNS"),
                         ("Crews and residents", "about 70 s end to end")]},
    )
    # Exploded view of the kit only: the existing street, basin and water are left out so that
    # no part is hidden by them; the existing pole stays as a grey reference.
    kit = [p for p in parts if p.bom is not None or p.name.startswith(("FieldNode 6 W", "Depth bands", "Existing sign"))]
    _render(kit, Path("media/exploded.png"), offsets=True, labels=True, title="FloodGauge: exploded view",
            note="Existing street, catch basin and water not shown. Grey: existing sign pole (not in kit).")
    import shutil
    for d in (Path("media/_views"), Path("media/_views_fig")):
        shutil.rmtree(d, ignore_errors=True)
