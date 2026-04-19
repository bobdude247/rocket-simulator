from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from math import exp

from .models import MissionPlan

G0 = 9.80665

SYNODIC_PERIOD_DAYS = {
    "moon": 27.3,
    "mercury": 116.0,
    "venus": 584.0,
    "mars": 780.0,
    "jupiter": 399.0,
    "saturn": 378.0,
    "uranus": 370.0,
    "neptune": 367.0,
}

REFERENCE_WINDOWS = {
    "moon": date(2026, 1, 10),
    "mercury": date(2027, 3, 1),
    "venus": date(2026, 11, 15),
    "mars": date(2026, 11, 20),
    "jupiter": date(2027, 8, 1),
    "saturn": date(2028, 5, 1),
    "uranus": date(2029, 6, 1),
    "neptune": date(2030, 7, 1),
}


@dataclass(frozen=True)
class MissionAnalysis:
    required_propellant_kg: int
    propellant_fraction: float
    next_launch_window_open: date
    next_launch_window_close: date
    launch_window_cadence_days: int


def estimate_propellant_required(
    delta_v_mps: int,
    dry_mass_kg: float,
    average_isp_s: float,
) -> tuple[int, float]:
    if dry_mass_kg <= 0:
        raise ValueError("dry_mass_kg must be > 0")
    if average_isp_s <= 0:
        raise ValueError("average_isp_s must be > 0")

    mass_ratio = exp(delta_v_mps / (average_isp_s * G0))
    initial_mass = dry_mass_kg * mass_ratio
    propellant = max(0.0, initial_mass - dry_mass_kg)
    fraction = propellant / initial_mass if initial_mass else 0.0
    return int(round(propellant)), fraction


def estimate_next_launch_window(destination: str, today: date | None = None) -> tuple[date, date, int]:
    today = today or date.today()

    if destination == "earth":
        return today, today + timedelta(days=30), 30

    cadence = int(round(SYNODIC_PERIOD_DAYS.get(destination, 400)))
    reference = REFERENCE_WINDOWS.get(destination, today)

    if today <= reference:
        opening = reference
    else:
        days = (today - reference).days
        cycles = (days // cadence) + 1
        opening = reference + timedelta(days=cycles * cadence)

    closing = opening + timedelta(days=30)
    return opening, closing, cadence


def analyze_mission(plan: MissionPlan) -> MissionAnalysis:
    if plan.vehicle.mode == "hobby":
        dry_mass = 140.0
        isp = 210.0
    else:
        # Coarse SLS-inspired dry mass + capsule + recovery margin
        dry_mass = 145_000.0
        isp = 380.0

    required_propellant, fraction = estimate_propellant_required(
        delta_v_mps=plan.estimated_delta_v_mps,
        dry_mass_kg=dry_mass,
        average_isp_s=isp,
    )

    open_date, close_date, cadence = estimate_next_launch_window(plan.destination.name)

    return MissionAnalysis(
        required_propellant_kg=required_propellant,
        propellant_fraction=fraction,
        next_launch_window_open=open_date,
        next_launch_window_close=close_date,
        launch_window_cadence_days=cadence,
    )

