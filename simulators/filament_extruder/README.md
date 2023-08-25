# 3D Printer Filament Extruder

3D Printer Filament Extruder Sim is a Python simulator made from Transfer functions that control the heating collar for a 3D printer filament extruder.<br>
This model simulates a 3D printer filament extruder with the objective to control the extrude temperature by manipulating the heating collar and avoid longer settling time, large time constants and undesirable overshoot.

## Transfer Function Equations

SISO system:
* 1 sensor (Measured Temperature)
* 1 control action (Setpoint)

### Assumptions

## State, Actions, Config and Constraints
Episode = 60 steps
dt = 1 min

### State Variables
* y1 - Extruder Temperature
* y1ref - Extruder Temperature Setpoint
* u1 - Heater actuator
* rms - root mean square error between y1 and y1ref

### Action Variables
* du1 - Heater actuator variation

### Config Variables

### Constraints:
* 0 < y1 < 400

## Getting Started

```bash
# Build the container
./scripts/build.sh

# Run the container
./scripts/run.sh
```

## Building

```bash
docker build -t composabl/sim-filament .
docker run --rm -it -p 1337:1337 composabl/sim-filament
```

## Running from Remote

```bash
docker pull composabl/sim-filament
docker run --rm -it -p 1337:1337 composabl/sim-filament
```

## References


