# Boeing 747 cruising altitude Simulation

Airplane Sim is a Python simulator made from Transfer functions that optimize the response to setpoint changes in Air Speed and Climb Rate (transition altitude while cruising).<br>
This model simulates a Boeing 747 airplane cruising at 40,000 ft. In this application, we seek a model to link the elevator (e) and thrust (t) with the airspeed and climb rate. The model's equations are presented in state space form, connecting the elevator angle in centi-radians and thrust to four states: horizontal airspeed, vertical airspeed, aircraft rotation, and the aircraft's angle.

![Airplane model](http://apmonitor.com/do/uploads/Main/flight_controls_747.png)

## Transfer Function Equations
![Transfer function 1](http://apmonitor.com/do/uploads/Main/flight_equations_747.png)
![Transfer function 2](http://apmonitor.com/do/uploads/Main/flight_equations2_747.png)

MIMO system:
* 4 sensors (Horizontal Velocity, Vertical Velocity, Rotation, Angle)
* 2 control actions (Elevator angle (e) and Thrust (t))

### Assumptions
* Boeing 747 aircraft with constant mass
* Cruising altitude of 40000 ft
* Nominal velocity = 774 ft/sec (0.8 Mach speed)
* Not considering fuel usage, faults or stall

## State, Actions, Config and Constraints
Episode = 16 steps
dt = 1 min

### State Variables
* y1 - Air Speed
* y2 - Climb Rate
* u1 - Horizontal Velocity
* u2 - Vertical velocity
* u3 - Aircraft Rotation
* u4 - Aicraft Angle

### Action Variables
* de - Elevator Angle variation
* dt - Thrust variation

### Config Variables

### Constraints:

## Getting Started

```bash
# Build the container
./scripts/build.sh

# Run the container
./scripts/run.sh
```

## Building

```bash
docker build -t composabl/sim-airplane .
docker run --rm -it -p 1337:1337 composabl/sim-airplane
```

## Running from Remote

```bash
docker pull composabl/sim-airplane
docker run --rm -it -p 1337:1337 composabl/sim-airplane
```

## References

http://apmonitor.com/do/index.php/Main/ModelSimulation

[1] Camacho, E.F. and Bordons, C., Model Predictive Control, 2nd Edition, Advanced Textbooks in Control and Signal Processing, Springer, 2004.

