# rocket-simulator

A lightweight mission simulator with two modes:

- **SLS-style heavy launch vehicle mode** for long-duration, automated missions.
- **Hobby rocket mode** for suborbital flights with parachute recovery.

## Project Scope

This is a planning and timeline simulator, not a high-fidelity astrodynamics tool. It is designed to:

1. Simulate automated mission phases from launch to Earth splashdown/landing.
2. Support selectable destinations across the solar system.
3. Run quickly with configurable time compression.

The heavy-launch configuration is **SLS-inspired fiction for simulation**, not an official NASA model.

## Simulation Assumptions

- Uses simplified v budgeting and phase sequencing.
- Uses coarse phase durations for launch, transfer, landing, return, and recovery.
- Destination gravity wells are represented with static penalties.
- Time compression multiplies simulation time per tick.

## Quick Start

Run from repository root:

```bash
python -m src.rocket_simulator.cli --vehicle sls --destination mars --time-compression 3600
```

Hobby mode:

```bash
python -m src.rocket_simulator.cli --vehicle hobby --destination earth --time-compression 30
```

## CLI Options

- `--vehicle`: `sls` or `hobby`
- `--destination`: `earth`, `moon`, `mercury`, `venus`, `mars`, `jupiter`, `saturn`, `uranus`, `neptune`
- `--time-compression`: simulated seconds advanced per real tick (default `60`)
- `--tick-seconds`: real-time tick size in mission seconds before compression (default `1`)

## Current Limitations

- Not physically accurate for mission certification.
- No atmospheric drag, staging transients, or orbital mechanics integration.
- No graphics yet (text timeline output only).
