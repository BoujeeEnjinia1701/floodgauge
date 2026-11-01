"""FloodGauge STEM check calculations (FLG-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. Each claim of the three concept options (A radar and ultrasonic, B hydrostatic,
C float and reed chain) gets a first-order check from the geometry in cad/src/model.py (PARAMS, derived) and from textbook
physics. This is an independent screen: it does not import docs/04-calcs/sizing.py (FLG-CAL-001), which holds the full sizing;
the CAL values it closes against are read from docs/04-calcs/results.csv where they are numbers.
Assumed values are marked "assumed" in the law column and are listed again in FLG-STM-001.
"""
import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX, R  # noqa: E402,F401
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)
c = Check(ROOT / "docs" / "04-calcs" / "stem_results.csv")
RHO_W, RHO_PP, RHO_MAG = 1000.0, 900.0, 7500.0       # kg/m3: water, polypropylene, sintered NdFeB
Q_WIND = 0.5 * 1.225 * 35.0 ** 2                       # Pa at 35 m/s
CAL = {r["id"]: r for r in csv.DictReader((ROOT / "docs" / "04-calcs" / "results.csv").open())}


def cal_num(rid, pattern):
    m = re.search(pattern, CAL[rid]["value"])
    return float(m.group(1)) if m else float("nan")


# ------------------------------------------------------------------ Option A: radar over the gutter, ultrasonic in a stilling tube
# Physics: waves
c.claim("S1", "A: the street radar (60 GHz, module range 20 m) reaches the dry road 4.6 m below the lens and the water surface in between",
        "Physics", "Waves and radar", "Free-space propagation of a 60 GHz pulse; module range 20 m (Acconeer product page, as cited in FLG-PRB-001, 2026-09-25)",
        P["head_band"][1] / 1000, 20.0, "m", rule="below", closed_by="FLG-CAL-001 A1b")
lam = 299792458.0 / 60e9 * 1000
rad_acc = 2.0
thermal = 12e-6 * D["arm_z"] * 35.0
rss_other = math.sqrt(5.0 ** 2 + thermal ** 2 + 3.0 ** 2)
max_mod = math.sqrt(max(10.0 ** 2 - rss_other ** 2, 0.0))
c.cited("S2", "A: street depth error stays within 10 mm when the radar module is accurate to 2 mm (assumed) and datum, pole expansion and ripple add 5, 2 and 3 mm",
        "Physics", "Measurement error", "Root sum square of independent errors; the 2 mm module accuracy is assumed (S3), so the budget holds only if the module meets it",
        "2 mm <= %.2f mm: the module may be as poor as %.1f mm before the 10 mm limit is reached, but pole bow in the sun (about 3 mm for a 5 K difference across the pole, independent review) and the worst-case sum of 12 mm are not inside the RSS" % (max_mod, max_mod),
        PLAUSIBLE)
c.cited("S3", "A: a 60 GHz carrier (wavelength %.2f mm) gives a 2 mm range accuracy" % lam, "Physics", "Waves and radar",
        "Coherent radar reads range from the phase of the echo: a 1 mm change in range shifts the phase by 4 pi / lambda = %.2f rad, so 2 mm is several radians of phase" % (4 * math.pi / lam),
        "Phase argument supports mm-level accuracy, but the module's guaranteed accuracy, beam width through the PTFE lens and curb echo rejection are not in a data sheet yet",
        PLAUSIBLE)
t_ideal = lambda tc: math.sqrt(1.4 * 287.05 * (tc + 273.15))
worst_lin = max(abs((331.3 + 0.606 * tc) / t_ideal(tc) - 1) for tc in (-20, 0, 20, 50))
c.order_of_magnitude("S4", "A: speed of sound c = 331.3 + 0.606 T (m/s) used to compensate the drain ranger over -20 to 50 C",
                     "Physics", "Acoustics", claimed=331.3 + 0.606 * 50, estimate=t_ideal(50), unit="m/s at 50 C", factor=1.01,
                     law="Ideal gas: c = sqrt(gamma R T / M) with gamma 1.4, R 287.05 J/(kg K); worst deviation %.2f %% over the range" % (worst_lin * 100),
                     closed_by="FLG-CAL-001 B2")
