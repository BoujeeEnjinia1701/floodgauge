"""FloodGauge sizing calculations, FLG-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md; each line carries a tag such as [B2]
that the note cites. It also writes docs/04-calcs/results.csv (requirement status table).
Geometry comes from cad/src/model.py (PARAMS and derived), the parts cost from bom/bom.csv and
the budget from project.yaml. FieldNode figures come from the FieldNode repo (FND-CAL-001).
First-principles estimates for a paper proof of concept; not a substitute for tests.
"""
import csv
import math
import random
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)


def tag(t, text):
    print(f"[{t}] {text}")


def c_sound(t_c):
    """Speed of sound in air, m/s (linear approximation)."""
    return 331.3 + 0.606 * t_c


# ------------------------------------------------------------------ assumptions
T_CAL = 20.0                  # degC, air temperature at which an uncompensated ultrasonic range is calibrated
T_AIR = (-20.0, 50.0)         # degC, R2 and R14 air range
RADAR_ACC = 2.0               # mm, radar module distance accuracy (ASSUMED; data sheet not verified)
BEAM_FULL = 25.0              # deg, radar half-power beam width with a PTFE lens (ASSUMED)
DATUM = 5.0                   # mm, head height survey (R13 limit)
RIPPLE = 3.0                  # mm, residual surface ripple and rain splash after averaging 5 readings (assumed)
ALPHA_STEEL = 12e-6           # 1/K, pole
DT_POLE = 35.0                # K, pole temperature swing from the survey day
US_ACC = 10.0                 # mm, A02YYUW accuracy ±1 cm (DFRobot)
US_COMP_DT = 3.0              # K, air sensor versus air column, street variant
DRAIN_COMP_DT = 2.0           # K, NTC in the drain head versus air in the tube
DRAIN_UNCOMP_DT = 10.0        # K, basin air swing from a 20 degC calibration without compensation
DRAIN_DATUM = 3.0             # mm, drain head face measured from the grate seat with a tape
V_RAIL_R, I_RADAR, T_RADAR = 3.3, 0.060, 0.30     # radar: V, A, s per reading (ASSUMED)
V_RAIL_U, I_US, T_US = 5.0, 0.008, 0.30          # ultrasonic: <= 8 mA (DFRobot); 3 x 100 ms responses
I_MCU, T_MCU = 0.005, 0.35    # A, s: STM32WL awake per sampling cycle (assumed)
ETA_RAIL = 0.90               # switched rail converters (FieldNode)
E_REPORT = 16.0e-3 * 3.2      # J per SF9 report (FieldNode [A1]: 16.0 mA s at 3.2 V)
FND_CORE_WH = 0.0040          # Wh/day, FieldNode core at 15 min reports (FND-CAL-001 [A1])
FND_USABLE_WH = 15.36         # Wh usable (FND-CAL-001 [A3])
FND_COLD = 4.03 / 5.75        # autonomy factor at -20 degC (FND-CAL-001 [A5])
FND_ALLOW = (100.0, 115.0)    # mW: recommended design value and 5-day ceiling (FND-CAL-001)
FND_HOT_STORED = 0.8          # Wh stored on a hot clear day without a shield (FND-CAL-001 [C3])
PAYLOAD = 20                  # bytes, FieldNode standard reading
TTN_S = 30.0                  # s/day fair use
DUTY = 0.01                   # EU868 sub-band duty cycle
EVENT_REPORT_S = 60.0         # s between uplinks in an event
NORMAL_REPORT_S = 900.0       # s, FieldNode default
SAMPLE_NORMAL, SAMPLE_FAST = 60.0, 10.0
CONFIRM = 2                   # confirming samples at 10 s before a band alert
NET_PRIVATE = (1.0, 4.7)      # s, TwinKit forwarding and service (TWK-CAL-001 worst 4.7 s)
NET_PUBLIC = (2.0, 10.0)      # s, city or public network server and service (assumed)
LOSS = 0.01                   # uplink loss (TwinKit R1 target)
WAKE = 1.0                    # s, wake, read and queue the uplink
Q_WIND = 0.5 * 1.225 * 35.0 ** 2   # Pa at 35 m/s (as FND-CAL-001)
CD_SQ, CD_CYL = 2.0, 1.2
E_AL, SY_AL = 69000.0, 214.0  # MPa, 6063-T6 class aluminium (typical)
RHO_AL = 2.70e-6              # kg/mm3
BAND_PRELOAD, MU = 1000.0, 0.30    # N per band clamp (FND-CAL-001 assumption), friction
HANG = 490.0                  # N, a 50 kg person hanging on the arm tip (misuse case)
VEH_H = (4.0, 4.3)            # m, tall vehicle envelope (typical legal limits; confirm locally)
VEH_MARGIN = 0.3              # m, clearance margin above the vehicle envelope (assumed)

