"""Pedal angle and force ratio across sled travel.

Uses the same geometry as the DIY-Sim-Racing-FFB-Pedal firmware (PedalGeometry.cpp).
Edit the values below and run:  python tools/kinematics.py
"""
import math

A_ROD = 202     # a: rod length, eye centre to eye centre (C -> B)
B_ARM = 130     # b: pedal hinge O -> rod joint C
D_FOOT = 34     # d: rod joint C -> foot point D
C_HOR = 224     # c horizontal: hinge O -> point A under B, sled at home (motor-side stop)
C_VER = 64      # c vertical: height of B above the hinge O
TRAVEL = 100    # sled positions to print (mm)


def pedal_angle_deg(sled_mm):
    c = math.hypot(C_HOR + sled_mm, C_VER)
    alpha = math.acos((B_ARM**2 + c**2 - A_ROD**2) / (2 * B_ARM * c))
    return math.degrees(alpha + math.atan2(C_VER, C_HOR + sled_mm))


def force_ratio(sled_mm):
    """Foot force / load-cell force."""
    c = math.hypot(C_HOR + sled_mm, C_VER)
    cos_gamma = (A_ROD**2 + B_ARM**2 - c**2) / (2 * A_ROD * B_ARM)
    return B_ARM / (B_ARM + D_FOOT) * math.sqrt(max(0.0, 1 - cos_gamma**2))


if __name__ == "__main__":
    print(f"{'sled mm':>8} {'angle':>7} {'ratio':>6}")
    for s in range(0, TRAVEL + 1, 10):
        print(f"{s:8d} {pedal_angle_deg(s):6.1f}° {force_ratio(s):6.2f}")