c_cal = 331.3 + 0.606 * 20
unc = D["dh_range_max"] * 0.606 * 10.0 / c_cal
comp = D["dh_range_max"] * 0.606 * 2.0 / c_cal
err_drain = math.sqrt(10.0 ** 2 + comp ** 2 + 3.0 ** 2)
c.claim("S5", "A: drain level error stays within 20 mm at the 950 mm maximum range, with the NTC correcting air temperature to 2 K (10 mm module accuracy, 3 mm datum)",
        "Physics", "Acoustics", "Two-way time of flight, c = 331.3 + 0.606 T; root sum square of module, temperature and datum errors (an uncompensated 10 K swing would add %.1f mm); if the module accuracy is plus or minus (1 cm + 0.3 %% of range) the error is about 13.6 mm, and humidity in a saturated basin adds a further 0.3 to 1 %% to c, both to check on the data sheet" % unc,
        round(err_drain, 1), 20.0, "mm", rule="below", closed_by="FLG-CAL-001 C1")
c.cited("S6", "A: the ultrasonic ranger (60 degree beam) reads the water surface 0.3 m to 1.25 m below it inside a 69 mm bore tube",
        "Physics", "Acoustics", "The axial echo off the water is the shortest path for a smooth wall; but slot edges, joints, the cable loop and drops inside the tube can return an echo before the water echo, so the first echo is not always the water",
        "Smooth-wall geometry supports it; echoes from the slot edges, the cable loop and condensation on the face are not excluded by the module (independent review), so the wet probe and a recorded empty-tube background are needed",
        PLAUSIBLE)
# Physics: fluid mechanics (stilling tube lag)
a_tube = math.pi / 4 * (D["tube_id"] / 1000) ** 2
a_row = P["slots_per_row"] * P["slot"][0] * P["slot"][1] * 1e-6
rise = 10e-3                                           # m/s, a fast surcharge, 10 mm/s
v = a_tube * rise / (0.6 * a_row)
lag = v ** 2 / (2 * G) * 1000
c.claim("S7", "A: the slotted stilling tube follows a basin rising at 10 mm/s with a lag head under 5 mm even with only the lowest slot row wet",
        "Physics", "Fluid mechanics", "Orifice flow, v = Q / (Cd A) with Cd 0.6, head = v^2 / 2 g",
        round(lag, 3), 5.0, "mm", rule="below", closed_by="FLG-CAL-001 C4")
# Physics: strength of materials (arm, clamps, brace)
E_AL, SY_AL = 69000.0, 214.0
arm_I = (P["arm_sq"] ** 4 - (P["arm_sq"] - 2 * P["arm_wall"]) ** 4) / 12
z_arm = arm_I / (P["arm_sq"] / 2)
hang = 490.0
m_tip = hang * (D["pin_top"][0] - D["head_x"]) / 1000
sig = m_tip * 1000 / z_arm
c.claim("S8", "A: the 40 x 40 x 1.6 mm aluminium arm survives a 50 kg person hanging on the head (misuse case)",
        "Physics", "Strength of materials", "Cantilever to the top brace pin, sigma = M / Z; 6063-T6 class yield 214 MPa (typical, assumed)",
        round(sig, 0), SY_AL, "MPa", rule="below", margin=0.0, closed_by="FLG-CAL-001 H3")
bI = (P["brace_sq"] ** 4 - (P["brace_sq"] - 2 * P["brace_wall"]) ** 4) / 12
lever = D["arm_z"] - D["pin_foot"][1]
m_clamp = hang * (D["plate_front_x"] - D["head_x"]) / 1000
f_br = m_clamp / (lever / 1000) * math.sqrt(2)
b_area = P["brace_sq"] ** 2 - (P["brace_sq"] - 2 * P["brace_wall"]) ** 2
slender = D["brace_pins"] / math.sqrt(bI / b_area)
pcr_j = b_area * SY_AL * (1 - SY_AL / (4 * math.pi ** 2 * E_AL) * slender ** 2)
bear_pin = 2 * 2.5 * 240.0 * 6.0 * P["brace_wall"]
pcr = min(pcr_j, bear_pin)
c.claim("S9", "A: the 25 x 25 x 1.6 mm knee brace and its pins carry the same load", "Physics", "Strength of materials",
        "L/r = %.0f is below the Euler range, so Johnson inelastic buckling (%.0f N) and pin bearing in 1.6 mm walls (%.0f N) apply; the Euler value (73 kN) is not valid" % (slender, pcr_j, bear_pin),
        round(f_br, 0), round(pcr, 0), "N", rule="below", closed_by="FLG-CAL-001 H3")
