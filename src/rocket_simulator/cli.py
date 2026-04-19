from __future__ import annotations

import argparse

from .planner import build_mission_plan
from .simulator import run_simulation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rocket mission simulator")
    parser.add_argument("--vehicle", required=True, choices=["sls", "hobby"])
    parser.add_argument(
        "--destination",
        required=True,
        choices=["earth", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune"],
    )
    parser.add_argument("--time-compression", type=int, default=60)
    parser.add_argument("--tick-seconds", type=int, default=1)
    parser.add_argument(
        "--max-events",
        type=int,
        default=40,
        help="Maximum timeline events printed to console",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    plan = build_mission_plan(args.vehicle, args.destination)
    events = run_simulation(plan, tick_seconds=args.tick_seconds, time_compression=args.time_compression)

    print(f"Vehicle: {plan.vehicle.name}")
    print(f"Destination: {plan.destination.name.title()}")
    print(f"Estimated mission delta-v: {plan.estimated_delta_v_mps} m/s")
    print(f"Vehicle delta-v capacity: {plan.vehicle.total_delta_v_mps} m/s")
    print(f"Delta-v margin: {plan.delta_v_margin_mps} m/s")
    print(f"Feasible with current vehicle: {'yes' if plan.feasible else 'no'}")
    print(f"Mission phases: {len(plan.phases)}")
    print("--- Timeline ---")

    if len(events) <= args.max_events:
        for event in events:
            print(event.note)
    else:
        head = max(1, args.max_events // 2)
        tail = max(1, args.max_events - head)
        for event in events[:head]:
            print(event.note)
        print("... (timeline truncated) ...")
        for event in events[-tail:]:
            print(event.note)


if __name__ == "__main__":
    main()