print("FloodGauge sizing, FLG-CAL-001 v0.1")
print(f"Geometry from cad/src/model.py: lens {P['head_z']:.0f} mm above the road, {P['head_offset']:.0f} mm past the curb face; "
      f"tube {D['tube_len']:.0f} mm, ID {D['tube_id']:.0f} mm")

# ------------------------------------------------------------------ A. Geometry and range
print("\nA. Geometry and range (R1, R3)")
tag("A1", f"street head range: {D['range_dry'] / 1000:.2f} m to the dry road, {D['range_600'] / 1000:.2f} m at 600 mm depth; "
          f"radar module range up to 20 m (Acconeer); depth = {P['head_z']:.0f} mm minus range")
r_fp = P["head_z"] * math.tan(math.radians(BEAM_FULL / 2))
curb_slant = math.hypot(P["head_offset"], P["head_z"] - P["curb_h"])
tag("A2", f"beam footprint radius at the road {r_fp:.0f} mm (assumed {BEAM_FULL:.0f} deg beam); curb face {P['head_offset']:.0f} mm away is inside it; "
          f"curb top echo at {curb_slant:.0f} mm reads as a false depth of {P['head_z'] - curb_slant:.0f} mm if picked")
half_angle_clear = math.degrees(math.atan(P["head_offset"] / P["head_z"]))
tag("A3", f"a beam that misses the curb needs a full width below {2 * half_angle_clear:.1f} deg, not practical; "
          f"a recorded dry-road background and nadir peak tracking are required (R10)")
tag("A4", f"drain head: face {-D['dh_face']:.0f} mm below the road; ultrasonic reads levels from "
          f"{P['basin_floor'] + 50:.0f} to {D['dh_top_level']:.0f} mm (range {P['us_blind']:.0f} to {D['dh_range_max']:.0f} mm, module 30 to 4,500 mm); "
          f"wet probe trips at {D['probe_level']:.0f} mm")
gap = D["dh_top_level"] - D["grate_under"]
tag("A5", f"grate underside at {D['grate_under']:.0f} mm: band from {D['dh_top_level']:.0f} to {D['grate_under']:.0f} mm "
          f"({-gap:.0f} mm) has only the wet probe (one point); R3 asks for a continuous reading to the grate")
tag("A6", f"tube mouth {P['tube_bot_gap']:.0f} mm above the floor, outlet invert {D['outlet_invert'] - P['basin_floor']:.0f} mm above the floor; "
          f"the 50 mm level lies {P['tube_bot_gap'] - 50:.0f} mm below the mouth, in the beam path")
clear_need = VEH_H[1] + VEH_MARGIN
tag("A7", f"head underside {P['head_z'] / 1000:.2f} m is inside a {VEH_H[0]:.1f} to {VEH_H[1]:.1f} m vehicle envelope at the curb; "
          f"clear mounting needs about {clear_need:.1f} m; range there {clear_need:.1f} m, within radar range; R1 band (2.5 to 3.5 m) excludes it")

