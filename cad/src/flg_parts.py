"""FloodGauge helpers for the kit 1.9 model (repo-specific, not part of .kit/).

Fasteners placed in a joint (hex, button and countersunk screws, nyloc and security nuts, washers), crush
sleeves, countersink cutters and small plate helpers, all as build123d solids in millimetres. The
standard parts follow ISO 4017 (hex screws), ISO 4032 and ISO 7040 (nuts), ISO 7089 (washers), ISO 7380
(button heads) and ISO 10642 (countersunk heads); threads are plain shanks, as is usual in assembly CAD.
`fasten()` returns kit part dicts (cad_parts.part) so every screw, nut and washer is its own solid.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[2] / ".kit")]

from build123d import Cone, Cylinder, Plane, Pos, RegularPolygon, Sketch, Circle, extrude  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

# M3 and M4 are not in cad_parts.ISO: (s across flats, k head height, m nut height, washer d2, washer h, pitch)
cp.ISO.setdefault(3, (5.5, 2.0, 2.4, 7.0, 0.5, 0.5))
cp.ISO.setdefault(4, (7.0, 2.8, 3.2, 9.0, 0.8, 0.7))
ISO = cp.ISO
# ISO 7380 button head (dk, k, hex socket) and ISO 10642 countersunk head (dk, k) by size
BUTTON = {3: (5.7, 1.65, 2.0), 4: (7.6, 2.2, 2.5), 5: (9.5, 2.75, 3.0), 6: (10.5, 3.3, 4.0), 8: (14.0, 4.4, 5.0)}
CSK = {3: (6.3, 1.7, 2.0), 4: (8.4, 2.3, 2.5), 5: (10.5, 2.8, 3.0), 6: (12.6, 3.3, 4.0), 8: (16.8, 4.4, 5.0)}


def orient(shape, origin, outward):
    """Move a shape built with its axis along +Z (head side up) so that +Z points along `outward` and z = 0
    sits at `origin`."""
    n = math.sqrt(sum(c * c for c in outward))
    pl = Plane(origin=tuple(origin), z_dir=tuple(c / n for c in outward))
    return pl * shape


def nyloc_h(d):
    return ISO[d][2] + 0.45 * d


def nyloc_nut(d):
    """Nylon-insert lock nut (ISO 7040 type): a hex nut with a round crown, z from 0 to m + 0.45 d."""
    m = ISO[d][2]
    crown_h = 0.45 * d
    crown = extrude(Sketch() + Circle(0.72 * ISO[d][0]) - Circle(d / 2), crown_h)
    return cp.hex_nut(d) + Pos(0, 0, m) * break_edges(crown, 0.4)


def _socket(af, depth):
    return extrude(RegularPolygon(af / math.sqrt(3), 6), depth)


def button_screw(d, length):
    """ISO 7380 button-head socket screw: head z 0 to k, shank from z 0 down to -length."""
    dk, k, af = BUTTON[d]
    head = break_edges(Pos(0, 0, k / 2) * Cylinder(dk / 2, k), k * 0.45)
    head -= Pos(0, 0, k - k * 0.55) * _socket(af, k * 0.6)
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    return head + shank


def csk_screw(d, length):
    """ISO 10642 countersunk socket screw: head top at z = 0, cone down to z = -k, shank to -length."""
    dk, k, af = CSK[d]
    head = Pos(0, 0, -k / 2) * Cone(d / 2, dk / 2, k)
    head -= Pos(0, 0, -k * 0.5) * _socket(af, k * 0.5)
    shank = Pos(0, 0, -(k + (length - k) / 2)) * Cylinder(d / 2, length - k)
    return head + shank


def csk_cutter(d, depth, clearance=0.2):
    """Countersink and hole to cut from a plate (top face at z = 0): cone then bore of depth `depth`."""
    dk, k, _ = CSK[d]
    cone = Pos(0, 0, -k / 2 + 0.01) * Cone(d / 2 + clearance, dk / 2 + clearance, k + 0.02)
    bore = Pos(0, 0, -depth / 2) * Cylinder(d / 2 + clearance, depth)
    return cone + bore


def snake_eye_nut(d):
    """Tamper-resistant two-hole (snake-eye) nut for an M8 stud: round, flat, z from 0 to 7."""
    body = Cylinder(9.0, 7.0)
    body = Pos(0, 0, 3.5) * body
    body = break_edges(body, 0.6)
    body -= Pos(0, 0, 3.5) * Cylinder(d / 2, 8)
    for sx in (-1, 1):
        body -= Pos(sx * 5.8, 0, 3.5) * Cylinder(1.6, 8)
    return body


def sleeve(od, id_, length):
    """Crush sleeve (tube) along +Z centred on the origin."""
    return Pos(0, 0, -length / 2) * extrude(Sketch() + Circle(od / 2) - Circle(id_ / 2), length)


def roundup_len(x):
    return math.ceil(x / 2) * 2 if x < 20 else math.ceil(x / 5) * 5


def fasten(d, grip, origin, outward, head="hex", wash_head=False, wash_nut=False, nut="nyloc", bom=None,
           group="arm", key="fixings", length=None, material="stainless", explode=(0, 0, 0), nut_group=None):
    """A screw or bolt with its washers and nut clamping a joint `grip` mm thick, as kit part dicts.

    origin is the centre of the joint face under the head; outward points from that face away from the
    joint (the direction the head faces). The nut and washer lie beyond the joint's far face. nut is
    "nyloc", "hex", "snake" or None (a screw into a tapped hole)."""
    s, k, m, d2, h, p = ISO[d]
    zh = h if wash_head else 0.0
    nut_h = {"nyloc": nyloc_h(d), "hex": m, "snake": 7.0, None: 0.0}[nut]
    zn_top = -grip - (h if wash_nut else 0.0)            # top face of the nut
    tail = 1.2 * p
    if head == "csk":
        need = CSK[d][1] * 0 + grip + (h if wash_nut else 0) + nut_h + tail
    else:
        need = zh + grip + (h if wash_nut else 0) + nut_h + tail
    L = length or roundup_len(need if nut else need - nut_h)
    if head == "hex":
        hs, hn = cp.hex_bolt(d, L), f"M{d}x{L} hex head screw (ISO 4017)"
    elif head == "button":
        hs, hn = button_screw(d, L), f"M{d}x{L} button head screw (ISO 7380)"
    else:
        hs, hn = csk_screw(d, L), f"M{d}x{L} countersunk screw (ISO 10642)"
    out = []

    def add(name, shape, kind="fastener", mat=material, g=group, k_=key):
        q = part(name, orient(shape, origin, outward), mat, kind=kind, bom=bom, group=g, explode=explode)
        q["key"] = k_
        out.append(q)

    add(hn, Pos(0, 0, zh) * hs if head != "csk" else hs)
    if wash_head:
        add(f"M{d} washer (ISO 7089)", cp.washer(d))
    if wash_nut:
        add(f"M{d} washer (ISO 7089)", Pos(0, 0, -grip - h) * cp.washer(d))
    if nut == "nyloc":
        add(f"M{d} nylon-insert lock nut (ISO 7040)", Pos(0, 0, zn_top - nut_h) * nyloc_nut(d), g=nut_group or group)
    elif nut == "hex":
        add(f"M{d} hex nut (ISO 4032)", Pos(0, 0, zn_top - nut_h) * cp.hex_nut(d), g=nut_group or group)
    elif nut == "snake":
        add(f"M{d} security (snake-eye) nut", Pos(0, 0, zn_top - nut_h) * snake_eye_nut(d), g=nut_group or group)
    return out


def tag(parts, key):
    """Give every part dict in a list the legacy component key and return the list."""
    for q in parts:
        q["key"] = key
    return parts
