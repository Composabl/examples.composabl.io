# Chemical Process Control (CSTR - Continuous Stirred Tank Reactor)

CSTR Sim is a Python simulator made from ODE functions that control an Exothermic Chemical Reaction in a Continuous Stirred Tank Reactor.<br>
The reaction consistis in transform the raw material A into product B (A -> B + heat) by controlling the temperature of collant fluid in a specific CSTR operation with the goal of increasing the conversion rate. During this process we have a strongly non linear transition from a low conversion rate area (low B production) to a high productivity rate area (high B production) and the temperature can quickly get out of control.

![CSTR model](https://www.mathworks.com/help/mpc/gs/cstr_diagram.png)

SIMO system:
* 2 sensors (Temperature and Concentration)
* 1 control action (Jacket cooland temperature Tc)

### Assumptions
* Extothermic reation
* Reactor is isothermal (no heat exchange with exterior)
* Irreversible chemical reaction A -> B
* First order reaction
* Perfect Stired reaction
* Constant volume tank
* Simple Liquid-phase - constant densitiy
* The inlet stream of reagent A enters the tank at a constant volumetric rate.
* The product stream B exits continuously at the same volumetric rate.

Steady State 1 (low conversion area) - Ca = 8.5 kmol/m3 <br>
Steady State 2 (high conversion area) - Ca = 2.o kmol/m3

## State, Actions, Config and Constraints
Episode = 90 steps
dt = 0.5 min

### State Variables
* Ca - Residual (A) concentration - output (y1)
* T - Reactor Temperature (y2)
* Cref - Concentration Setpoint
* Tref - Temperature Setpoint
* Tc - Coolant Fluid Temperature

### Action Variables
* Tc_adjust - Coolant Fluid Temperature Variation

### Config Variables
* Cref_signal - programmed signal for Cref and Tref :
    * "ss1" - Setpoint signal to control the system only on steady state 1
    * "ss2" - Setpoint signal to control the system only on steady state 2
    * "transition" - Setpoint signal to control the system only on transition area
* noise_percentage - sensor noise

### Constraints:
* Physical limitation for Action : Tc_adjust +- 10 oC
* Prevent Thermal Runaway: T < 400

## Building

```bash
docker build -t composabl/sim-cstr .
docker run --rm -it -p 1337:1337 composabl/sim-cstr
```

## Running from Remote

```bash
docker pull composabl/sim-cstr
docker run --rm -it -p 1337:1337 composabl/sim-cstr
```

## References

https://www.mathworks.com/help/mpc/gs/cstr-model.html

[1] Bequette, B., Process Dynamics: Modeling, Analysis and Simulation, Prentice-Hall, 1998, Module 8, pp. 641-660.

[2] Seborg, D. E., T. F. Edgar, and D. A. Mellichamp, Process Dynamics and Control, 2nd Edition, Wiley, 2004, pp. 34–36 and 94–95.