# wind twist about the pole
CD_SQ, CD_CYL = 2.0, 1.2
L_arm_out = D["plate_front_x"] - D["arm_x0"]
f_arm = L_arm_out * P["arm_sq"] * 1e-6 * CD_SQ * Q_WIND
lev_arm = P["pole_x"] - (D["arm_x0"] + D["plate_front_x"]) / 2
f_head = P["head_d"] * P["head_h"] * 1e-6 * CD_CYL * Q_WIND
f_brace = D["brace_pins"] * P["brace_sq"] * 1e-6 * CD_SQ * Q_WIND
lev_brace = P["pole_x"] - (D["pin_top"][0] + D["pin_foot"][0]) / 2
torque = (f_arm * lev_arm + f_head * D["cantilever"] + f_brace * lev_brace) / 1000
t_fric = 2 * 0.30 * 2 * 1000.0 * D["pole_r"] / 1000
t_fric40 = 2 * 0.30 * 2 * 1000.0 * 20.0 / 1000
d_s = math.sqrt(4 * 36.6 / math.pi)
f_bend = 600.0 * (math.pi * d_s ** 3 / 32) / (D["spacer_len"] + P["bplate"][0] / 2)
t_bolt = min(f_bend, 0.6 * 800.0 * 36.6, 2.5 * 360.0 * P["bolt_d"] * 2.5) * (P["pole_x"] - (D["plate_rear_x"] + D["plate_front_x"]) / 2) / 1000
c.claim("S10", "A: two band clamps alone hold the arm against the twist of a 35 m/s wind along the street (60 mm pole; on a 40 mm pole friction gives %.1f N m)" % t_fric40,
        "Physics", "Strength of materials", "Coulomb friction, mu 0.30, 1 kN preload per band (FieldNode assumption); wind drag, q = 0.5 rho v^2",
        round(torque, 1), round(t_fric, 1), "N m", rule="below", margin=0.4, closed_by="S11 carries the twist as a second path; on a 40 mm pole it is the only one")
c.claim("S11", "A: the M8 A4-80 anti-rotation through-bolt holds the arm against the same twist",
        "Physics", "Strength of materials", "The bolt bends as a %.1f mm cantilever out of the pole wall through the spacer (independent review corrected the first couple model): M = f_y Z, f_y 600 MPa (A4-80), stress-area section; plate load 52 mm from the pole axis" % (D["spacer_len"] + P["bplate"][0] / 2),
        round(torque, 1), round(t_bolt, 1), "N m", rule="below", margin=0.6, closed_by="FLG-CAL-001 H2b; FLG-DDR-004 F2 (class raised from A4-70 to A4-80)")
mass = cal_num("R15", r"([\d.]+) kg")
c.claim("S12", "A: the added mass on the pole stays at or under 5 kg", "Engineering and technology", "Mass budget",
        "Sum of part volumes times density from the CAD model plus FieldNode 2.45 kg and cables (FLG-CAL-001 I1, I2)",
        mass, 5.0, "kg", rule="below", margin=0.02, closed_by="weigh at TRL 4; FLG-DEC-001 item 3 (bracket plate to 2.5 mm)")
thermal_exp = 12e-6 * D["arm_z"] * 35.0
c.order_of_magnitude("S13", "A: pole expansion moves the lens by about 2 mm over a 35 K swing", "Physics", "Thermodynamics",
                     claimed=2.0, estimate=thermal_exp, unit="mm", factor=1.3, law="Linear expansion, dL = alpha L dT with steel alpha 12e-6 per K",
                     closed_by="FLG-CAL-001 B1")