# ------------------------------------------------------------------ B. Street depth error (R2)
print("\nB. Street depth error (R2)")
thermal = ALPHA_STEEL * (P["arm_z"]) * DT_POLE
rss_r = math.sqrt(RADAR_ACC ** 2 + DATUM ** 2 + thermal ** 2 + RIPPLE ** 2)
lin_r = RADAR_ACC + DATUM + thermal + RIPPLE
tag("B1", f"radar: module ±{RADAR_ACC:.1f} (assumed), datum ±{DATUM:.1f}, pole expansion ±{thermal:.2f}, ripple ±{RIPPLE:.1f} mm: "
          f"RSS ±{rss_r:.1f} mm, worst-case sum ±{lin_r:.1f} mm (target ±10 mm)")
rng = P["head_z"]
lo = rng * c_sound(T_CAL) / c_sound(T_AIR[0]) - rng
hi = rng * c_sound(T_CAL) / c_sound(T_AIR[1]) - rng
tag("B2", f"ultrasonic variant, uncompensated from a {T_CAL:.0f} C calibration: range error {lo:+.0f} mm at {T_AIR[0]:.0f} C, "
          f"{hi:+.0f} mm at {T_AIR[1]:.0f} C (c = {c_sound(T_AIR[0]):.1f} to {c_sound(T_AIR[1]):.1f} m/s)")
comp = rng * 0.606 * US_COMP_DT / c_sound(T_CAL)
rss_u = math.sqrt(US_ACC ** 2 + comp ** 2 + DATUM ** 2 + thermal ** 2 + RIPPLE ** 2)
tag("B3", f"ultrasonic variant, compensated (±{US_COMP_DT:.0f} K air column): ±{comp:.1f} mm temperature, RSS ±{rss_u:.1f} mm with module ±{US_ACC:.0f} mm; R2 not met")
arm_I = (P["arm_sq"] ** 4 - (P["arm_sq"] - 2 * P["arm_wall"]) ** 4) / 12
sag_bird = 10.0 * (D["cantilever"] - D["pole_r"]) ** 3 / (3 * E_AL * arm_I)
tag("B4", f"arm I = {arm_I:,.0f} mm4; a 1 kg bird at the head moves it {sag_bird:.2f} mm (unbraced upper bound); negligible")

# ------------------------------------------------------------------ C. Drain level error and tube hydraulics (R4, R3)
print("\nC. Drain level (R4, R3)")
rmax = D["dh_range_max"]
t_comp = rmax * 0.606 * DRAIN_COMP_DT / c_sound(T_CAL)
t_unc = rmax * 0.606 * DRAIN_UNCOMP_DT / c_sound(T_CAL)
rss_d = math.sqrt(US_ACC ** 2 + t_comp ** 2 + DRAIN_DATUM ** 2)
rss_du = math.sqrt(US_ACC ** 2 + t_unc ** 2 + DRAIN_DATUM ** 2)
tag("C1", f"compensated with the head NTC (±{DRAIN_COMP_DT:.0f} K) at {rmax:.0f} mm range: temperature ±{t_comp:.1f} mm, "
          f"RSS ±{rss_d:.1f} mm (target ±20 mm)")
tag("C2", f"uncompensated (±{DRAIN_UNCOMP_DT:.0f} K): temperature ±{t_unc:.1f} mm, RSS ±{rss_du:.1f} mm; the NTC is needed for margin")
a_tube = math.pi * (D["tube_id"] / 2) ** 2
sw, sl = P["slot"]
a_row = P["slots_per_row"] * sw * sl
a_all = a_row * P["slot_rows"]
open_ratio = a_all / (math.pi * P["tube_od"] * D["tube_len"])
tag("C3", f"tube bore {a_tube:,.0f} mm2; slots {a_row:,.0f} mm2 per row, {a_all:,.0f} mm2 in all ({open_ratio * 100:.1f} % of the wall)")
for rise in (0.33, 10.0, 50.0):                    # mm/s: 20 mm/min, fast surcharge, extreme
    q = a_tube * rise * 1e-9                        # m3/s
    v = q / (0.6 * a_row * 1e-6)
    tag("C4", f"basin rising {rise:g} mm/s with only the lowest slot row wet: lag head {v ** 2 / 19.62 * 1000:.2f} mm")

