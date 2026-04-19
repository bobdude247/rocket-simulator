from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Destination:
    name: str
    transfer_days_from_earth: int
    landing_delta_v_penalty_mps: int


@dataclass(frozen=True)
class Vehicle:
    name: str
    mode: str
    total_delta_v_mps: int
    has_boosters: bool
    has_capsule: bool
    supports_orbital_missions: bool
    parachute_recovery: bool


@dataclass(frozen=True)
class MissionPhase:
    name: str
    duration_seconds: int


@dataclass(frozen=True)
class MissionPlan:
    profile_name: str
    vehicle: Vehicle
    destination: Destination
    phases: List[MissionPhase]
    estimated_delta_v_mps: int
    feasible: bool
    delta_v_margin_mps: int

