from __future__ import annotations

import argparse

from .mission_analysis import analyze_mission
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
        "--profile",
        default="auto",
        choices=["auto", "artemis2", "generic"],
        help="Mission profile selection. auto picks Artemis II-inspired profile for SLS+Moon.",
    )
    parser.add_argument(
        "--max-events",
        type=int,
        default=40,
        help="Maximum timeline events printed to console",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    profile = "artemis2" if args.profile == "artemis2" else "auto"
    if args.profile == "generic":
        profile = "generic"

    plan = build_mission_plan(args.vehicle, args.destination, profile=profile)
    analysis = analyze_mission(plan)
    events = run_simulation(plan, tick_seconds=args.tick_seconds, time_compression=args.time_compression)

    print(f"Vehicle: {plan.vehicle.name}")
    print(f"Mission profile: {plan.profile_name}")
    print(f"Destination: {plan.destination.name.title()}")
    print(f"Estimated mission delta-v: {plan.estimated_delta_v_mps} m/s")
    print(f"Vehicle delta-v capacity: {plan.vehicle.total_delta_v_mps} m/s")
    print(f"Delta-v margin: {plan.delta_v_margin_mps} m/s")
    print(f"Feasible with current vehicle: {'yes' if plan.feasible else 'no'}")
    print(f"Estimated required propellant: {analysis.required_propellant_kg:,} kg")
    print(f"Propellant mass fraction: {analysis.propellant_fraction:.1%}")
    print(
        "Next launch window: "
        f"{analysis.next_launch_window_open.isoformat()} to {analysis.next_launch_window_close.isoformat()}"
    )
    print(f"Launch opportunity cadence: ~{analysis.launch_window_cadence_days} days")
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