# ------------------------------------------------------------------ D. Energy (R8, R5)
print("\nD. Energy (R8)")
e_cycle = (V_RAIL_R * I_RADAR * T_RADAR + V_RAIL_U * I_US * T_US) / ETA_RAIL + 3.3 * I_MCU * T_MCU
tag("D1", f"per sampling cycle: radar {V_RAIL_R * I_RADAR * T_RADAR * 1000:.1f} mJ, ultrasonic {V_RAIL_U * I_US * T_US * 1000:.1f} mJ, "
          f"rails at {ETA_RAIL:.0%}, MCU {3.3 * I_MCU * T_MCU * 1000:.1f} mJ: {e_cycle * 1000:.1f} mJ")
res = {}
for name, dt, rep in (("normal", SAMPLE_NORMAL, NORMAL_REPORT_S), ("event all day", SAMPLE_FAST, EVENT_REPORT_S)):
    n = 86400 / dt
    sens_mw = e_cycle * n / 86400 * 1000
    extra_reports = 86400 / rep - 86400 / NORMAL_REPORT_S
    radio_mw = extra_reports * E_REPORT / 86400 * 1000
    wh = FND_CORE_WH + (sens_mw + radio_mw) * 24 / 1000
    res[name] = (sens_mw, radio_mw, wh)
    tag("D2", f"{name}: {n:,.0f} cycles/day, sensor load {sens_mw:.2f} mW, extra uplinks {radio_mw:.2f} mW, "
              f"draw with core {wh:.3f} Wh/day")
s_ev, r_ev, wh_ev = res["event all day"]
tag("D3", f"event all day uses {(s_ev + r_ev) / FND_ALLOW[0] * 100:.1f} % of the {FND_ALLOW[0]:.0f} mW FieldNode design allowance "
          f"({FND_ALLOW[1]:.0f} mW ceiling)")
aut = FND_USABLE_WH / wh_ev
tag("D4", f"autonomy without sun at event sampling all day: {aut:.0f} days nominal, {aut * FND_COLD:.0f} days at -20 C (target 5 days)")
tag("D5", f"hot clear day, FieldNode without a shield stores {FND_HOT_STORED} Wh (FND-CAL-001) against {wh_ev:.3f} Wh drawn: still positive")

# ------------------------------------------------------------------ E. Airtime (R7)
print("\nE. Airtime (R7)")


def airtime(sf, pl=PAYLOAD + 13, bw=125e3, cr=1, preamble=8):
    tsym = 2 ** sf / bw
    de = 1 if sf >= 11 else 0
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (preamble + 4.25) * tsym + n * tsym


air = {sf: airtime(sf) for sf in range(7, 13)}
for sf, a in air.items():
    normal_day = a * 86400 / NORMAL_REPORT_S
    event_h = a * 3600 / EVENT_REPORT_S
    spare = TTN_S - normal_day
    extra_per_min = (1 - EVENT_REPORT_S / NORMAL_REPORT_S) / EVENT_REPORT_S * 60     # extra uplinks per minute of event
    ttn_min = spare / a / extra_per_min if spare > 0 else 0.0
    min_int = a / DUTY
    tag("E1", f"SF{sf}: {a * 1000:.1f} ms; normal {normal_day:.1f} s/day; event {event_h:.1f} s/h against 36 s/h "
              f"({'met' if event_h <= 36 else 'NOT met'}); shortest interval under 1 % {min_int:.0f} s; "
              f"TTN event minutes before 30 s/day {ttn_min:.0f}")

# ------------------------------------------------------------------ F. Alert latency (R6)
print("\nF. Alert latency (R6)")
random.seed(3)
off9 = air[9] / DUTY - air[9]


def latency(net, slow=True):
    sample = random.uniform(0, SAMPLE_NORMAL if slow else SAMPLE_FAST)
    confirm = CONFIRM * SAMPLE_FAST
    p_off = air[9] / (NORMAL_REPORT_S if slow else EVENT_REPORT_S) / DUTY
    wait = random.uniform(0, off9) if random.random() < p_off else 0.0
    t = sample + confirm + WAKE + air[9] + wait
    if random.random() < LOSS:                       # repeat after the off-time
        t += off9 + air[9]
    return t + random.uniform(*net)