# Physics: energy and radio
aut = cal_num("R8", r"([\d.]+) days nominal")
aut_cold = cal_num("R8", r"([\d.]+) days at")
c.claim("S14", "A: stored energy runs the sensors for 5 days without sun at event sampling", "Physics", "Energy balance",
        "Usable 15.36 Wh (FND-CAL-001), draw from the sampling cycle energy of FLG-CAL-001 D1 to D4; days at -20 C used",
        5.0, aut_cold, "days", rule="below", closed_by="FLG-CAL-001 D4")


def airtime(sf, pl=33, bw=125e3, cr=1, preamble=8):
    tsym = 2 ** sf / bw
    de = 1 if sf >= 11 else 0
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (preamble + 4.25) * tsym + n * tsym


a9 = airtime(9)
c.claim("S15", "A: normal-mode uplinks (every 15 min, 20-byte payload, SF9) stay within The Things Network fair use of 30 s airtime per day",
        "Engineering and technology", "Radio", "LoRa time on air (Semtech formula); fair use 30 s/day (The Things Network, checked 2026-10-31)",
        round(a9 * 86400 / 900, 1), 30.0, "s/day", rule="below", margin=0.25, closed_by="FLG-CAL-001 E1; PR-007 stays at risk at SF10 and slower")
c.claim("S16", "A: event-mode uplinks every 60 s at SF9 stay within the EU868 1 % duty cycle", "Engineering and technology", "Radio",
        "Duty cycle = time on air / interval; limit 1 % (EU868 sub-band, ETSI EN 300 220; text not reopened, see FLG-REG-001)",
        round(a9 / 60 * 100, 2), 1.0, "%", rule="below", margin=0.25, closed_by="FLG-CAL-001 E1")
# Physics: hydrostatics on the drain head
head = (600.0 - D["dh_face"]) / 1000
c.claim("S17", "A: the drain head face, 0.9 m under water in the worst design flood, stays inside the 1 m rating of its IP67 module",
        "Physics", "Fluid mechanics", "Hydrostatic head p = rho g h; IP67 is 1 m for 30 min (IEC 60529)",
        round(head, 2), 1.0, "m", rule="below", margin=0.15, closed_by="PR-009 stays at risk: 72 h duration unverified (FLG-CAL-001 K1)")
c.cited("S18", "A: the drain head survives 72 h under silty stormwater at 2 m (IP68)", "Engineering and technology", "Ingress protection",
        "IP68 is defined by agreement with the maker, not by the code; the potted electronics are sealed but the transducer face keeps the stock IP67 seal",
        "Not shown by calculation; needs the module maker's rating or an immersion test at TRL 4. Pressure at 2 m is %.1f kPa" % (2 * 9.80665), PLAUSIBLE)
# Chemistry
c.cited("S19", "A: stainless A4 fasteners in a 6063 aluminium arm and bracket survive road-salt spray for the life of the pilot", "Chemistry", "Corrosion",
        "Galvanic couple of stainless steel and aluminium; the cathode (fastener) is small and the anode (aluminium) large, the favourable area ratio, and anodising or sleeves separate them",
        "Favourable area ratio and crush sleeves; chloride splash can still pit the aluminium at the contact, to confirm with a coating or an isolating washer at TRL 3",
        PLAUSIBLE)
t_tube = 35.0
c.claim("S20", "A: the PVC stilling tube stays below its service temperature in a shaded basin", "Chemistry", "Materials",
        "PVC-U typical maximum continuous service temperature 60 C (manufacturer data, to confirm for the chosen pipe); PVC-U also turns brittle in the cold, so impacts at -20 C are a handling risk",
        t_tube, 60.0, "C", rule="below", closed_by="BOM item 5")
# Biology
c.cited("S21", "A: 5 x 50 mm slots in the stilling tube stay open in silty, leaf-laden stormwater for a season", "Biology", "Fouling",
        "Slots 5 mm wide pass silt but clog with leaf litter and biofilm over weeks in warm standing water; 40 slots in 10 rows leave %.0f %% of the open area if a quarter clog" % 75,
        "Open area is %.0f mm2 against a %.0f mm2 bore, so a quarter clogged still passes the flow of S7; cleaning interval to assess" % (a_row * 1e6 * P["slot_rows"], a_tube * 1e6), PLAUSIBLE)

