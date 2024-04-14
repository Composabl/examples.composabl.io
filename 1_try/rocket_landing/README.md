# Starship Landing

Starship Landing Sim is a Python simulator made from ODE functions that control variables of the starship in order to land.<br>
This model simulates a Starship Landing phase with some crucial variables to guide the ship for a safe landing.

![starship landing real](https://photos.smugmug.com/photos/i-J2xnNsL/0/XL/i-J2xnNsL-Th.jpg)
![starship landing](https://res.cloudinary.com/graham-media-group/image/upload/f_auto/q_auto/c_scale,w_900/v1/production/public/PUFQZ2E535BTPG3URNINL3UB6A.jpg?_a=AJFJtWIA)

SpaceX's Starship is a fully reusable spacecraft designed for a range of applications, from satellite deployment to interplanetary exploration. A pivotal aspect of its design is the capability to land back on Earth (or other celestial bodies) after mission completion, ensuring its reusability. The landing process of Starship, as with most rockets, is a complex integration of various control variables to ensure safety and precision. Let's delve into this intricate procedure:

1. Descent Initialization: At the beginning of the landing phase, Starship is oriented for the descent. This involves realigning the vehicle using its onboard control systems, ensuring its trajectory is in line with the designated landing zone.
2. Controlled Descent: As Starship descends, it uses a combination of aerodynamic surfaces and engine thrust to control its descent rate and trajectory.
3. Landing Burn: Just before landing, Starship initiates a landing burn. This involves reigniting one or more of its Raptor engines to further slow down its descent rate for a gentle touchdown.
4. Touchdown: As Starship approaches the ground, the landing legs are deployed. The vehicle touches down gently, with the thrust reduced to zero, completing the landing process.

The interplay of these variables, managed by sophisticated onboard computer systems and sensors, ensures that Starship can land safely and precisely. This process exemplifies the combination of cutting-edge technology and advanced control principles at work in modern aerospace engineering.

Control Variables :
1. Thrust: The vehicle's engines provide the necessary deceleration. By adjusting thrust, the vehicle can control its descent rate, ensuring a soft landing. This variable also assists in controlling x and y speeds when necessary.
2. x & x speed: These variables refer to the horizontal position and speed of Starship. Adjustments in these values are crucial to align the vehicle with the landing pad and compensate for any atmospheric disturbances.
3. y & y speed: These represent the vertical position and descent rate, respectively. It's vital to manage the descent rate to avoid a hard landing and potential damage.
4. Angle & Angle Speed: Adjusting the angle of descent is crucial. The vehicle's control systems work to stabilize and ensure the angle is conducive for a controlled descent. The angular velocity or rate at which the angle changes is closely monitored and regulated.


MIMO system:
* 4 sensors (Position, Velocity, Thrust, Angle)
* 2 control action (Thrust power and angle)

### Assumptions

## State, Actions, Config and Constraints
Episode = 400 steps
dt = 0.04

### State Variables
* x - Position on x axis
* x_speed - Velocity on x axis
* y - Position on y axis
* y_speed - velocity on y axis
* angle - Starship angle
* ang_speed - Starship angle speed

### Action Variables
* dthrust - Thrust power variation
* dangle - Thrust angle variation

### Config Variables

### Constraints:
* terminal y_speed < 5 m/s
* 0.4 < thrust < 1

## Getting Started

```bash
# Build the container
./scripts/build.sh

# Run the container
./scripts/run.sh
```

## Building

```bash
docker build -t composabl/sim-starship .
docker run --rm -it -p 1337:1337 composabl/sim-starship
```

## Running from Remote

```bash
docker pull composabl/sim-starship
docker run --rm -it -p 1337:1337 composabl/sim-starship
```

## References