def pct(xs, q):
    xs = sorted(xs)
    return xs[int(q * (len(xs) - 1))]


N = 200_000
for label, net in (("private gateway", NET_PRIVATE), ("city or public server", NET_PUBLIC)):
    for slow in (True, False):
        xs = [latency(net, slow) for _ in range(N)]
        tag("F1", f"{label}, {'slow rise from normal mode' if slow else 'already in event mode'}: "
                  f"mean {sum(xs) / N:.0f} s, 95th percentile {pct(xs, 0.95):.0f} s, max of {N:,} {max(xs):.0f} s")
worst = SAMPLE_NORMAL + CONFIRM * SAMPLE_FAST + WAKE + air[9] + off9 + NET_PRIVATE[1]
tag("F2", f"deterministic worst case without a lost packet, private gateway: {worst:.0f} s "
          f"(60 + 20 + {WAKE + air[9]:.1f} + {off9:.1f} duty-cycle wait + {NET_PRIVATE[1]} s)")
for rate in (20.0, 100.0):
    lat = worst if rate <= 20 else SAMPLE_FAST + CONFIRM * SAMPLE_FAST + WAKE + air[9] + off9 + NET_PRIVATE[1]
    tag("F3", f"water rising {rate:.0f} mm/min: {rate * lat / 60:.0f} mm more depth by the time the alert is issued ({lat:.0f} s)")

# ------------------------------------------------------------------ G. False readings (R10)
print("\nG. False readings (R10)")
for name, h in (("car roof", 1.45), ("van roof", 2.0), ("person", 1.75), ("snow bank", 0.5)):
    app = h * 1000
    tag("G1", f"{name} {h:.2f} m under the head reads as {app:.0f} mm depth: "
              f"{'outside the 600 mm range, rejected' if app > 600 else 'inside the range; needs the drain cross-check'}")
tag("G2", "rules: reject depth above 600 mm; reject a step above 50 mm between 10 s samples unless the drain head is full "
          "or rising; require 3 consecutive readings above a band; flag a gauge silent for 30 min")

# ------------------------------------------------------------------ H. Arm structure and clamps (R15)
print("\nH. Arm, brace and clamps (R15)")
L_arm_out = D["pole_face_x"] - D["arm_x0"]
f_arm = L_arm_out * P["arm_sq"] * 1e-6 * CD_SQ * Q_WIND
lev_arm = P["pole_x"] - (D["arm_x0"] + D["pole_face_x"]) / 2
f_head = P["head_d"] * P["head_h"] * 1e-6 * CD_CYL * Q_WIND
f_brace = D["brace_len"] * P["brace_sq"] * 1e-6 * CD_SQ * Q_WIND
lev_brace = P["pole_x"] - (D["pole_face_x"] - P["brace_leg"] / 2)
torque = f_arm * lev_arm / 1000 + f_head * D["cantilever"] / 1000 + f_brace * lev_brace / 1000
t_cap = 2 * MU * 2 * BAND_PRELOAD * D["pole_r"] / 1000
tag("H1", f"wind along the street at 35 m/s (q {Q_WIND:.0f} Pa): arm {f_arm:.1f} N, head {f_head:.1f} N, brace {f_brace:.1f} N; "
          f"twist about the pole {torque:.1f} N m")
tag("H2", f"two band clamps at {BAND_PRELOAD:.0f} N preload, friction {MU}: twist capacity {t_cap:.1f} N m, factor {t_cap / torque:.2f}")
brace_x = D["pole_face_x"] - P["brace_leg"]
m_tip = HANG * (brace_x - D["head_x"]) / 1000
z_arm = arm_I / (P["arm_sq"] / 2)
sig = m_tip * 1000 / z_arm
m_clamp = HANG * D["cantilever"] / 1000
h_brace = m_clamp / (P["clamp_dz"] / 1000)
f_br = h_brace * math.sqrt(2)
bI = (P["brace_sq"] ** 4 - (P["brace_sq"] - 2 * P["brace_wall"]) ** 4) / 12
pcr = math.pi ** 2 * E_AL * bI / D["brace_len"] ** 2
tag("H3", f"50 kg hanging on the head: arm moment at the brace joint {m_tip:.0f} N m, stress {sig:.0f} MPa against {SY_AL:.0f} MPa "
          f"(factor {SY_AL / sig:.1f}); brace force {f_br:.0f} N against buckling {pcr:,.0f} N")