# review additions
a10 = airtime(10)
off10 = a10 / 0.01 - a10
worst10 = 10 + 2 * 10 + 1 + a10 + off10 + 4.7
c.claim("S22", "A: an event-mode alert reaches the service within 120 s at SF10 on a private gateway, worst case without a lost packet (10 s sample, two confirming samples, wake, airtime, duty-cycle wait, 4.7 s network)",
        "Mathematics", "Timing budget", "Sum of the delays; SF11 gives about %.0f s and SF12 about %.0f s, so PR-006 holds to SF10 only (independent review)" % (10 + 20 + 1 + airtime(11) / 0.01 + 4.7, 10 + 20 + 1 + airtime(12) / 0.01 + 4.7),
        round(worst10, 0), 120.0, "s", rule="below", margin=0.3, closed_by="FLG-CAL-001 F4")
c.cited("S23", "A: the street head's I2C bus stays within 400 pF on a 3 m cable", "Engineering and technology", "Electrical interface",
        "Bus capacitance = cable length x pF/m + 50 pF: 350 pF at an assumed 100 pF/m; a 150 pF/m cable gives 500 pF",
        "Passes at the assumed cable; the real cable's capacitance is on its data sheet", PLAUSIBLE)

# ------------------------------------------------------------------ Option B: hydrostatic pressure transducers
p600 = RHO_W * G * 0.6
p_basin = RHO_W * G * (-P["basin_floor"] - 50 + 0) / 1000
fs = 20e3
c.claim("B1", "B: a 0 to 20 kPa vented transducer covers 600 mm in the street (%.1f kPa) and the 1.25 m basin range (%.1f kPa)" % (p600 / 1e3, RHO_W * G * 1.25 / 1e3),
        "Physics", "Fluid mechanics", "Hydrostatic pressure p = rho g h, gauge pressure against the vented atmosphere",
        round(RHO_W * G * 1.25 / 1e3, 2), fs / 1e3, "kPa", rule="below", margin=0.25, closed_by="FLG-OPT-001 Table 1")
acc_fs = 0.0025 * fs / (RHO_W * G) * 1000                       # 0.25 % of full scale, mm of water (assumed)
rho_t = (999.8 - 992.2) / 999.8                                   # water 0 to 40 C
rho_silt = 5.0 * (1 - 1 / 2.65) / 1000                            # 5 g/l suspended solids
err_b = math.sqrt(acc_fs ** 2 + (rho_t * 600) ** 2 + (rho_silt * 600) ** 2 + 5.0 ** 2)
c.claim("B2", "B: street depth error stays within 10 mm (0.25 % of a 20 kPa range, 0 to 40 C water density, 5 g/l silt, 5 mm datum)",
        "Physics", "Measurement error", "Root sum square; water density 999.8 to 992.2 kg/m3; silt density rise = SSC (1 - rho_w / rho_s), rho_s 2.65; accuracy class assumed",
        round(err_b, 1), 10.0, "mm", rule="below", margin=0.2, closed_by="FLG-OPT-001 Table 2")
c.cited("B3", "B: the vented cable keeps the atmospheric reference dry for years", "Chemistry", "Humidity and condensation",
        "A vented gauge transducer breathes through its cable; condensation or water in the vent tube shifts the zero",
        "Desiccant or a PTFE vent membrane is the usual remedy; lifetime in a flooded basin is not shown", PLAUSIBLE)
c.cited("B4", "B: a stand pipe on the curb face does not split or crush the transducer when street water freezes at -20 C", "Physics", "Phase change",
        "Water expands about 9 % on freezing and can split a closed pipe; the bottom cap has four drain holes, so only a film freezes",
        "Drain holes leave no standing column after an event; a trapped film is expected to be harmless, to confirm", PLAUSIBLE)

# ------------------------------------------------------------------ Option C: float and reed-switch chain
def ring_cm3(od, id_, h):
    return math.pi / 4 * (od ** 2 - id_ ** 2) * h / 1000


