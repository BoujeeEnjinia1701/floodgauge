"""FloodGauge sizing calculations, FLG-CAL-001 v0.6 (TRL 3, constructable design, FLG-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md; each line carries a tag such as [B2]
that the note cites. It also writes docs/04-calcs/results.csv (requirement status table).
Geometry comes from cad/src/model.py (PARAMS and derived), the parts cost from bom/bom.csv and
the value-engineering target (budget_usd) from project.yaml. FieldNode figures come from the FieldNode repo
(FND-CAL-001, FND-BLD-001). Masses of the made parts and the cable runs are measured on the model.
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
from model import PARAMS as P, derived, masses, cable_runs  # noqa: E402

D = derived(P)
MASS = masses(P)
RUNS = cable_runs(P)


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
BOLT_AS, BOLT_FUB = 36.6, 700.0    # mm2, MPa: M8 stainless A4-70 through-bolt (DDR-002)
POLE_T, POLE_FU = 2.5, 360.0       # mm, MPa: pole wall and steel strength at the bolt holes (assumed)
CABLE_PF = 100.0              # pF/m, outdoor multicore cable (assumed)
CABLE_KG = 0.07               # kg/m

print("FloodGauge sizing, FLG-CAL-001 v0.6")
print(f"Geometry from cad/src/model.py: lens {P['head_z']:.0f} mm above the road, {P['head_offset']:.0f} mm past the curb face; "
      f"tube {D['tube_len']:.0f} mm, ID {D['tube_id']:.0f} mm")

# ------------------------------------------------------------------ A. Geometry and range
print("\nA. Geometry and range (R1, R3)")
tag("A1", f"street head range: {D['range_dry'] / 1000:.2f} m to the dry road, {D['range_600'] / 1000:.2f} m at 600 mm depth; "
          f"radar module range up to 20 m (Acconeer); depth = {P['head_z']:.0f} mm minus range")
hb0, hb1 = P["head_band"]
tag("A1b", f"R1 mounting band {hb0 / 1000:.1f} to {hb1 / 1000:.1f} m: range {(hb0 - 600) / 1000:.1f} to {hb1 / 1000:.1f} m over the band, "
           f"within the 20 m module range; beam footprint radius {hb1 * math.tan(math.radians(BEAM_FULL / 2)):.0f} mm at {hb1 / 1000:.1f} m")
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
          f"({-gap:.0f} mm) has only the wet probe (one point); R3 as restated under DDR-002 asks for a continuous reading to "
          f"{-D['dh_top_level']:.0f} mm below the road plus a drain-full signal above that")
tag("A6", f"tube mouth {P['tube_bot_gap']:.0f} mm above the floor, outlet invert {D['outlet_invert'] - P['basin_floor']:.0f} mm above the floor; "
          f"the 50 mm level lies {P['tube_bot_gap'] - 50:.0f} mm below the mouth, in the beam path")
clear_need = VEH_H[1] + VEH_MARGIN
clears = P["head_z"] / 1000 >= clear_need - 1e-9
tag("A7", f"head underside {P['head_z'] / 1000:.2f} m against a {VEH_H[0]:.1f} to {VEH_H[1]:.1f} m vehicle envelope at the curb plus {VEH_MARGIN:.1f} m: "
          f"needs {clear_need:.1f} m, {'clear' if clears else 'NOT clear'}; inside the R1 band {hb0 / 1000:.1f} to {hb1 / 1000:.1f} m; "
          f"at 2.95 m (the TRL 3 v0.1 height) the head would be inside the envelope")

# ------------------------------------------------------------------ B. Street depth error (R2)
print("\nB. Street depth error (R2)")
thermal = ALPHA_STEEL * (D["arm_z"]) * DT_POLE
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
sag_bird = 10.0 * (D["plate_front_x"] - D["head_x"]) ** 3 / (3 * E_AL * arm_I)
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
print("\nH. Arm, brace, pole bracket and clamps (R15)")
L_arm_out = D["plate_front_x"] - D["arm_x0"]
f_arm = L_arm_out * P["arm_sq"] * 1e-6 * CD_SQ * Q_WIND
lev_arm = P["pole_x"] - (D["arm_x0"] + D["plate_front_x"]) / 2
f_head = P["head_d"] * P["head_h"] * 1e-6 * CD_CYL * Q_WIND
(xt, zt), (xf_, zf_) = D["pin_top"], D["pin_foot"]
f_brace = D["brace_pins"] * P["brace_sq"] * 1e-6 * CD_SQ * Q_WIND
lev_brace = P["pole_x"] - (xt + xf_) / 2
f_plate = P["bplate"][1] * D["bplate_h"] * 1e-6 * CD_SQ * Q_WIND * 0.0   # plate edge-on to wind along the street
torque = f_arm * lev_arm / 1000 + f_head * D["cantilever"] / 1000 + f_brace * lev_brace / 1000
t_cap = 2 * MU * 2 * BAND_PRELOAD * D["pole_r"] / 1000
tag("H1", f"wind along the street at 35 m/s (q {Q_WIND:.0f} Pa): arm {f_arm:.1f} N, head {f_head:.1f} N, brace {f_brace:.1f} N; "
          f"twist about the pole {torque:.1f} N m")
tag("H2", f"two band clamps at {BAND_PRELOAD:.0f} N preload, friction {MU}: twist capacity {t_cap:.1f} N m, factor {t_cap / torque:.2f} on friction alone")
f_shear = 0.6 * BOLT_FUB * BOLT_AS
f_bear = 2.5 * POLE_FU * P["bolt_d"] * POLE_T
f_bolt = min(f_shear, f_bear)
t_bolt = f_bolt * P["pole_od"] / 1000
tag("H2b", f"M8 through-bolt across the street through the bracket plate, a {D['spacer_len']:.1f} mm spacer and the pole: shear {f_shear / 1000:.1f} kN per plane, "
           f"pole wall bearing {f_bear / 1000:.1f} kN ({POLE_T} mm wall assumed); couple across the {P['pole_od']:.0f} mm pole {t_bolt:.0f} N m, "
           f"factor {t_bolt / torque:.0f} against wind twist")
m_tip = HANG * (xt - D["head_x"]) / 1000
arm_I = (P["arm_sq"] ** 4 - (P["arm_sq"] - 2 * P["arm_wall"]) ** 4) / 12
z_arm = arm_I / (P["arm_sq"] / 2)
sig = m_tip * 1000 / z_arm
lever = D["arm_z"] - zf_                                   # arm axis to the brace foot pin
m_clamp = HANG * (D["plate_front_x"] - D["head_x"]) / 1000
h_pull = m_clamp / (lever / 1000)                          # arm pull at the cleats = brace push across, horizontal
f_br = h_pull * math.sqrt(2)
bI = (P["brace_sq"] ** 4 - (P["brace_sq"] - 2 * P["brace_wall"]) ** 4) / 12
pcr = math.pi ** 2 * E_AL * bI / D["brace_pins"] ** 2
tag("H3", f"50 kg hanging on the head: arm moment at the top brace pin {m_tip:.0f} N m, stress {sig:.0f} MPa against {SY_AL:.0f} MPa "
          f"(factor {SY_AL / sig:.1f}, {P['arm_wall']} mm wall); brace force {f_br:.0f} N against buckling {pcr:,.0f} N "
          f"({P['brace_sq']:.0f} x {P['brace_sq']:.0f} x {P['brace_wall']} mm, {D['brace_pins']:.0f} mm between pins)")
tag("H4", f"arm pull at the cleats {h_pull:.0f} N, carried by the upper band against {2 * BAND_PRELOAD:.0f} N band capacity "
          f"(factor {2 * BAND_PRELOAD / h_pull:.1f}); slip resistance {2 * MU * 2 * BAND_PRELOAD:.0f} N against {HANG + 30:.0f} N down")
M6_AS, M6_FUB, AL_FU = 20.1, 700.0, 240.0
v_m6 = 0.6 * M6_FUB * M6_AS
bear_wall = 2.5 * AL_FU * 6.0 * P["arm_wall"]
tag("H5", f"M6 A4-70 bolts: shear {v_m6 / 1000:.1f} kN per plane; arm cleat joint two bolts in double shear, {4 * v_m6 / 1000:.0f} kN, "
          f"bearing in the {P['arm_wall']} mm arm walls {4 * bear_wall / 1000:.1f} kN, against the {h_pull / 1000:.2f} kN pull; "
          f"brace pins in double shear {2 * v_m6 / 1000:.1f} kN against {f_br / 1000:.2f} kN")

# ------------------------------------------------------------------ I. Mass on the pole (R15)
print("\nI. Mass on the pole (R15)")
on_pole = ["bplate", "vblocks", "bands", "cleats", "top_clip", "foot_clip", "arm", "brace", "spacer", "through_bolt",
           "head_plate", "head_screws", "fixings", "pins", "marker", "marker_bands"]
drain_on_pole = (D["node_bot"] - D["riser_top"] + 250) / 1000
masses = {"FieldNode core (FND-BLD-001)": P["fieldnode_mass"]}
masses.update({f"{k} (model)": MASS[k] for k in on_pole})
masses.update({"street radar head (assumed)": 0.25, "street cable 3 m": 3.0 * CABLE_KG,
               f"drain cable on the pole {drain_on_pole:.1f} m": drain_on_pole * CABLE_KG})
tot = sum(masses.values())
tag("I1", "; ".join(f"{k} {v:.3f}" for k, v in masses.items()) + " kg")
off_pole = sum(MASS[k] for k in ("guard", "gutter_cover", "curb_cover", "walk_cover"))
tag("I2", f"total on the pole {tot:.2f} kg against 5.0 kg (margin {5.0 - tot:.2f} kg, {(5.0 - tot) / 5.0 * 100:.1f} %); v0.3 gave 4.74 kg; "
          f"the riser guard and the three covers ({off_pole:.2f} kg) stand on the sidewalk and are not carried by the pole")

# ------------------------------------------------------------------ J. Cables and interface (R11 context)
print("\nJ. Cables and ports")
tag("J1", f"street cable run along the arm and down the pole to port A {RUNS['street']:.0f} mm plus 300 mm drip loops: {(RUNS['street'] + 300) / 1000:.2f} m in a 3 m cable; "
          f"I2C bus about {3 * CABLE_PF + 50:.0f} pF against 400 pF (a 5 m cable would give {5 * CABLE_PF + 50:.0f} pF)")
tag("J2", f"drain cable run through the grate opening, under the covers, up the riser guard and the pole to port B {RUNS['drain']:.0f} mm plus 500 mm loops: {(RUNS['drain'] + 500) / 1000:.2f} m in a 5 m cable; "
          f"UART and one analog pin (wet probe)")
tag("J3", "port use: street head on port A at 3.3 V (I2C); drain head on port B at 5 V (UART plus analog wet probe); one switched rail per port (FND R11)")

# ------------------------------------------------------------------ K. Submersion (R9)
print("\nK. Submersion (R9)")
head_max = (600.0 - D["dh_face"]) / 1000
tag("K1", f"deepest design case: water 600 mm above the road puts {head_max:.2f} m ({head_max * 9.81:.1f} kPa) over the drain head face; "
          f"R9 asks 2.0 m ({2 * 9.81:.1f} kPa) for 72 h; stock module IP67 (1 m, 30 min); the transducer face cannot be potted over")

# ------------------------------------------------------------------ L. Installation (R12)
print("\nL. Installation (R12)")
tasks = [("Set up pedestrian and traffic protection", 10), ("Lift the arm, assembled on the ground, and fit its two band clamps from a mobile platform", 15),
         ("Drill the pole through the bracket plate and fit the anti-rotation through-bolt", 5),
         ("Hang FieldNode and plug the street head (FND-CAL-001 install)", 15), ("Fix marker plate", 5),
         ("Survey head height and record dry background", 10), ("Lift grate with hook, two people", 5),
         ("Drill two wall anchors through the grate opening with an extension", 20), ("Fit tube and drain head, close grate", 10),
         ("Fit the three covers (eight anchors), the riser guard and the marker band clamps", 25)]
t_no = sum(t for _, t in tasks)
R12_PILOT_MIN = 120      # decided 2026-10-02: 120 min for the pilot surface route; 90 min stays the target for permanent sites
tag("L1", "; ".join(f"{a} {t} min" for a, t in tasks) + f"; total {t_no} min with the surface cable route, no civil work")
tag("L2", f"surface cover {D['cover_len'] / 1000:.2f} m (gutter strip, curb face, sidewalk); anchors in the curb and sidewalk only, none in the road; "
          f"the conduit (coring the basin wall and a {(D['riser_x'] - P['basin'][1]) / 1000:.2f} m trench) is kept for permanent sites with road works")

# ------------------------------------------------------------------ M. Cost (R16)
print("\nM. Cost (R16)")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
priced = all((r["unit_cost_usd"] or "").strip() for r in rows)
line = lambda r: float(r["qty"]) * float(r["unit_cost_usd"])
total = sum(line(r) for r in rows)
fnd = sum(line(r) for r in rows if r["item"].startswith("1 "))
spec = total - fnd
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
tag("M1", f"BOM {len(rows)} lines, all priced: {priced}; FloodGauge-specific (lines 2 to 10) ${spec:.2f} against the value-engineering target "
          f"(budget_usd) ${budget:.0f}: ${abs(spec - budget):.2f} {'over' if spec > budget else 'under'} the target; complete gauge with FieldNode ${total:.2f}")
big = sorted(((line(r), r["item"]) for r in rows if not r["item"].startswith("1 ")), reverse=True)[:4]
tag("M2", "main cost drivers: " + "; ".join(f"{n} ${c:.2f}" for c, n in big))

# ------------------------------------------------------------------ status table
print("\n[S] Requirement status")
status = [
    ("R1", "Met on paper", f"lens {P['head_z'] / 1000:.2f} m clears a {VEH_H[1]:.1f} m vehicle; range {(hb0 - 600) / 1000:.1f} to {hb1 / 1000:.1f} m over the band; module to 20 m", "0 to 600 mm; head 2.5 to 5.0 m per site"),
    ("R2", "Met on paper (module accuracy assumed)", f"radar RSS ±{rss_r:.1f} mm, sum ±{lin_r:.1f} mm; ultrasonic variant ±{rss_u:.1f} mm", "±10 mm"),
    ("R3", "Met on paper", f"continuous {P['basin_floor'] + 50:.0f} to {D['dh_top_level']:.0f} mm; wet probe at {D['probe_level']:.0f} mm", "50 mm above floor to 330 mm below road, drain-full above"),
    ("R4", "Met on paper", f"±{rss_d:.1f} mm with NTC; ±{rss_du:.1f} mm without", "±20 mm"),
    ("R5", "Met by design", "60 s and 10 s schedule set in the sampling logic", "60 s; 10 s in events"),
    ("R6", "Met on paper (private gateway)", f"worst {worst:.0f} s without packet loss", "120 s, 95 % of events"),
    ("R7", "At risk", f"SF9 {air[9] * 86400 / NORMAL_REPORT_S:.1f} s/day; event 1 % met SF7 to SF10, not SF11 or SF12", "1 % always; TTN 30 s/day normal"),
    ("R8", "Met on paper", f"{aut:.0f} days nominal, {aut * FND_COLD:.0f} days at -20 C", "5 days at event sampling"),
    ("R9", "At risk", "potted head; transducer face seal IP67 only", "IP68, 2 m, 72 h"),
    ("R10", "Not verifiable at TRL 3", "rules defined; curb echo needs a recorded background", "1 false alert per year or fewer"),
    ("R11", "Met by design", "levels, status and battery only", "no camera or microphone"),
    ("R12", "Not met" if t_no > R12_PILOT_MIN else "Met on paper", f"{t_no} min on the surface route; no civil work",
     f"{R12_PILOT_MIN} min for the pilot surface route, no basin entry (90 min at permanent sites on the conduit route)"),
    ("R13", "Met on paper", "tape and radar dry-background survey; yearly marker check", "±5 mm"),
    ("R14", "At risk", "FieldNode R2/R3 heat (inherited); A02YYUW rated -15 to 60 C", "-20 to 50 C"),
    ("R15", "Met on paper" if tot <= 5.0 else "Not met", f"{tot:.2f} kg; twist factor {t_bolt / torque:.0f} with the through-bolt", "40 to 60 mm poles; 5 kg"),
    ("R16", "Within the value-engineering target" if spec <= budget else f"Over the value-engineering target by ${spec - budget:.2f}",
     f"${spec:.2f} FloodGauge-specific; ${total:.2f} with FieldNode", f"${budget:.0f} FloodGauge-specific (value-engineering target)"),
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