tag("H4", f"upper clamp pull {h_brace:.0f} N against {2 * BAND_PRELOAD:.0f} N band capacity (factor {2 * BAND_PRELOAD / h_brace:.1f}); "
          f"slip resistance {2 * MU * 2 * BAND_PRELOAD:.0f} N against {HANG + 30:.0f} N down")

# ------------------------------------------------------------------ I. Mass on the pole (R15)
print("\nI. Mass on the pole (R15)")
sq = lambda a, t: a * a - (a - 2 * t) ** 2
masses = {
    "FieldNode core (FND-CAL-001)": P["fieldnode_mass"],
    "arm tube (model length)": sq(P["arm_sq"], P["arm_wall"]) * D["arm_len"] * RHO_AL,
    "knee brace (model length)": sq(P["brace_sq"], P["brace_wall"]) * D["brace_len"] * RHO_AL,
    "band clamps and brackets, 2 (assumed)": 0.30,
    "head saddle and fixings (assumed)": 0.10,
    "street radar head (assumed)": 0.25,
    "street cable 2 m at 0.07 kg/m": 0.14,
    "drain cable on the pole, 2.5 m at 0.07 kg/m": 0.175,
    "depth marker plate (model)": P["marker"][0] * P["marker"][1] * P["marker"][2] * RHO_AL,
}
tot = sum(masses.values())
tag("I1", "; ".join(f"{k} {v:.2f}" for k, v in masses.items()) + " kg")
tag("I2", f"total on the pole {tot:.2f} kg against 5.0 kg ({(5.0 - tot) / 5.0 * 100:.0f} % margin); TRL 2 estimate was 3.1 kg with FieldNode at 1.7 kg")

# ------------------------------------------------------------------ J. Cables and interface (R11 context)
print("\nJ. Cables and ports")
tag("J1", f"street cable run {D['cable_street']:.0f} mm plus 300 mm drip loops: {(D['cable_street'] + 300) / 1000:.2f} m in a 2 m cable; "
          f"I2C bus about {2 * 100 + 50:.0f} pF against 400 pF")
tag("J2", f"drain cable run {D['cable_drain']:.0f} mm plus 500 mm loops: {(D['cable_drain'] + 500) / 1000:.2f} m in a 5 m cable; UART and one analog pin (wet probe)")
tag("J3", "port use: street head on port A at 3.3 V (I2C); drain head on port B at 5 V (UART plus analog wet probe); one switched rail per port (FND R11)")

# ------------------------------------------------------------------ K. Submersion (R9)
print("\nK. Submersion (R9)")
head_max = (600.0 - D["dh_face"]) / 1000
tag("K1", f"deepest design case: water 600 mm above the road puts {head_max:.2f} m ({head_max * 9.81:.1f} kPa) over the drain head face; "
          f"R9 asks 2.0 m ({2 * 9.81:.1f} kPa) for 72 h; stock module IP67 (1 m, 30 min); the transducer face cannot be potted over")

# ------------------------------------------------------------------ L. Installation (R12)
print("\nL. Installation (R12)")
tasks = [("Set up pedestrian and traffic protection", 10), ("Fit clamps, arm and brace from a ladder", 15),
         ("Hang FieldNode and plug the street head (FND-CAL-001 install)", 15), ("Fix marker plate", 5),
         ("Survey head height and record dry background", 10), ("Lift grate with hook, two people", 5),
         ("Drill two wall anchors through the grate opening with an extension", 20), ("Fit tube and drain head, close grate", 10)]