def float_state(od, h, rp, hollow, mag_h):
    wt, hp = 1.6, 7.0
    env = ring_cm3(od, 17.8, h)
    pocket = ring_cm3(2 * rp, 17.8, hp)
    mag_g = ring_cm3(2 * rp - 0.2, 17.8, mag_h) * RHO_MAG / 1000
    void = 0.0
    if hollow:
        seg = (h - hp) / 2 - 2 * wt
        void = 2 * math.pi * ((od / 2 - wt) ** 2 - (8.9 + wt) ** 2) * seg / 1000
    pp_cm3 = env - pocket - void
    mass_g = pp_cm3 * RHO_PP / 1000 + mag_g
    buoy_g = env - pocket                                           # pocket floods with water
    return mass_g, buoy_g, (mass_g / buoy_g)


# first pass, recorded here: a solid 38 mm ring float with an 8 mm ring magnet sinks (this is the fix-rule record)
m_solid, b_solid, _ = float_state(38.0, 40.0, 12.5, False, 8.0)
m_drain_solid, b_drain_solid, _ = float_state(56.0, 45.0, 13.5, False, 8.0)
m_h, b_h, frac_h = float_state(42.0, 44.0, 12.5, True, 5.0)
md_h, bd_h, frac_dh = float_state(56.0, 45.0, 13.5, True, 5.0)
FIRST_PASS = (m_solid, b_solid, m_drain_solid, b_drain_solid)
c.claim("C1", "C: the street float (hollow shell, 42 mm OD) floats with its magnet at under 70 % of its volume submerged", "Physics", "Fluid mechanics",
        "Archimedes: weight (shell %.1f g, plus about 3 g of foam) = displaced water; solid ring first pass was %.1f g against %.1f g of buoyancy and sank; the voids are filled with closed-cell foam (about 3 g) so a leaking shell still floats (FLG-DDR-004 F1)" % (m_h, m_solid, b_solid),
        round(frac_h * 100, 0), 70.0, "% of buoyancy used", rule="below", closed_by="FLG-DDR-004 F1 (fix rule); model options_bc.py")
c.claim("C2", "C: the basin float (hollow shell, 56 mm OD) floats with its magnet at under 70 % of its volume submerged", "Physics", "Fluid mechanics",
        "Archimedes: weight (shell %.1f g, plus about 3 g of foam) = displaced water; solid ring first pass was %.1f g against %.1f g and sank" % (md_h, m_drain_solid, b_drain_solid),
        round(frac_dh * 100, 0), 70.0, "% of buoyancy used", rule="below", closed_by="FLG-DDR-004 F1 (fix rule); model options_bc.py")
pitch = 25.0
c.cited("C3", "C: a reed chain at 25 mm pitch reads the level to 25 mm steps (plus or minus %.1f mm)" % (pitch / 2), "Mathematics", "Quantisation",
        "Resolution of a switch chain = pitch; the level is the highest closed reed, with one or two reeds closing at once, so the error is at most one pitch",
        "True as stated. It exceeds the 10 mm street target of PR-002, so this is scored against the user requirements in FLG-OPT-001, not a failure of the science", WITHIN)
c.cited("C4", "C: a ring magnet beside the sealed stem closes a glass reed switch 1.9 mm from the stem axis", "Physics", "Magnetism",
        "Reed switches close at 10 to 30 ampere-turns of applied field; a sintered ring magnet at a few millimetres gives a field far above that; hysteresis spreads the closing height by a few mm",
        "Plausible; the closing height and its spread need the reed's data sheet, assumed typical 10 to 30 AT", PLAUSIBLE)
c.cited("C5", "C: the floats move freely on 16 mm stems in silty stormwater and at -20 C", "Biology", "Fouling",
        "Silt and biofilm in the 0.9 mm radial gap between bore and stem can bind a float; ice binds it solid in a frozen tube",
        "Plausible; the bottom cap drain holes empty the street pipe, the basin float is not protected from ice, to assess in OPT scoring", PLAUSIBLE)

state = c.write()
print(f"first pass record: street float solid {FIRST_PASS[0]:.1f} g vs {FIRST_PASS[1]:.1f} g buoyancy; basin float solid {FIRST_PASS[2]:.1f} g vs {FIRST_PASS[3]:.1f} g")
print(f"fixed hollow floats: street {m_h:.1f} g ({frac_h:.0%}), basin {md_h:.1f} g ({frac_dh:.0%}); err_b {err_b:.1f} mm; drain A {err_drain:.1f} mm; lag {lag:.3f} mm; mass {mass}")
