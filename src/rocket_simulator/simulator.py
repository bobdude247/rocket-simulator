from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .models import MissionPhase, MissionPlan


@dataclass(frozen=True)
class SimulationEvent:
    mission_time_seconds: int
    phase: str
    progress: float
    note: str


def _format_duration(total_seconds: int) -> str:
    days, rem = divmod(total_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    if days:
        return f"{days}d {hours:02}:{minutes:02}:{seconds:02}"
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def _simulate_phase(
    phase: MissionPhase,
    start_time: int,
    tick_seconds: int,
    time_compression: int,
) -> Iterable[SimulationEvent]:
    elapsed = 0
    simulated_step = max(1, tick_seconds * time_compression)
    while elapsed < phase.duration_seconds:
        elapsed = min(phase.duration_seconds, elapsed + simulated_step)
        mission_time = start_time + elapsed
        progress = elapsed / phase.duration_seconds if phase.duration_seconds else 1.0
        yield SimulationEvent(
            mission_time_seconds=mission_time,
            phase=phase.name,
            progress=progress,
            note=f"T+{_format_duration(mission_time)} {phase.name} ({progress * 100:5.1f}%)",
        )


def run_simulation(plan: MissionPlan, tick_seconds: int = 1, time_compression: int = 60) -> List[SimulationEvent]:
    if tick_seconds <= 0:
        raise ValueError("tick_seconds must be > 0")
    if time_compression <= 0:
        raise ValueError("time_compression must be > 0")

    events: List[SimulationEvent] = []
    cursor = 0
    for phase in plan.phases:
        events.extend(_simulate_phase(phase, cursor, tick_seconds, time_compression))
        cursor += phase.duration_seconds

    events.append(
        SimulationEvent(
            mission_time_seconds=cursor,
            phase="Mission complete",
            progress=1.0,
            note=f"T+{_format_duration(cursor)} Mission complete",
        )
    )
    return events