t_no = sum(t for _, t in tasks)
tag("L1", "; ".join(f"{a} {t} min" for a, t in tasks) + f"; total {t_no} min without the conduit")
tag("L2", "conduit: core 32 mm through the basin wall (needs excavation outside the wall or entry), trench or bore about "
          f"{(P['pole_x'] + 60 - P['basin'][1]) / 1000:.2f} m under the sidewalk: civil crew, well over 90 min")

# ------------------------------------------------------------------ M. Cost (R16)
print("\nM. Cost (R16)")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
priced = all((r["unit_cost_usd"] or "").strip() for r in rows)
line = lambda r: float(r["qty"]) * float(r["unit_cost_usd"])
total = sum(line(r) for r in rows)
fnd = sum(line(r) for r in rows if r["item"].startswith("1 "))
spec = total - fnd
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
tag("M1", f"BOM {len(rows)} lines, all priced: {priced}; FloodGauge-specific (lines 2 to 10) ${spec:.2f} against budget_usd ${budget:.0f} "
          f"(margin ${budget - spec:.2f}); complete gauge with FieldNode ${total:.2f}")

# ------------------------------------------------------------------ status table
print("\n[S] Requirement status")
status = [
    ("R1", "Met on paper", f"{D['range_dry'] / 1000:.2f} to {D['range_600'] / 1000:.2f} m range; module to 20 m", "0 to 600 mm; head 2.5 to 3.5 m"),
    ("R2", "Met on paper (module accuracy assumed)", f"radar RSS ±{rss_r:.1f} mm, sum ±{lin_r:.1f} mm; ultrasonic variant ±{rss_u:.1f} mm", "±10 mm"),
    ("R3", "Not met", f"continuous to {-D['dh_top_level']:.0f} mm below the road; top {-gap:.0f} mm wet probe only", "50 mm above floor to grate underside"),
    ("R4", "Met on paper", f"±{rss_d:.1f} mm with NTC; ±{rss_du:.1f} mm without", "±20 mm"),
    ("R5", "Met by design", "60 s and 10 s schedule set in the sampling logic", "60 s; 10 s in events"),
    ("R6", "Met on paper (private gateway)", f"worst {worst:.0f} s without packet loss", "120 s, 95 % of events"),
    ("R7", "At risk", f"SF9 {air[9] * 86400 / NORMAL_REPORT_S:.1f} s/day; event 1 % met SF7 to SF10, not SF11 or SF12", "1 % always; TTN 30 s/day normal"),
    ("R8", "Met on paper", f"{aut:.0f} days nominal, {aut * FND_COLD:.0f} days at -20 C", "5 days at event sampling"),
    ("R9", "At risk", "potted head; transducer face seal IP67 only", "IP68, 2 m, 72 h"),
    ("R10", "Not verifiable at TRL 3", "rules defined; curb echo needs a recorded background", "1 false alert per year or fewer"),
    ("R11", "Met by design", "levels, status and battery only", "no camera or microphone"),
    ("R12", "Not met", f"{t_no} min without conduit; conduit is civil work", "90 min, surface only, no basin entry"),
    ("R13", "Met on paper", "tape and radar dry-background survey; yearly marker check", "±5 mm"),
    ("R14", "At risk", "FieldNode R2/R3 heat (inherited); A02YYUW rated -15 to 60 C", "-20 to 50 C"),
    ("R15", "Met on paper", f"{tot:.2f} kg; clamp twist factor {t_cap / torque:.2f}", "40 to 60 mm poles; 5 kg"),
    ("R16", "Met on paper", f"${spec:.2f} FloodGauge-specific; ${total:.2f} with FieldNode", "$150 FloodGauge-specific"),
    ("R17", "Met by design", "JSON or CSV through the gateway", "open format"),
]
with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    for rid, st, val, tgt in status:
        w.writerow([rid, val, tgt, st])
        print(f"  {rid:<4} | {st:<40} | {val}")
counts = {}
for _, st, _, _ in status:
    k = st.split(" (")[0]
    counts[k] = counts.get(k, 0) + 1
print("  counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
