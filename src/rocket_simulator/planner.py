from __future__ import annotations

from .models import MissionPhase, MissionPlan


def build_mission_plan(vehicle_key: str, destination_key: str) -> MissionPlan:
    from .config import DESTINATIONS, VEHICLES

    if vehicle_key not in VEHICLES:
        raise ValueError(f"Unknown vehicle '{vehicle_key}'")
    if destination_key not in DESTINATIONS:
        raise ValueError(f"Unknown destination '{destination_key}'")

    vehicle = VEHICLES[vehicle_key]
    destination = DESTINATIONS[destination_key]

    if vehicle.mode == "hobby" and destination.name != "earth":
        raise ValueError("Hobby rocket mode only supports Earth suborbital missions")

    if vehicle.mode == "hobby":
        phases = [
            MissionPhase("Launch", 20),
            MissionPhase("Coast to apogee", 45),
            MissionPhase("Descent", 60),
            MissionPhase("Parachute recovery", 120),
        ]
        estimated_delta_v = 800
        margin = vehicle.total_delta_v_mps - estimated_delta_v
        return MissionPlan(
            vehicle=vehicle,
            destination=destination,
            phases=phases,
            estimated_delta_v_mps=estimated_delta_v,
            feasible=margin >= 0,
            delta_v_margin_mps=margin,
        )

    launch_to_orbit_dv = 9400
    transfer_dv = max(600, destination.transfer_days_from_earth * 4)
    landing_dv = destination.landing_delta_v_penalty_mps
    return_dv = 3200 if destination.name != "earth" else 1200
    earth_recovery_dv = 400

    estimated_delta_v = launch_to_orbit_dv + transfer_dv + landing_dv + return_dv + earth_recovery_dv

    phases = [
        MissionPhase("Liftoff and booster ascent", 510),
        MissionPhase("Parking orbit operations", 5400),
        MissionPhase("Trans-planetary injection", 1800),
    ]

    if destination.name != "earth":
        phases.extend(
            [
                MissionPhase("Cruise phase", destination.transfer_days_from_earth * 86400),
                MissionPhase(f"{destination.name.title()} approach and landing", 28800),
                MissionPhase("Surface mission", 172800),
                MissionPhase("Ascent and return injection", 21600),
                MissionPhase("Return cruise", destination.transfer_days_from_earth * 86400),
            ]
        )
    else:
        phases.extend(
            [
                MissionPhase("Earth orbital operations", 43200),
                MissionPhase("Reentry and splashdown", 5400),
            ]
        )

    phases.append(MissionPhase("Earth recovery", 7200))

    margin = vehicle.total_delta_v_mps - estimated_delta_v

    return MissionPlan(
        vehicle=vehicle,
        destination=destination,
        phases=phases,
        estimated_delta_v_mps=estimated_delta_v,
        feasible=margin >= 0,
        delta_v_margin_mps=margin,
    )

