from __future__ import annotations

from typing import Dict

from .models import Destination, Vehicle


DESTINATIONS: Dict[str, Destination] = {
    "earth": Destination("earth", transfer_days_from_earth=0, landing_delta_v_penalty_mps=200),
    "moon": Destination("moon", transfer_days_from_earth=3, landing_delta_v_penalty_mps=1800),
    "mercury": Destination("mercury", transfer_days_from_earth=120, landing_delta_v_penalty_mps=3200),
    "venus": Destination("venus", transfer_days_from_earth=150, landing_delta_v_penalty_mps=2800),
    "mars": Destination("mars", transfer_days_from_earth=210, landing_delta_v_penalty_mps=2400),
    "jupiter": Destination("jupiter", transfer_days_from_earth=850, landing_delta_v_penalty_mps=8000),
    "saturn": Destination("saturn", transfer_days_from_earth=1500, landing_delta_v_penalty_mps=9000),
    "uranus": Destination("uranus", transfer_days_from_earth=3000, landing_delta_v_penalty_mps=10000),
    "neptune": Destination("neptune", transfer_days_from_earth=4500, landing_delta_v_penalty_mps=11000),
}


VEHICLES: Dict[str, Vehicle] = {
    "sls": Vehicle(
        name="SLS-inspired heavy vehicle",
        mode="heavy",
        total_delta_v_mps=18000,
        has_boosters=True,
        has_capsule=True,
        supports_orbital_missions=True,
        parachute_recovery=True,
    ),
    "hobby": Vehicle(
        name="Hobby rocket",
        mode="hobby",
        total_delta_v_mps=1200,
        has_boosters=False,
        has_capsule=False,
        supports_orbital_missions=False,
        parachute_recovery=True,
    ),
}

